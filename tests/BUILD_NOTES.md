# Build notes: ipa-flight-policy (wave 3, 2026-11-24)

Built from `_template` with `instantiate.py` (slug `ipa-travel`, `--task-id book-ipa-flight`, `--currency USD`,
`--background 0`, `--scenarios 32`). Frozen handbook: `pilot_work/originals/ipa-travel/frozen/ipa-travel_policy.txt`,
10,801 words (over 10,000, so 32 scenarios), 1,109 lines, sha256 `59362430...f3fdffac8`, raw PDF sha256 `41bab017...`.
Decisions were taken without asking (the lead was away); each is recorded here. Nothing rests on the nine annexes,
which the source lists by title only (lines 27-35, 1098-1109).

## 1. What the handbook supports

Mandatory or checkable flight clauses (frozen line numbers):

| Lines | Clause | Operator / force | Used by |
|---|---|---|---|
| 334-336 (888-889, 654-656) | lowest economy fare that meets the business need (incl. arrival and departure times), via the most direct and expeditious route, changeable with a fee | "must ... to the fullest extent possible" | every booking |
| 336-338 | alternative routing for personal preference (carrier, layover) : traveller pays the difference | "must" | quill-harbor, russet-brook, tamarind-crest |
| 339-341 | upgraded classes not reimbursable; permitted at personal expense; exceptions by the CFO | mandatory | cobalt-reed, fennel-gorge, pewter-lake, elm-thistle |
| 344-346 | medical exception with a signed doctor's note no more than one year old | "may be approved" | pewter-lake, elm-thistle |
| 347-353 | international rest period: flight time "in excess of 14 hours", layover "may not exceed 24 hours", usual route, coach | strict / inclusive | heron-moss, indigo-fern, jasper-cove, kestrel-bloom (basil-tern, yarrow-bluff not asked) |
| 360-361, 365 | frequent flyer programmes must not influence selection beyond the lowest available economy fare | "must not" | quill-harbor, russet-brook |
| 388-394 | personal travel is the employee's; traveller pays incremental costs | "will not reimburse" | saffron-dell, cedar-flint, dahlia-mist, birch-hollow |
| 175-183, 891-892 | personal changes (another departure city) disclosed in the approval; cost comparison | "must" | saffron-dell |
| 115-116, 159-161, 659, 686-687 | all travel approved before booking; domestic by the Assignment Supervisor, international by the Country Director (Country Office staff) or Global Team Director | "must" | every booking; fir-cobble |
| 142-146 | spouse/child travel only with a bona fide business purpose, documented, approved by the budget-holder | "only when" | umber-glade, birch-hollow |
| 147-153 | listed countries (Egypt, India, Turkey are the ones the world has): Global Operations told before booking and at least two weeks ahead | "must" | yarrow-bluff (on time) |
| 504-509, 1065-1067 | Fly America: U.S.-funded travel with origin or destination in the U.S. on a U.S.-flag, Open Skies or code-share flight; cost alone no justification | "must" | larkspur-tide, walnut-spire, tamarind-crest, gull-heather |
| 513-517, 1081 | exception: a U.S. carrier "at least 6 hours longer" | inclusive | larkspur-tide, marble-finch |
| 1073-1076 | EU airlines between the U.S. and an EU Member State, or between two points abroad | (unclear for U.S.-third country via the EU) | zephyr-moor, gull-heather |
| 354-355 | book "as far in advance as practical", "whenever possible" | soft | alder-crane (distractor) |
| 403-404 | business change fees reimbursable | permissive | violet-quarry |

Not used: business class under U.S. funding (lines 536-546, 1059-1061: Agreement/Contract Officer approval plus the
USAID 14-hour condition; no case needs it), USAID prior approval and medical certification (533-535, 553-567), the
other Fly America exceptions (two plane changes, a 4-hour overseas wait, under-3-hour flights twice as long, 24 hours
longer, no U.S. coach seat, involuntary switch, two points abroad; the rules raise on any case near one), travel
advances, per diem, lodging, ground transport. The handbook has no rule on several travellers on one flight
(`multi_traveller` overlay not required) and no round-trip rule: every case buys one one-way ticket and the trip
record has no return date.

