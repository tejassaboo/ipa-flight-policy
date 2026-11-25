# Independent audit: ipa-flight-policy (2026-11-25)

Audited the builder's commit f40a955 against `pilot_work/tier_plan/build/WAVE3_AUDIT_BRIEF.md`, the wave 3 build brief's
12 lessons, MASTER_PLAN section 4, EDGE_CASES 1-3 and 5 and `_template/SYNC_NOTES.md` 4'. No money spent, nothing
pushed. Line numbers are lines of the frozen handbook (`src/plugin/data/policy.txt`).

## Method

I printed each scenario's request, the `get_trip` record, and every pinned `search_flights` listing through the
plugin's own `world.search`, with offers mapped back to their slots. I read the handbook's airfare, approval,
personal-travel, spouse, listed-country, rest-period and U.S. Government sections (lines 65-187, 333-418, 503-567,
597-702, 860-900, 1040-1090). Then I answered every case from that text and the tool output alone, before comparing
my answers with `expected`. I did not read rules.py first.

## Verdict

**Pass after one fix.** On all 28 non-flag cases the key's decision and offer match my own reading. The four flags
are sound:

- `hazel-pond` and `gull-heather` are open on a careful reading.
- `fir-cobble` and `elm-thistle` are clear approval holds.

The one defect was in the accept sets: the unclear holds accepted too few approvers. Twins differ in one fact each:

- heron-moss/indigo-fern: 840/841 minutes
- jasper-cove/kestrel-bloom: 1,440/1,445 minutes
- larkspur-tide/marble-finch: 359/360 minutes
- nectar-ridge/opal-heath: 09:00 next day against 14:00 the same day
- quill-harbor/russet-brook: pays or does not pay
- ember-kite/fir-cobble: the Country Director's sign-off

The decline-reason sentence is in the task instructions. Every request that names something the policy may refuse
has a fallback: heron, indigo, jasper, kestrel, russet, tamarind and violet say so outright, and cobalt-reed says "if
not, economy is fine". No request states a threshold.

## Defect found and fixed

| Scenario | Problem | Fix |
|---|---|---|
| hazel-pond, gull-heather | The unclear holds accepted only NOT_NAMED, the CFO, and the Assignment Supervisor (hazel) or the Grants team (gull). Two roles a careful reader would name were missing. (1) Global Operations is the policy owner: it is "responsible for establishing and updating IPA travel policies ... overseeing IPA's compliance with this Travel Manual" (lines 81-84). (2) The Global Team Director approves an international trip's "air travel itinerary, and airfare" (lines 159-162), and both trips are international by Global Team staff. gull-heather also lacked the Assignment Supervisor, who reviews "compliance with IPA travel policy" (lines 671-672). | `rules.UNCLEAR_ROLES` = NOT_NAMED, CHIEF_FINANCIAL_OFFICER, GLOBAL_OPERATIONS, plus `trip_roles(trip)`, and gull-heather keeps GRANTS_TEAM. Both rules.py copies were changed and are still byte-identical. A must_keep for lines 82-84 was added and the JSON regenerated. NONE is still never accepted on a hold (4'). The always-flag agent (NOT_NAMED) still passes 2. |

## The builder's open items, settled

