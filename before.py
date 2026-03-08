"""Specification-based tests for pricing_engine.calculate_total."""

import pytest

from pricing_engine import Cart, calculate_total


def test_regular_no_coupon_under_shipping_threshold() -> None:
    """Subtotal 40, regular, no coupon -> 40 + 5.2 tax + 10 shipping = 55.2."""
    cart = Cart(subtotal=40, customer_type="regular")
    assert calculate_total(cart) == pytest.approx(55.2, abs=1e-2)


def test_regular_no_coupon_free_shipping() -> None:
    """Subtotal 50, regular, no coupon -> 50 + 6.5 tax + 0 shipping = 56.5."""
    cart = Cart(subtotal=50, customer_type="regular")
    assert calculate_total(cart) == pytest.approx(56.5, abs=1e-2)


def test_vip_discount_applied() -> None:
    """Subtotal 100, VIP -> discounted 90, tax 11.7, final 101.7."""
    cart = Cart(subtotal=100, customer_type="vip")
    assert calculate_total(cart) == pytest.approx(101.7, abs=1e-2)


def test_vip_then_percentage_coupon_order() -> None:
    """
    Spec math:
      100 -> VIP 10% => 90 -> SAVE10 => 81
      shipping 0, tax 10.53, final 91.53
    """
    cart = Cart(subtotal=100, customer_type="vip", coupon_code="SAVE10")
    assert calculate_total(cart) == pytest.approx(91.53, abs=1e-2)


def test_flat5_coupon() -> None:
    """
    Subtotal 60, FLAT5:
      discounted subtotal = 55
      shipping = 0
      tax = 55 * 0.13 = 7.15
      final = 62.15
    """
    cart = Cart(subtotal=60, customer_type="regular", coupon_code="FLAT5")
    assert calculate_total(cart) == pytest.approx(62.15, abs=1e-2)


def test_shipping_threshold_uses_discounted_subtotal() -> None:
    """
    Subtotal 52 with FLAT5:
      discounted subtotal = 47 (shipping should apply)
      tax = 47 * 0.13 = 6.11
      shipping = 10
      final = 63.11
    """
    cart = Cart(subtotal=52, customer_type="regular", coupon_code="FLAT5")
    assert calculate_total(cart) == pytest.approx(63.11, abs=1e-2)


def test_shipping_not_taxed() -> None:
    """Tax is 13% of discounted subtotal only; shipping should not be taxed."""
    cart = Cart(subtotal=40, customer_type="regular")
    expected_tax = 40 * 0.13
    expected_total = 40 + expected_tax + 10
    assert calculate_total(cart) == pytest.approx(expected_total, abs=1e-2)


def test_invalid_coupon_raises() -> None:
    """Invalid coupon codes must raise ValueError."""
    cart = Cart(subtotal=40, customer_type="regular", coupon_code="BADCODE")
    with pytest.raises(ValueError):
        calculate_total(cart)


def test_invalid_customer_type_raises() -> None:
    """Unknown customer type should raise ValueError."""
    cart = Cart(subtotal=40, customer_type="student")
    with pytest.raises(ValueError):
        calculate_total(cart)


def test_negative_subtotal_raises() -> None:
    """Negative subtotal should raise ValueError."""
    cart = Cart(subtotal=-1, customer_type="regular")
    with pytest.raises(ValueError):
        calculate_total(cart)
