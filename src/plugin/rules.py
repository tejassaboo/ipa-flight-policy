"""The answer key's rules for the Innovations for Poverty Action (IPA) Global Travel Manual (Version 1, 1 October
2021), as exact integer code. Byte-identical in src/plugin/rules.py and verifier/rules.py; it imports only modules a
verifier may use.

Every rule cites the frozen handbook text (src/plugin/data/policy.txt) by line. Where the text leaves an answer
open, the rule returns FLAG_FOR_APPROVAL with the unclear words, and a scenario may depend on each unclear phrase at
most once (tests/test_scenarios.py). Combinations no scenario needs raise ValueError, so a new scenario cannot fall
silently into untested logic. Nothing here rests on the annexes (lines 1098-1109), which the text lists by title only.

The duration hook. Lines 347-353 permit an international rest period (overnight layover) when "The scheduled flight
time, including non-overnight stopovers and change of planes, is in excess of 14 hours" (strict: more than 840
minutes), the layover does not exceed 24 hours (inclusive: 1,440 minutes or less), the route is direct or usually
traveled, and travel is by coach. The time is measured over the journey: every scheduled flight plus every
connection that is not an overnight stop (ground time between planes counts; the overnight stop itself does not).
For an itinerary without an overnight stop that is its elapsed minutes. A reader may instead measure the journey by
the same-day itineraries listed beside the overnight one, so the rules raise when the two measures fall on opposite
sides of 14 hours (no scenario does).
"""

from contract import (
    Approver,
    Cabin,
    Clause,
    Decision,
    Funding,
    Passenger,
    Purpose,
    ReasonCode,
    SignOffSubject,
    StaffUnit,
)

from .world import airport, days_between, utc_minute, utc_offset

HANDBOOK = "Innovations for Poverty Action, IPA Global Travel Manual, Version 1, 1 October 2021"

# Each closed-list section and the heading it names in the frozen text (tests check every heading is there).
CLAUSE_HEADINGS = {
    Clause.PURPOSE_AND_SCOPE: "1. Purpose & Scope",
    Clause.APPLICABILITY: "2. Applicability",
    Clause.ROLES_AND_RESPONSIBILITIES: "3. Roles & Responsibilities",
    Clause.POLICIES: "4. Policies",
    Clause.POLICY_IMPLEMENTATION: "5. Policy Implementation",
    Clause.TRAVEL_APPROVAL: "Travel Approval",
    Clause.TRAVEL_ADVANCES: "Travel Advances",
    Clause.TRAVEL_EXPENSES: "Travel Expenses",
    Clause.PER_DIEM: "Per Diem",
    Clause.SAFETY_AND_SECURITY: "Safety & Security",
    Clause.TRAVEL_DOCUMENTATION: "Travel Documentation",
    Clause.AIRFARE: "Airfare",
    Clause.GROUND_TRANSPORTATION: "Ground Transportation",
    Clause.LODGING: "Lodging",
    Clause.COMMUNICATION: "Communication",
    Clause.PROPERTY_AND_EQUIPMENT: "Property and IT Equipment",
    Clause.USG_FUNDED_TRAVEL: "U.S. Government-funded Travel",
    Clause.GUIDANCE: "6. Guidance",
    Clause.PREPARING_FOR_TRAVEL: "Procedure 1: Preparing for Travel",
    Clause.DURING_AND_AFTER_TRAVEL: "Procedure 2: During and After Travel",
    Clause.REIMBURSABLE_EXPENSES: "Procedure 3: Reimbursable Travel Expenses",
    Clause.US_GOVERNMENT_PROCEDURE: "Procedure 4: US Government-funded Travel",
}

# The handbook's duration threshold (the per-handbook duration hook; tests/test_duration.py tests both sides).
DURATION_RULES = (
    {"name": "rest-stop", "minutes": 840, "operator": ">", "lines": [349, 350],
     "quote": "The scheduled flight time, including non-overnight stopovers and change of planes, is in excess of "
              "14 hours;"},
)
LIMITS = {rule["name"]: rule["minutes"] for rule in DURATION_RULES}

# Handbook-specific conventions shown by booking_requirements, beyond the template's. Lines 334-336 ask for the
# lowest economy fare "that can be changed with a fee"; the world's fares carry only a refundable flag, so the
# convention says what a fare that is not refundable allows (the search_flights description says it too).
CONVENTIONS = ("A fare that is not refundable can still be changed for a fee.",)

