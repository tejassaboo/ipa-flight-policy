# IPA Global Travel Manual Flight Booking

**Source of the handbook:** https://fr.poverty-action.org/sites/default/files/publications/IPA-Global-Travel-Manual-October-2021.pdf. The agent reads it verbatim (bundled at `src/plugin/data/policy.txt`); flights, fares and trips are synthetic.

**No affiliation with Innovations for Poverty Action.** The handbook is IPA's *Global Travel Manual for international
travel and U.S. domestic travel* (Version 1, released 1 October 2021), a PDF IPA posts in its public publications
folder, bundled verbatim for research. It is a nonprofit's public document with no confidentiality marking
(`pilot_work/originals/ipa-travel/frozen/README.md`); still, confirm with the course staff before publishing.

A `nanoagent.plugin/v0001` plugin. An agent handles one traveller's flight request under the organisation's real
travel manual: it reads the trip record, searches a simulated flight world and submits **BOOK**, **REFUSE** or
**FLAG_FOR_APPROVAL** with the offer, cabin, reason, approver and manual section. A deterministic Python verifier,
with no LLM, rebuilds the offers and the manual's answer itself and checks every field. Built from the
original-handbook template (`handbook_plugins/_template`); `tests/build_scenarios.py` writes the scenario files.

## The handbook and the harness flag

The frozen text (`src/plugin/data/policy.txt`, 10,801 words, 1,109 lines, 72,112 bytes, sha256 `59362430...f3fdffac8`,
equal to `pilot_work/originals/ipa-travel/frozen/SHA256SUMS`) is never paraphrased, and the task text restates no
rule. Under stock NanoAgent the agent does not see it: the plugin then runs as the `off` baseline. The
`harness.policy` switch of the NanoAgent fork (github.com/tejassaboo/nanoagent, branch `policy-switch`) adds it to
the system prompt: `harness.policy: full` adds all of it, and the selection methods add parts of it. These plugins
are meant to run with `query: instructions+input`, so a selector sees the traveller's request. The nine annexes are
listed by title only in the source; no case rests on them.

**Size.** At 1.33 tokens a word the manual alone is about 14,400 tokens (about 18,000 at 4 characters a token).
Under `full` the first call carries about 16,000 to 16,500 input tokens (manual, instructions, tool and submit
schemas, request), later calls up to about 17,500 as tool results accumulate. A 3-call run (`get_trip`,
`search_flights`, `submit`) is about 50,000 to 51,000 input tokens: under the hosted cap of 65,536. `saffron-dell`
asks for a second search (the fare from home), so it makes 4 calls (about 68,000) and crosses the cap: run it
locally with a raised cap, or expect it to stop before `submit` when hosted.

## Task

- **Input:** `TaskInput`: `scenario` (one of 32 case ids) and `request`, the traveller's own words.
- **Steps:** `get_trip`, then `search_flights` on the trip's route and date (and any other route the request asks to
  price; only `saffron-dell` does), then `submit`. Every case buys one one-way ticket; the trip record has no return
  date.
- **Output:** `BookingOutput`: `decision`, `offer_id` (empty when refusing), `cabin` (`NONE` when refusing),
  `reason_code`, `approver` and `clause`, each from a closed list. The reason list is the template's shared list plus
  nine codes of this manual (`REST_STOP_PERMITTED`, `REST_STOP_CONDITIONS_NOT_MET`, `FLY_AMERICA_US_CARRIER_REQUIRED`,
  `FLY_AMERICA_EXCEPTION`, `OPEN_SKIES_AGREEMENT`, `TRAVELER_PAYS_DIFFERENCE`, `POLICY_EXCEPTION_APPROVED`,
  `COMPANION_TRAVEL_AUTHORIZED`, `BUSINESS_NEED_TIMING`) and twelve decoy codes from other handbooks' rules. Fares
  are in cents of US dollars (`currency: USD`).
- **Success:** every field is one the answer key accepts; the cabin is graded as the chosen offer's own. Score =
  fields right / 6.
