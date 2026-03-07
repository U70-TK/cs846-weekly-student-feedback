"""
Thread-Safe Bank Transfer System
A simple banking module supporting deposits, withdrawals, transfers
between accounts, and balance queries that intended to be used from
multiple threads simultaneously.

Contains 5 intentional concurrency bugs. Do NOT modify this file.
"""

import threading


class BankAccount:
    """A single bank account with a balance."""

    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self.balance = balance
        self._lock = threading.Lock()

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        with self._lock:
            self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        with self._lock:
            if self.balance < amount:
                raise ValueError("Insufficient funds")
            self.balance -= amount

    def get_balance(self) -> float:
        """
        BUG #1 (Data Race):
        Reads self.balance WITHOUT acquiring the lock.
        Another thread can be mid-deposit or mid-withdraw,
        so the caller may see a stale or torn value.
        """
        return self.balance


class TransferService:
    """Handles transfers between two BankAccount objects."""

    def __init__(self):
        self.transfer_count = 0
        self._log = []

    def transfer(self, src: BankAccount, dst: BankAccount, amount: float) -> bool:
        """
        Move *amount* from *src* to *dst*.

        BUG #2 (Atomicity Violation):
        Acquires src lock, withdraws, releases it, then acquires dst lock
        and deposits.  Between the two locks another thread can observe
        the money "missing" from both accounts (src debited, dst not yet
        credited).  Total money in the system is temporarily wrong.

        BUG #3 (No Deadlock Prevention):
        Two concurrent transfers in opposite directions
        (A->B and B->A) can deadlock because locks are acquired in
        caller order, not a fixed global order.
        """
        with src._lock:
            if src.balance < amount:
                return False
            src.balance -= amount

        with dst._lock:
            dst.balance += amount

        self._log.append((src.owner, dst.owner, amount))
        self.transfer_count += 1          # BUG #4: not protected by a lock
        return True

    def get_total_transfers(self) -> int:
        """
        BUG #4 (Lost Update on Counter):
        transfer_count is incremented without any lock.
        Under concurrent transfers the final count can be less than
        the actual number of successful transfers.
        """
        return self.transfer_count

    def get_log(self) -> list:
        """
        BUG #5 (Unsafe Shared List):
        _log is a plain list appended from multiple threads with no lock.
        list.append is CPython-atomic due to the GIL, but the spec does
        not guarantee it, and the log length may not match transfer_count.
        """
        return list(self._log)
