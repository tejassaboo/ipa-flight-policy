"""Writes the IPA scenario JSON files (an authoring aid, not a test; the JSON files are the truth).

    uv run python tests/build_scenarios.py

Expected answers are hand-written here; tests/test_scenarios.py checks them against rules.solve.
"""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

POLICY = (ROOT / "src/plugin/data/policy.txt").read_text(encoding="utf-8").split("\n")
OUT = ROOT / "src/plugin/data/scenarios"


def norm(text):
    return " ".join(text.split())


def keep(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    quote = text if quote is None else quote
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "sha256": hashlib.sha256(text.encode()).hexdigest(), "quote": quote, "why": why}


def aside(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "quote": quote, "why": why}


# ----- clauses the answers rest on -----
LOWEST = keep(334, 336, "Air travel must be arranged to the fullest extent possible using the lowest economy fare "
              "(coach) that meets the business need (including arrival and departure times) via the most direct and "
              "expeditious route that can be changed with a fee.",
              "the lowest changeable economy fare that meets the business need, on the most direct route")
TABLE = keep(888, 889, "Book using the most direct, expeditious and economical fare.",
             "the reimbursable-expenses table repeats the airfare standard")
INDEPENDENT = keep(654, 656, "ensuring that the selected flight is the lowest economy fare via the most direct and "
                   "expeditious route", "the booking procedure repeats the airfare standard")
PREFERENCE = keep(336, 338, "If travelers opt for alternative routing due to personal preferences, such as air carrier "
                  "or layover duration or location, the traveler must pay the difference.",
                  "a personal preference of carrier or layover is the traveller's to pay for")
UPGRADES = keep(339, 341, "Upgraded classes of service (e.g., Economy Plus, Coach Elite, Coach Plus, Preferred Coach) "
                "airfare are not reimbursable. Upgrades to other-than-economy fare are permitted at the traveler's "
                "personal expense. Exceptions to this policy must be approved by the CFO.",
                "no upgraded class at IPA's cost; permitted at the traveller's expense; exceptions by the CFO")
MEDICAL = keep(344, 346, None, "a medical exception to upgraded classes with a signed doctor's note under a year old")
REST = keep(347, 353, None, "an international rest stop: over 14 hours, layover up to 24 hours, usual route, coach")
FREQUENT = keep(360, 361, "participation in these programs must not influence flight selection",
                "frequent flyer programmes must not steer the flight choice")
FREQUENT_COST = keep(365, 365, "when doing so would result in incremental cost to IPA beyond the lowest available "
                     "economy fare.", "... at a cost beyond the lowest available economy fare")
CHANGE_FEES = keep(403, 404, "Change fees for air travel are reimbursable due to official business purposes when "
                   "justifiably documented.", "a change of date for business is a reimbursable change fee")
PERSONAL = keep(388, 394, None, "personal travel is the employee's; the traveller pays incremental costs")
DEVIATION = keep(175, 179, None, "an itinerary changed for personal reasons (another departure city) is disclosed")
DEVIATION_COST = keep(182, 183, "the traveler must present written evidence of the cost of trip if no personal travel "
                      "adjustments were to be made", "the business-only fare is the comparison")
COMPARISON = keep(891, 892, "Cost comparison if route or duration of stay is modified for personal reasons.",
                  "a cost comparison when the route changes for personal reasons")
APPROVE_ALL = keep(115, 116, "All travel must be approved by the relevant supervisory authority as described in this "
                   "policy prior to booking travel, including travel dates, proposed itinerary, and airfare costs.",
                   "every trip is approved before booking")
APPROVERS = keep(159, 161, None, "domestic travel: Assignment Supervisor; international: Country or Global Team Director")
ITINERARY = keep(659, 659, None, "the Assignment Supervisor approves the selected itinerary")
FURTHER = keep(686, 687, None, "further approvals are forwarded to the right people")
SPOUSE = keep(142, 146, None, "a spouse's travel only with a bona fide business purpose, documented, budget-holder approved")
BUSINESS_ONLY = keep(128, 129, "IPA will reimburse employees for all reasonable and necessary expenses while traveling "
                     "on authorized business", "IPA pays for travel on authorized business")
NOTICE = keep(147, 153, None, "listed countries (India among them): Global Operations told before booking, two weeks ahead")
FLY = keep(504, 506, None, "federally funded travel to or from the U.S. on a U.S.-flag, Open Skies or code share flight")
FLY_COST = keep(507, 509, "Cost alone is not a justification for taking a foreign carrier",
                "cost alone does not justify a foreign carrier")
POLICY_OWNER = keep(82, 84, "Global Operations is also responsible for establishing and updating IPA travel "
                    "policies in conjunction with internal stakeholders, overseeing IPA's compliance with this Travel "
                    "Manual", "Global Operations owns the travel policies: an unclear hold may await it")
FLY_SIX = keep(513, 517, None, "the exceptions, among them a U.S. carrier at least 6 hours longer")
FLY_PROC = keep(1065, 1066, None, "the procedure restates the U.S.-flag carrier rule")
FLY_PROC_SIX = keep(1081, 1081, None, "the procedure restates the 6-hour exception")
OPEN_SKIES = keep(1073, 1076, None, "EU airlines between the U.S. and an EU Member State, or between two points abroad")

# ----- nearby clauses that must not change the answer -----
ADVANCE = aside(354, 355, "Whenever possible, travelers must make air travel reservations as far in advance of travel as "
                "practical in order to obtain reasonable pricing.", "booking early 'whenever possible', not a ban")
WEEKS = aside(635, 636, "several weeks in advance of departure", "a procedural pointer, not a ban on late booking")
ELECTRONICS = aside(492, 494, "all IPA equipment must be transported in carry-on baggage", "a baggage rule, not a fare rule")
BAGGAGE = aside(382, 384, "Additional baggage costs will be covered by IPA only if the extra baggage is directly related "
                "to the transportation of IPA property", "a baggage rule, not a fare rule")
PER_DIEM = aside(270, 272, "IPA employees are eligible to receive per diem only when traveling for more than 12 "
                 "consecutive hours in one day.", "a per diem hour rule, not a flight rule")
SECURITY = aside(302, 303, "must request a security briefing from International SOS at least one week prior to travel.",
                 "a briefing rule, not a booking rule")
ABROAD = aside(526, 527, "Travel originates in a foreign country and is destined for a foreign country",
               "the two-points-abroad exception, which a trip from the U.S. does not meet")
HOLD = aside(577, 577, "Ability to hold tickets for 24 hours", "a benefit of the agency, not a rule")
CHANGE_PERSONAL = aside(417, 418, "Change fees resulting from traveler personal preferences", "personal change fees")

# ----- builders -----

AS = ("ASSIGNMENT_SUPERVISOR", "TRIP")
GTD = ("GLOBAL_TEAM_DIRECTOR", "TRIP")
CD = ("COUNTRY_DIRECTOR", "TRIP")


def sign(role, name, subject):
    return {"role": role, "name": name, "subject": subject}


def approvals(*pairs):
    names = {"ASSIGNMENT_SUPERVISOR": "Maya Chen", "GLOBAL_TEAM_DIRECTOR": "Daniel Osei",
             "COUNTRY_DIRECTOR": "Grace Wanjiru", "CHIEF_FINANCIAL_OFFICER": "Ruth Alvarez",
             "BUDGET_HOLDER": "Samuel Kim"}
    return [sign(role, names[role], subject) for role, subject in pairs]


def trip(**fields):
    base = {
        "traveller_name": "", "traveller_title": "", "passenger": "EMPLOYEE", "accompanies": "",
        "staff_unit": "GLOBAL_TEAM", "home_airport": "", "origin": "", "destination": "", "travel_date": "",
        "booking_date": "", "business_starts": "", "purpose": "", "purpose_kind": "PROJECT_WORK", "funding": "OVERHEAD",
        "funding_source": "IPA overhead funds", "award_terms": "", "requested_cabin": "ECONOMY", "chosen_airline": "",
        "pays_difference": False, "wants_refundable": False, "wants_overnight_stop": False, "medical_note_date": "",
        "global_operations_told": "", "sign_offs": [],
    }
    unknown = set(fields) - set(base)
    assert not unknown, unknown
    base.update(fields)
    if not base["home_airport"]:
        base["home_airport"] = base["origin"]
    return base


