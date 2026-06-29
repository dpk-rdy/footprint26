"""Contract and sanity tests for the Footprint 26 model. Run: pytest -q"""
import numpy as np
import footprint26 as f26


def test_matches_sum_to_104():
    assert f26.VENUES["matches"].sum() == 104


def test_country_match_splits():
    v = f26.VENUES
    assert v[v.country == "USA"].matches.sum() == 78
    assert v[v.country == "Canada"].matches.sum() == 13
    assert v[v.country == "Mexico"].matches.sum() == 13


def test_haversine_known_distance():
    # New York -> Los Angeles is ~3,940 km
    d = f26.haversine(40.71, -74.01, 34.05, -118.24)
    assert 3800 < d < 4100


def test_distance_matrix_symmetric_zero_diag():
    dm = f26.build_distance_matrix()
    assert (np.diag(dm.values) == 0).all()
    assert np.allclose(dm.values, dm.values.T)


def test_bottom_up_exceeds_fifa_style():
    """Realistic accounting must exceed optimistic for a flight-dominated route."""
    bu = f26.simulate(f26.EURO_FAN, f26.BOTTOM_UP).total_t
    ff = f26.simulate(f26.EURO_FAN, f26.FIFA_STYLE).total_t
    assert bu > ff


def test_accounting_gap_in_expected_range():
    bu = f26.simulate(f26.EURO_FAN, f26.BOTTOM_UP).total_t
    ff = f26.simulate(f26.EURO_FAN, f26.FIFA_STYLE).total_t
    assert 3.0 < bu / ff < 3.8        # documented ~3.4x


def test_leg_emissions_uses_rail_below_threshold():
    short = f26.leg_emissions(300, f26.BOTTOM_UP)   # rail
    longer = f26.leg_emissions(900, f26.BOTTOM_UP)  # air
    # per-km air >> per-km rail, so 900 km air should dwarf 300 km rail
    assert longer / 900 > short / 300


def test_rollup_total_is_lower_bound_above_qatar():
    total_mt = f26.rollup().segment_t.sum() / 1e6
    assert total_mt > f26.QATAR_REPORTED_MT     # fan travel alone exceeds Qatar's reported total


def test_round_trip_doubles_origin_leg():
    one_way = f26.simulate(f26.FanItinerary(5000, ["LA"], 0, True), f26.FIFA_STYLE)
    round_trip = f26.simulate(f26.FanItinerary(5000, ["LA"], 0, True), f26.BOTTOM_UP)
    assert round_trip.travel_kg > one_way.travel_kg
