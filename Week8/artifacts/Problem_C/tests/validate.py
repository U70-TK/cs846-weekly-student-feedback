#!/usr/bin/env python3
"""
tests/validate.py
Automated correctness checker for LibraryTracker.

Run AFTER executing main.py:
    python3 main.py
    python3 tests/validate.py

Prints PASS/FAIL for each check with targeted hints.
Exit code 0 = all pass, 1 = one or more failures.
"""

import json
import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
results = []


def check(label: str, condition: bool, hint: str = "") -> None:
    tag = PASS if condition else FAIL
    msg = f"{tag}  {label}"
    if not condition and hint:
        msg += f"\n       Hint: {hint}"
    print(msg)
    results.append(condition)


# Load outputs
try:
    with open(OUTPUT_DIR / "late_fees.json") as f:
        late_fees = json.load(f)
    with open(OUTPUT_DIR / "availability_by_genre.json") as f:
        genre_data = json.load(f)
    with open(OUTPUT_DIR / "most_checked_out.json") as f:
        top_books = json.load(f)
except FileNotFoundError as e:
    print(f"\033[91mERROR\033[0m: Output file missing - {e}")
    print("Run  python3 main.py  first.")
    sys.exit(1)



print("  LibraryTracker - Correctness Validation Suite")




# CHECK GROUP 1 - Bug 1: available_copies (loader.py)

print("[Bug 1] Loader: available_copies calculation\n")

# All genres must have non-negative available copies
all_non_negative = all(g["available_copies"] >= 0 for g in genre_data)
check(
    "All genres report non-negative available_copies",
    all_non_negative,
    hint="available_copies = total - total - checked_out produces a negative value. Fix: total - checked_out."
)

# Technology genre: B001(5-2=3) + B002(3-3=0) + B007(4-2=2) = total 12, available 5
tech = next((g for g in genre_data if g["genre"] == "Technology"), None)
check(
    "Technology genre: total_copies == 12, available_copies == 5",
    tech is not None and tech["total_copies"] == 12 and tech["available_copies"] == 5,
    hint=(
        f"Got total={tech['total_copies'] if tech else '?'}, "
        f"available={tech['available_copies'] if tech else '?'}. "
        "available_copies formula in load_books() is wrong."
    )
)

# Fiction genre: B004(6-6=0) + B006(3-1=2) = total 9, available 2
fiction = next((g for g in genre_data if g["genre"] == "Fiction"), None)
check(
    "Fiction genre: total_copies == 9, available_copies == 2",
    fiction is not None and fiction["total_copies"] == 9 and fiction["available_copies"] == 2,
    hint=(
        f"Got total={fiction['total_copies'] if fiction else '?'}, "
        f"available={fiction['available_copies'] if fiction else '?'}."
    )
)

print()



# CHECK GROUP 2 - Bug 2: late fee direction (reports.py)

print("[Bug 2] Reports: Late Fee Calculation\n")

# All fees must be positive - a negative fee means subtraction was reversed
all_positive_fees = all(r["total_fee"] >= 0 for r in late_fees)
check(
    "All computed late fees are non-negative",
    all_positive_fees,
    hint="days_late = (due_date - return_date).days returns negative when late. Fix: (return_date - due_date).days."
)

# C002: checkout B003, due 2024-01-24, returned 2024-01-30 → 6 days late → $1.50
c002 = next((r for r in late_fees if r["checkout_id"] == "C002"), None)
check(
    "C002 (returned 6 days late): days_late == 6, total_fee == 1.50",
    c002 is not None and c002["days_late"] == 6 and c002["total_fee"] == 1.50,
    hint=(
        f"Got days_late={c002['days_late'] if c002 else '?'}, "
        f"total_fee={c002['total_fee'] if c002 else '?'}. "
        "Subtraction operands are reversed."
    )
)

# C004: checkout B002, due 2024-02-15, returned 2024-02-20 → 5 days late → $1.25
c004 = next((r for r in late_fees if r["checkout_id"] == "C004"), None)
check(
    "C004 (returned 5 days late): days_late == 5, total_fee == 1.25",
    c004 is not None and c004["days_late"] == 5 and c004["total_fee"] == 1.25,
    hint=(
        f"Got days_late={c004['days_late'] if c004 else '?'}, "
        f"total_fee={c004['total_fee'] if c004 else '?'}."
    )
)

# C001 was returned early (2024-01-18, due 2024-01-19) - must NOT appear in late fees
c001_in_fees = any(r["checkout_id"] == "C001" for r in late_fees)
check(
    "C001 (returned 1 day early) does NOT appear in late fees",
    not c001_in_fees,
    hint="An on-time/early return should not generate a fee entry."
)

print()



# CHECK GROUP 3 -  Bug 3: utilisation_rate direction (reports.py)

print("[Bug 3] Reports: Genre Utilisation Rate\n")

# Fantasy: B010 has 7 total, 7 checked out → utilisation should be 1.0 (fully utilised)
fantasy = next((g for g in genre_data if g["genre"] == "Fantasy"), None)
check(
    "Fantasy (7/7 checked out): utilisation_rate == 1.0",
    fantasy is not None and fantasy["utilisation_rate"] == 1.0,
    hint=(
        f"Got {fantasy['utilisation_rate'] if fantasy else '?'}. "
        "utilisation = available/total is inverted. Fix: (total - available) / total."
    )
)

# History: B005 has 2 total, 0 checked out → utilisation should be 0.0
history = next((g for g in genre_data if g["genre"] == "History"), None)
check(
    "History (0/2 checked out): utilisation_rate == 0.0",
    history is not None and history["utilisation_rate"] == 0.0,
    hint=(
        f"Got {history['utilisation_rate'] if history else '?'}. "
        "A genre with all copies available should have utilisation 0.0, not 1.0."
    )
)

# Technology: 12 total, 5 available → 7 checked out → utilisation = 7/12 ≈ 0.5833
check(
    "Technology: utilisation_rate ≈ 0.5833 (7 of 12 copies in use)",
    tech is not None and abs(tech["utilisation_rate"] - round(7/12, 4)) < 0.001,
    hint=(
        f"Got {tech['utilisation_rate'] if tech else '?'}. "
        "Expected ~0.5833 = (12-5)/12."
    )
)

print()


# Summary
passed = results.count(True)
total  = len(results)
colour = "\033[92m" if passed == total else "\033[91m"
print(f"  Result: {colour}{passed}/{total} checks passed\033[0m")

sys.exit(0 if passed == total else 1)
