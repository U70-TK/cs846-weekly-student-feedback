"""
LibraryTracker - Main Entry Point
Runs a 3-stage reporting pipeline over library books and checkout data.

  Stage 1 → loader.py    Load & validate CSV data
  Stage 2 → reports.py   Compute late fees, genre availability, top books
  Stage 3 → Write JSON reports to output/
"""

import json
import sys
from datetime import date
from pathlib import Path

from tracker.loader import load_books, load_checkouts
from tracker.reports import compute_late_fees, availability_by_genre, most_checked_out

DATA_DIR   = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"

# Reference date used to compute accrued fees on unreturned overdue books
REFERENCE_DATE = date(2024, 4, 20)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    #Stage 1: Load 
    print("[1/3] Loading data...")
    books     = load_books(DATA_DIR / "books.csv")
    checkouts = load_checkouts(DATA_DIR / "checkouts.csv")
    print(f"      Books: {len(books)} | Checkouts: {len(checkouts)}")

    #Stage 2: Reports 
    print("[2/3] Generating reports...")
    late_fees   = compute_late_fees(checkouts, REFERENCE_DATE)
    by_genre    = availability_by_genre(books)
    top_books   = most_checked_out(checkouts, books, top_n=5)

    #Stage 3: Write Outputs 
    print("[3/3] Writing outputs...")
    with open(OUTPUT_DIR / "late_fees.json", "w") as f:
        json.dump(late_fees, f, indent=2, default=str)

    with open(OUTPUT_DIR / "availability_by_genre.json", "w") as f:
        json.dump(by_genre, f, indent=2, default=str)

    with open(OUTPUT_DIR / "most_checked_out.json", "w") as f:
        json.dump(top_books, f, indent=2, default=str)

    #Summary 
    total_fees = sum(r["total_fee"] for r in late_fees)
    overdue_count = sum(1 for r in late_fees if r["status"] == "overdue_unreturned")

    print("\n Report Completed")
    print(f"   Overdue/late checkouts : {len(late_fees)}")
    print(f"   Still unreturned       : {overdue_count}")
    print(f"   Total fees owed        : ${total_fees:.2f}")
    print(f"   Genres tracked         : {len(by_genre)}")
    print(f"   Outputs written to     : {OUTPUT_DIR}/")
   


if __name__ == "__main__":
    main()
