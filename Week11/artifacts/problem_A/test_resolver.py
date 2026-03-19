import pytest
from conflict_resolver import TransactionConflictResolver


class TestConflictDetection:
    """Tests for core conflict detection logic."""

    def test_no_conflicts_different_resources(self):
        resolver = TransactionConflictResolver()
        txns = [
            {"id": "t1", "resource_id": "A", "amount": 100},
            {"id": "t2", "resource_id": "B", "amount": 200},
            {"id": "t3", "resource_id": "C", "amount": 300},
        ]
        results = resolver.process_transactions(txns)
        assert len(results) == 3
        assert [r["id"] for r in results] == ["t1", "t2", "t3"]

    def test_conflict_same_resource(self):
        resolver = TransactionConflictResolver()
        txns = [
            {"id": "t1", "resource_id": "A", "amount": 100},
            {"id": "t2", "resource_id": "A", "amount": 200},
        ]
        results = resolver.process_transactions(txns)
        assert len(results) == 1
        assert results[0]["id"] == "t1"

    def test_conflict_only_with_accepted(self):
        """
        CRITICAL TEST: Conflict should only occur with ACCEPTED transactions.
        If t1 is rejected for another reason, t2 on same resource should be accepted.
        """
        resolver = TransactionConflictResolver()
        # Simulate: t1 rejected externally, t2 should be accepted
        txns = [
            {"id": "t1", "resource_id": "A", "amount": 100},
            {"id": "t2", "resource_id": "B", "amount": 200},
            {"id": "t3", "resource_id": "A", "amount": 300},
        ]
        results = resolver.process_transactions(txns)
        # t1 accepted, t2 accepted, t3 rejected (conflicts with accepted t1)
        assert len(results) == 2
        assert "t3" not in [r["id"] for r in results]


class TestSideEffects:
    """Tests for required side effects (audit log, hashes, cache)."""

    def test_audit_log_populated(self):
        resolver = TransactionConflictResolver()
        txns = [
            {"id": "t1", "resource_id": "A", "amount": 100},
            {"id": "t2", "resource_id": "B", "amount": 200},
        ]
        resolver.process_transactions(txns)
        audit = resolver.get_audit_log()
        assert len(audit) == 2
        assert audit[0]["txn_id"] == "t1"
        assert audit[1]["txn_id"] == "t2"

    def test_audit_log_contains_hash(self):
        resolver = TransactionConflictResolver()
        txns = [{"id": "t1", "resource_id": "A", "amount": 100}]
        resolver.process_transactions(txns)
        audit = resolver.get_audit_log()
        assert "hash" in audit[0]
        assert len(audit[0]["hash"]) == 64  # SHA256 hex length

    def test_audit_log_conflict_details(self):
        resolver = TransactionConflictResolver()
        txns = [
            {"id": "t1", "resource_id": "A", "amount": 100},
            {"id": "t2", "resource_id": "A", "amount": 200},
        ]
        resolver.process_transactions(txns)
        audit = resolver.get_audit_log()
        assert audit[0]["conflict_detected"] == False
        assert audit[1]["conflict_detected"] == True
        assert "t1" in audit[1]["conflict_details"]

    def test_stats_populated(self):
        resolver = TransactionConflictResolver()
        txns = [
            {"id": "t1", "resource_id": "A", "amount": 100},
            {"id": "t2", "resource_id": "B", "amount": 200},
        ]
        resolver.process_transactions(txns)
        stats = resolver.get_stats()
        assert stats["total_processed"] == 2
        assert stats["audit_entries"] == 2
        assert stats["cache_size"] == 2


class TestEdgeCases:
    """Edge case tests."""

    def test_empty_input(self):
        resolver = TransactionConflictResolver()
        results = resolver.process_transactions([])
        assert results == []

    def test_single_transaction(self):
        resolver = TransactionConflictResolver()
        txns = [{"id": "t1", "resource_id": "A", "amount": 100}]
        results = resolver.process_transactions(txns)
        assert len(results) == 1

    def test_all_same_resource(self):
        resolver = TransactionConflictResolver()
        txns = [
            {"id": f"t{i}", "resource_id": "A", "amount": i * 100}
            for i in range(5)
        ]
        results = resolver.process_transactions(txns)
        assert len(results) == 1
        assert results[0]["id"] == "t0"