NSF = {"funding": "US_GOVERNMENT", "funding_source": "U.S. National Science Foundation research grant",
       "award_terms": "The grant's terms ask for no sponsor approval before travel."}
DOL = {"funding": "US_GOVERNMENT", "funding_source": "U.S. Department of Labor research grant",
       "award_terms": "The grant's terms ask for no sponsor approval before travel."}


def offer(slot, flight, cabin, cents, seats=True, refundable=False):
    data = {"slot": slot, "flight": flight, "cabin": cabin, "fare_cents": cents}
    if not seats:
        data["seats"] = False
    if refundable:
        data["refundable"] = True
    return data


def expected(decision, slots, cabins, reasons, approvers, clauses, phrase=""):
    return {"decision": decision, "offer_slots": slots, "cabins": cabins, "reason_codes": reasons,
            "approvers": approvers, "clauses": clauses, "unclear_phrase": phrase}


def search(origin, destination, date, flights, offers, name="main"):
    # No background offers: handbook.json background_offers is 0 and every search lists exactly its pinned offers.
    return {"name": name, "origin": origin, "destination": destination, "date": date, "return_date": "",
            "background": 0, "flights": flights, "offers": offers}


S = []


def scenario(id, category, overlays, request, trip_, searches, exp, must_keep, notes, twin_of="", twin_fact="",
             flag_twins=(), ambiguity="none", distractors=()):
    if isinstance(searches, dict):
        searches = [searches]
    S.append({
        "id": id, "category": category, "overlays": list(overlays), "twin_of": twin_of, "twin_fact": twin_fact,
        "flag_twins": list(flag_twins), "ambiguity_note": ambiguity, "request": request, "trip": trip_,
        "world": {"searches": list(searches)}, "expected": exp, "must_keep": list(must_keep),
        "distractors": list(distractors), "design_notes": notes,
    })


LOW = ["AIRFARE", "PREPARING_FOR_TRAVEL", "REIMBURSABLE_EXPENSES"]
USG = ["AIRFARE", "US_GOVERNMENT_PROCEDURE", "USG_FUNDED_TRAVEL"]
FLY_REQUIRED = ["FLY_AMERICA_US_CARRIER_REQUIRED", "LOWEST_FARE", "NATIONAL_CARRIER_REQUIRED"]
INTL = ["ASSIGNMENT_SUPERVISOR", "GLOBAL_TEAM_DIRECTOR", "NONE"]
DOMESTIC = ["ASSIGNMENT_SUPERVISOR", "NONE"]
APPROVAL_CLAUSES = ["POLICIES", "PREPARING_FOR_TRAVEL", "TRAVEL_APPROVAL"]
UNCLEAR = ["APPROVAL_REQUIRED", "UNCLEAR_POLICY_TEXT"]

# Shared worlds.
NAIROBI_GULF = {  # Dulles to Nairobi through the Gulf, same day
    "dubai": {"carrier": "EK", "via": ["DXB"], "depart": "10:15", "minutes": [780, 290], "layovers": [125]},
    "doha": {"carrier": "QR", "via": ["DOH"], "depart": "16:40", "minutes": [760, 330], "layovers": [150]},
}
BOGOTA = {
    "avianca": {"carrier": "AV", "depart": "08:05", "minutes": [330]},
    "miami": {"carrier": "AA", "via": ["MIA"], "depart": "07:00", "minutes": [165, 215], "layovers": [100]},
}

# ===== easy (6) =====

scenario(
    "amber-wharf", "easy", [],
    "I need to fly from New York LaGuardia to Chicago on December 8th for the donor meeting on the 9th at 9am. "
    "Economy, the cheapest seat is fine.",
    trip(traveller_name="Priya Raman", traveller_title="Associate Director, Development", origin="LGA",
         destination="ORD", travel_date="2026-12-08", booking_date="2026-11-24", business_starts="2026-12-09 09:00",
         purpose="Donor meeting in Chicago", purpose_kind="DONOR_MEETING", sign_offs=approvals(AS)),
    search("LGA", "ORD", "2026-12-08", {
        "early": {"carrier": "AA", "depart": "06:30"},
        "mid": {"carrier": "UA", "depart": "08:15"},
        "noon": {"carrier": "DL", "depart": "11:40"},
        "late": {"carrier": "AA", "depart": "17:05"},
    }, [
        offer("early-economy", "early", "ECONOMY", 18900, seats=False),
        offer("mid-economy", "mid", "ECONOMY", 21400),
        offer("noon-economy", "noon", "ECONOMY", 23600),
        offer("late-economy", "late", "ECONOMY", 25200, refundable=True),
    ]),
    expected("BOOK", ["mid-economy"], ["ECONOMY"], ["LOWEST_FARE"], DOMESTIC, LOW),
    [LOWEST, APPROVE_ALL, APPROVERS],
    "A domestic trip, approved by the Assignment Supervisor (lines 159-161). Every flight is a nonstop of the same "
    "length, so the lowest economy fare is also on the most direct and expeditious route (lines 334-336). The "
    "cheaper 06:30 fare is sold out; the refundable fare is dearer.")

scenario(
    "basil-tern", "easy", ["multi_leg", "overnight", "upgrade_not_taken"],
    "Please book me from New York JFK to Nairobi on January 12th for the field team training that starts on the "
    "15th. Economy is fine.",
    trip(traveller_name="Marcus Feld", traveller_title="Research Manager", origin="JFK", destination="NBO",
         travel_date="2027-01-12", booking_date="2026-12-01", business_starts="2027-01-15 09:00",
         purpose="Field team training in Nairobi", purpose_kind="TRAINING", sign_offs=approvals(AS, GTD)),
    search("JFK", "NBO", "2027-01-12", {
        "kenya": {"carrier": "KQ", "depart": "11:30", "minutes": [900]},
        "dubai": {"carrier": "EK", "via": ["DXB"], "depart": "10:40", "minutes": [770, 300], "layovers": [140]},
        "amsterdam": {"carrier": "KL", "via": ["AMS"], "depart": "18:00", "minutes": [400, 495], "layovers": [960],
                      "stopovers": [True]},
    }, [
        offer("kenya-economy", "kenya", "ECONOMY", 118000),
        offer("dubai-economy", "dubai", "ECONOMY", 129000),
        offer("amsterdam-economy", "amsterdam", "ECONOMY", 133000),
    ]),
    expected("BOOK", ["kenya-economy"], ["ECONOMY"], ["LOWEST_FARE"], INTL, LOW),
    [LOWEST, APPROVERS, REST],
    "International trip by a Global Team employee, approved by the Assignment Supervisor and the Global Team "
    "Director (lines 159-161). The Kenya Airways nonstop is the lowest economy fare and the most direct and "
    "expeditious. The KLM itinerary with a hotel night in Amsterdam would be a permitted rest stop (895 flying "
    "minutes, a 16-hour layover, lines 347-353), but the traveller did not ask for one and it costs more.")

scenario(
    "cobalt-reed", "easy", [],
    "JFK to Johannesburg on February 9th for the partner workshop on the 11th. It's a very long flight, so premium "
    "economy if I'm allowed it; if not, economy is fine.",
    trip(traveller_name="Hannah Okafor", traveller_title="Senior Policy Associate", origin="JFK", destination="JNB",
         travel_date="2027-02-09", booking_date="2027-01-05", business_starts="2027-02-11 09:00",
         purpose="Partner workshop in Johannesburg", purpose_kind="PARTNER_MEETING", requested_cabin="PREMIUM_ECONOMY",
         sign_offs=approvals(AS, GTD)),
    search("JFK", "JNB", "2027-02-09", {
        "delta": {"carrier": "DL", "depart": "11:15", "minutes": [960]},
        "doha": {"carrier": "QR", "via": ["DOH"], "depart": "09:40", "minutes": [750, 500], "layovers": [140]},
    }, [
        offer("delta-economy", "delta", "ECONOMY", 134000),
        offer("delta-premium", "delta", "PREMIUM_ECONOMY", 247000),
        offer("doha-economy", "doha", "ECONOMY", 139000),
        offer("doha-premium", "doha", "PREMIUM_ECONOMY", 256000),
    ]),
    expected("BOOK", ["delta-economy"], ["ECONOMY"], ["UPGRADE_NOT_ELIGIBLE"], INTL, ["AIRFARE"]),
    [UPGRADES, LOWEST],
    "Lines 339-340: upgraded classes are not reimbursable whatever the flight's length; no CFO exception and no "
    "doctor's note are on file, and the traveller does not offer to pay. The traveller accepts economy: the lowest "
    "economy fare, the Delta nonstop, which is also quicker than the Qatar connection.")