- **Approvals on every trip (lines 159-161 with 659).** Kept, and correct. Line 159 names the Assignment
  Supervisor for domestic travel and line 160 the Country or Global Team Director for international travel. Line 659
  ("Obtain Assignment Supervisor approval of the selected itinerary"), lines 70-72 and lines 671-675 have the
  supervisor approve the itinerary on every trip. A careful reader could therefore hold an international booking
  that lacked the supervisor's sign-off.
  - I checked every record. All 25 BOOKs carry the supervisor's TRIP sign-off. Every international one also carries
    the right director: the Global Team Director, or the Country Director for ember-kite.
  - So every booking is clean on either reading, and the accept sets give those roles and NONE (4'). fir-cobble is
    the only case with a missing director, and it is keyed as a hold for COUNTRY_DIRECTOR only.
- **violet-quarry keeps LOWEST_FARE.** Kept. The handbook never forbids a refundable fare. The request for one is
  declined only because the standard is "the lowest economy fare ... that can be changed with a fee" (lines
  334-336), and the $198 non-refundable fare meets it while the $289 refundable fare is dearer. That is the
  lowest-fare rule itself, so lesson 12 allows LOWEST_FARE beside REFUNDABLE_FARE_NOT_ALLOWED.
- **saffron-dell (traveller pays the difference from a non-home departure).** Kept.
  - Lines 175-179 name "departing from a different location than the traveler's home of record" as a personal
    change to disclose. The request says it was disclosed, and the TRIP sign-off covers "any personal change the
    request names".
  - Lines 390-394 have the traveller pay the incremental cost. The business-only comparison (lines 182-183,
    891-892) is the lowest Dulles fare, the $430 Avianca nonstop, which is also the most direct. The traveller pays
    the $110 above it on the $540 Avianca Mexico City nonstop.
  - Refusing is not defensible, because the trip is for business and only the increment is personal. Booking
    Dulles is not defensible either, because the traveller will not be there.
  - The three reason codes (TRAVELER_PAYS_DIFFERENCE, PERSONAL_TRAVEL_NOT_COVERED, LOWEST_FARE) and the three
    clauses (AIRFARE, TRAVEL_APPROVAL, REIMBURSABLE_EXPENSES) are each a fair citation.
- **The "changeable for a fee" sentence in `search_flights`.** Fair, and it states no rule.
  - Offers carry only `refundable`, which the shared field defines as "refunded or changed without a fee". Without
    the sentence, a careful reader could conclude that a non-refundable fare cannot be changed at all, so that lines
    334-336 force the refundable fare. That would be a false failure on almost every case.
  - The sentence states a fact about this world's fares. It names no rule or threshold, and it shares no four-word
    phrase with line 336 (the lint passes).
- **hazel-pond (direct against lowest).** A genuine flag.
  - "the lowest economy fare ... that meets the business need ... via the most direct and expeditious route" (lines
    334-336) and "the most direct, expeditious and economical fare" (line 889) give no order when the lowest fare
    is not the most direct. Here American via Miami is $395 and 480 minutes, against the Avianca nonstop at $520 and
    330 minutes. Both land the afternoon before a 09:00 meeting.
  - Both readings are accepted as the held offer. The twins dune-sparrow (where the nonstop is also the cheapest)
    and larkspur-tide decide the matter on other facts.
  - I checked that no other case has a lowest fare off the fewest-stop, quickest itinerary of its pool, apart from a
    requested rest stop or a Fly America carrier. None does, so the phrase decides nothing else.
- **gull-heather (Open Skies per flight against the whole journey).** A genuine flag.
  - Lines 1073-1076 allow an EU airline "(1) between the U.S. and any point in an EU Member State or (2) between any
    two points outside the United States". KLM's Dulles-Amsterdam flight fits (1) and its Amsterdam-Nairobi flight
    fits (2), but the journey from the U.S. to Kenya fits neither. Lines 504-506 say "Open Skies carrier" with no
    route limit.
  - Both readings are accepted as the held offer: KLM at $1,180 (also the quickest) and United at $1,460.
  - Emirates is excluded on both readings. No Fly America exception applies: United via Newark takes 1,135 minutes
    against KLM's 1,075, so it is not 6 hours longer, and its connection is in the U.S.

## Other checks (kept)

- marble-finch/larkspur-tide measure "at least 6 hours longer" by elapsed time. Both itineraries leave JFK at 11:00,
  so the arrival times differ by 360 and 359 minutes. A flying-minutes reading (160 minutes) is not natural for
  "would take ... longer".
- heron-moss/indigo-fern leave the overnight stop out of the flight time, as "including non-overnight stopovers"
  implies. The nonstop is the same 840 or 841 minutes, so measuring by the listed same-day itinerary gives the same
  answer.
- In indigo-fern and jasper-cove the rest stop is "permitted" at IPA's cost (GSA 301-11.20). It is not a
  traveller-paid layover preference under lines 336-338: the rest-period clause is the specific rule, and the
  traveller does not offer to pay.
- alder-crane books 4 days ahead. Lines 354-355 ("whenever possible") and line 636 ("several weeks") attach no
  consequence to a late booking, so it is a fair distractor.
- yarrow-bluff told Global Operations 3 days before booking and 18 days before travel, across the month end.
- umber-glade's request ("written in the travel request ... the budget-holder has approved") states the facts that
  lines 142-146 test. It names no threshold and the lint is clean, so it was not reworded.

## Baselines

`MAX_PASS_ALWAYS_LOWEST` 12 -> 12 (12 of 32, within the 13-of-32 target). `MAX_PASS_ALWAYS_FLAG` 2 -> 2.

## Acceptance outputs (after the fix)

```
$ uv run pytest -q
252 passed
$ uv run ruff check .
All checks passed!
$ uv lock --check
Resolved 42 packages
$ python3 ../_template/check_shared.py .
: ok
$ cmp src/plugin/rules.py verifier/rules.py   (identical)
$ .../nanoagent/.venv/bin/python ../_template/tools/stock_verify.py .
32 scenarios, 0 failures
$ .../nanoagent/.venv/bin/nanoagent plugin inspect .
inspect exit 0
```