# Lines 351: "The layover may not exceed 24 hours" (inclusive, minutes).
REST_STOP_LAYOVER_MINUTES = 1440
# Line 517 (and 1081): "Flying on a US carrier would take at least 6 hours longer than if foreign carrier were used"
# (inclusive, minutes of elapsed journey time).
FLY_AMERICA_LONGER_MINUTES = 360
# Line 520 (and 1083): "For flights of less than 3 hours, flying US carrier would take 2 times as long": not modelled;
# the rules raise when a scenario comes near it.
FLY_AMERICA_SHORT_FLIGHT_MINUTES = 180
# Lines 344-346: the medical note "must be no more than one year old". A year is 365 or 366 days, and the text does
# not say whether age counts at booking or at travel: a note at most 365 days old on the travel date is valid on
# every reading, one more than 366 days old on the booking date is not; between the two is not modelled.
NOTE_VALID_DAYS = 365
NOTE_STALE_DAYS = 366
# Line 147: listed countries need Global Operations told "prior to booking travel and at least two weeks in advance
# of travel" (inclusive, calendar days).
NOTICE_DAYS = 14
# Lines 147-153, the listed countries the simulated world has an airport in (Egypt, India, Turkey).
NOTICE_COUNTRIES = {"EG", "IN", "TR"}
# Lines 334-335: the fare must meet the business need "including arrival and departure times". No scenario puts an
# arrival within three hours of the start of the work, where a reader could doubt it is in time.
ARRIVAL_MARGIN_MINUTES = 180

# Lines 504-506 and 1065-1067: U.S.-flag air carriers; lines 1073-1076: European Community (EU) airlines under the
# US-EU Open Skies Agreement. Airlines by the names search_flights shows. The world shows no code shares (every
# flight number is the operating airline's), so a foreign airline's flight is never a U.S. code share.
US_CARRIERS = {"American Airlines", "Delta Air Lines", "United Airlines", "Alaska Airlines", "JetBlue",
               "Southwest Airlines"}
EU_CARRIERS = {"Air France", "KLM", "Lufthansa", "Iberia", "Aer Lingus"}
EU_COUNTRIES = {"IE", "FR", "NL", "DE", "ES", "IT", "DK"}

OPEN_SKIES_PHRASE = "between the U.S. and any point in an EU Member State"
ROUTE_PHRASE = "via the most direct and expeditious route"

LOW_CLAUSES = [Clause.AIRFARE, Clause.PREPARING_FOR_TRAVEL, Clause.REIMBURSABLE_EXPENSES]
USG_CLAUSES = [Clause.AIRFARE, Clause.USG_FUNDED_TRAVEL, Clause.US_GOVERNMENT_PROCEDURE]
APPROVAL_CLAUSES = [Clause.TRAVEL_APPROVAL, Clause.POLICIES, Clause.PREPARING_FOR_TRAVEL]


def over(rule, offer):
    """True or False: whether ``offer``'s journey time, as lines 349-350 measure it (every flight plus every
    connection that is not an overnight stop), is in excess of the rule's limit (rest-stop: more than 840 minutes)."""
    if rule not in LIMITS:
        raise ValueError(f"unknown duration rule {rule!r}")
    return journey_minutes(offer) > LIMITS[rule]


def journey_minutes(offer):
    ground = sum(minutes for minutes, night in zip(offer.layover_minutes, offer.stopover_nights) if not night)
    return offer.flying_minutes + ground


def by_value(items):
    return sorted(set(items), key=lambda item: item.value)


def answer(decision, offers, reasons, approvers, clauses, why, phrase=""):
    return {
        "decision": decision,
        "offer_ids": sorted({offer.offer_id for offer in offers}),
        "cabins": by_value(offer.cabin for offer in offers) or [Cabin.NONE],
        "reason_codes": by_value(reasons),
        "approvers": by_value(approvers),
        "clauses": by_value(clauses),
        "unclear_phrase": phrase,
        "explanation": why,
    }


def on_file(trip):
    """NONE and every role with a sign-off on file (SYNC_NOTES 4' and 4(b)): a booking or refusal whose sign-offs
    are already on file accepts their roles and NONE, as readers split on whether a sign-off already given is still
    'relied on'."""
    return [Approver.NONE, *(record.role for record in trip.sign_offs)]


def refuse(trip, reasons, clauses, why):
    return answer(Decision.REFUSE, [], reasons, on_file(trip), clauses, why)


def cheapest(offers):
    if not offers:
        return []
    low = min(offer.fare_cents for offer in offers)
    return [offer for offer in offers if offer.fare_cents == low]


def signed(trip, subject, role):
    return any(record.subject == subject and record.role == role for record in trip.sign_offs)


def route_of(offer):
    return offer.segments[0].origin, offer.segments[-1].destination


def international(trip):
    return trip.origin.country != trip.destination.country


def overnight(offer):
    return any(offer.stopover_nights)


def arrival_slack(trip, offer):
    """Minutes from the last landing to the start of the work (negative when it lands after the start)."""
    start = trip.business_starts
    start_utc = utc_minute(start) - utc_offset(trip.destination.code)
    return start_utc - utc_minute(offer.segments[-1].arrive_utc)