scenario(
    "dune-sparrow", "easy", [],
    "Washington Dulles to Bogota on January 20th for the partner meeting the next morning. Economy please.",
    trip(traveller_name="Paula Restrepo", traveller_title="Research Associate", origin="IAD", destination="BOG",
         travel_date="2027-01-20", booking_date="2026-12-14", business_starts="2027-01-21 09:00",
         purpose="Partner meeting in Bogota", purpose_kind="PARTNER_MEETING", sign_offs=approvals(AS, GTD)),
    search("IAD", "BOG", "2027-01-20", BOGOTA, [
        offer("avianca-economy", "avianca", "ECONOMY", 43000),
        offer("miami-economy", "miami", "ECONOMY", 46800),
    ]),
    expected("BOOK", ["avianca-economy"], ["ECONOMY"], ["LOWEST_FARE"], INTL, LOW),
    [LOWEST, APPROVERS],
    "The Avianca nonstop (330 minutes) is both the lowest economy fare and the most direct and expeditious route "
    "(the American connection through Miami takes 480 minutes and costs more): lines 334-336 on every reading.")

scenario(
    "ember-kite", "easy", ["outside_air_section"],
    "Nairobi to Johannesburg on February 16th for the regional data quality workshop on the 17th. My supervisor and "
    "the Country Director have approved the trip.",
    trip(traveller_name="Wanjiku Kamau", traveller_title="Data Quality Manager, Kenya", staff_unit="COUNTRY_OFFICE",
         origin="NBO", destination="JNB", travel_date="2027-02-16", booking_date="2027-01-25",
         business_starts="2027-02-17 09:00", purpose="Regional data quality workshop in Johannesburg",
         purpose_kind="TRAINING", sign_offs=approvals(AS, CD)),
    search("NBO", "JNB", "2027-02-16", {
        "kenya": {"carrier": "KQ", "depart": "08:30", "minutes": [240]},
        "springbok": {"carrier": "SA", "depart": "13:45", "minutes": [240]},
    }, [
        offer("kenya-economy", "kenya", "ECONOMY", 41000),
        offer("springbok-economy", "springbok", "ECONOMY", 45500),
    ]),
    expected("BOOK", ["kenya-economy"], ["ECONOMY"], ["LOWEST_FARE"],
             ["ASSIGNMENT_SUPERVISOR", "COUNTRY_DIRECTOR", "NONE"], LOW),
    [LOWEST, APPROVERS, APPROVE_ALL],
    "International travel by Country Office staff is approved by the Country Director (lines 159-161), whose "
    "sign-off is on file beside the Assignment Supervisor's: the lowest economy fare, Kenya Airways.")

scenario(
    "fennel-gorge", "easy", ["dearer_option"],
    "Dulles to London Heathrow on March 2nd for the funder meeting on the 3rd at 2pm. I'd like premium economy, and "
    "I'll cover the extra over the economy fare out of my own pocket.",
    trip(traveller_name="Owen Castellano", traveller_title="Director, Global Partnerships", origin="IAD",
         destination="LHR", travel_date="2027-03-02", booking_date="2027-02-01", business_starts="2027-03-03 14:00",
         purpose="Funder meeting in London", purpose_kind="DONOR_MEETING", requested_cabin="PREMIUM_ECONOMY",
         pays_difference=True, sign_offs=approvals(AS, GTD)),
    search("IAD", "LHR", "2027-03-02", {
        "british": {"carrier": "BA", "depart": "18:20", "minutes": [440]},
        "united": {"carrier": "UA", "depart": "17:45", "minutes": [440]},
    }, [
        offer("british-economy", "british", "ECONOMY", 69000),
        offer("british-premium", "british", "PREMIUM_ECONOMY", 142000),
        offer("united-economy", "united", "ECONOMY", 72000),
        offer("united-premium", "united", "PREMIUM_ECONOMY", 148000),
    ]),
    expected("BOOK", ["british-premium"], ["PREMIUM_ECONOMY"], ["TRAVELER_PAYS_DIFFERENCE", "TRAVELER_PAYS_UPGRADE"],
             INTL, ["AIRFARE"]),
    [UPGRADES],
    "Line 340: upgrades to other-than-economy fare are permitted at the traveler's personal expense, and the "
    "traveller pays the excess: book the lowest premium economy fare (British Airways; both nonstops are 440 "
    "minutes).")

# ===== boundary twins (8) =====

NAIROBI_STOP_REQUEST = ("JFK to Nairobi on February 23rd for the evaluation workshop that starts on the 26th. I'd like "
                        "to break the journey with a night in Amsterdam. If that isn't allowed, book what the policy "
                        "allows.")
NAIROBI_STOP_TRIP = {"traveller_name": "Elena Voss", "traveller_title": "Senior Research Manager", "origin": "JFK",
                         "destination": "NBO", "travel_date": "2027-02-23", "booking_date": "2027-01-26",
                         "business_starts": "2027-02-26 09:00", "purpose": "Evaluation workshop in Nairobi",
                         "purpose_kind": "PROJECT_WORK", "wants_overnight_stop": True, "sign_offs": approvals(AS, GTD)}


def nairobi_stop(extra):
    return search("JFK", "NBO", "2027-02-23", {
        "kenya": {"carrier": "KQ", "depart": "11:30", "minutes": [840 + extra]},
        "amsterdam": {"carrier": "KL", "via": ["AMS"], "depart": "18:00", "minutes": [395, 445 + extra],
                      "layovers": [900], "stopovers": [True]},
    }, [
        offer("kenya-economy", "kenya", "ECONOMY", 118000),
        offer("amsterdam-economy", "amsterdam", "ECONOMY", 129500),
    ])


scenario(
    "heron-moss", "boundary_twin", ["multi_leg", "overnight"], NAIROBI_STOP_REQUEST, trip(**NAIROBI_STOP_TRIP),
    nairobi_stop(0),
    expected("BOOK", ["kenya-economy"], ["ECONOMY"], ["LONG_FLIGHT_CONDITION_NOT_MET", "REST_STOP_CONDITIONS_NOT_MET"],
             INTL, ["AIRFARE"]),
    [REST, LOWEST],
    "The KLM flights add to exactly 840 minutes (395 + 445; the Amsterdam night is the overnight stop and is left "
    "out), and the Kenya Airways nonstop is 840 minutes too: 14 hours is not 'in excess of 14 hours' (lines "
    "349-350), so the rest period is not permitted. The traveller asked for what the policy allows otherwise: the "
    "lowest economy fare, the nonstop.",
    twin_of="indigo-fern", twin_fact="flight time to Nairobi 840 or 841 minutes on both itineraries")

scenario(
    "indigo-fern", "boundary_twin", ["multi_leg", "overnight", "dearer_option"], NAIROBI_STOP_REQUEST,
    trip(**NAIROBI_STOP_TRIP), nairobi_stop(1),
    expected("BOOK", ["amsterdam-economy"], ["ECONOMY"], ["INTERNATIONAL_LONG_FLIGHT", "REST_STOP_PERMITTED"], INTL,
             ["AIRFARE"]),
    [REST, LOWEST],
    "The KLM flights add to 841 minutes (395 + 446) and the nonstop is 841 minutes: in excess of 14 hours. The "
    "Amsterdam layover is 15 hours (not over 24), Amsterdam is a usual route to Nairobi and the fare is coach, so the "
    "rest period is permitted (lines 347-353): book the overnight itinerary asked for.",
    twin_of="heron-moss", twin_fact="flight time to Nairobi 841 or 840 minutes on both itineraries")

DUBAI_REQUEST = ("Washington Dulles to Nairobi on March 9th; the training starts on the 13th. I'd like to spend a "
                 "night in Dubai on the way. If that isn't allowed, book what the policy allows.")
