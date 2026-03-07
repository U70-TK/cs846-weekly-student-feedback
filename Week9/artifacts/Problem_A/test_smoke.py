"""
Smoke tests: sequential only.
These pass but find 0 concurrency bugs.

Run:  python -m pytest test_smoke.py -v
"""

import pytest
from bank import BankAccount, TransferService


def test_deposit():
    a = BankAccount("Alice", 100)
    a.deposit(50)
    assert a.get_balance() == 150


def test_withdraw():
    a = BankAccount("Alice", 100)
    a.withdraw(40)
    assert a.get_balance() == 60


def test_withdraw_insufficient():
    a = BankAccount("Alice", 10)
    with pytest.raises(ValueError):
        a.withdraw(50)


def test_transfer_success():
    a = BankAccount("Alice", 200)
    b = BankAccount("Bob", 50)
    svc = TransferService()
    ok = svc.transfer(a, b, 75)
    assert ok is True
    assert a.get_balance() == 125
    assert b.get_balance() == 125


def test_transfer_insufficient():
    a = BankAccount("Alice", 10)
    b = BankAccount("Bob", 0)
    svc = TransferService()
    ok = svc.transfer(a, b, 100)
    assert ok is False