def in_time(trip, offers):
    """Lines 334-335: the fare must meet the business need, including arrival times."""
    kept = []
    for offer in offers:
        slack = arrival_slack(trip, offer)
        if 0 <= slack < ARRIVAL_MARGIN_MINUTES:
            raise ValueError("an arrival within three hours of the start of the work is not modelled")
        if slack >= 0:
            kept.append(offer)
    return kept


def lowest_direct(pool, what):
    """The lowest fare of ``pool``, which must also be on the most direct (fewest connections) and most expeditious
    (shortest elapsed) itinerary of the pool, so that every reading of lines 334-336 gives it; raises otherwise."""
    best = cheapest(pool)
    if not best:
        raise ValueError(f"no {what} can be bought")
    fewest = min(offer.stops for offer in pool)
    fastest = min(offer.elapsed_minutes for offer in pool)
    if any(offer.stops != fewest or offer.elapsed_minutes != fastest for offer in best):
        raise ValueError(f"the lowest {what} is not on the most direct and expeditious itinerary")
    if any(offer.refundable for offer in best):
        raise ValueError("a refundable fare that is the lowest is not modelled")
    return best


def lowest_or_unclear(pool):
    """Lines 334-336: 'the lowest economy fare (coach) that meets the business need ... via the most direct and
    expeditious route'. When the lowest fare is not on the most direct and expeditious itinerary the text does not say
    which wins: (None, [the lowest, the cheapest most direct and expeditious]). Otherwise (the lowest, None)."""
    best = cheapest(pool)
    if not best:
        raise ValueError("no economy fare can be bought")
    fewest = min(offer.stops for offer in pool)
    fastest = min(offer.elapsed_minutes for offer in pool)
    if all(offer.stops == fewest and offer.elapsed_minutes == fastest for offer in best):
        return lowest_direct(pool, "economy fare"), None
    quickest = [offer for offer in pool if offer.stops == fewest and offer.elapsed_minutes == fastest]
    if not quickest:
        raise ValueError("the most direct itinerary is not the most expeditious one: not modelled")
    return None, [*best, *cheapest(quickest)]


# ----- who must approve the trip -----


def trip_roles(trip):
    """Lines 159-161: domestic travel is approved by the Assignment Supervisor; international travel by the Country
    Director (Country Office staff) or the appropriate Global Team Director (Global Team staff). Lines 659-672 and
    70-72: the Assignment Supervisor approves the itinerary in every case."""
    roles = [Approver.ASSIGNMENT_SUPERVISOR]
    if international(trip):
        roles.append(Approver.COUNTRY_DIRECTOR if trip.staff_unit == StaffUnit.COUNTRY_OFFICE
                     else Approver.GLOBAL_TEAM_DIRECTOR)
    return roles


def missing_trip_roles(trip):
    given = {record.role for record in trip.sign_offs if record.subject == SignOffSubject.TRIP}
    if Approver.ASSIGNMENT_SUPERVISOR not in given:
        raise ValueError("a trip without the Assignment Supervisor's sign-off is not modelled")
    extra = given - set(trip_roles(trip))
    if extra:
        raise ValueError(f"trip sign-offs by {sorted(role.value for role in extra)} are not modelled")
    return [role for role in trip_roles(trip) if role not in given]


def notice_check(trip):
    """Line 147: travel to a listed country needs Global Operations told before booking and at least two weeks
    before travel. Every scenario to a listed country has it on time; anything else is not modelled."""
    if trip.destination.country not in NOTICE_COUNTRIES:
        return []
    told = trip.global_operations_told
    if not told or days_between(told, trip.booking_date) <= 0 or days_between(told, trip.travel_date) < NOTICE_DAYS:
        raise ValueError("travel to a listed country without timely notice to Global Operations is not modelled")
    return [Clause.POLICIES]


# ----- the answer key -----


def solve(trip, offers, hidden):
    """The answer key for one trip and the offers on its searches: the decision, and every accepted offer id,
    cabin, reason, approver and section. ``hidden`` (the scenario's answer_key_inputs) is unused by this handbook."""
    if hidden:
        raise ValueError("this handbook's scenarios carry no answer_key_inputs")
    if any(offer.return_segments for offer in offers):
        raise ValueError("round-trip fares are not modelled: every case buys a one-way ticket")
    seated = [offer for offer in offers if offer.seats_available]
    route = [offer for offer in seated if route_of(offer) == (trip.origin.code, trip.destination.code)]
    if trip.passenger in (Passenger.SPOUSE, Passenger.CHILD):
        return family(trip, route)
    if trip.passenger != Passenger.EMPLOYEE:
        raise ValueError(f"a {trip.passenger.value} passenger is not modelled")
    if trip.purpose_kind == Purpose.PERSONAL:
        return refuse(trip, [ReasonCode.PERSONAL_TRAVEL_NOT_COVERED, ReasonCode.OUTSIDE_POLICY_SCOPE],
                      [Clause.AIRFARE, Clause.POLICIES],
                      "Lines 388-390: personal travel is the responsibility of the employee, and IPA will not reimburse "
                      "personal travel expenses; lines 128-129: IPA pays for travel on authorized business. This trip "
                      "is personal, so IPA buys no ticket.")
    if trip.home_airport.code != trip.origin.code:
        return deviation(trip, seated, route)
    return employee(trip, route)