## 2. Unclear points and how they are handled

- **"via the most direct and expeditious route"** (lines 334-336) against "the lowest economy fare". Flag
  `hazel-pond`: the American connection through Miami is $125 cheaper and 150 minutes slower than the Avianca nonstop;
  both land the day before the meeting. Twins: `dune-sparrow` (same route, the nonstop is also the cheapest: book it)
  and `larkspur-tide` (a U.S. carrier connection is required by Fly America: book it). Every other case is built so
  the keyed fare is also on the fewest-connection, shortest itinerary of its pool (`rules.lowest_direct` raises
  otherwise), so the phrase decides nothing else.
- **"between the U.S. and any point in an EU Member State"** (lines 1073-1076) for an EU airline from the U.S. to a
  third country through an EU hub. Flag `gull-heather` (KLM Dulles-Amsterdam-Nairobi on an NSF grant; each flight
  fits a branch, the journey fits neither; lines 504-506 name "Open Skies carrier" without a route limit). Hold KLM or
  United. Twins: `zephyr-moor` (Dulles-Frankfurt on Lufthansa: plainly covered) and `walnut-spire` (only foreign
  non-EU airlines are cheaper: United).
- **"one year"** for the medical note (365 or 366 days; at booking or at travel): avoided. Both notes are well under
  a year on every reading (168 and 140 days); the rules raise between 365 days at travel and 366 at booking.
- **"scheduled flight time, including non-overnight stopovers and change of planes"** for an itinerary with an
  overnight stop: measured as every flight plus every non-overnight connection. A reader could instead measure the
  journey by the same-day itineraries listed beside it, so `heron-moss`/`indigo-fern` give the Kenya Airways nonstop
  the same 840/841 minutes as the KLM flights, and the rules raise if the two measures disagree.
- **Changeable with a fee.** The world's offers carry only `refundable`. The `search_flights` description and
  `rules.CONVENTIONS` say "A fare that is not refundable can still be changed for a fee", so the lowest
  non-refundable fare meets lines 334-336 on every reading (lint-clean: no 4-word phrase of the clause).
- **Approval holds** (not unclear text): `fir-cobble` (international trip by Country Office staff with only the
  Assignment Supervisor's sign-off: hold for the Country Director) and `elm-thistle` (medical exception requested,
  CFO not yet answered: hold the premium economy fare for the CFO). Both accept `APPROVAL_REQUIRED` (elm-thistle also
  `MEDICAL_NEED`, the reason that calls for the sign-off) and only the awaited role.
- **Global Operations notice.** Missing or late notice has no stated consequence for the booking (hold? refuse?),
  so no case tests it; `yarrow-bluff` has it on time (18 days, across the month end) and the rules raise otherwise.

Numeric twin pairs: rest stop 840/841 minutes (strict), rest-stop layover 1,440/1,445 minutes (inclusive), Fly
America 359/360 minutes longer (inclusive), and the work start time (next morning 09:00 against 14:00 the same day)
for the arrival-time business need.

## 3. Choices made without asking

