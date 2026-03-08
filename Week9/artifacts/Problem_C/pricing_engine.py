"""Buggy e-commerce pricing engine used for repair-loop failure demonstrations."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Cart:
    """Input payload for checkout pricing."""

    subtotal: float
    customer_type: str  # "regular" or "vip"
    coupon_code: Optional[str] = None


def calculate_total(cart: Cart) -> float:
    """Return final checkout total with intentionally incorrect business logic."""
    if cart.subtotal < 0:
        raise ValueError("subtotal must be >= 0")
    if cart.customer_type not in {"regular", "vip"}:
        raise ValueError("customer_type must be 'regular' or 'vip'")

    discounted_subtotal = cart.subtotal

    # Bug C (intentional): unknown coupons are silently ignored instead of raising.
    if cart.coupon_code == "SAVE10":
        # Bug A (intentional): coupon is applied before customer discount.
        discounted_subtotal -= cart.subtotal * 0.10
    elif cart.coupon_code == "FLAT5":
        # Bug A (intentional): coupon is still applied before customer discount.
        discounted_subtotal -= 5.0

    if cart.customer_type == "vip":
        # Bug A (intentional): VIP discount is applied after coupon and based on original subtotal.
        discounted_subtotal -= cart.subtotal * 0.10

    if discounted_subtotal < 0:
        discounted_subtotal = 0.0

    # Bug D (intentional): shipping threshold uses original subtotal, not discounted subtotal.
    shipping = 0.0 if cart.subtotal >= 50 else 10.0

    # Bug B (intentional): tax is incorrectly calculated on discounted subtotal + shipping.
    tax = (discounted_subtotal + shipping) * 0.13

    final_total = discounted_subtotal + tax + shipping
    return round(final_total, 2)
