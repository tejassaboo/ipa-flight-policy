# Validation notes: ipa-flight-policy (paid wave 3 validation, 2026-11-25)

Run: `efficient_corporate_travel_agent/pilot/ladder/runs/validation_w3_2026-11-25/ipa-flight-policy@w3/`, arm
`full`, DeepSeek V4 Flash (Nebius fp8), temperature 0, max_steps 6, max_tokens 8192, one run per scenario, at plugin
head 72a740c. Line numbers are lines of `src/plugin/data/policy.txt`.

## Results

27/32 valid (84.4%), mean field score 0.927, **easy 6/6**. By category: boundary 6/8, distractor 3/3, easy 6/6,
flag 1/4, hidden 3/3, multi 5/5, refusal 3/3. $0.00171 billed per run, 3.9 calls per run, 18,158 prompt tokens per
call, no run over the hosted 65,536 cap. Every run submitted.

## Every failure, classified

| scenario | category | submitted vs key | class | evidence |
|---|---|---|---|---|
| fir-cobble | flag | BOOK Kenya Airways (the held offer), LOWEST_FARE, ASSIGNMENT_SUPERVISOR, AIRFARE; key FLAG for COUNTRY_DIRECTOR | model slip | Nairobi to Johannesburg by Country Office staff is international; lines 159-161 require the Country Director's approval, and only the Assignment Supervisor has signed. The reasoning never opens the approval section; it spent its time on whether the approver field should name the supervisor ("the decision relies on the supervisor's approval which is on file"). The twins ember-kite and amber-wharf passed. |
| gull-heather | flag | BOOK United, FLY_AMERICA_US_CARRIER_REQUIRED; key FLAG (KLM or United) | model slip | It quoted lines 1073-1076 in full, including branch (2) "between any two points outside the United States", then took the journey reading as settled: "The trip is IAD to NBO. NBO is in Kenya, not an EU member state. So the Open Skies exception does not apply." It never weighed that Amsterdam-Nairobi is a flight between two points outside the U.S., or that lines 504-506 name "Open Skies carrier" with no route limit. The twins zephyr-moor and walnut-spire passed. |
| hazel-pond | flag | BOOK American via Miami ($395), LOWEST_FARE; key FLAG (Miami or the Avianca nonstop) | model slip | "The policy says air travel must be arranged using the lowest economy fare that meets the business need ... via the most direct and expeditious route", then "The lowest fare is American Airlines at $395 ... So book the AA economy offer". It quoted the route words and never weighed them against the 480-minute connection and the 330-minute nonstop (lines 334-336, 654-656). The twin dune-sparrow passed. |
| jasper-cove | boundary_twin | BOOK same-day Emirates ($1,240), PERSONAL_TRAVEL_NOT_COVERED; key the Dubai stopover ($1,365), REST_STOP_PERMITTED or INTERNATIONAL_LONG_FLIGHT | **scenario defect: the request invites a reading the key rules out** | The model checked every condition of lines 347-353 and found them met ("Flight time is 1070 minutes = 17.8 hours > 14 hours ... layover of 1440 minutes = 24 hours exactly ... So it meets the rest period conditions"). It then set the permission aside on motive: "the rest period is permitted for the traveler's rest, not for personal sightseeing. The traveller explicitly wants to 'spend a night in Dubai on the way' - this is personal travel", and applied lines 336-338 ("layover duration or location" preferences are traveller-paid). The key and the audit (AUDIT_NOTES: the rest stop is "not a traveller-paid layover preference") rest on reading the stop as a rest period. "Spend a night in Dubai" names a city visit, while the sister pair's request (heron-moss and indigo-fern) says "break the journey with a night in Amsterdam", and indigo-fern passed with REST_STOP_PERMITTED. The boundary this twin tests is 1,440 against 1,445 minutes, not the traveller's motive. |
| marble-finch | boundary_twin | BOOK Delta ($1,420), FLY_AMERICA_US_CARRIER_REQUIRED; key Kenya Airways ($1,150), FLY_AMERICA_EXCEPTION or LOWEST_FARE | model slip (limit rationalised away) | It computed the boundary right and read it right: "1260-900=360 min = 6 hours ... 6 hours is 'at least 6 hours'. So the exception could apply", then "the exception doesn't clearly apply (or the difference is exactly 6 hours which is borderline)" and booked Delta. Line 517 says "at least 6 hours". The twin larkspur-tide (359 minutes) passed. |

## Fixes (this commit)

1. **jasper-cove and kestrel-bloom (scenario):** the shared `DUBAI_REQUEST` now reads "I'd like to break the journey
   with a night in Dubai" instead of "I'd like to spend a night in Dubai on the way", the wording of the
   Amsterdam pair. Records, offers, keys, ids and the 1,440/1,445-minute boundary are unchanged.
   `tests/build_scenarios.py`; regenerated `jasper-cove.json` and `kestrel-bloom.json`.

No rule or accept set changed. Not loosened: fir-cobble, gull-heather, hazel-pond, marble-finch.

## Q2

The always-cheapest agent passes 12/32 (37.5%) before and after (`MAX_PASS_ALWAYS_LOWEST = 12`, unchanged). Both
Dubai twins are unchanged for it: it fails jasper-cove (stopover is dearer) and kestrel-bloom (wrong reason code).

## Re-score

The stored answers re-score 27/32 at the new head (easy 6/6): the five failures stand. jasper-cove's request changed,
so its stored answer is not evidence about the fixed case.

## Re-run

Required: jasper-cove and kestrel-bloom (their request changed). Optional: marble-finch (rationalised boundary) and
gull-heather (one reading taken as settled), for variance only.

## Checks

`uv run pytest -q` (252 passed), `uv run ruff check .`, `uv lock --check`, `check_shared.py`,
`tools/stock_verify.py` (32 scenarios, 0 failures), stock `nanoagent plugin inspect .` (exit 0).