DUBAI_TRIP = {"traveller_name": "Kenji Morales", "traveller_title": "Field Manager", "origin": "IAD", "destination": "NBO",
                  "travel_date": "2027-03-09", "booking_date": "2027-02-08", "business_starts": "2027-03-13 09:00",
                  "purpose": "Enumerator training in Nairobi", "purpose_kind": "TRAINING", "wants_overnight_stop": True,
                  "sign_offs": approvals(AS, GTD)}


def dubai_stop(layover):
    return search("IAD", "NBO", "2027-03-09", {
        **NAIROBI_GULF,
        "stopover": {"carrier": "EK", "via": ["DXB"], "depart": "21:50", "minutes": [780, 290], "layovers": [layover],
                     "stopovers": [True]},
    }, [
        offer("dubai-economy", "dubai", "ECONOMY", 124000),
        offer("doha-economy", "doha", "ECONOMY", 131000),
        offer("stopover-economy", "stopover", "ECONOMY", 136500),
    ])


scenario(
    "jasper-cove", "boundary_twin", ["multi_leg", "overnight", "dearer_option"], DUBAI_REQUEST, trip(**DUBAI_TRIP),
    dubai_stop(1440),
    expected("BOOK", ["stopover-economy"], ["ECONOMY"], ["INTERNATIONAL_LONG_FLIGHT", "REST_STOP_PERMITTED"], INTL,
             ["AIRFARE"]),
    [REST, LOWEST],
    "The flights take 1,070 minutes, in excess of 14 hours on every measure (the same-day itineraries take 1,195 "
    "and 1,240). The Dubai layover is exactly 1,440 minutes: 'may not exceed 24 hours' allows 24 hours. Usual "
    "route, coach: the rest period is permitted (lines 347-353).",
    twin_of="kestrel-bloom", twin_fact="Dubai layover 1,440 or 1,445 minutes")

scenario(
    "kestrel-bloom", "boundary_twin", ["multi_leg", "overnight"], DUBAI_REQUEST, trip(**DUBAI_TRIP), dubai_stop(1445),
    expected("BOOK", ["dubai-economy"], ["ECONOMY"], ["CONNECTION_TOO_LONG", "REST_STOP_CONDITIONS_NOT_MET"], INTL,
             ["AIRFARE"]),
    [REST, LOWEST],
    "The Dubai layover is 1,445 minutes, which exceeds 24 hours (line 351), so the rest period is not permitted. "
    "The traveller asked for what the policy allows otherwise: the lowest economy fare, the same-day Emirates "
    "connection, which is also the quickest same-day itinerary (1,195 minutes against 1,240).",
    twin_of="jasper-cove", twin_fact="Dubai layover 1,445 or 1,440 minutes")

LAUNCH_REQUEST = ("JFK to Nairobi on April 6th for the survey launch on the 8th; the trip is charged to our NSF grant. "
                  "Economy please.")
LAUNCH_TRIP = dict(traveller_name="Rita Szabo", traveller_title="Senior Research Associate", origin="JFK",
                   destination="NBO", travel_date="2027-04-06", booking_date="2027-03-08",
                   business_starts="2027-04-08 09:00", purpose="Household survey launch in Kenya",
                   purpose_kind="PROJECT_WORK", sign_offs=approvals(AS, GTD), **NSF)


def launch(layover):
    return search("JFK", "NBO", "2027-04-06", {
        "kenya": {"carrier": "KQ", "depart": "11:00", "minutes": [900]},
        "atlanta": {"carrier": "DL", "via": ["ATL"], "depart": "11:00", "minutes": [140, 920], "layovers": [layover]},
    }, [
        offer("kenya-economy", "kenya", "ECONOMY", 115000),
        offer("atlanta-economy", "atlanta", "ECONOMY", 142000),
    ])


scenario(
    "larkspur-tide", "boundary_twin", ["multi_leg", "outside_air_section", "dearer_option"], LAUNCH_REQUEST,
    trip(**LAUNCH_TRIP), launch(199),
    expected("BOOK", ["atlanta-economy"], ["ECONOMY"], FLY_REQUIRED, INTL, USG),
    [FLY, FLY_COST, FLY_SIX, FLY_PROC],
    "Federally funded travel from the U.S.: a U.S.-flag carrier is required (lines 504-506), and cost alone does not "
    "justify a foreign one (lines 508-509). Both leave JFK at 11:00; Delta through Atlanta takes 1,259 minutes "
    "against Kenya Airways' 900, 359 minutes longer: not 'at least 6 hours' (line 517). Book Delta.",
    twin_of="marble-finch", twin_fact="Atlanta connection 199 or 200 minutes (U.S. carrier 359 or 360 minutes longer)")

scenario(
    "marble-finch", "boundary_twin", ["multi_leg", "outside_air_section"], LAUNCH_REQUEST, trip(**LAUNCH_TRIP),
    launch(200),
    expected("BOOK", ["kenya-economy"], ["ECONOMY"], ["FLY_AMERICA_EXCEPTION", "LOWEST_FARE"], INTL, USG),
    [FLY, FLY_SIX, FLY_PROC_SIX, LOWEST],
    "Both leave JFK at 11:00; Delta through Atlanta takes 1,260 minutes against Kenya Airways' 900: exactly 6 hours "
    "longer, which is 'at least 6 hours longer' (line 517), a valid Fly America exception. The lowest economy fare, "
    "the Kenya Airways nonstop, is also the most direct and expeditious.",
    twin_of="larkspur-tide", twin_fact="Atlanta connection 200 or 199 minutes (U.S. carrier 360 or 359 minutes longer)")

MEXICO_TRIP = {"traveller_name": "Arjun Mehta", "traveller_title": "Research Manager", "origin": "IAD", "destination": "MEX",
                   "travel_date": "2027-01-27", "booking_date": "2027-01-04", "purpose": "Partner meeting in Mexico City",
                   "purpose_kind": "PARTNER_MEETING", "sign_offs": approvals(AS, GTD)}
MEXICO = search("IAD", "MEX", "2027-01-27", {
    "united": {"carrier": "UA", "depart": "07:10", "minutes": [285]},
    "aeromexico": {"carrier": "AM", "depart": "15:50", "minutes": [285]},
}, [
    offer("united-economy", "united", "ECONOMY", 37200),
    offer("aeromexico-economy", "aeromexico", "ECONOMY", 31800),
])

scenario(
    "nectar-ridge", "boundary_twin", [],
    "Washington Dulles to Mexico City on January 27th; the partner meeting is the next morning at 9. Economy please.",
    trip(business_starts="2027-01-28 09:00", **MEXICO_TRIP), MEXICO,
    expected("BOOK", ["aeromexico-economy"], ["ECONOMY"], ["LOWEST_FARE"], INTL, LOW),
    [LOWEST],
    "Both nonstops take 285 minutes. The Aeromexico flight lands at 19:35 the evening before the 09:00 meeting, so "
    "the lowest economy fare meets the business need (lines 334-335).",
    twin_of="opal-heath", twin_fact="the meeting starts at 09:00 the next day or at 14:00 the day of the flight")

scenario(
    "opal-heath", "boundary_twin", ["dearer_option"],
    "Washington Dulles to Mexico City on January 27th; the partner meeting is that afternoon at 2. Economy please.",
    trip(business_starts="2027-01-27 14:00", **MEXICO_TRIP), MEXICO,
    expected("BOOK", ["united-economy"], ["ECONOMY"], ["BUSINESS_NEED_TIMING", "LOWEST_FARE"], INTL, LOW),
    [LOWEST],
    "The cheaper Aeromexico flight lands at 19:35, after the 14:00 meeting, so it does not meet the business need "
    "'(including arrival and departure times)' (lines 334-335). The United nonstop lands at 10:55: the lowest "
    "economy fare that meets the need.",
    twin_of="nectar-ridge", twin_fact="the meeting starts at 14:00 the day of the flight or at 09:00 the next day")

# ===== multi-rule (5) =====