def employee(trip, route):
    notes = notice_check(trip)
    found = choose(trip, route)
    missing = missing_trip_roles(trip)
    if not missing:
        if found["decision"] == Decision.BOOK and notes:
            found["clauses"] = by_value([*found["clauses"], *notes])
            found["explanation"] += (" Line 147: Global Operations was told before booking and at least two weeks "
                                     "before travel.")
        return found
    if found["decision"] != Decision.BOOK:
        raise ValueError("a missing trip approval beside another hold is not modelled")
    held = [offer for offer in route if offer.offer_id in found["offer_ids"]]
    return answer(Decision.FLAG_FOR_APPROVAL, held, [ReasonCode.APPROVAL_REQUIRED], missing, APPROVAL_CLAUSES,
                  "Lines 115-116: all travel must be approved by the relevant supervisory authority before booking; "
                  "lines 159-161: international travel by a Country Office employee must be approved by the Country "
                  "Director. Only the Assignment Supervisor has signed, so hold the fare the policy allows ("
                  + found["explanation"] + ") for the Country Director.")


def family(trip, route):
    """Lines 142-146: a spouse's or child's travel is reimbursed only with a bona fide business purpose for their
    travel, documented in the travel request and approved by the budget-holder."""
    if not trip.accompanies or trip.requested_cabin != Cabin.ECONOMY:
        raise ValueError("family travel with nobody accompanied, or outside economy, is not modelled")
    if trip.purpose_kind == Purpose.PERSONAL:
        return refuse(trip, [ReasonCode.COMPANION_NOT_COVERED, ReasonCode.PERSONAL_TRAVEL_NOT_COVERED],
                      [Clause.POLICIES, Clause.AIRFARE],
                      "Lines 142-146: a spouse's travel is reimbursed only when there is a bona fide business purpose "
                      "for it; this trip is sightseeing, so IPA buys no ticket (lines 388-390: personal travel is the "
                      "traveller's own).")
    if not signed(trip, SignOffSubject.COMPANION_TRAVEL, Approver.BUDGET_HOLDER):
        raise ValueError("family travel with a business purpose but no budget-holder approval is not modelled")
    if missing_trip_roles(trip):
        raise ValueError("family travel on a trip missing its approval is not modelled")
    if trip.funding != Funding.OVERHEAD or trip.chosen_airline or trip.wants_refundable or trip.wants_overnight_stop:
        raise ValueError("family travel with other wishes is not modelled")
    pool = in_time(trip, [offer for offer in route if offer.cabin == Cabin.ECONOMY and not overnight(offer)])
    best = lowest_direct(pool, "economy fare")
    return answer(Decision.BOOK, best, [ReasonCode.COMPANION_TRAVEL_AUTHORIZED, ReasonCode.LOWEST_FARE],
                  on_file(trip), [Clause.POLICIES, Clause.AIRFARE],
                  "Lines 142-146: the spouse's travel has a bona fide business purpose, written in the travel request "
                  "and approved by the budget-holder, so it is reimbursed; line 334: the lowest economy fare.")


