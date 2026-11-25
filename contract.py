"""Each tool's and task's typed input and output (see nanoagent.plugin.v0001.contract): declarations only.

The first part is the original-handbook template's shared contract and is the same in every plugin made from
it. The HANDBOOK-SPECIFIC part in the middle is filled per handbook: the scenario ids, the closed lists of
approvers and sections, and the trip record; the shared inputs and outputs after it refer to those names.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output

# ---------------------------------------------------------------------------------------------------------
# SHARED (template): keep identical across plugins, except the agent task's id in Task.BOOK_FLIGHT.
# ---------------------------------------------------------------------------------------------------------


class Tool(Enum):
    BOOKING_REQUIREMENTS = "booking_requirements"
    GET_TRIP = "get_trip"
    SEARCH_FLIGHTS = "search_flights"
    SOLVE_BOOKING = "solve_booking"


class Task(Enum):
    BOOKING_REQUIREMENTS = "booking-requirements"
    SEARCH_FLIGHTS = "search-flights"
    BOOK_FLIGHT = "book-ipa-flight"


class Decision(Enum):
    BOOK = "BOOK"
    REFUSE = "REFUSE"
    FLAG_FOR_APPROVAL = "FLAG_FOR_APPROVAL"


class Cabin(Enum):
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"
    NONE = "NONE"


class ReasonCode(Enum):
    """Why the decision was made. The list is shared by every handbook plugin, so it also holds reasons
    that a given handbook never uses."""

    LOWEST_FARE = "LOWEST_FARE"
    UPGRADE_NOT_ELIGIBLE = "UPGRADE_NOT_ELIGIBLE"
    CLIENT_REIMBURSABLE = "CLIENT_REIMBURSABLE"
    UPGRADE_WITHIN_FARE_MARGIN = "UPGRADE_WITHIN_FARE_MARGIN"
    MEDICAL_NEED = "MEDICAL_NEED"
    COST_SAVINGS = "COST_SAVINGS"
    NO_ECONOMY_SEATS_URGENT = "NO_ECONOMY_SEATS_URGENT"
    TRAVELER_PAYS_UPGRADE = "TRAVELER_PAYS_UPGRADE"
    LONG_FLIGHT_APPROVED = "LONG_FLIGHT_APPROVED"
    LONG_FLIGHT_CONDITION_NOT_MET = "LONG_FLIGHT_CONDITION_NOT_MET"
    PREMIUM_ECONOMY_ALLOWED = "PREMIUM_ECONOMY_ALLOWED"
    UPGRADE_COST_NOT_NOMINAL = "UPGRADE_COST_NOT_NOMINAL"
    ALTERNATE_ROUTE_WITHIN_MARGIN = "ALTERNATE_ROUTE_WITHIN_MARGIN"
    ALTERNATE_ROUTE_TOO_EXPENSIVE = "ALTERNATE_ROUTE_TOO_EXPENSIVE"
    LOYALTY_PROGRAM_PREFERENCE = "LOYALTY_PROGRAM_PREFERENCE"
    COMPANION_NOT_COVERED = "COMPANION_NOT_COVERED"
    PERSONAL_TRAVEL_NOT_COVERED = "PERSONAL_TRAVEL_NOT_COVERED"
    OUTSIDE_POLICY_SCOPE = "OUTSIDE_POLICY_SCOPE"
    NO_COMPLIANT_OFFER = "NO_COMPLIANT_OFFER"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    UNCLEAR_POLICY_TEXT = "UNCLEAR_POLICY_TEXT"
    ADVANCE_PURCHASE_TOO_LATE = "ADVANCE_PURCHASE_TOO_LATE"
    DISTANCE_BELOW_MINIMUM = "DISTANCE_BELOW_MINIMUM"
    DRIVING_EXPECTED = "DRIVING_EXPECTED"
    RAIL_PREFERRED = "RAIL_PREFERRED"
    REFUNDABLE_FARE_NOT_ALLOWED = "REFUNDABLE_FARE_NOT_ALLOWED"
    PREFERRED_CARRIER_REQUIRED = "PREFERRED_CARRIER_REQUIRED"
    CONNECTION_TOO_LONG = "CONNECTION_TOO_LONG"
    OVERNIGHT_STOP_REQUIRED = "OVERNIGHT_STOP_REQUIRED"
    NATIONAL_CARRIER_REQUIRED = "NATIONAL_CARRIER_REQUIRED"
    SENIOR_ROLE_ENTITLEMENT = "SENIOR_ROLE_ENTITLEMENT"
    INTERNATIONAL_LONG_FLIGHT = "INTERNATIONAL_LONG_FLIGHT"
    TRAVELLER_LIMIT_PER_FLIGHT = "TRAVELLER_LIMIT_PER_FLIGHT"
    # HANDBOOK-SPECIFIC reason codes go below this line; keep every shared one above.
    REST_STOP_PERMITTED = "REST_STOP_PERMITTED"
    REST_STOP_CONDITIONS_NOT_MET = "REST_STOP_CONDITIONS_NOT_MET"
    FLY_AMERICA_US_CARRIER_REQUIRED = "FLY_AMERICA_US_CARRIER_REQUIRED"
    FLY_AMERICA_EXCEPTION = "FLY_AMERICA_EXCEPTION"
    OPEN_SKIES_AGREEMENT = "OPEN_SKIES_AGREEMENT"
    TRAVELER_PAYS_DIFFERENCE = "TRAVELER_PAYS_DIFFERENCE"
    POLICY_EXCEPTION_APPROVED = "POLICY_EXCEPTION_APPROVED"
    COMPANION_TRAVEL_AUTHORIZED = "COMPANION_TRAVEL_AUTHORIZED"
    BUSINESS_NEED_TIMING = "BUSINESS_NEED_TIMING"
    # Decoys: codes for rules of other handbooks that this one lacks, so the list hints at none of its own rules.
    WEEKEND_TRAVEL_HOME = "WEEKEND_TRAVEL_HOME"
    WEEKEND_TRIP_NOT_EARNED = "WEEKEND_TRIP_NOT_EARNED"
    NEXT_OF_KIN_TRAVEL = "NEXT_OF_KIN_TRAVEL"
    CHANCELLOR_WRITTEN_AUTHORIZATION = "CHANCELLOR_WRITTEN_AUTHORIZATION"
    CREATIVE_TICKETING = "CREATIVE_TICKETING"
    PRIVATE_AIRCRAFT_NOT_APPROVED = "PRIVATE_AIRCRAFT_NOT_APPROVED"
    DOUBLE_BOOKING_PROHIBITED = "DOUBLE_BOOKING_PROHIBITED"
    DENIED_BOARDING_NOT_ALLOWED = "DENIED_BOARDING_NOT_ALLOWED"
    CANDIDATE_TRIP_NOT_COVERED = "CANDIDATE_TRIP_NOT_COVERED"
    SAME_CLASS_AS_CUSTOMER = "SAME_CLASS_AS_CUSTOMER"
    TRAVEL_PACKAGE_NOT_ITEMIZED = "TRAVEL_PACKAGE_NOT_ITEMIZED"
    TICKET_TOTAL_APPROVED = "TICKET_TOTAL_APPROVED"


class TripType(Enum):
    ONE_WAY = "ONE_WAY"
    ROUND_TRIP = "ROUND_TRIP"


class Topic(Enum):
    ALL = "ALL"
    FIELDS = "FIELDS"
    AIRPORTS = "AIRPORTS"


CODE = "An IATA airport code, e.g. JFK"


@dataclass
class Airport(Output):
    code: Annotated[str, CODE]
    name: Annotated[str, "The airport's name"]
    city: Annotated[str, "The city it serves"]
    country: Annotated[str, "Its country, as an ISO code"]


@dataclass
class Segment(Output):
    flight_number: Annotated[str, "The airline's flight number, e.g. BA 117"]
    origin: Annotated[str, CODE]
    destination: Annotated[str, CODE]
    depart_local: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, local time at that airport"]
    arrive_local: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, local time at that airport"]
    depart_utc: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, UTC"]
    arrive_utc: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, UTC"]
    scheduled_minutes: Annotated[int, "Its scheduled time from departure to arrival, in minutes"]


@dataclass
class Offer(Output):
    offer_id: Annotated[str, "The offer's id, to submit when booking or holding it"]
    carrier: Annotated[str, "The airline"]
    trip_type: Annotated[TripType, "ONE_WAY, or ROUND_TRIP when the fare covers the flights out and back"]
    cabin: Annotated[Cabin, "The cabin sold on every flight of the offer"]
    fare_cents: Annotated[int, "The whole fare for one passenger, in cents of the search's currency"]
    seats_available: Annotated[bool, "False when this cabin is sold out on these flights: it is listed but cannot be bought"]
    refundable: Annotated[bool, "Whether the fare can be refunded or changed without a fee"]
    stops: Annotated[int, "Connections on the way out; zero for a nonstop"]
    segments: Annotated[list[Segment], "The flights out, in order"]
    layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights out"]
    stopover_nights: Annotated[list[bool], "Per connection out: true when it is a ticketed stopover with a hotel night booked"]
    flying_minutes: Annotated[int, "The flights' scheduled minutes out added together, ground time left out"]
    elapsed_minutes: Annotated[int, "Minutes from the first departure out to the last arrival, ground time included"]
    return_segments: Annotated[list[Segment], "For a round trip, the flights back, in order; empty otherwise"]
    return_layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights back"]
    return_stopover_nights: Annotated[list[bool], "Per connection back: true for a ticketed stopover with a hotel night"]
    return_flying_minutes: Annotated[int, "The flights' scheduled minutes back added together; zero one way"]
    return_elapsed_minutes: Annotated[int, "Minutes from the first departure back to the last arrival; zero one way"]


# ---------------------------------------------------------------------------------------------------------
# HANDBOOK-SPECIFIC: Innovations for Poverty Action, IPA Global Travel Manual (Version 1, October 2021).
# ---------------------------------------------------------------------------------------------------------


class Scenario(Enum):
    ALDER_CRANE = "alder-crane"
    AMBER_WHARF = "amber-wharf"
    BASIL_TERN = "basil-tern"
    BIRCH_HOLLOW = "birch-hollow"
    CEDAR_FLINT = "cedar-flint"
    COBALT_REED = "cobalt-reed"
    DAHLIA_MIST = "dahlia-mist"
    DUNE_SPARROW = "dune-sparrow"
    ELM_THISTLE = "elm-thistle"
    EMBER_KITE = "ember-kite"
    FENNEL_GORGE = "fennel-gorge"
    FIR_COBBLE = "fir-cobble"
    GULL_HEATHER = "gull-heather"
    HAZEL_POND = "hazel-pond"
    HERON_MOSS = "heron-moss"
    INDIGO_FERN = "indigo-fern"
    JASPER_COVE = "jasper-cove"
    KESTREL_BLOOM = "kestrel-bloom"
    LARKSPUR_TIDE = "larkspur-tide"
    MARBLE_FINCH = "marble-finch"
    NECTAR_RIDGE = "nectar-ridge"
    OPAL_HEATH = "opal-heath"
    PEWTER_LAKE = "pewter-lake"
    QUILL_HARBOR = "quill-harbor"
    RUSSET_BROOK = "russet-brook"
    SAFFRON_DELL = "saffron-dell"
    TAMARIND_CREST = "tamarind-crest"
    UMBER_GLADE = "umber-glade"
    VIOLET_QUARRY = "violet-quarry"
    WALNUT_SPIRE = "walnut-spire"
    YARROW_BLUFF = "yarrow-bluff"
    ZEPHYR_MOOR = "zephyr-moor"


class Approver(Enum):
    """Roles that may sign off. NONE: the decision relies on no one's sign-off, given or awaited (one for
    something else may be on file). NOT_NAMED: one is needed, but the handbook names no role."""

    NONE = "NONE"
    NOT_NAMED = "NOT_NAMED"
    ASSIGNMENT_SUPERVISOR = "ASSIGNMENT_SUPERVISOR"
    COUNTRY_DIRECTOR = "COUNTRY_DIRECTOR"
    GLOBAL_TEAM_DIRECTOR = "GLOBAL_TEAM_DIRECTOR"
    BUDGET_HOLDER = "BUDGET_HOLDER"
    CHIEF_FINANCIAL_OFFICER = "CHIEF_FINANCIAL_OFFICER"
    AGREEMENT_OFFICER = "AGREEMENT_OFFICER"
    GRANTS_TEAM = "GRANTS_TEAM"
    GLOBAL_OPERATIONS = "GLOBAL_OPERATIONS"
    TRAVEL_AGENCY = "TRAVEL_AGENCY"
    VICE_PRESIDENT = "VICE_PRESIDENT"
    CHIEF_EXECUTIVE = "CHIEF_EXECUTIVE"
    DEPARTMENT_HEAD = "DEPARTMENT_HEAD"


class Clause(Enum):
    """The handbook's sections, by heading."""

    PURPOSE_AND_SCOPE = "PURPOSE_AND_SCOPE"
    APPLICABILITY = "APPLICABILITY"
    ROLES_AND_RESPONSIBILITIES = "ROLES_AND_RESPONSIBILITIES"
    POLICIES = "POLICIES"
    POLICY_IMPLEMENTATION = "POLICY_IMPLEMENTATION"
    TRAVEL_APPROVAL = "TRAVEL_APPROVAL"
    TRAVEL_ADVANCES = "TRAVEL_ADVANCES"
    TRAVEL_EXPENSES = "TRAVEL_EXPENSES"
    PER_DIEM = "PER_DIEM"
    SAFETY_AND_SECURITY = "SAFETY_AND_SECURITY"
    TRAVEL_DOCUMENTATION = "TRAVEL_DOCUMENTATION"
    AIRFARE = "AIRFARE"
    GROUND_TRANSPORTATION = "GROUND_TRANSPORTATION"
    LODGING = "LODGING"
    COMMUNICATION = "COMMUNICATION"
    PROPERTY_AND_EQUIPMENT = "PROPERTY_AND_EQUIPMENT"
    USG_FUNDED_TRAVEL = "USG_FUNDED_TRAVEL"
    GUIDANCE = "GUIDANCE"
    PREPARING_FOR_TRAVEL = "PREPARING_FOR_TRAVEL"
    DURING_AND_AFTER_TRAVEL = "DURING_AND_AFTER_TRAVEL"
    REIMBURSABLE_EXPENSES = "REIMBURSABLE_EXPENSES"
    US_GOVERNMENT_PROCEDURE = "US_GOVERNMENT_PROCEDURE"


