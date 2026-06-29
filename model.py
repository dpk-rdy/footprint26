"""Footprint 26: fan cost and carbon model for the 2026 FIFA World Cup.

A reproducible bottom-up model of fan travel cost and emissions, using real venue
coordinates, confirmed match allocations, and published emission factors. The same
logic backs the companion notebook (`Footprint26.ipynb`).

Scope: fan travel + lodging only. Construction, operations, and team/official travel
are excluded (additive, so totals are lower bounds).
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Reference data
# --------------------------------------------------------------------------- #
_DATA = Path(__file__).resolve().parent.parent / "data" / "reference"


def load_venues() -> pd.DataFrame:
    """16 host venues with coordinates, capacity, match count, grid intensity."""
    df = pd.read_csv(_DATA / "venues.csv")
    assert df["venue_id"].is_unique, "duplicate venue_id"
    assert df["matches"].sum() == 104, f"matches sum to {df['matches'].sum()}, expected 104"
    by_country = df.groupby("country").matches.sum().to_dict()
    assert by_country == {"USA": 78, "Canada": 13, "Mexico": 13}, by_country
    return df


def load_emission_factors() -> dict[str, float]:
    """Per-passenger-km emission factors plus the aviation RF multiplier."""
    df = pd.read_csv(_DATA / "emission_factors.csv")
    return dict(zip(df["factor_id"], df["value"]))


VENUES = load_venues()
EF = load_emission_factors()

# Map the CSV factor_ids to the short keys used by the model.
EF = {
    "air_short_haul": EF["air_short_haul"],
    "air_long_haul": EF["air_long_haul"],
    "rail_intercity": EF["rail_intercity"],
    "coach_bus": EF["coach_bus"],
    "car_petrol_avg": EF["car_petrol_avg"],
    "hotel_night": EF["hotel_night"],
    "rf_multiplier": EF["radiative_forcing_multiplier"],
}

# Out-of-pocket cost assumptions (USD), editable.
COST = {"air_per_km": 0.12, "ground_per_km": 0.06, "hotel_night": 220.0}

# Below this inter-city distance, ground transport is realistic; above it, fly.
GROUND_THRESHOLD_KM = 600.0

EARTH_KM = 6371.0088


# --------------------------------------------------------------------------- #
# Geography
# --------------------------------------------------------------------------- #
def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance (km) between two lat/lon points."""
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * EARTH_KM * np.arcsin(np.sqrt(a))


def build_distance_matrix(venues: pd.DataFrame = VENUES) -> pd.DataFrame:
    """Symmetric venue-to-venue great-circle distance matrix (km)."""
    ids = venues["venue_id"].tolist()
    v = venues.set_index("venue_id")
    m = np.zeros((len(ids), len(ids)))
    for a, b in combinations(ids, 2):
        d = round(haversine(v.loc[a, "lat"], v.loc[a, "lon"],
                            v.loc[b, "lat"], v.loc[b, "lon"]), 1)
        i, j = ids.index(a), ids.index(b)
        m[i, j] = m[j, i] = d
    return pd.DataFrame(m, index=ids, columns=ids)


DM = build_distance_matrix()


# --------------------------------------------------------------------------- #
# Emissions engine
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Method:
    """An accounting methodology = a named set of assumptions."""
    name: str
    apply_rf: bool        # count aviation non-CO2 radiative forcing?
    round_trip: bool      # count the return leg?
    ground_ok: bool       # allow rail/coach below the threshold?


FIFA_STYLE = Method("FIFA-style (optimistic)", apply_rf=False, round_trip=False, ground_ok=True)
BOTTOM_UP = Method("Bottom-up (realistic)", apply_rf=True, round_trip=True, ground_ok=True)
ALL_FLY = Method("All-fly (upper bound)", apply_rf=True, round_trip=True, ground_ok=False)