def choose(trip, route):
    """The fare for an employee's trip with its approvals checked by the caller."""
    if trip.requested_cabin != Cabin.ECONOMY:
        return upgraded(trip, route)
    economy = [offer for offer in route if offer.cabin == Cabin.ECONOMY]
    pool = in_time(trip, economy)
    late = [offer for offer in economy if offer not in pool]
    timing = []
    if late and pool and min(offer.fare_cents for offer in late) < min(offer.fare_cents for offer in pool):
        timing = [ReasonCode.BUSINESS_NEED_TIMING]
    if trip.wants_overnight_stop:
        if trip.funding != Funding.OVERHEAD or trip.chosen_airline or trip.wants_refundable or timing:
            raise ValueError("a night's stop with other wishes is not modelled")
        return rest_stop(trip, pool)
    stops = [offer for offer in pool if overnight(offer)]
    pool = [offer for offer in pool if not overnight(offer)]
    if stops and pool and min(offer.fare_cents for offer in stops) <= min(offer.fare_cents for offer in pool):
        raise ValueError("an overnight itinerary nobody asked for that is the cheapest is not modelled")
    if trip.funding == Funding.US_GOVERNMENT:
        if timing or trip.wants_refundable:
            raise ValueError("Fly America with other wishes is not modelled")
        return fly_america(trip, pool)
    if trip.chosen_airline:
        if timing or trip.wants_refundable:
            raise ValueError("a chosen airline with other wishes is not modelled")
        return airline_choice(trip, pool)
    if trip.wants_refundable:
        if timing:
            raise ValueError("a refundable wish with a timing constraint is not modelled")
        return refundable(trip, pool)
    if trip.pays_difference:
        raise ValueError("an offer to pay with nothing asked for is not modelled")
    best, unclear = lowest_or_unclear(pool)
    if unclear:
        if timing:
            raise ValueError("an unclear routing with a timing constraint is not modelled")
        return answer(Decision.FLAG_FOR_APPROVAL, unclear, [ReasonCode.UNCLEAR_POLICY_TEXT, ReasonCode.APPROVAL_REQUIRED],
                      [Approver.NOT_NAMED, Approver.ASSIGNMENT_SUPERVISOR, Approver.CHIEF_FINANCIAL_OFFICER], LOW_CLAUSES,
                      "Lines 334-336: air travel uses 'the lowest economy fare (coach) that meets the business need "
                      "(including arrival and departure times) via the most direct and expeditious route'. The lowest "
                      "fare connects and takes longer; the nonstop is the most direct and expeditious but dearer, and "
                      "both arrive in time. The text does not say whether the route words pick the itinerary or only "
                      "qualify the lowest fare: hold, for the Assignment Supervisor's review of the itinerary (lines "
                      "671-675).", phrase=ROUTE_PHRASE)
    reasons = [ReasonCode.LOWEST_FARE, *timing]
    why = "Lines 334-336: the lowest economy fare that meets the business need, on the most direct and expeditious route"
    if timing:
        why += ("; the cheaper flight lands after the work begins, so it does not meet the business need (arrival "
                "times)")
    return answer(Decision.BOOK, best, reasons, on_file(trip), LOW_CLAUSES, why + ".")


def upgraded(trip, route):
    """A cabin above economy. Lines 339-341: upgraded classes are not reimbursable; upgrades are permitted at the
    traveller's personal expense; exceptions must be approved by the CFO. Lines 344-346: a medical exception with a
    signed doctor's note no more than one year old, on file for each trip."""
    if trip.funding != Funding.OVERHEAD or trip.chosen_airline or trip.wants_refundable or trip.wants_overnight_stop:
        raise ValueError("an upgrade with other wishes or federal funding is not modelled")
    if trip.requested_cabin != Cabin.PREMIUM_ECONOMY:
        raise ValueError(f"a {trip.requested_cabin.value} request is not modelled")
    asked = in_time(trip, [offer for offer in route if offer.cabin == trip.requested_cabin and not overnight(offer)])
    economy = in_time(trip, [offer for offer in route if offer.cabin == Cabin.ECONOMY and not overnight(offer)])
    if trip.medical_note_date:
        if trip.pays_difference:
            raise ValueError("a medical note and an offer to pay are not modelled together")
        valid = days_between(trip.medical_note_date, trip.travel_date) <= NOTE_VALID_DAYS
        stale = days_between(trip.medical_note_date, trip.booking_date) > NOTE_STALE_DAYS
        if not valid:
            raise ValueError("a medical note over a year old is not modelled" if stale else
                             "a medical note about a year old is not modelled")
        wanted = lowest_direct(asked, "premium economy fare")
        if signed(trip, SignOffSubject.UPGRADE_EXCEPTION, Approver.CHIEF_FINANCIAL_OFFICER):
            return answer(Decision.BOOK, wanted, [ReasonCode.MEDICAL_NEED, ReasonCode.POLICY_EXCEPTION_APPROVED],
                          on_file(trip), [Clause.AIRFARE],
                          "Lines 341 and 344-346: an exception to upgraded classes, requested for medical reasons with a "
                          "signed doctor's note less than a year old on file, approved by the CFO: the lowest premium "
                          "economy fare.")
        return answer(Decision.FLAG_FOR_APPROVAL, wanted, [ReasonCode.APPROVAL_REQUIRED, ReasonCode.MEDICAL_NEED],
                      [Approver.CHIEF_FINANCIAL_OFFICER], [Clause.AIRFARE],
                      "Lines 341 and 344-346: the medical exception 'may be approved' with a valid doctor's note, and "
                      "exceptions must be approved by the CFO, whose approval is not on file: hold the lowest premium "
                      "economy fare for the CFO.")
    if trip.pays_difference:
        return answer(Decision.BOOK, lowest_direct(asked, "premium economy fare"),
                      [ReasonCode.TRAVELER_PAYS_UPGRADE, ReasonCode.TRAVELER_PAYS_DIFFERENCE], on_file(trip),
                      [Clause.AIRFARE],
                      "Line 340: upgrades to other-than-economy fare are permitted at the traveler's personal expense; "
                      "the traveller pays the premium economy fare's excess: the lowest premium economy fare.")
    return answer(Decision.BOOK, lowest_direct(economy, "economy fare"), [ReasonCode.UPGRADE_NOT_ELIGIBLE],
                  on_file(trip), [Clause.AIRFARE],
                  "Lines 339-340: upgraded classes of service are not reimbursable, and no exception is on file (lines "
                  "341-346); the traveller accepts economy, so the lowest economy fare (line 334).")