class Passenger(Enum):
    EMPLOYEE = "EMPLOYEE"
    CONSULTANT = "CONSULTANT"
    SPOUSE = "SPOUSE"
    CHILD = "CHILD"


class StaffUnit(Enum):
    GLOBAL_TEAM = "GLOBAL_TEAM"
    COUNTRY_OFFICE = "COUNTRY_OFFICE"


class Purpose(Enum):
    PROJECT_WORK = "PROJECT_WORK"
    TRAINING = "TRAINING"
    CONFERENCE = "CONFERENCE"
    DONOR_MEETING = "DONOR_MEETING"
    PARTNER_MEETING = "PARTNER_MEETING"
    PERSONAL = "PERSONAL"


class Funding(Enum):
    OVERHEAD = "OVERHEAD"
    US_GOVERNMENT = "US_GOVERNMENT"


class SignOffSubject(Enum):
    TRIP = "TRIP"
    UPGRADE_EXCEPTION = "UPGRADE_EXCEPTION"
    COMPANION_TRAVEL = "COMPANION_TRAVEL"


@dataclass
class SignOff(Output):
    role: Annotated[Approver, "The signer's role toward this traveller"]
    name: Annotated[str, "Their name"]
    subject: Annotated[
        SignOffSubject,
        "What they signed off: the trip itself (its dates, air itinerary and fare as the request describes them, "
        "with any personal change the request names), a cabin above economy as an exception, or a family "
        "member's travel",
    ]


