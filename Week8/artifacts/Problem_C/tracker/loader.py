"""
tracker/loader.py
Reads and validates the two CSV data files (books.csv, checkouts.csv)
and returns typed Python dicts for downstream processing.

Book record schema:
  {
    "book_id"           : str,
    "title"             : str,
    "author"            : str,
    "genre"             : str,
    "year"              : int,
    "copies_total"      : int,
    "copies_checked_out": int,
    "available_copies"  : int   ← derived field
  }

Checkout record schema:
  {
    "checkout_id"    : str,
    "book_id"        : str,
    "member_id"      : str,
    "checkout_date"  : date,
    "due_date"       : date,
    "return_date"    : date | None,
    "late_fee_per_day: float
  }
"""

import csv
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional


def _parse_date(s: str) -> Optional[date]:
    """Parse a YYYY-MM-DD string into a date object, or return None if empty."""
    if not s.strip():
        return None
    return date.fromisoformat(s.strip())


def load_books(filepath: Path) -> List[Dict[str, Any]]:
    """
    Read books.csv and return a list of validated book dicts.

    # BUG 1- available_copies is calculated with an incorrect formula that subtracts total twice, resulting in negative values. This corrupts availability reports and genre summaries that rely on this field.
    # available_copies is calculated as:
    #
    #     copies_total - copies_total - copies_checked_out
    #
    # The double subtraction of copies_total causes available_copies to always
    # equal -copies_checked_out (a negative number). This corrupts the
    # availability report and the genre summary, both of which rely on this field.
    #
    # Fix: change to  copies_total - copies_checked_out
    """
    books = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total    = int(row["copies_total"])
            checked  = int(row["copies_checked_out"])
            books.append({
                "book_id"           : row["book_id"],
                "title"             : row["title"],
                "author"            : row["author"],
                "genre"             : row["genre"],
                "year"              : int(row["year"]),
                "copies_total"      : total,
                "copies_checked_out": checked,
                # BUG 1: subtracts total twice — result is always negative
                "available_copies"  : total - total - checked,
            })
    return books


def load_checkouts(filepath: Path) -> List[Dict[str, Any]]:
    """
    Read checkouts.csv and return a list of validated checkout dicts.
    Rows with unparseable dates are skipped silently.
    """
    checkouts = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                checkouts.append({
                    "checkout_id"    : row["checkout_id"],
                    "book_id"        : row["book_id"],
                    "member_id"      : row["member_id"],
                    "checkout_date"  : _parse_date(row["checkout_date"]),
                    "due_date"       : _parse_date(row["due_date"]),
                    "return_date"    : _parse_date(row["return_date"]),
                    "late_fee_per_day": float(row["late_fee_per_day"]),
                })
            except (ValueError, KeyError):
                continue
    return checkouts