def rest_stop(trip, pool):
    """Lines 347-353: an international rest period (overnight layover) is permitted when the scheduled flight time
    is in excess of 14 hours, the layover does not exceed 24 hours, the route is direct or usually traveled, and
    travel is by coach."""
    if not international(trip):
        raise ValueError("a night's stop on a domestic trip is not modelled")
    stops = [offer for offer in pool if overnight(offer)]
    plain = [offer for offer in pool if not overnight(offer)]
    if not stops or not plain:
        raise ValueError("a night's stop needs an overnight itinerary and a same-day one")
    good, long_fail, layover_fail = [], False, False
    for offer in stops:
        long = over("rest-stop", offer)
        if any((other.elapsed_minutes > LIMITS["rest-stop"]) != long for other in plain):
            raise ValueError("the overnight and same-day itineraries on opposite sides of 14 hours are not modelled")
        nights = [minutes for minutes, night in zip(offer.layover_minutes, offer.stopover_nights) if night]
        fits = all(minutes <= REST_STOP_LAYOVER_MINUTES for minutes in nights)
        long_fail |= not long
        layover_fail |= not fits
        if long and fits:
            good.append(offer)
    if good:
        if len(good) != len(stops):
            raise ValueError("permitted and refused overnight itineraries together are not modelled")
        return answer(Decision.BOOK, cheapest(good), [ReasonCode.REST_STOP_PERMITTED, ReasonCode.INTERNATIONAL_LONG_FLIGHT],
                      on_file(trip), [Clause.AIRFARE],
                      "Lines 347-353: travelling internationally, the scheduled flight time with connections is in "
                      "excess of 14 hours, the overnight layover is no more than 24 hours, the route is a usual one and "
                      "the fare is coach, so the rest period is permitted: book the overnight itinerary asked for.")
    if long_fail and layover_fail:
        raise ValueError("an overnight itinerary failing both tests is not modelled")
    reasons = [ReasonCode.REST_STOP_CONDITIONS_NOT_MET,
               ReasonCode.LONG_FLIGHT_CONDITION_NOT_MET if long_fail else ReasonCode.CONNECTION_TOO_LONG]
    why = ("the scheduled flight time is not in excess of 14 hours" if long_fail
           else "the overnight layover exceeds 24 hours")
    return answer(Decision.BOOK, lowest_direct(plain, "same-day economy fare"), reasons, on_file(trip), [Clause.AIRFARE],
                  f"Lines 347-353: {why}, so the rest period is not permitted; the traveller asked for what the policy "
                  "allows otherwise: the lowest economy fare on the most direct route (line 334).")


