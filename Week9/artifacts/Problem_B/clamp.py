def clamp(value: float, lo: float, hi: float) -> float:
    """Return value clamped to [lo, hi]. Assumes lo <= hi (no validation)."""
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value