@dataclass
class Trip(Output):
    traveller_name: Annotated[str, "Who flies"]
    traveller_title: Annotated[str, "Their job title, or their relation to the employee they go with"]
    passenger: Annotated[Passenger, "What the person flying is to the organisation"]
    accompanies: Annotated[str, "The employee this person goes with, when the person flying is family; empty otherwise"]
    staff_unit: Annotated[StaffUnit, "Where the employee works (for family, the employee they go with): the global team or a country office"]
    home_airport: Annotated[Airport, "The airport of the traveller's home base"]
    origin: Annotated[Airport, "Where this flight leaves from"]
    destination: Annotated[Airport, "Where it goes"]
    travel_date: Annotated[str, "The day to leave, YYYY-MM-DD: the local date at the origin airport"]
    booking_date: Annotated[str, "Today in this world, the day the ticket is bought, YYYY-MM-DD"]
    business_starts: Annotated[str, "When the work at the destination begins, YYYY-MM-DD HH:MM, local time there; empty when the trip has no work"]
    purpose: Annotated[str, "Why the trip is made, in plain words"]
    purpose_kind: Annotated[Purpose, "The kind of trip"]
    funding: Annotated[Funding, "What pays for the trip: overhead funds, or an award from a US federal agency"]
    funding_source: Annotated[str, "The fund or award charged, in plain words"]
    award_terms: Annotated[str, "What the award's own terms ask before travel, in plain words; empty when no award pays"]
    requested_cabin: Annotated[Cabin, "The cabin the traveller asks for"]
    chosen_airline: Annotated[str, "The airline the traveller asks to fly, as search_flights names airlines; empty when none"]
    pays_difference: Annotated[bool, "Whether the traveller offers to pay, from their own money, whatever their wish costs above the fare otherwise bought"]
    wants_refundable: Annotated[bool, "Whether the traveller asks for a fare that can be refunded"]
    wants_overnight_stop: Annotated[bool, "Whether the traveller asks to break the journey with a hotel night on the way"]
    medical_note_date: Annotated[str, "The date written on a doctor's signed letter on file about the seat the traveller needs, YYYY-MM-DD; empty when none"]
    global_operations_told: Annotated[str, "The day the Global Operations team was told of this trip, YYYY-MM-DD; empty when it was not"]
    sign_offs: Annotated[list[SignOff], "Sign-offs already on file for this trip, each given before today"]