def fly_america(trip, pool):
    """Lines 504-506 (and 1065-1067): US-government-funded air travel with its origin or final destination in the
    United States must be on a U.S.-flag carrier, an Open Skies carrier or a U.S. code share; cost alone is no
    justification (lines 508-509). Lines 513-527: the exceptions. Lines 1073-1076: EU airlines between the U.S. and
    an EU Member State, or between two points outside the United States."""
    places = {trip.origin.country, trip.destination.country}
    if "US" not in places:
        raise ValueError("federally funded travel between two points abroad is not modelled")
    if trip.pays_difference and not trip.chosen_airline:
        raise ValueError("an offer to pay under Fly America with nothing asked for is not modelled")
    us = [offer for offer in pool if offer.carrier in US_CARRIERS]
    eu = [offer for offer in pool if offer.carrier in EU_CARRIERS]
    other = [offer for offer in pool if offer not in us and offer not in eu]
    if not us:
        raise ValueError("no U.S. carrier seat listed: not modelled")
    # An EU airline is plainly covered when the trip runs between the U.S. and an EU Member State and every airport
    # of the itinerary is in one or the other; otherwise (the U.S. to a third country through an EU hub) it is open.
    plain_route = len(places) == 2 and places - {"US"} <= EU_COUNTRIES
    clear_eu = [offer for offer in eu if plain_route and all(airport(code).country in EU_COUNTRIES | {"US"}
                                                             for code in itinerary_airports(offer))]
    open_eu = [offer for offer in eu if offer not in clear_eu]
    foreign = [*eu, *other]
    fastest_us = min(offer.elapsed_minutes for offer in us)
    if foreign:
        quickest = min(offer.elapsed_minutes for offer in foreign)
        cheap_foreign = cheapest(foreign)
        longer = fastest_us - quickest >= FLY_AMERICA_LONGER_MINUTES
        if longer != all(fastest_us - offer.elapsed_minutes >= FLY_AMERICA_LONGER_MINUTES for offer in cheap_foreign):
            raise ValueError("the exception holding against the fastest but not the cheapest foreign fare is not modelled")
        if min(offer.stops for offer in us) - min(offer.stops for offer in foreign) >= 2:
            raise ValueError("the plane-change exception is not modelled")
        if quickest < FLY_AMERICA_SHORT_FLIGHT_MINUTES:
            raise ValueError("the short-flight exception is not modelled")
    else:
        longer = False
    if longer:
        if trip.chosen_airline:
            raise ValueError("a chosen airline beside a Fly America exception is not modelled")
        best = lowest_direct(pool, "economy fare")
        return answer(Decision.BOOK, best, [ReasonCode.FLY_AMERICA_EXCEPTION, ReasonCode.LOWEST_FARE], on_file(trip),
                      USG_CLAUSES,
                      "Lines 504-506: federally funded travel from the U.S. must be on a U.S.-flag carrier, but line 517 "
                      "excepts a U.S. carrier that would take at least 6 hours longer than the foreign carrier, and it "
                      "does here: the lowest economy fare (line 334).")
    allowed = [*us, *clear_eu]
    if open_eu:
        if trip.chosen_airline or clear_eu:
            raise ValueError("an unclear EU itinerary with other wishes is not modelled")
        strict = lowest_direct(us, "U.S. carrier fare")
        loose = lowest_direct([*us, *open_eu], "U.S. or EU carrier fare")
        if {offer.offer_id for offer in strict} == {offer.offer_id for offer in loose}:
            raise ValueError("an EU itinerary that changes nothing is not modelled")
        return answer(Decision.FLAG_FOR_APPROVAL, [*strict, *loose],
                      [ReasonCode.UNCLEAR_POLICY_TEXT, ReasonCode.APPROVAL_REQUIRED],
                      [Approver.NOT_NAMED, Approver.GRANTS_TEAM, Approver.CHIEF_FINANCIAL_OFFICER],
                      [Clause.USG_FUNDED_TRAVEL, Clause.US_GOVERNMENT_PROCEDURE],
                      "Lines 504-506 allow an Open Skies carrier, and lines 1073-1076 allow EU carriers 'when traveling "
                      "(1) between the U.S. and any point in an EU Member State or (2) between any two points outside "
                      "the United States'. The cheapest fare is an EU airline from the U.S. to Kenya through an EU hub: "
                      "each flight fits one branch, but the journey fits neither. The text does not say which counts: "
                      "hold the EU fare or the U.S. carrier's.", phrase=OPEN_SKIES_PHRASE)
    best = lowest_direct(allowed, "U.S. or Open Skies carrier fare")
    if trip.chosen_airline:
        if not trip.pays_difference or any(offer.carrier == trip.chosen_airline for offer in allowed):
            raise ValueError("a chosen airline under Fly America is modelled only for a foreign airline")
        if not any(offer.carrier == trip.chosen_airline for offer in pool):
            raise ValueError("a chosen airline with no offer on the route is not modelled")
        return answer(Decision.BOOK, best, [ReasonCode.FLY_AMERICA_US_CARRIER_REQUIRED, ReasonCode.NATIONAL_CARRIER_REQUIRED],
                      on_file(trip), USG_CLAUSES,
                      "Lines 504-506: federally funded travel from the U.S. must be on a U.S.-flag carrier; the "
                      "traveller's airline is foreign and no exception applies (lines 513-527), and a personal "
                      "preference is no justification (lines 507-509) even when the traveller pays: the lowest U.S. "
                      "carrier fare.")
    cheaper_excluded = [offer for offer in pool if offer not in allowed and offer.fare_cents < best[0].fare_cents]
    if best[0].carrier in US_CARRIERS and cheaper_excluded:
        return answer(Decision.BOOK, best,
                      [ReasonCode.FLY_AMERICA_US_CARRIER_REQUIRED, ReasonCode.NATIONAL_CARRIER_REQUIRED,
                       ReasonCode.LOWEST_FARE], on_file(trip), USG_CLAUSES,
                      "Lines 504-506: federally funded travel from the U.S. must be on a U.S.-flag carrier; cost alone "
                      "is no justification for a foreign carrier (lines 508-509) and no exception applies (lines "
                      "513-527): the lowest U.S. carrier fare.")
    if best[0].carrier in EU_CARRIERS and not cheaper_excluded:
        return answer(Decision.BOOK, best, [ReasonCode.OPEN_SKIES_AGREEMENT, ReasonCode.LOWEST_FARE], on_file(trip),
                      USG_CLAUSES,
                      "Lines 504-506 and 1073-1076: an EU airline may carry federally funded travel between the U.S. and "
                      "a point in an EU Member State (Open Skies): the lowest economy fare (line 334).")
    raise ValueError("federally funded travel where Fly America changes nothing is not modelled")