- **Fare convention.** Lines 334-336 ask for the lowest economy fare "that can be changed with a fee"; the world's
  offers carry only a refundable flag, so the `search_flights` description (and `booking_requirements`) says a fare
  that is not refundable can still be changed for a fee.
- **Reasons on a declined request.** The task instructions end with "When you book something other than what the
  traveller asked for, the reason code gives why their request is declined." Such bookings accept only the
  manual's ground: `cobalt-reed` (`UPGRADE_NOT_ELIGIBLE`), `heron-moss` and `kestrel-bloom` (the rest-stop codes),
  `tamarind-crest` (the Fly America codes). `russet-brook` and `violet-quarry` keep `LOWEST_FARE`, because the ground
  for declining is the lowest-fare rule itself (lines 360-365 "beyond the lowest available economy fare"; lines
  334-336 "the lowest economy fare ... that can be changed with a fee").
- **No hidden facts:** no scenario has `answer_key_inputs`.

| Scenario | Category | Expected (offer; cabin), reasons | Frozen lines |
|---|---|---|---|
| `amber-wharf` | easy | BOOK (mid-economy; ECONOMY), LOWEST_FARE | 115-116, 159-161, 334-336 |
| `basil-tern` | easy | BOOK (kenya-economy; ECONOMY), LOWEST_FARE | 159-161, 334-336, 347-353 |
| `cobalt-reed` | easy | BOOK (delta-economy; ECONOMY), UPGRADE_NOT_ELIGIBLE | 334-336, 339-341 |
| `dune-sparrow` | easy | BOOK (avianca-economy; ECONOMY), LOWEST_FARE | 159-161, 334-336 |
| `ember-kite` | easy | BOOK (kenya-economy; ECONOMY), LOWEST_FARE | 115-116, 159-161, 334-336 |
| `fennel-gorge` | easy | BOOK (british-premium; PREMIUM_ECONOMY), TRAVELER_PAYS_DIFFERENCE, TRAVELER_PAYS_UPGRADE | 339-341 |
| `heron-moss` | boundary_twin | BOOK (kenya-economy; ECONOMY), LONG_FLIGHT_CONDITION_NOT_MET, REST_STOP_CONDITIONS_NOT_MET | 334-336, 347-353 |
| `indigo-fern` | boundary_twin | BOOK (amsterdam-economy; ECONOMY), INTERNATIONAL_LONG_FLIGHT, REST_STOP_PERMITTED | 334-336, 347-353 |
| `jasper-cove` | boundary_twin | BOOK (stopover-economy; ECONOMY), INTERNATIONAL_LONG_FLIGHT, REST_STOP_PERMITTED | 334-336, 347-353 |
| `kestrel-bloom` | boundary_twin | BOOK (dubai-economy; ECONOMY), CONNECTION_TOO_LONG, REST_STOP_CONDITIONS_NOT_MET | 334-336, 347-353 |
| `larkspur-tide` | boundary_twin | BOOK (atlanta-economy; ECONOMY), FLY_AMERICA_US_CARRIER_REQUIRED, LOWEST_FARE, NATIONAL_CARRIER_REQUIRED | 504-506, 507-509, 513-517, 1065-1066 |
| `marble-finch` | boundary_twin | BOOK (kenya-economy; ECONOMY), FLY_AMERICA_EXCEPTION, LOWEST_FARE | 334-336, 504-506, 513-517, 1081 |
| `nectar-ridge` | boundary_twin | BOOK (aeromexico-economy; ECONOMY), LOWEST_FARE | 334-336 |
| `opal-heath` | boundary_twin | BOOK (united-economy; ECONOMY), BUSINESS_NEED_TIMING, LOWEST_FARE | 334-336 |
| `pewter-lake` | multi_rule | BOOK (kenya-premium; PREMIUM_ECONOMY), MEDICAL_NEED, POLICY_EXCEPTION_APPROVED | 339-341, 344-346 |
| `quill-harbor` | multi_rule | BOOK (united-economy; ECONOMY), LOYALTY_PROGRAM_PREFERENCE, TRAVELER_PAYS_DIFFERENCE | 336-338, 360-361, 365 |
| `russet-brook` | multi_rule | BOOK (american-economy; ECONOMY), LOWEST_FARE, LOYALTY_PROGRAM_PREFERENCE | 334-336, 336-338, 360-361, 365 |
| `saffron-dell` | multi_rule | BOOK (avianca-economy; ECONOMY), LOWEST_FARE, PERSONAL_TRAVEL_NOT_COVERED, TRAVELER_PAYS_DIFFERENCE | 175-179, 182-183, 334-336, 388-394, 891-892 |
| `tamarind-crest` | multi_rule | BOOK (united-economy; ECONOMY), FLY_AMERICA_US_CARRIER_REQUIRED, NATIONAL_CARRIER_REQUIRED | 336-338, 504-506, 507-509, 513-517, 1065-1066 |
| `umber-glade` | hidden_clause | BOOK (dubai-economy; ECONOMY), COMPANION_TRAVEL_AUTHORIZED, LOWEST_FARE | 142-146, 334-336 |
| `violet-quarry` | hidden_clause | BOOK (first-economy; ECONOMY), LOWEST_FARE, REFUNDABLE_FARE_NOT_ALLOWED | 334-336, 403-404 |
| `walnut-spire` | hidden_clause | BOOK (united-economy; ECONOMY), FLY_AMERICA_US_CARRIER_REQUIRED, LOWEST_FARE, NATIONAL_CARRIER_REQUIRED | 504-506, 507-509, 1065-1066 |
| `alder-crane` | distractor | BOOK (afternoon-economy; ECONOMY), LOWEST_FARE | 159-161, 334-336 |
| `yarrow-bluff` | distractor | BOOK (india-economy; ECONOMY), LOWEST_FARE | 147-153, 159-161, 334-336 |
| `zephyr-moor` | distractor | BOOK (lufthansa-economy; ECONOMY), LOWEST_FARE, OPEN_SKIES_AGREEMENT | 334-336, 504-506, 1073-1076 |
| `birch-hollow` | refusal | REFUSE, COMPANION_NOT_COVERED, PERSONAL_TRAVEL_NOT_COVERED | 142-146, 388-394 |
| `cedar-flint` | refusal | REFUSE, OUTSIDE_POLICY_SCOPE, PERSONAL_TRAVEL_NOT_COVERED | 128-129, 388-394 |
| `dahlia-mist` | refusal | REFUSE, OUTSIDE_POLICY_SCOPE, PERSONAL_TRAVEL_NOT_COVERED | 128-129, 388-394 |
| `elm-thistle` | flag | FLAG_FOR_APPROVAL (united-premium; PREMIUM_ECONOMY), APPROVAL_REQUIRED, MEDICAL_NEED | 339-341, 344-346 |
| `fir-cobble` | flag | FLAG_FOR_APPROVAL (kenya-economy; ECONOMY), APPROVAL_REQUIRED | 115-116, 159-161, 659, 686-687 |
| `gull-heather` | flag | FLAG_FOR_APPROVAL (amsterdam-economy or newark-economy; ECONOMY), APPROVAL_REQUIRED, UNCLEAR_POLICY_TEXT | 504-506, 507-509, 1073-1076 |
| `hazel-pond` | flag | FLAG_FOR_APPROVAL (avianca-economy or miami-economy; ECONOMY), APPROVAL_REQUIRED, UNCLEAR_POLICY_TEXT | 334-336, 654-656, 888-889 |