# ---------------------------------------------------------------------------------------------------------
# SHARED (template), continued: the tools' and tasks' inputs and outputs.
# ---------------------------------------------------------------------------------------------------------


@dataclass
class TaskInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    request: Annotated[str, "The traveller's request, in their own words"]


@dataclass
class TripInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id, as the task input gives it"]


@dataclass
class TripOutput(Output):
    scenario: Annotated[Scenario, "The case id"]
    request: Annotated[str, "The traveller's request, in their own words"]
    trip: Annotated[Trip, "The trip record behind the request"]


@dataclass
class SearchInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    origin: Annotated[str, "The airport to leave from: An IATA airport code, e.g. JFK"]
    destination: Annotated[str, "The airport to fly to: An IATA airport code, e.g. JFK"]
    date: Annotated[str, "The day to leave, YYYY-MM-DD: the local date at the origin airport, on or after the booking date"]
    return_date: Annotated[str, "For round-trip fares, the day to fly back, YYYY-MM-DD, local at the destination; empty for one way"]


@dataclass
class SearchOutput(Output):
    note: Annotated[str, "Where the offers come from, and a word when this case lists none for the search"]
    currency: Annotated[str, "The currency of every fare, as an ISO code"]
    offers: Annotated[list[Offer], "Every offer leaving on that local date, in departure order"]