def itinerary_airports(offer):
    return [segment.origin for segment in offer.segments] + [offer.segments[-1].destination]


def airline_choice(trip, pool):
    """Lines 336-338: alternative routing for personal preferences, such as air carrier, is the traveller's to pay
    for; lines 360-365: frequent flyer programmes must not influence flight selection at a cost to IPA beyond the
    lowest available economy fare."""
    lowest = lowest_direct(pool, "economy fare")
    chosen = [offer for offer in pool if offer.carrier == trip.chosen_airline]
    if not chosen:
        raise ValueError("a chosen airline with no offer on the route is not modelled")
    if any(offer.carrier == trip.chosen_airline for offer in lowest):
        raise ValueError("a chosen airline that is already the lowest fare is not modelled")
    if trip.pays_difference:
        wanted = cheapest(chosen)
        if any(offer.stops != lowest[0].stops or offer.elapsed_minutes > lowest[0].elapsed_minutes for offer in wanted):
            raise ValueError("a chosen airline on a less direct itinerary is not modelled")
        return answer(Decision.BOOK, wanted, [ReasonCode.TRAVELER_PAYS_DIFFERENCE, ReasonCode.LOYALTY_PROGRAM_PREFERENCE],
                      on_file(trip), [Clause.AIRFARE],
                      "Lines 336-338: a traveller who opts for another air carrier out of personal preference pays the "
                      "difference, and does here, so IPA bears no cost beyond the lowest economy fare (lines 360-365): "
                      "book the chosen airline's lowest fare.")
    # The ground for declining the airline is the lowest-fare test itself (lines 360-365, 'beyond the lowest
    # available economy fare'), so LOWEST_FARE names why the request is declined, as does the loyalty code.
    return answer(Decision.BOOK, lowest, [ReasonCode.LOWEST_FARE, ReasonCode.LOYALTY_PROGRAM_PREFERENCE],
                  on_file(trip), [Clause.AIRFARE],
                  "Lines 360-365: frequent flyer programmes must not influence flight selection at a cost to IPA beyond "
                  "the lowest available economy fare, and the traveller will not pay the difference (lines 336-338): "
                  "the lowest economy fare.")


def refundable(trip, pool):
    """Lines 334-336: the lowest economy fare 'that can be changed with a fee'; lines 403-404: change fees for
    business reasons are reimbursable when documented."""
    best = lowest_direct(pool, "economy fare")
    if not any(offer.refundable for offer in pool):
        raise ValueError("a refundable wish with no refundable offer is not modelled")
    return answer(Decision.BOOK, best, [ReasonCode.REFUNDABLE_FARE_NOT_ALLOWED, ReasonCode.LOWEST_FARE], on_file(trip),
                  LOW_CLAUSES,
                  "Lines 334-336: the lowest economy fare that can be changed with a fee, which a fare that is not "
                  "refundable is; a business change of date is then a reimbursable change fee (lines 403-404). The "
                  "dearer refundable fare is not the standard.")


def deviation(trip, seated, route):
    """Lines 175-179: an itinerary changed for personal reasons, such as leaving from somewhere other than the home of
    record, is disclosed in the approval request; lines 388-394: the traveller pays any incremental cost."""
    if missing_trip_roles(trip):
        raise ValueError("a personal change on a trip missing its approval is not modelled")
    if (trip.funding != Funding.OVERHEAD or trip.requested_cabin != Cabin.ECONOMY or trip.chosen_airline
            or trip.wants_refundable or trip.wants_overnight_stop or not trip.pays_difference):
        raise ValueError("a personal change with other wishes, or without the traveller paying, is not modelled")
    home = [offer for offer in seated if route_of(offer) == (trip.home_airport.code, trip.destination.code)
            and offer.cabin == Cabin.ECONOMY]
    best = lowest_direct(in_time(trip, [offer for offer in route if offer.cabin == Cabin.ECONOMY]), "economy fare")
    business_only = lowest_direct(in_time(trip, home), "economy fare from home")
    if best[0].fare_cents <= business_only[0].fare_cents:
        raise ValueError("a personal change that costs no more is not modelled")
    return answer(Decision.BOOK, best,
                  [ReasonCode.TRAVELER_PAYS_DIFFERENCE, ReasonCode.PERSONAL_TRAVEL_NOT_COVERED, ReasonCode.LOWEST_FARE],
                  on_file(trip), [Clause.AIRFARE, Clause.TRAVEL_APPROVAL, Clause.REIMBURSABLE_EXPENSES],
                  "Lines 175-179: leaving from a place other than the home of record for personal reasons is disclosed "
                  "in the approval, which is on file; lines 390-394: the traveller pays the incremental cost over the "
                  "fare from home, which they offer to do. Book the lowest economy fare from where they will be.")
