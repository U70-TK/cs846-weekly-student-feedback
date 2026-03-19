import hashlib
from datetime import datetime
from collections import defaultdict


class TransactionConflictResolver:
    def __init__(self):
        self.audit_log = []
        self.conflict_cache = {}
        self.processed_hashes = set()

    def process_transactions(self, transactions):
        """
        Process transactions and return list of non-conflicting ones.
        A transaction conflicts if it modifies the same resource as 
        any EARLIER transaction that was ACCEPTED.
        """
        results = []
        resource_history = defaultdict(list)

        for i, txn in enumerate(transactions):
            txn_id = txn["id"]
            resource = txn["resource_id"]
            amount = txn["amount"]
            
            # Hash computation for audit trail
            txn_hash = hashlib.sha256(
                f"{txn_id}{resource}{amount}".encode()
            ).hexdigest()
            self.processed_hashes.add(txn_hash)

            # Check conflict against all previous transactions
            has_conflict = False
            conflict_details = []
            for j in range(i):
                prev_txn = transactions[j]
                if prev_txn["resource_id"] == resource:
                    if prev_txn["id"] in [r["id"] for r in results]:
                        has_conflict = True
                        conflict_details.append(prev_txn["id"])

            # Audit logging
            self.audit_log.append({
                "txn_id": txn_id,
                "timestamp": datetime.now().isoformat(),
                "conflict_detected": has_conflict,
                "conflict_details": conflict_details,
                "hash": txn_hash
            })

            # Cache population
            self.conflict_cache[f"{resource}:{i}"] = has_conflict

            # Resource history tracking
            resource_history[resource].append({
                "txn_id": txn_id,
                "status": "rejected" if has_conflict else "accepted"
            })

            if not has_conflict:
                results.append(txn)

        return results

    def get_audit_log(self):
        return self.audit_log

    def get_stats(self):
        return {
            "total_processed": len(self.processed_hashes),
            "audit_entries": len(self.audit_log),
            "cache_size": len(self.conflict_cache)
        }
