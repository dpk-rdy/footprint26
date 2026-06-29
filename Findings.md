# Footprint 26: Findings

**Companion write-up to the `Footprint26.ipynb` model.** The notebook produces the numbers; this document explains what they mean. All per-fan figures come from the model running on real venue coordinates and published emission factors. Tournament-scale figures depend on an estimated fan population and are flagged as such. Sources are listed at the end.

---

## Background

The 2026 FIFA World Cup is the first hosted across three countries: the United States, Canada, and Mexico [^1]. It is the first with 48 teams and 104 matches, played across 16 host cities, with matches allocated 78 to the US, 13 to Canada, and 13 to Mexico [^2][^3].

In 2021, FIFA committed as a signatory to the UN Sports for Climate Action Framework to halve its emissions by 2030 and reach net zero by 2040 [^4][^5]. The precedent for measuring against that commitment is Qatar 2022, which FIFA reported at 3.6 million tonnes of CO₂e, attributing 51.7% to travel [^6][^7]. That figure was disputed. Carbon Market Watch and Lancaster University's Mike Berners-Lee argued the true total was at least three times higher, citing the use of one-way flight assumptions and an eightfold underestimate of stadium-construction emissions [^8][^9]. A Swiss regulator later ruled the "carbon-neutral" claim unsubstantiated [^10].

The model exists to test one question. Given the geography and format of 2026, what does it cost a fan, in money and carbon, to attend, and how does the total relate to the net-zero commitment.

---

## Finding 1: The format requires fans to fly

The 16 host cities form 120 city-pairs. The model computes the great-circle distance for each. The longest is Vancouver to Miami at 4,492 km; the mean inter-city distance is 2,359 km. **111 of the 120 pairs (92.5%) exceed 600 km**, the distance beyond which intercity rail or coach ceases to be a realistic substitute for flying.

This matters because North America lacks the dense high-speed rail network that made prior tournaments navigable by ground. Reporting on 2026 confirms the practical consequence: unlike Russia 2018 and Qatar 2022, where fans had free or simple intercity travel, supporters in 2026 face substantial transport costs across the continent [^11]. The format makes flying close to unavoidable for any fan following a team between cities, which is the root cause of both findings that follow.

A representative case shows the scale. A fan travelling from Europe and attending six matches across all three countries accumulates 13,279 km of travel *within* the tournament, on top of the transatlantic journey to reach it.

---

## Finding 2: Attendance cost is a step-change from prior tournaments

Ticket prices alone have risen sharply. The cheapest group-stage entry ticket went from roughly $11 at Qatar 2022 to about $100 in 2026 [^12]. A comparable mid-tier (Category 3) group-stage seat rose from $69 to as much as $265 [^11]. The cheapest final ticket climbed from $206 to $2,030, so the cheapest 2026 final seat now costs more than the most expensive Category-1 final seat in 2022, which was $1,607 [^12]. On the resale market, a single marquee group-stage seat in Dallas averaged about $1,028 [^13].

Tickets are only part of the cost. The model decomposes the non-ticket spend for the representative European fan: roughly $7,500 across the origin round-trip flight, intra-tournament flights, and 18 nights of lodging. Intra-tournament flights are the largest single component, a direct result of the geography in Finding 1. This is consistent with an England Supporters' club estimate of just over $7,000 for tickets alone to every match through the final [^12], and with per-person trip estimates in the $3,300 to $7,500+ range depending on host city [^14].

The increase is structural rather than incremental: the tri-nation format removed the free intercity travel that earlier tournaments provided, so the cost rises with the distances the format imposes.

---

## Finding 3: The carbon figure moves 3.4× on accounting choices alone

The model costs the same representative journey three ways, varying only the accounting method:

- **Optimistic ("FIFA-style"):** counts combustion CO₂ only, treats journeys as one-way.
- **Realistic ("bottom-up"):** counts return legs and includes aviation's radiative-forcing uplift, the non-CO₂ warming effect applied to high-altitude emissions (consensus multiplier ~1.9) [^15].
- **Upper bound ("all-fly"):** as realistic, but assumes no ground transport substitution.

The same journey is **2.00 tonnes under optimistic accounting and 6.78 tonnes under realistic accounting, a factor of 3.4**. The gap does not come from an aggressive assumption. It follows from two defensible bookkeeping choices: one-way versus round-trip, and CO₂-only versus full radiative forcing. It also reproduces, from first principles, the order of magnitude that critics alleged separated Qatar's reported figure from reality [^8].

The practical implication is that a single headline carbon number is uninformative without its assumptions. The model therefore reports the optimistic figure, the realistic figure, and the ratio, rather than a single value.

---

## Finding 4: Fan travel alone exceeds the relevant benchmarks

Scaling per-fan results to the tournament requires knowing how many fans travel and from where. That data is not yet available for an in-progress tournament, so the model uses an explicit estimate of approximately 2.5 million travelling fans, segmented by confederation of origin. The resulting total should be read as an order of magnitude, not a precise count. Every input is adjustable in the notebook.