scenario(
    "pewter-lake", "multi_rule", ["dearer_option", "date_arithmetic"],
    "JFK to Nairobi on March 16th for the research week starting on the 18th. I need premium economy for a back "
    "condition; my doctor's note is on file and the CFO has approved the exception.",
    trip(traveller_name="Dana Whitcomb", traveller_title="Senior Research Manager", origin="JFK", destination="NBO",
         travel_date="2027-03-16", booking_date="2027-02-15", business_starts="2027-03-18 09:00",
         purpose="Research week at the Nairobi office", purpose_kind="PROJECT_WORK", requested_cabin="PREMIUM_ECONOMY",
         medical_note_date="2026-09-30",
         sign_offs=approvals(AS, GTD, ("CHIEF_FINANCIAL_OFFICER", "UPGRADE_EXCEPTION"))),
    search("JFK", "NBO", "2027-03-16", {
        "kenya": {"carrier": "KQ", "depart": "11:30", "minutes": [900]},
        "amsterdam": {"carrier": "KL", "via": ["AMS"], "depart": "17:20", "minutes": [400, 500], "layovers": [110]},
    }, [
        offer("kenya-economy", "kenya", "ECONOMY", 118000),
        offer("kenya-premium", "kenya", "PREMIUM_ECONOMY", 229000),
        offer("amsterdam-economy", "amsterdam", "ECONOMY", 126000),
        offer("amsterdam-premium", "amsterdam", "PREMIUM_ECONOMY", 245000),
    ]),
    expected("BOOK", ["kenya-premium"], ["PREMIUM_ECONOMY"], ["MEDICAL_NEED", "POLICY_EXCEPTION_APPROVED"],
             ["ASSIGNMENT_SUPERVISOR", "CHIEF_FINANCIAL_OFFICER", "GLOBAL_TEAM_DIRECTOR", "NONE"], ["AIRFARE"]),
    [UPGRADES, MEDICAL],
    "Lines 344-346: an exception to upgraded classes for medical reasons, with a signed doctor's note no more than "
    "a year old (dated 2026-09-30: 168 days before the flight) on file; line 341: approved by the CFO, whose "
    "approval is on file. The lowest premium economy fare, on the Kenya Airways nonstop.")

UNITED_TRIP = {"traveller_name": "Tom Reilly", "traveller_title": "Policy Manager", "origin": "DCA", "destination": "SFO",
                   "travel_date": "2027-02-03", "booking_date": "2027-01-11", "business_starts": "2027-02-04 09:00",
                   "purpose": "Evidence summit in San Francisco", "purpose_kind": "CONFERENCE",
                   "chosen_airline": "United Airlines", "sign_offs": approvals(AS)}
SFO = search("DCA", "SFO", "2027-02-03", {
    "american": {"carrier": "AA", "depart": "08:00"},
    "united": {"carrier": "UA", "depart": "09:15"},
    "evening": {"carrier": "AA", "depart": "18:30"},
}, [
    offer("american-economy", "american", "ECONOMY", 34200),
    offer("united-economy", "united", "ECONOMY", 38900),
    offer("evening-economy", "evening", "ECONOMY", 35600),
])

scenario(
    "quill-harbor", "multi_rule", ["personal_travel", "dearer_option"],
    "Reagan National to San Francisco on February 3rd for the evidence summit on the 4th. Please put me on United, I "
    "collect their miles. I'll cover whatever it costs above the cheapest fare myself.",
    trip(pays_difference=True, **UNITED_TRIP), SFO,
    expected("BOOK", ["united-economy"], ["ECONOMY"], ["LOYALTY_PROGRAM_PREFERENCE", "TRAVELER_PAYS_DIFFERENCE"],
             DOMESTIC, ["AIRFARE"]),
    [PREFERENCE, FREQUENT, FREQUENT_COST],
    "Lines 336-338: a traveller who opts for another carrier out of personal preference pays the difference, and "
    "this one does, so IPA's cost stays at the lowest economy fare (lines 360-365): book the United nonstop.",
    twin_of="russet-brook", twin_fact="the traveller pays the extra for United, or will not")

scenario(
    "russet-brook", "multi_rule", ["personal_travel"],
    "Reagan National to San Francisco on February 3rd for the evidence summit on the 4th. Please put me on United, I "
    "collect their miles, but I can't pay anything extra out of my own pocket. If United isn't possible, book what "
    "the policy allows.",
    trip(**UNITED_TRIP), SFO,
    expected("BOOK", ["american-economy"], ["ECONOMY"], ["LOWEST_FARE", "LOYALTY_PROGRAM_PREFERENCE"], DOMESTIC,
             ["AIRFARE"]),
    [FREQUENT, FREQUENT_COST, PREFERENCE, LOWEST],
    "Lines 360-365: frequent flyer programmes must not influence flight selection at a cost to IPA beyond the lowest "
    "available economy fare, and the traveller will not pay the difference (lines 336-338): the American 08:00 "
    "nonstop at the lowest fare.",
    twin_of="quill-harbor", twin_fact="the traveller will not pay the extra for United, or pays it")

scenario(
    "saffron-dell", "multi_rule", ["personal_travel", "dearer_option"],
    "I'll be on leave in Mexico City the week before the Bogota workshop, so please fly me from Mexico City on March "
    "15th instead of from home in Washington; I put that in my approval request. Price it against the flight from "
    "Dulles too, and I'll pay whatever the Mexico City ticket costs above it.",
    trip(traveller_name="Sofia Herrera", traveller_title="Research Manager", home_airport="IAD", origin="MEX",
         destination="BOG", travel_date="2027-03-15", booking_date="2027-02-22", business_starts="2027-03-16 09:00",
         purpose="Monitoring workshop in Bogota", purpose_kind="TRAINING", pays_difference=True,
         sign_offs=approvals(AS, GTD)),
    [search("MEX", "BOG", "2027-03-15", {
        "avianca": {"carrier": "AV", "depart": "09:20", "minutes": [285]},
        "aeromexico": {"carrier": "AM", "depart": "13:00", "minutes": [285]},
    }, [
        offer("avianca-economy", "avianca", "ECONOMY", 54000),
        offer("aeromexico-economy", "aeromexico", "ECONOMY", 58500),
    ]),
     search("IAD", "BOG", "2027-03-15", {
         "dulles": {"carrier": "AV", "depart": "08:05", "minutes": [330]},
         "houston": {"carrier": "UA", "via": ["IAH"], "depart": "09:30", "minutes": [235, 305], "layovers": [90]},
     }, [
         offer("dulles-economy", "dulles", "ECONOMY", 43000),
         offer("houston-economy", "houston", "ECONOMY", 50500),
     ], name="home")],
    expected("BOOK", ["avianca-economy"], ["ECONOMY"],
             ["LOWEST_FARE", "PERSONAL_TRAVEL_NOT_COVERED", "TRAVELER_PAYS_DIFFERENCE"], INTL,
             ["AIRFARE", "REIMBURSABLE_EXPENSES", "TRAVEL_APPROVAL"]),
    [DEVIATION, DEVIATION_COST, PERSONAL, COMPARISON, LOWEST],
    "Lines 175-179: leaving from somewhere other than the home of record for personal reasons is disclosed in the "
    "approval request, as it was; lines 390-394: the traveller pays the incremental cost. The business-only fare from "
    "Dulles is $430; the lowest from Mexico City is $540, and the traveller pays the $110. Book the Avianca nonstop "
    "from Mexico City, not the cheaper Dulles flight the traveller will not be at.")

scenario(
    "tamarind-crest", "multi_rule", ["personal_travel", "outside_air_section", "dearer_option"],
    "Dulles to Johannesburg on April 13th for the partner meeting on the 15th; the trip is on our Department of Labor "
    "grant. Please book Emirates through Dubai, I collect their miles and I'll cover anything above the cheapest fare "
    "myself. If Emirates isn't allowed, book what the policy allows.",
    trip(traveller_name="Lucia Ferraro", traveller_title="Associate Research Manager", origin="IAD", destination="JNB",
         travel_date="2027-04-13", booking_date="2027-03-15", business_starts="2027-04-15 09:00",
         purpose="Partner meeting in Johannesburg", purpose_kind="PARTNER_MEETING", chosen_airline="Emirates",
         pays_difference=True, sign_offs=approvals(AS, GTD), **DOL),
    search("IAD", "JNB", "2027-04-13", {
        "doha": {"carrier": "QR", "via": ["DOH"], "depart": "16:40", "minutes": [760, 500], "layovers": [140]},
        "dubai": {"carrier": "EK", "via": ["DXB"], "depart": "10:30", "minutes": [760, 495], "layovers": [135]},
        "united": {"carrier": "UA", "depart": "17:30", "minutes": [960]},
    }, [
        offer("doha-economy", "doha", "ECONOMY", 124000),
        offer("dubai-economy", "dubai", "ECONOMY", 128000),
        offer("united-economy", "united", "ECONOMY", 156000),
    ]),
    expected("BOOK", ["united-economy"], ["ECONOMY"], ["FLY_AMERICA_US_CARRIER_REQUIRED", "NATIONAL_CARRIER_REQUIRED"],
             INTL, USG),
    [FLY, FLY_COST, FLY_SIX, FLY_PROC, PREFERENCE],
    "Lines 504-506: the grant pays, so a U.S.-flag carrier is required; Emirates is foreign, and no exception of "
    "lines 513-527 applies (United's nonstop is as fast as any). Paying the difference (lines 336-338) does not make "
    "a foreign carrier compliant: book the United nonstop.")

