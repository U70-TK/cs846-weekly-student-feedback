"""
tracker/reports.py
Generates three summary reports from the loaded library data:

  1.  compute_late_fees()    - For each returned late checkout, compute the
                                 total fine owed. For unreturned overdue items,
                                 compute accrued fine as of a reference date.

  2.  availability_by_genre() -  For each genre, report total copies,
                                 currently available copies, and utilisation rate.

  3.  most_checked_out()    - Return the top N books ranked by number of
                                 checkouts recorded in the checkout log.
"""

from collections import defaultdict
from datetime import date
from typing import Any, Dict, List


#Late fee computation

def compute_late_fees(
    checkouts: List[Dict[str, Any]],
    reference_date: date,
) -> List[Dict[str, Any]]:
    """
    Compute late fees for all checkouts where the item was (or still is)
    overdue.

    A checkout is overdue if:
      • It has been returned AND return_date > due_date, OR
      • It has NOT been returned AND reference_date > due_date.

    The fee is:
      days_late * late_fee_per_day

    Args:
        checkouts:      List of checkout dicts from loader.load_checkouts().
        reference_date: Today's date, used to compute accrued fees on
                        unreturned items.

    Returns:
        A list of dicts - one per overdue checkout - containing:
          checkout_id, book_id, member_id, days_late, total_fee, status.

    # BUG 2
    # The days_late calculation is inverted for returned items:
    #
    #   days_late = (due_date - return_date).days   ← BUG 2
    #
    # This subtracts in the wrong direction: when return_date > due_date
    # (i.e. the book IS late), the result is negative.
    # A negative days_late produces a negative fee, which makes overdue
    # members appear to be OWED money rather than owing a fine.
    #
    # Fix: reverse the operands → (return_date - due_date).days
    """
    results = []

    for c in checkouts:
        due         = c["due_date"]
        returned    = c["return_date"]
        fee_per_day = c["late_fee_per_day"]

        if returned is not None:
            # Book has been returned — check if it was late
            if returned > due:
                # BUG 2: wrong subtraction direction → produces negative days
                days_late = (due - returned).days   # BUG 2
                results.append({
                    "checkout_id": c["checkout_id"],
                    "book_id"    : c["book_id"],
                    "member_id"  : c["member_id"],
                    "days_late"  : days_late,
                    "total_fee"  : round(days_late * fee_per_day, 2),
                    "status"     : "returned_late",
                })
        else:
            # Book not yet returned — check if overdue as of reference_date
            if reference_date > due:
                days_late = (reference_date - due).days
                results.append({
                    "checkout_id": c["checkout_id"],
                    "book_id"    : c["book_id"],
                    "member_id"  : c["member_id"],
                    "days_late"  : days_late,
                    "total_fee"  : round(days_late * fee_per_day, 2),
                    "status"     : "overdue_unreturned",
                })

    return sorted(results, key=lambda r: r["total_fee"], reverse=True)


#Availability by genre 

def availability_by_genre(books: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Group books by genre and compute aggregate availability statistics.

    For each genre, returns:
      - genre            : str
      - total_copies     : int  - sum of all copies across books in genre
      - available_copies : int  - copies currently on the shelf
      - utilisation_rate : floa - fraction of copies checked out (0.0–1.0)

    # BUG 3
    # The utilisation_rate is computed as:
    #
    #   utilisation_rate = available / total   ← BUG 3
    #
    # This reports the fraction of copies that are AVAILABLE - the inverse of
    # utilisation.  Utilisation should reflect how many copies are IN USE:
    #
    #   utilisation_rate = (total - available) / total
    #                    = copies_checked_out / total
    #
    # With Bug 3 a genre with all copies checked out shows utilisation = 0.0
    # (appears idle) and a fully available genre shows utilisation = 1.0
    # (appears fully utilised - exactly backwards.
    #
    # Fix: change  available / total  →  (total - available) / total
    """
    genre_data: Dict[str, Dict[str, int]] = defaultdict(lambda: {"total": 0, "available": 0})

    for book in books:
        g = book["genre"]
        genre_data[g]["total"]     += book["copies_total"]
        genre_data[g]["available"] += book["available_copies"]

    result = []
    for genre, data in sorted(genre_data.items()):
        total     = data["total"]
        available = data["available"]
        result.append({
            "genre"            : genre,
            "total_copies"     : total,
            "available_copies" : available,
            # BUG 3: reports availability fraction, not utilisation
            "utilisation_rate" : round(available / total, 4) if total else 0.0,
        })

    return result


#Most-checked-out books 

def most_checked_out(
    checkouts: List[Dict[str, Any]],
    books: List[Dict[str, Any]],
    top_n: int = 5,
) -> List[Dict[str, Any]]:
    """
    Return the top N books by total number of checkout records.

    Args:
        checkouts: Full checkout history.
        books:     Book catalogue for title/author lookup.
        top_n:     How many results to return.

    Returns:
        A list of up to top_n dicts containing:
          book_id, title, author, genre, checkout_count.
    """
    counts: Dict[str, int] = defaultdict(int)
    for c in checkouts:
        counts[c["book_id"]] += 1

    book_lookup = {b["book_id"]: b for b in books}

    ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
    return [
        {
            "book_id"       : bid,
            "title"         : book_lookup.get(bid, {}).get("title", "Unknown"),
            "author"        : book_lookup.get(bid, {}).get("author", "Unknown"),
            "genre"         : book_lookup.get(bid, {}).get("genre", "Unknown"),
            "checkout_count": count,
        }
        for bid, count in ranked
    ]