Every accepted reason, approver and section per case is in the scenario files and `tests/BUILD_NOTES.md`.

**Duration (`rules.over`).** Lines 347-353 permit an international rest period (overnight layover) when "The scheduled
flight time, including non-overnight stopovers and change of planes, is in excess of 14 hours" (strict: more than
840 minutes), the layover does not exceed 24 hours (1,440 minutes or less), the route is direct or usually traveled
and the fare is coach. The time is every scheduled flight plus every connection that is not an overnight stop; for an
itinerary without one it is the elapsed minutes. The rules raise if the overnight itinerary and the same-day ones
fall on opposite sides of 14 hours (no case does). The Fly America 6-hour exception (line 517, "at least", inclusive)
compares elapsed journey times of flights leaving at the same time.

**Approvers.** Lines 159-161 (and the Assignment Supervisor's itinerary approval, lines 659-675): a domestic trip
needs the Assignment Supervisor; an international one also the Global Team Director (Global Team staff) or the
Country Director (Country Office staff). Every booking or refusal accepts `NONE` and each role on file (SYNC_NOTES 4'
and 4(b)); a hold accepts only the awaited role (`fir-cobble`: `COUNTRY_DIRECTOR`, not the supervisor who signed;
`elm-thistle`: `CHIEF_FINANCIAL_OFFICER`). The unclear holds also wait on someone's decision, so they accept
`APPROVAL_REQUIRED` beside `UNCLEAR_POLICY_TEXT` and `NOT_NAMED` beside the roles the text points to.

Degenerate agents (`tests/test_verifier.py`): always holding the right offer as unclear passes 2 cases (the two
unclear flags); always booking the cheapest seat with `LOWEST_FARE`, `NONE` and the right section passes 12 of 32.

## Tools

| Tool | Does | Code |
|---|---|---|
| `booking_requirements` | The trip record's fields, the world's conventions (local times, dates, fares, sold-out seats, changeable fares) and its airports | `src/plugin/guide.py` |
| `get_trip` | A case's request and trip record: traveller and whom they accompany, staff unit, home and route, date, when the work begins, purpose, funding and award terms, requested cabin, airline, fare type and hotel night, doctor's letter date, Global Operations notice, sign-offs | `src/plugin/tools.py` |
| `search_flights` | Every offer on a route and local date: the pinned scenario offers only (no background offers); a search the case does not pin lists nothing and says so | `src/plugin/world.py` |
| `solve_booking` | The answer key (`rules.solve`), the agent task's `reference`, never shown to the agent | `src/plugin/rules.py` |

| Task | Does | Runner |
|---|---|---|
| `book-ipa-flight` | Handles one booking request | `agent`, with `get_trip` and `search_flights`; reference `solve_booking` |
| `booking-requirements` | Shows `booking_requirements` | `tool` |
| `search-flights` | Shows `search_flights` | `tool` |

## Layout

- `contract.py`: the template's shared contract plus this manual's scenario ids, approvers, sections, reason codes
  and trip record.
- `src/plugin/`: `world.py`, `scenarios.py`, `guide.py`, `answer.py`, `tools.py` (shared), `rules.py` (this
  manual's rules, citing frozen lines), `__main__.py`.
- `src/plugin/data/`: `policy.txt` (frozen), `handbook.json`, `scenarios/*.json`.
- `verifier/`: byte-identical copies of the shared modules and `rules.py`, plus `booking.py` and `tools.py`.
- `tests/`: the template's acceptance suite; `tests/plugin_spec.py` holds this manual's settings.
- `tests/build_scenarios.py`: writes the scenario files (an authoring aid, not a test).
- `tests/BUILD_NOTES.md`: design choices, the blind read and the acceptance outputs.

## Develop and run

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv lock --check
python3 ../_template/check_shared.py .
# from a NanoAgent checkout (read-only use):
nanoagent plugin inspect <this folder>
nanoagent plugin pack <this folder> /tmp/ipa-flight-policy.tar.gz
# from this folder, with that checkout's Python:
/path/to/nanoagent/nanoagent/.venv/bin/python ../_template/tools/stock_verify.py .
```

Offline: `hosts: []`, an empty `.env`, `write: []`, no clock (each case fixes its `booking_date`).