# ===== hidden clause (3) =====

scenario(
    "umber-glade", "hidden_clause", ["outside_air_section", "multi_leg"],
    "Please book my husband Jonah from Dulles to Nairobi on February 2nd. He is leading the community health session "
    "of our field training on the 4th at the project's request; that is written in the travel request, and the "
    "budget-holder has approved his travel.",
    trip(traveller_name="Jonah Mensah", traveller_title="Spouse of Ama Mensah, Senior Research Manager",
         passenger="SPOUSE", accompanies="Ama Mensah, Senior Research Manager", origin="IAD", destination="NBO",
         travel_date="2027-02-02", booking_date="2027-01-05", business_starts="2027-02-04 09:00",
         purpose="Leads the community health session of the field training at the project's request",
         purpose_kind="TRAINING",
         sign_offs=approvals(AS, GTD, ("BUDGET_HOLDER", "COMPANION_TRAVEL"))),
    search("IAD", "NBO", "2027-02-02", NAIROBI_GULF, [
        offer("dubai-economy", "dubai", "ECONOMY", 124000),
        offer("doha-economy", "doha", "ECONOMY", 131000),
    ]),
    expected("BOOK", ["dubai-economy"], ["ECONOMY"], ["COMPANION_TRAVEL_AUTHORIZED", "LOWEST_FARE"],
             ["ASSIGNMENT_SUPERVISOR", "BUDGET_HOLDER", "GLOBAL_TEAM_DIRECTOR", "NONE"], ["AIRFARE", "POLICIES"]),
    [SPOUSE, LOWEST],
    "Lines 142-146 (in the Policies section, not Airfare): a spouse's travel is reimbursed when there is a bona fide "
    "business purpose for it, documented in the travel request and approved by the budget-holder; all three hold. "
    "The lowest economy fare, the Emirates connection, which is also the quicker of the two.")

scenario(
    "violet-quarry", "hidden_clause", ["synonym"],
    "Reagan National to Boston on January 19th for the board briefing on the 20th. The date might still move, so "
    "please get me a fully flexible ticket I can cancel for a refund. If that isn't allowed, book what the policy "
    "allows; I have to be at the briefing.",
    trip(traveller_name="Grace Liu", traveller_title="Executive Officer", origin="DCA", destination="BOS",
         travel_date="2027-01-19", booking_date="2026-12-28", business_starts="2027-01-20 10:00",
         purpose="Board briefing in Boston; the date may still move", purpose_kind="DONOR_MEETING",
         wants_refundable=True, sign_offs=approvals(AS)),
    search("DCA", "BOS", "2027-01-19", {
        "first": {"carrier": "AA", "depart": "07:00"},
        "second": {"carrier": "DL", "depart": "09:30"},
        "flex": {"carrier": "AA", "depart": "12:00"},
        "jetblue": {"carrier": "B6", "depart": "15:10"},
    }, [
        offer("first-economy", "first", "ECONOMY", 19800),
        offer("second-economy", "second", "ECONOMY", 21400),
        offer("flex-economy", "flex", "ECONOMY", 28900, refundable=True),
        offer("jetblue-economy", "jetblue", "ECONOMY", 22500),
    ]),
    expected("BOOK", ["first-economy"], ["ECONOMY"], ["LOWEST_FARE", "REFUNDABLE_FARE_NOT_ALLOWED"], DOMESTIC, LOW),
    [LOWEST, CHANGE_FEES],
    "Lines 334-336: the standard is the lowest economy fare 'that can be changed with a fee', which a fare that is "
    "not refundable is (search_flights says so); if the date moves for business, the change fee is reimbursable "
    "(lines 403-404). The request's 'fully flexible ... refund' is not the standard: the lowest fare, American "
    "07:00.")

scenario(
    "walnut-spire", "hidden_clause", ["outside_air_section", "dearer_option"],
    "Dulles to Nairobi on March 23rd for the baseline survey training on the 25th; it's billed to our National "
    "Science Foundation grant. Economy please.",
    trip(traveller_name="Ibrahim Diallo", traveller_title="Research Associate", origin="IAD", destination="NBO",
         travel_date="2027-03-23", booking_date="2027-02-22", business_starts="2027-03-25 09:00",
         purpose="Baseline survey training in Kenya", purpose_kind="TRAINING", sign_offs=approvals(AS, GTD), **NSF),
    search("IAD", "NBO", "2027-03-23", {
        **NAIROBI_GULF,
        "united": {"carrier": "UA", "depart": "17:55", "minutes": [945]},
    }, [
        offer("dubai-economy", "dubai", "ECONOMY", 119000),
        offer("doha-economy", "doha", "ECONOMY", 123000),
        offer("united-economy", "united", "ECONOMY", 152000),
    ]),
    expected("BOOK", ["united-economy"], ["ECONOMY"], FLY_REQUIRED, INTL, USG),
    [FLY, FLY_COST, FLY_PROC],
    "Lines 504-506 (U.S. Government-funded Travel, not Airfare): federally funded travel from the U.S. is on a "
    "U.S.-flag carrier; cost alone does not justify Emirates or Qatar (lines 508-509), and United's nonstop is the "
    "quickest itinerary, so no exception applies. Book United.")

# ===== distractor (3) =====

scenario(
    "yarrow-bluff", "distractor", ["date_arithmetic", "month_end", "outside_air_section", "upgrade_not_taken",
                                   "overnight"],
    "JFK to Delhi on December 15th for the evaluation design workshop on the 18th. I told Global Operations about the "
    "trip on November 27th. It's a long trip and I'll claim per diem for the travel days; just the cheapest economy "
    "seat please.",
    trip(traveller_name="Nikhil Rao", traveller_title="Senior Research Associate", origin="JFK", destination="DEL",
         travel_date="2026-12-15", booking_date="2026-11-30", business_starts="2026-12-18 09:00",
         purpose="Evaluation design workshop in Delhi", purpose_kind="TRAINING", global_operations_told="2026-11-27",
         sign_offs=approvals(AS, GTD)),
    search("JFK", "DEL", "2026-12-15", {
        "india": {"carrier": "AI", "depart": "20:30", "minutes": [870]},
        "american": {"carrier": "AA", "depart": "21:10", "minutes": [875]},
        "frankfurt": {"carrier": "LH", "via": ["FRA"], "depart": "17:40", "minutes": [450, 455], "layovers": [720],
                      "stopovers": [True]},
    }, [
        offer("india-economy", "india", "ECONOMY", 105000),
        offer("american-economy", "american", "ECONOMY", 114000),
        offer("frankfurt-economy", "frankfurt", "ECONOMY", 121000),
    ]),
    expected("BOOK", ["india-economy"], ["ECONOMY"], ["LOWEST_FARE"], INTL, [*LOW, "POLICIES"]),
    [LOWEST, NOTICE, APPROVERS],
    "India is on the list of line 147: Global Operations was told on November 27th, before booking (November 30th) "
    "and 18 days before travel (at least two weeks, across the month end). The per diem hours (lines 270-272) and "
    "the possible rest stop in Frankfurt (not asked for) do not change the fare: the Air India nonstop at the lowest "
    "economy fare.",
    distractors=[PER_DIEM, SECURITY])