@dataclass
class BookingOutput(Output):
    decision: Annotated[
        Decision,
        "BOOK: buy offer_id now. REFUSE: buy nothing, because the organisation buys no ticket at all for this request. "
        "FLAG_FOR_APPROVAL: hold offer_id and buy nothing yet, because someone must approve it first or "
        "the handbook's words leave the answer open",
    ]
    offer_id: Annotated[str, "The offer bought or held, exactly as search_flights listed it; empty when refusing"]
    cabin: Annotated[Cabin, "That offer's cabin; NONE when refusing"]
    reason_code: Annotated[ReasonCode, "Why, from the closed list"]
    approver: Annotated[
        Approver,
        "The role whose sign-off this decision relies on, whether already on file or still awaited; NONE when "
        "this decision relies on no one's sign-off, even if a sign-off for something else is on file; NOT_NAMED "
        "when a sign-off is needed but the handbook names no role",
    ]
    clause: Annotated[Clause, "The handbook section the decision rests on"]


@dataclass
class SolveOutput(Output):
    trip: Annotated[Trip, "The trip record"]
    offers: Annotated[list[Offer], "Every offer on the trip's route and date"]
    decision: Annotated[Decision, "The correct decision"]
    offer_ids: Annotated[list[str], "Every offer id that is a correct choice; empty when refusing"]
    cabins: Annotated[list[Cabin], "Every correct cabin"]
    reason_codes: Annotated[list[ReasonCode], "Every accepted reason"]
    approvers: Annotated[list[Approver], "Every accepted approver"]
    clauses: Annotated[list[Clause], "Every accepted section"]
    unclear_phrase: Annotated[str, "For a hold over unclear words, those words; empty otherwise"]
    explanation: Annotated[str, "How the answer key reached the answer"]


@dataclass
class FieldHelp(Output):
    name: Annotated[str, "The trip record field's name"]
    kind: Annotated[str, "Its type"]
    description: Annotated[str, "What it means"]


@dataclass
class RequirementsInput(Output):
    topic: Annotated[Topic, "ALL for everything, FIELDS for the trip record's fields, AIRPORTS for the airport list"]


@dataclass
class RequirementsOutput(Output):
    fields: Annotated[list[FieldHelp], "The trip record's fields; empty for AIRPORTS"]
    conventions: Annotated[list[str], "How times, dates, fares and seats work in this world; empty for AIRPORTS"]
    airports: Annotated[list[Airport], "The airports the simulated world knows; empty for FIELDS"]


TOOLS = {
    Tool.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Tool.GET_TRIP: (TripInput, TripOutput),
    Tool.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Tool.SOLVE_BOOKING: (TaskInput, SolveOutput),
}
TASKS = {
    Task.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Task.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Task.BOOK_FLIGHT: (TaskInput, BookingOutput),
}
