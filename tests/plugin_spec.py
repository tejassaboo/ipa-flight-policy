"""The handbook-specific settings the template's acceptance tests read. Every other file in tests/ is the
template's and stays identical across plugins (see TEMPLATE_GUIDE.md)."""

from pathlib import Path

import contract

ROOT = Path(__file__).resolve().parents[1]

# Ids that are published or taken: a new plugin never reuses one (MASTER_PLAN section 4, "id check").
PUBLISHED_IDS = {
    "aiib-delegation-entitlement", "ec-mission-cabin-allowance", "ftr-city-pair-fare-selection",
    "gates-vendor-flight-ranking", "njc-cabin-meal-allowance", "sfc-travel-preapproval", "uc-g28-expense-audit",
    "un-staff-air-travel-audit", "vt-airfare-policy-booking", "wa-saam-travel-versioned-audit",
    "energy-corporate-flight-booking", "pharma-distributor-flight-booking", "shipping-company-flight-booking",
    "telecommunications-flight-booking", "preference-aware-flight-booking", "llm-context-compress",
    "weather-alert", "word-check", "arxiv-source",
}

# The frozen original's SHA256SUMS, when this checkout sits beside pilot_work/ (skipped elsewhere).
FROZEN_SHA256SUMS = ROOT.parents[1] / "pilot_work" / "originals" / "ipa-travel" / "frozen" / "SHA256SUMS"

# Scenario mix by primary category (EDGE_CASES.md section 5.2; the 32-scenario row).
MIX = {"easy": 6, "boundary_twin": 8, "multi_rule": 5, "hidden_clause": 3, "distractor": 3, "refusal": 3, "flag": 4}

# Overlay minimums (EDGE_CASES.md section 5.3) for the rules this handbook has. It has no rule on several
# travellers on one flight, so the multi-traveller overlay is not required.
OVERLAY_MINIMUMS = {
    "multi_leg": 3, "overnight": 1, "date_arithmetic": 2, "month_end": 1, "personal_travel": 1,
    "dearer_option": 2, "upgrade_not_taken": 2, "outside_air_section": 2,
}

# Words a scenario id may not contain beyond the template's universal list: this handbook's rule and role
# terms.
ID_FORBIDDEN_TERMS = {
    "spouse", "husband", "wife", "partner", "child", "family", "holiday", "leave", "wedding", "personal", "medical",
    "doctor", "note", "knee", "back", "supervisor", "director", "country", "team", "budget", "holder", "cfo", "chief",
    "finance", "financial", "officer", "grants", "grant", "operations", "global", "nonstop", "direct", "connection",
    "layover", "stopover", "rest", "night", "premium", "coach", "economy", "refundable", "flexible", "loyalty",
    "miles", "airline", "carrier", "america", "american", "foreign", "skies", "open", "eu", "government", "federal",
    "award", "notice", "week", "weeks", "year", "home", "route", "routing", "deadline", "arrival", "morning",
    "afternoon", "change", "fee", "lowest", "expeditious", "agency", "approval", "nairobi", "kenya", "dubai",
    "amsterdam", "delhi", "india", "bogota", "frankfurt", "safari",
}

# The handbook-specific enums whose member words a scenario id may not contain either.
ID_CATEGORY_ENUMS = [contract.Passenger, contract.StaffUnit, contract.Purpose, contract.Funding,
                     contract.SignOffSubject]

# How many scenarios a degenerate agent may pass: one that always holds the right offer for approval, and
# one that always books the cheapest seat (with the right section).
MAX_PASS_ALWAYS_FLAG = 2
MAX_PASS_ALWAYS_LOWEST = 12

# Hand-built duration cases beyond the automatic both-sides tests: (rule, outbound scheduled minutes per
# flight, layovers, expected True / False). Same-day connections count their ground time (lines 349-350,
# "including non-overnight stopovers and change of planes").
DURATION_CASES = [
    ("rest-stop", [840], [], False),  # strict: "in excess of 14 hours"
    ("rest-stop", [841], [], True),
    ("rest-stop", [400, 400], [40], False),  # 840 with the change of planes
    ("rest-stop", [400, 400], [41], True),  # 841: the change of planes counts
    ("rest-stop", [420, 380], [90], True),  # flights 800, journey 890
    ("rest-stop", [300, 350], [120], False),  # journey 770
]