def leg_emissions(distance_km: float, method: Method,
                  threshold: float = GROUND_THRESHOLD_KM) -> float:
    """kgCO2e for one inter-venue leg under a given accounting method."""
    if distance_km <= 0:
        return 0.0
    if method.ground_ok and distance_km <= threshold:
        per_km, rf = EF["rail_intercity"], 1.0
    else:
        per_km = EF["air_short_haul"] if distance_km < 1500 else EF["air_long_haul"]
        # published air factors already fold in RF; strip it out for CO2-only accounting
        rf = 1.0 if method.apply_rf else (1.0 / EF["rf_multiplier"])
    return distance_km * per_km * rf * (2.0 if method.round_trip else 1.0)


# --------------------------------------------------------------------------- #
# Fan-journey simulator
# --------------------------------------------------------------------------- #
@dataclass
class FanItinerary:
    origin_air_km: float        # one-way distance home -> first venue
    venue_sequence: list        # ordered venue_ids attended
    nights_per_stop: int = 3
    origin_long_haul: bool = True


@dataclass
class JourneyResult:
    travel_kg: float
    hotel_kg: float
    cost_usd: float
    intra_km: float

    @property
    def total_kg(self) -> float:
        return self.travel_kg + self.hotel_kg

    @property
    def total_t(self) -> float:
        return self.total_kg / 1000.0


def simulate(it: FanItinerary, method: Method) -> JourneyResult:
    """Carbon + cost for one fan itinerary under one accounting method."""
    o_factor = EF["air_long_haul"] if it.origin_long_haul else EF["air_short_haul"]
    rf = 1.0 if method.apply_rf else (1.0 / EF["rf_multiplier"])
    travel = it.origin_air_km * o_factor * rf * (2.0 if method.round_trip else 1.0)
    cost = it.origin_air_km * COST["air_per_km"] * (2.0 if method.round_trip else 1.0)

    intra_km = 0.0
    for a, b in zip(it.venue_sequence, it.venue_sequence[1:]):
        d = DM.loc[a, b]
        intra_km += d
        travel += leg_emissions(d, method)
        cost += d * (COST["ground_per_km"] if d <= GROUND_THRESHOLD_KM else COST["air_per_km"])

    nights = it.nights_per_stop * len(it.venue_sequence)
    hotel = nights * EF["hotel_night"]
    cost += nights * COST["hotel_night"]

    return JourneyResult(round(travel, 1), round(hotel, 1), round(cost, 2), round(intra_km, 1))


# --------------------------------------------------------------------------- #
# Tournament rollup
# --------------------------------------------------------------------------- #
# NOTE: population and segment shares are ESTIMATES, not measured attendance.
# The rollup total is therefore an order-of-magnitude result.
TOTAL_TRAVELLING_FANS = 2_500_000
SEGMENTS = {  # name: (share, origin_km, long_haul, route)
    "Domestic (CONCACAF)": (0.55, 1200, False, ["LA", "SEA", "ARL"]),
    "South America": (0.12, 7500, True, ["MIA", "ARL", "NYNJ"]),
    "Europe": (0.20, 8200, True, ["TOR", "BOS", "NYNJ"]),
    "Africa": (0.05, 11000, True, ["MEX", "HOU", "ATL"]),
    "Asia/Oceania": (0.08, 12500, True, ["VAN", "SF", "LA"]),
}
QATAR_REPORTED_MT = 3.6
TARGET_2030_MT = 3.6 * 0.5


def rollup(method: Method = BOTTOM_UP) -> pd.DataFrame:
    """Scale per-fan journeys by the estimated population to a tournament total."""
    out = []
    for name, (share, km, lh, route) in SEGMENTS.items():
        per_fan_t = simulate(FanItinerary(km, route, 3, lh), method).total_t
        pop = TOTAL_TRAVELLING_FANS * share
        out.append({"segment": name, "pop": int(pop),
                    "per_fan_t": round(per_fan_t, 2), "segment_t": round(per_fan_t * pop)})
    return pd.DataFrame(out)


# Reference itinerary used throughout the notebook and tests.
EURO_FAN = FanItinerary(8200, ["TOR", "MEX", "SEA", "ARL", "MIA", "NYNJ"], 3, True)