On that basis, fan travel and lodging total roughly **6.9 Mt CO₂e** under realistic accounting. That is **1.9× Qatar 2022's entire reported footprint** and **3.8× the level implied by FIFA's 50%-by-2030 interim target**. This is a lower bound: it excludes stadium construction, venue operations, and the travel of the 48 teams and officials, all of which are additive.

By origin, domestic North American fans contribute the largest absolute share, simply by volume. On a per-fan basis, intercontinental fans from Africa and Asia/Oceania carry the heaviest footprints, about 4.6 tonnes each, driven almost entirely by the long-haul flight to reach the tournament. The distinction is operationally relevant: measures aimed at the largest total target the domestic segment, while per-fan measures target long-haul arrivals.

---

## Finding 5: Venue operations are a controllable variable

Stadium electricity demand is large, and its carbon intensity depends on the local grid. The model ranks host cities by grid intensity: Vancouver runs at about 13 gCO₂/kWh (predominantly hydroelectric) and Seattle at about 94, while Kansas City sits near 512 and the Texas and Florida venues in the 400s. The cleanest and dirtiest venues differ by roughly 40× per kilowatt-hour. Because match scheduling determines which venues host the most-watched, most energy-intensive fixtures, venue allocation is a lever the organiser controls directly, independent of fan behaviour.

---

## Mitigation levers

The model tests three interventions against the realistic baseline of 6.78 tonnes per fan:

| Intervention | Result | Change |
|---|---|---|
| Geographic clustering of a team's route | 5.25 t | −23% |
| Rail substitution (generous 1,000 km threshold) | 6.78 t | no effect |
| Attending four matches instead of six | 4.82 t | −29% |

Two of the three reduce the footprint materially. The rail lever does not: even at a generous 1,000 km threshold, every hop in a typical route still exceeds it, so no journey shifts to rail. This is a substantive result rather than a modelling gap. It indicates that rail substitution is not an available mitigation for this tournament's geography, and that interventions should focus on routing and scheduling instead.

Taken together, the levers indicate that the net-zero-by-2040 commitment cannot be met through tournament design alone under the 2026 format; closing the gap would rely heavily on offsets and removals, the mechanism that drew criticism at Qatar [^8][^10]. The levers that do work (clustering matches geographically, weighting schedules toward clean-grid venues, and reducing forced long-haul hops) are quantifiable, which is what separates a practical target from a stated one. FIFA has not submitted its targets to an independent validator such as the Science Based Targets initiative [^5].

---

## Limitations

- Fan population and segment shares are estimates, not measured attendance; the tournament rollup is an order-of-magnitude result.
- Scope is fan travel and lodging only. Construction, operations, and team travel are excluded and additive, so all totals are lower bounds.
- Emission factors carry uncertainty; they are sourced and adjustable in the model.
- Routes are representative rather than actual. Distances are great-circle and therefore slightly understate routed travel.
- Ticket and cost figures are sourced to early-to-mid 2026 reporting and remain volatile under FIFA's dynamic pricing.

---

## Sources

[^1]: Encyclopædia Britannica, "2026 FIFA World Cup." First tournament hosted by three countries.

[^2]: Al Jazeera / Sky Sports. 48 teams, 104 matches, 16 host cities.

[^3]: LiveScore / USA TODAY. Match distribution USA 78, Canada 13, Mexico 13.

[^4]: FIFA, "COP26: FIFA commits to net-zero emission by 2040," media release, November 2021.

[^5]: "FIFA's climate strategy 3 years on," Football & Climate Change, November 2024. Targets not submitted to SBTi/CDP.

[^6]: Al Jazeera, "Will the World Cup in Qatar be carbon-neutral?" 3.6 Mt CO₂e reported.

[^7]: BBC Sport, "Qatar World Cup: FIFA's carbon neutrality claim 'misleading'." 51.7% from travel.

[^8]: BBC Sport (as above). Mike Berners-Lee, Lancaster University, "way over 10 million tonnes."

[^9]: Scientific American / Carbon Market Watch, 2024. Construction emissions underestimated eightfold; one-way flight assumption.

[^10]: Swiss Fairness Commission ruling (via ReddMonitor / Bloomberg). "Carbon neutral" claim unsubstantiated.

[^11]: Business Standard, "FIFA World Cup 2026: Rising costs, travel hurdles leave fan bases hanging," June 2026. Cat-3 group ticket $69→$265; loss of free intercity travel vs 2018/2022.

[^12]: ESPN, "FIFA slashes some 2026 World Cup ticket prices after backlash," December 2025; Gulf News, "FIFA World Cup 2026 vs Qatar 2022." Group $11→$100, final $206→$2,030, ESTC ~$7,000 estimate.

[^13]: ESPN, "World Cup sticker shock," June 2026. Average cheapest Dallas group-stage seat ~$1,028.

[^14]: edhat / SoFi, "Cost of the 2026 World Cup," April 2026. Per-person totals ~$3,300 to $7,500+, ~$5,440 average across US host cities.

[^15]: UK DEFRA/BEIS 2024 greenhouse-gas conversion factors (transport, including aviation radiative forcing, consensus multiplier ~1.7 to 2.0); Cornell Hotel Sustainability Benchmarking Index 2023 (lodging).