scenario(
    "zephyr-moor", "distractor", ["outside_air_section"],
    "Dulles to Frankfurt on February 9th for the research methods conference on the 10th; it's charged to our NSF "
    "grant. Economy, the cheapest that's allowed.",
    trip(traveller_name="Mei Tanaka", traveller_title="Postdoctoral Fellow", origin="IAD", destination="FRA",
         travel_date="2027-02-09", booking_date="2027-01-11", business_starts="2027-02-10 14:00",
         purpose="Research methods conference in Frankfurt", purpose_kind="CONFERENCE", sign_offs=approvals(AS, GTD),
         **NSF),
    search("IAD", "FRA", "2027-02-09", {
        "lufthansa": {"carrier": "LH", "depart": "17:50", "minutes": [500]},
        "united": {"carrier": "UA", "depart": "18:10", "minutes": [500]},
    }, [
        offer("lufthansa-economy", "lufthansa", "ECONOMY", 64000),
        offer("united-economy", "united", "ECONOMY", 79000),
    ]),
    expected("BOOK", ["lufthansa-economy"], ["ECONOMY"], ["LOWEST_FARE", "OPEN_SKIES_AGREEMENT"], INTL, USG),
    [FLY, OPEN_SKIES, LOWEST],
    "The grant brings in Fly America (lines 504-506), which looks like it requires United, but it allows an Open "
    "Skies carrier, and lines 1073-1076 let an EU airline carry the trip between the U.S. and an EU Member State: "
    "Lufthansa's nonstop to Frankfurt at the lowest economy fare.",
    distractors=[ABROAD])

scenario(
    "alder-crane", "distractor", ["date_arithmetic"],
    "Something came up: I need New York LaGuardia to Atlanta on December 7th for a partner meeting on the 8th. I know "
    "it's late to book. I'll carry two survey tablets in my hand luggage.",
    trip(traveller_name="Chris Adeyemi", traveller_title="Field Coordinator", origin="LGA", destination="ATL",
         travel_date="2026-12-07", booking_date="2026-12-03", business_starts="2026-12-08 09:00",
         purpose="Partner meeting in Atlanta", purpose_kind="PARTNER_MEETING", sign_offs=approvals(AS)),
    search("LGA", "ATL", "2026-12-07", {
        "morning": {"carrier": "DL", "depart": "07:30"},
        "american": {"carrier": "AA", "depart": "10:00"},
        "afternoon": {"carrier": "DL", "depart": "15:45"},
    }, [
        offer("morning-economy", "morning", "ECONOMY", 26800),
        offer("american-economy", "american", "ECONOMY", 28100),
        offer("afternoon-economy", "afternoon", "ECONOMY", 25900),
    ]),
    expected("BOOK", ["afternoon-economy"], ["ECONOMY"], ["LOWEST_FARE"], DOMESTIC, LOW),
    [LOWEST, APPROVERS],
    "Four days ahead: lines 354-355 ask for booking as far ahead as practical 'whenever possible', which does not bar "
    "a late booking; the tablets go in hand luggage (lines 492-494), a baggage rule. The lowest economy fare, Delta "
    "15:45, lands the evening before the meeting.",
    distractors=[ADVANCE, WEEKS, ELECTRONICS])

# ===== refusal (3) =====

scenario(
    "birch-hollow", "refusal", ["outside_air_section"],
    "Could you book my wife Leah from Dulles to Nairobi on January 26th too? She'd like to see Kenya and go on a "
    "safari while I'm at the field office.",
    trip(traveller_name="Leah Brandt", traveller_title="Spouse of Tomas Brandt, Director of Research Operations",
         passenger="SPOUSE", accompanies="Tomas Brandt, Director of Research Operations", origin="IAD",
         destination="NBO", travel_date="2027-01-26", booking_date="2026-12-29", business_starts="",
         purpose="Sightseeing and a safari while her husband works at the Nairobi office", purpose_kind="PERSONAL",
         sign_offs=approvals(AS, GTD)),
    search("IAD", "NBO", "2027-01-26", NAIROBI_GULF, [
        offer("dubai-economy", "dubai", "ECONOMY", 124000),
        offer("doha-economy", "doha", "ECONOMY", 131000),
    ]),
    expected("REFUSE", [], ["NONE"], ["COMPANION_NOT_COVERED", "PERSONAL_TRAVEL_NOT_COVERED"], INTL,
             ["AIRFARE", "POLICIES"]),
    [SPOUSE, PERSONAL],
    "Lines 142-146: a spouse's travel is reimbursed only with a bona fide business purpose for it; sightseeing is "
    "none, so IPA buys no ticket. The trip approvals on file are the employee's.")

scenario(
    "cedar-flint", "refusal", ["personal_travel"],
    "After the Nairobi workshop I'm taking a few days of holiday with friends in Johannesburg. Can IPA book my flight "
    "from Nairobi to Johannesburg on March 3rd, since I'm already out here for work?",
    trip(traveller_name="Amara Nwosu", traveller_title="Research Associate", home_airport="IAD", origin="NBO",
         destination="JNB", travel_date="2027-03-03", booking_date="2027-02-10", business_starts="",
         purpose="Holiday with friends in Johannesburg after the Nairobi workshop", purpose_kind="PERSONAL"),
    search("NBO", "JNB", "2027-03-03", {
        "kenya": {"carrier": "KQ", "depart": "08:30", "minutes": [240]},
        "springbok": {"carrier": "SA", "depart": "13:45", "minutes": [240]},
    }, [
        offer("kenya-economy", "kenya", "ECONOMY", 41000),
        offer("springbok-economy", "springbok", "ECONOMY", 45500),
    ]),
    expected("REFUSE", [], ["NONE"], ["OUTSIDE_POLICY_SCOPE", "PERSONAL_TRAVEL_NOT_COVERED"], ["NONE"],
             ["AIRFARE", "POLICIES"]),
    [PERSONAL, BUSINESS_ONLY],
    "Lines 388-390: personal travel booked in conjunction with work-related travel is the employee's responsibility, "
    "and IPA will not reimburse it. A holiday flight is personal: IPA buys no ticket.")

scenario(
    "dahlia-mist", "refusal", ["personal_travel"],
    "I'm going to my cousin's wedding in Bogota on February 12th, on annual leave. I'll answer email while I'm there; "
    "could IPA buy the ticket?",
    trip(traveller_name="Carlos Mendez", traveller_title="Grants Associate", origin="IAD", destination="BOG",
         travel_date="2027-02-12", booking_date="2027-01-18", business_starts="",
         purpose="A family wedding in Bogota, on annual leave", purpose_kind="PERSONAL"),
    search("IAD", "BOG", "2027-02-12", BOGOTA, [
        offer("avianca-economy", "avianca", "ECONOMY", 43000),
        offer("miami-economy", "miami", "ECONOMY", 46800),
    ]),
    expected("REFUSE", [], ["NONE"], ["OUTSIDE_POLICY_SCOPE", "PERSONAL_TRAVEL_NOT_COVERED"], ["NONE"],
             ["AIRFARE", "POLICIES"]),
    [PERSONAL, BUSINESS_ONLY],
    "Lines 128-129: IPA pays for travel on authorized business; lines 388-390: personal travel is the employee's. A "
    "wedding on annual leave is personal, whatever email is answered: IPA buys no ticket.")

# ===== flag (4) =====

