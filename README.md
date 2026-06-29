# Footprint 26

**A reproducible model of fan travel cost and carbon emissions for the 2026 FIFA World Cup** (USA / Canada / Mexico), the first World Cup hosted across three countries, tested against FIFA's commitment to reach net zero by 2040.

The model is bottom-up and transparent: it uses real stadium coordinates, the confirmed 104-match allocation, and published emission factors, and reports results under three accounting methodologies so the effect of accounting choices is explicit rather than hidden.

---

## Headline results

| Result | Value |
|---|---|
| Host cities / matches | 16 cities, 104 matches (USA 78, CAN 13, MEX 13) |
| Longest inter-city hop | Vancouver → Miami, 4,492 km |
| Venue pairs requiring a flight (>600 km) | 111 of 120 (**92.5%**) |
| Reference fan footprint (realistic) | **6.78 tCO₂e** over 13,279 intra-tournament km |
| Accounting gap (realistic ÷ optimistic) | **3.39×** |
| Reference fan non-ticket cost | ~**$7,500** |
| Fan travel + lodging, tournament total¹ | ~**6.9 Mt CO₂e** = 1.9× Qatar 2022's reported footprint |

¹ Tournament total uses an *estimated* travelling-fan population and is an order-of-magnitude figure. Per-fan results use real geography and published factors. See limitations in [`Findings.md`](Findings.md).

![Accounting gap](figures/02_accounting_gap.png)

---

## Repository layout

```
footprint26/            importable model package
  __init__.py
  model.py              geography, emissions engine, fan-journey simulator, rollup
data/reference/
  venues.csv            16 venues: coords, capacity, matches, grid intensity
  emission_factors.csv  per-passenger-km factors + sources
tests/
  test_model.py         9 contract & sanity tests
docs/
  Findings.html         the write-up, with charts embedded
  Footprint26_preview.html   static notebook render
  dashboard.html        interactive fan-journey explorer (no build step)
figures/                charts exported from the notebook
Footprint26.ipynb       the analysis, end to end
Findings.md             companion write-up (interpretation + sources)
```

## Quickstart

```bash
git clone <repo-url> && cd footprint26
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

pytest -q                                   # 9 tests
jupyter notebook Footprint26.ipynb          # run the analysis
```

Or use the model directly:

```python
import footprint26 as f26

fan = f26.FanItinerary(origin_air_km=8200,
                       venue_sequence=["TOR","MEX","SEA","ARL","MIA","NYNJ"])
realistic = f26.simulate(fan, f26.BOTTOM_UP)
optimistic = f26.simulate(fan, f26.FIFA_STYLE)

print(f"{realistic.total_t:.2f} tCO2e  (gap {realistic.total_t/optimistic.total_t:.2f}x)")
print(f"${realistic.cost_usd:,.0f} non-ticket cost")
```

## Method in brief

The model costs any fan itinerary (origin distance + ordered venue sequence + nights) under three accounting methods that differ only in stated assumptions:

| Method | Radiative forcing | Return legs | Ground on short hops |
|---|---|---|---|
| `FIFA_STYLE` (optimistic) | no (CO₂ only) | no (one-way) | yes |
| `BOTTOM_UP` (realistic) | yes | yes | yes |
| `ALL_FLY` (upper bound) | yes | yes | no |

Reporting all three, and the ratio between them, turns the contested question of World Cup carbon accounting into a measured quantity. Every emission factor, distance, and population assumption is exposed and editable.

**Scope.** Fan travel and lodging only. Construction, operations, and team/official travel are excluded and additive, so all totals are lower bounds.

## Data sources

Venue coordinates and match allocations from published host-city/schedule data. Emission factors from UK DEFRA/BEIS 2024 (transport, including aviation radiative forcing) and Cornell Hotel Sustainability Benchmarking 2023 (lodging). Ticket and cost figures from ESPN, Business Standard, and Gulf News reporting (2025–26). Full citations in [`Findings.md`](Findings.md).

## License

[MIT](LICENSE). Reference data compiled from public sources (see the `source_note` column in `data/reference/emission_factors.csv`). Figures are illustrative, not official.