1. Every trip record carries the trip approvals the manual requires: the Assignment Supervisor for every trip (line
   659 has the supervisor approve the itinerary even for international travel) plus the Global Team or Country
   Director for international trips (lines 159-161). Bookings accept those roles and `NONE` (SYNC_NOTES 4').
2. `fennel-gorge` (premium economy at the traveller's expense) accepts only the premium economy fare: line 340
   permits it and the request decides (EDGE_CASES 3.17), as Standex juniper-flint.
3. `quill-harbor` (United, traveller pays the difference) accepts only United; `russet-brook` (United, will not pay)
   accepts only the lowest fare and keeps `LOWEST_FARE` beside `LOYALTY_PROGRAM_PREFERENCE` because lines 360-365
   decline the airline on the lowest-fare test itself.
4. `violet-quarry` (refundable asked) keeps `LOWEST_FARE` beside `REFUNDABLE_FARE_NOT_ALLOWED`: the ground is the
   lowest-fare sentence itself ("the lowest economy fare ... that can be changed with a fee").
5. `saffron-dell` books the dearer Mexico City-Bogota fare (the traveller pays the $110 above the Dulles fare) and
   accepts `TRAVELER_PAYS_DIFFERENCE`, `PERSONAL_TRAVEL_NOT_COVERED` (the personal part is not covered) and
   `LOWEST_FARE`.
6. `tamarind-crest`: paying the difference does not make a foreign carrier compliant under Fly America; only the Fly
   America codes are accepted (the request is declined on that ground).
7. Unclear holds accept `UNCLEAR_POLICY_TEXT` or `APPROVAL_REQUIRED`. Roles: `hazel-pond` NOT_NAMED,
   ASSIGNMENT_SUPERVISOR (reviews the itinerary, lines 671-675), CHIEF_FINANCIAL_OFFICER (non-compliant expenses,
   lines 129-131); `gull-heather` NOT_NAMED, GRANTS_TEAM (sponsor requirements, lines 185-186), CHIEF_FINANCIAL_OFFICER. (Audit
   2026-11-25 widened both: GLOBAL_OPERATIONS, lines 81-84, and the trip's own approvers; see AUDIT_NOTES.md.)
8. Personal-trip refusals give `business_starts` empty ("empty when the trip has no work").
9. Decoy reason codes (grepped; none has a subject in the text): WEEKEND_TRAVEL_HOME, WEEKEND_TRIP_NOT_EARNED (line 237
   is about salary on weekends, not trips home), NEXT_OF_KIN_TRAVEL, CHANCELLOR_WRITTEN_AUTHORIZATION,
   CREATIVE_TICKETING, PRIVATE_AIRCRAFT_NOT_APPROVED, DOUBLE_BOOKING_PROHIBITED, DENIED_BOARDING_NOT_ALLOWED,
   CANDIDATE_TRIP_NOT_COVERED, SAME_CLASS_AS_CUSTOMER, TRAVEL_PACKAGE_NOT_ITEMIZED, TICKET_TOTAL_APPROVED. The
   template's usual decoys FLY_AMERICA_US_CARRIER_REQUIRED and OPEN_SKIES_AGREEMENT are real codes here. Approver
   decoys: VICE_PRESIDENT, CHIEF_EXECUTIVE, DEPARTMENT_HEAD.
10. No background offers anywhere (`background: 0` on every search): every search lists exactly its pinned offers.
11. Clause sets: the lowest-fare bookings accept AIRFARE, PREPARING_FOR_TRAVEL (4.3, 4.7) and REIMBURSABLE_EXPENSES
    (the Airfare row), which state the same standard; Fly America bookings accept AIRFARE, USG_FUNDED_TRAVEL and
    US_GOVERNMENT_PROCEDURE.

## 4. Mix and overlays

6 easy, 8 boundary_twin, 5 multi_rule, 3 hidden_clause, 3 distractor, 3 refusal, 4 flag (12.5%). Decisions: 25 BOOK
(2 premium economy, 23 economy), 3 REFUSE, 4 FLAG (2 approval, 2 unclear). Overlays: multi_leg 10, overnight 6,
date_arithmetic 4 (month_end 1), personal_travel 6, dearer_option 11, upgrade_not_taken 2, outside_air_section 11.

Degenerate agents: always-flag passes 2 (gull-heather, hazel-pond); always-cheapest passes 12 of 32 (alder-crane,
amber-wharf, basil-tern, dune-sparrow, ember-kite, marble-finch, nectar-ridge, russet-brook, umber-glade,
violet-quarry, yarrow-bluff, zephyr-moor), within the 13-of-32 target. In five of those (marble-finch, russet-brook,
umber-glade, violet-quarry, zephyr-moor) a handbook rule pulls toward another offer or a refusal and the manual has to
be read to see that it does not apply.

## 5. Independent blind read (non-flag scenarios)

Re-derived from the frozen text and the tool outputs only (the `get_trip` record and every pinned `search_flights`
listing, dumped per scenario), not from rules.py, then compared with `expected`.

| Scenario | My reading from text + offers | Agrees |
|---|---|---|
| amber-wharf | domestic, supervisor signed; AA 06:30 sold out; all nonstops 115 min: UA $214 | yes |
| basil-tern | AS + GTD signed; KQ nonstop $1,180 cheapest and quickest; the KLM Amsterdam night not asked | yes |
| cobalt-reed | premium asked, no note, no CFO, no offer to pay: lines 339-340, economy; DL nonstop $1,340 | yes |
| dune-sparrow | AV nonstop $430 is cheapest and most direct | yes |
| ember-kite | Country Office staff, CD + AS signed: KQ $410 | yes |
| fennel-gorge | premium at own expense permitted (line 340): BA premium $1,420 | yes |
| heron-moss | KLM flights 395+445 = 840, nonstop 840: not "in excess of 14 hours": KQ nonstop | yes |
| indigo-fern | 841 both, layover 900 min, usual route, coach: rest stop permitted: KLM $1,295 | yes |
| jasper-cove | flights 1,070 min; Dubai layover 1,440 = 24 h, "may not exceed": permitted: EK stopover $1,365 | yes |
| kestrel-bloom | layover 1,445 > 24 h: not permitted; same-day EK $1,240 (quicker than QR) | yes |
| larkspur-tide | NSF grant; DL 1,259 vs KQ 900 (both 11:00): 359 < 360: U.S. carrier: DL $1,420 | yes |
| marble-finch | DL 1,260: exactly 6 h longer, "at least": exception: KQ $1,150 | yes |
| nectar-ridge | meeting next 09:00; AM lands 19:35: AM $318 | yes |
| opal-heath | meeting 14:00; AM lands 19:35 too late; UA lands 10:55: UA $372 | yes |
| pewter-lake | note 2026-09-30 (< 1 year), CFO approved: KQ premium $2,290 | yes |
| quill-harbor | United for miles, traveller pays the difference (336-338): UA $389 | yes |
| russet-brook | will not pay; 360-365: lowest fare AA 08:00 $342 | yes |
| saffron-dell | approved deviation from MEX; Dulles fare $430; MEX lowest AV $540, traveller pays $110: AV MEX-BOG | yes |
| tamarind-crest | DOL grant: Fly America; Emirates foreign, UA nonstop fastest, no exception: UA $1,560 | yes |
| umber-glade | spouse with documented business purpose, budget-holder approved (142-146): EK $1,240 | yes |
| violet-quarry | refundable asked; standard is changeable with a fee: AA 07:00 $198 non-refundable | yes |
| walnut-spire | NSF: U.S. carrier; UA nonstop fastest: UA $1,520 | yes |
| yarrow-bluff | India listed; GO told 11-27, before booking 11-30 and 18 days ahead; AI $1,050 | yes |
| zephyr-moor | NSF, IAD-FRA: EU airline between U.S. and EU (1073-1076): LH $640 | yes |
| alder-crane | 4 days ahead, soft rule; tablets in hand luggage; DL 15:45 $259 | yes |
| birch-hollow | spouse sightseeing, no business purpose: refuse | yes |
| cedar-flint | holiday side trip: personal, refuse | yes |
| dahlia-mist | wedding on leave: personal, refuse | yes |

28 of 28 non-flag scenarios agree. The read caught two wording defects, both fixed before commit: violet-quarry's
request named only the refundable fare with no fallback (lesson 3: "If that isn't allowed, book what the policy
allows; I have to be at the briefing" added), and the personal-trip records gave a work start time for trips with no
work (now empty, and the field description says so). The flags were checked for both readings: hazel-pond (Miami
$395 against the nonstop $520, both in time) and gull-heather (KLM $1,180, fastest of the U.S./EU pool, against
United $1,460; Emirates excluded on both readings).

## 6. Hosted-cap estimate

Full-handbook prompt: 72,112 bytes, 10,801 words: about 14,400 tokens at 1.33 a word, about 16,200 on the
Thornton/NJC calibration (0.2 a character plus 1,800) for the first call. A 3-call run (`get_trip`,
`search_flights`, `submit`) is about 50,000 to 51,000 input tokens: under the 65,536 cap (about 15,000 to spare,
enough for no repeated search). `saffron-dell` needs a second search, so about 68,000 over 4 calls: it crosses the
cap when hosted.

## 7. Template change requests

- **Airports for IPA's country offices** (shared `world.py`): ACC (Accra), EBB (Entebbe), LUN (Lusaka), LIM (Lima),
  MNL (Manila), DAC (Dhaka), and the carrier ET (Ethiopian Airlines, hub ADD). Not needed for this build: Nairobi,
  Bogota, Mexico City, Johannesburg and Delhi stood in.
- **A changeability flag on offers** (shared `contract.Offer`): "changeable for a fee" separate from refundable would
  let lines 334-336 be tested on basic-economy fares that cannot be changed. Worked around with the convention
  sentence in the `search_flights` description and `rules.CONVENTIONS`.
- South African Airways' range (12,000 km) rules out U.S.-Johannesburg nonstops; Delta, United, Emirates and Qatar
  were used instead. No change requested.

## 8. Acceptance outputs

```
$ uv run pytest -q
252 passed in 2.68s
$ uv run ruff check .
All checks passed!
$ uv lock --check
Resolved 42 packages in 11ms
$ python3 ../_template/check_shared.py .
: ok
$ /Users/tejassaboo/Code/Rice/COMP580/nanoagent/nanoagent/.venv/bin/nanoagent plugin inspect .
inspect exit 0
$ nanoagent plugin pack . <scratchpad>/ipa-flight-policy-final.tar.gz
packed . into .../ipa-flight-policy-final.tar.gz (187862 bytes)
$ /Users/tejassaboo/Code/Rice/COMP580/nanoagent/nanoagent/.venv/bin/python ../_template/tools/stock_verify.py .
alder-crane          right=True score=1.00 identical=True wrong-decision-rejected=True
amber-wharf          right=True score=1.00 identical=True wrong-decision-rejected=True
basil-tern           right=True score=1.00 identical=True wrong-decision-rejected=True
birch-hollow         right=True score=1.00 identical=True wrong-decision-rejected=True
cedar-flint          right=True score=1.00 identical=True wrong-decision-rejected=True
cobalt-reed          right=True score=1.00 identical=True wrong-decision-rejected=True
dahlia-mist          right=True score=1.00 identical=True wrong-decision-rejected=True
dune-sparrow         right=True score=1.00 identical=True wrong-decision-rejected=True
elm-thistle          right=True score=1.00 identical=True wrong-decision-rejected=True
ember-kite           right=True score=1.00 identical=True wrong-decision-rejected=True
fennel-gorge         right=True score=1.00 identical=True wrong-decision-rejected=True
fir-cobble           right=True score=1.00 identical=True wrong-decision-rejected=True
gull-heather         right=True score=1.00 identical=True wrong-decision-rejected=True
hazel-pond           right=True score=1.00 identical=True wrong-decision-rejected=True
heron-moss           right=True score=1.00 identical=True wrong-decision-rejected=True
indigo-fern          right=True score=1.00 identical=True wrong-decision-rejected=True
jasper-cove          right=True score=1.00 identical=True wrong-decision-rejected=True
kestrel-bloom        right=True score=1.00 identical=True wrong-decision-rejected=True
larkspur-tide        right=True score=1.00 identical=True wrong-decision-rejected=True
marble-finch         right=True score=1.00 identical=True wrong-decision-rejected=True
nectar-ridge         right=True score=1.00 identical=True wrong-decision-rejected=True
opal-heath           right=True score=1.00 identical=True wrong-decision-rejected=True
pewter-lake          right=True score=1.00 identical=True wrong-decision-rejected=True
quill-harbor         right=True score=1.00 identical=True wrong-decision-rejected=True
russet-brook         right=True score=1.00 identical=True wrong-decision-rejected=True
saffron-dell         right=True score=1.00 identical=True wrong-decision-rejected=True
tamarind-crest       right=True score=1.00 identical=True wrong-decision-rejected=True
umber-glade          right=True score=1.00 identical=True wrong-decision-rejected=True
violet-quarry        right=True score=1.00 identical=True wrong-decision-rejected=True
walnut-spire         right=True score=1.00 identical=True wrong-decision-rejected=True
yarrow-bluff         right=True score=1.00 identical=True wrong-decision-rejected=True
zephyr-moor          right=True score=1.00 identical=True wrong-decision-rejected=True
32 scenarios, 0 failures
```