scenario(
    "elm-thistle", "flag", ["approval_required", "date_arithmetic", "dearer_option"],
    "Dulles to Johannesburg on April 20th for the partner review on the 22nd. I need premium economy for a knee "
    "condition; my doctor's note is on file and I've asked the CFO to approve it, but she hasn't answered yet.",
    trip(traveller_name="Samira Haddad", traveller_title="Senior Research Manager", origin="IAD", destination="JNB",
         travel_date="2027-04-20", booking_date="2027-03-22", business_starts="2027-04-22 09:00",
         purpose="Partner review in Johannesburg", purpose_kind="PARTNER_MEETING", requested_cabin="PREMIUM_ECONOMY",
         medical_note_date="2026-12-01", sign_offs=approvals(AS, GTD)),
    search("IAD", "JNB", "2027-04-20", {
        "united": {"carrier": "UA", "depart": "17:30", "minutes": [960]},
        "dubai": {"carrier": "EK", "via": ["DXB"], "depart": "10:30", "minutes": [760, 495], "layovers": [135]},
    }, [
        offer("united-economy", "united", "ECONOMY", 136000),
        offer("united-premium", "united", "PREMIUM_ECONOMY", 254000),
        offer("dubai-economy", "dubai", "ECONOMY", 142000),
        offer("dubai-premium", "dubai", "PREMIUM_ECONOMY", 265000),
    ]),
    expected("FLAG_FOR_APPROVAL", ["united-premium"], ["PREMIUM_ECONOMY"], ["APPROVAL_REQUIRED", "MEDICAL_NEED"],
             ["CHIEF_FINANCIAL_OFFICER"], ["AIRFARE"]),
    [UPGRADES, MEDICAL],
    "Lines 344-346: the medical exception 'may be approved' when requested with a signed doctor's note no more than a "
    "year old (dated 2026-12-01, 140 days before the flight); line 341: exceptions must be approved by the CFO, who "
    "has not yet answered. Hold the lowest premium economy fare (the United nonstop) for the CFO; approval required, not 'no compliant "
    "offer'.",
    flag_twins=["pewter-lake", "cobalt-reed"],
    ambiguity="none: the CFO's approval of the medical exception is required and not yet on file; the text is clear")

scenario(
    "fir-cobble", "flag", ["approval_required", "outside_air_section"],
    "Nairobi to Johannesburg on February 16th for the regional data quality workshop on the 17th. My supervisor has "
    "approved the trip.",
    trip(traveller_name="Wanjiku Kamau", traveller_title="Data Quality Manager, Kenya", staff_unit="COUNTRY_OFFICE",
         origin="NBO", destination="JNB", travel_date="2027-02-16", booking_date="2027-01-25",
         business_starts="2027-02-17 09:00", purpose="Regional data quality workshop in Johannesburg",
         purpose_kind="TRAINING", sign_offs=approvals(AS)),
    search("NBO", "JNB", "2027-02-16", {
        "kenya": {"carrier": "KQ", "depart": "08:30", "minutes": [240]},
        "springbok": {"carrier": "SA", "depart": "13:45", "minutes": [240]},
    }, [
        offer("kenya-economy", "kenya", "ECONOMY", 41000),
        offer("springbok-economy", "springbok", "ECONOMY", 45500),
    ]),
    expected("FLAG_FOR_APPROVAL", ["kenya-economy"], ["ECONOMY"], ["APPROVAL_REQUIRED"], ["COUNTRY_DIRECTOR"],
             APPROVAL_CLAUSES),
    [APPROVE_ALL, APPROVERS, ITINERARY, FURTHER],
    "Lines 115-116: all travel is approved before booking; lines 159-161: international travel by Country Office "
    "staff must be approved by the Country Director. Only the Assignment Supervisor has signed (lines 686-687: further "
    "approvals are forwarded). Hold the lowest economy fare for the Country Director; the supervisor is not the "
    "approver this needs.",
    flag_twins=["ember-kite", "amber-wharf"],
    ambiguity="none: the Country Director's approval is required and missing; the text is clear")

scenario(
    "gull-heather", "flag", ["unclear_phrase", "outside_air_section", "multi_leg"],
    "Dulles to Nairobi on April 27th for the study's endline training on the 29th; it's on our NSF grant. Economy "
    "please.",
    trip(traveller_name="Ana Lucia Gomez", traveller_title="Research Manager", origin="IAD", destination="NBO",
         travel_date="2027-04-27", booking_date="2027-03-29", business_starts="2027-04-29 09:00",
         purpose="Endline survey training in Kenya", purpose_kind="TRAINING", sign_offs=approvals(AS, GTD), **NSF),
    search("IAD", "NBO", "2027-04-27", {
        "amsterdam": {"carrier": "KL", "via": ["AMS"], "depart": "17:35", "minutes": [470, 500], "layovers": [105]},
        "newark": {"carrier": "UA", "via": ["EWR"], "depart": "07:15", "minutes": [75, 920], "layovers": [140]},
        "dubai": {"carrier": "EK", "via": ["DXB"], "depart": "10:15", "minutes": [780, 290], "layovers": [125]},
    }, [
        offer("amsterdam-economy", "amsterdam", "ECONOMY", 118000),
        offer("newark-economy", "newark", "ECONOMY", 146000),
        offer("dubai-economy", "dubai", "ECONOMY", 123000),
    ]),
    expected("FLAG_FOR_APPROVAL", ["amsterdam-economy", "newark-economy"], ["ECONOMY"], UNCLEAR,
             ["ASSIGNMENT_SUPERVISOR", "CHIEF_FINANCIAL_OFFICER", "GLOBAL_OPERATIONS",
              "GLOBAL_TEAM_DIRECTOR", "GRANTS_TEAM", "NOT_NAMED"], ["US_GOVERNMENT_PROCEDURE", "USG_FUNDED_TRAVEL"],
             phrase="between the U.S. and any point in an EU Member State"),
    [FLY, OPEN_SKIES, FLY_COST, POLICY_OWNER],
    "The grant brings in Fly America. KLM is an EU airline flying Dulles-Amsterdam-Nairobi. Lines 1073-1076 allow EU "
    "airlines 'when traveling (1) between the U.S. and any point in an EU Member State or (2) between any two points "
    "outside the United States': each KLM flight fits one branch, but the journey (the U.S. to Kenya) fits neither. "
    "Lines 504-506 name 'Open Skies carrier' with no route limit. On one reading the KLM fare is the lowest compliant "
    "fare; on the other only United qualifies (Emirates is foreign either way). Hold either.",
    flag_twins=["zephyr-moor", "walnut-spire"],
    ambiguity={"phrase": "between the U.S. and any point in an EU Member State",
               "readings": [("each flight counts: Dulles-Amsterdam is between the U.S. and an EU Member State and "
                            "Amsterdam-Nairobi is between two points outside the U.S., so KLM is compliant: book it"),
                            ("the journey counts: Dulles to Nairobi is neither, so KLM is not covered and only the U.S. "
                            "carrier qualifies: book United")]})

scenario(
    "hazel-pond", "flag", ["unclear_phrase", "multi_leg"],
    "Washington Dulles to Bogota on February 24th for the partner meeting the next morning. Economy please.",
    trip(traveller_name="Daniel Park", traveller_title="Research Associate", origin="IAD", destination="BOG",
         travel_date="2027-02-24", booking_date="2027-01-25", business_starts="2027-02-25 09:00",
         purpose="Partner meeting in Bogota", purpose_kind="PARTNER_MEETING", sign_offs=approvals(AS, GTD)),
    search("IAD", "BOG", "2027-02-24", BOGOTA, [
        offer("avianca-economy", "avianca", "ECONOMY", 52000),
        offer("miami-economy", "miami", "ECONOMY", 39500),
    ]),
    expected("FLAG_FOR_APPROVAL", ["avianca-economy", "miami-economy"], ["ECONOMY"], UNCLEAR,
             ["ASSIGNMENT_SUPERVISOR", "CHIEF_FINANCIAL_OFFICER", "GLOBAL_OPERATIONS", "GLOBAL_TEAM_DIRECTOR",
              "NOT_NAMED"], LOW,
             phrase="via the most direct and expeditious route"),
    [LOWEST, TABLE, INDEPENDENT, POLICY_OWNER],
    "Lines 334-336: 'the lowest economy fare (coach) that meets the business need (including arrival and departure "
    "times) via the most direct and expeditious route'. The American connection through Miami is $125 cheaper but "
    "takes 480 minutes against the Avianca nonstop's 330; both land the day before the meeting. On one reading the "
    "route words only qualify the lowest fare (book Miami); on the other the fare must be on the most direct and "
    "expeditious route (book the nonstop). Hold either.",
    flag_twins=["dune-sparrow", "larkspur-tide"],
    ambiguity={"phrase": "via the most direct and expeditious route",
               "readings": [("the lowest fare that meets the business need decides, and a one-stop routing that lands "
                            "in time qualifies: book the Miami connection"),
                            "the fare must be on the most direct and expeditious route: book the Avianca nonstop"]})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    for data in S:
        (OUT / f"{data['id']}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(S)} scenarios to {OUT}")


if __name__ == "__main__":
    main()
