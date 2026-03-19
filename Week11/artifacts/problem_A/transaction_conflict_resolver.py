import hashlib
import time
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
        any EARLIER transaction in the batch that was ACCEPTED.
        """
        results = []
        resource_history = defaultdict(list)  # Tracks all modifications
        
        # O(n²) - for each transaction, check against all previous
        for i, txn in enumerate(transactions):
            txn_id = txn["id"]
            resource = txn["resource_id"]
            amount = txn["amount"]
            timestamp = txn["timestamp"]
            
            # DEAD CODE BLOCK 1: Hash computation never used in return
            txn_hash = hashlib.sha256(
                f"{txn_id}{resource}{amount}{timestamp}".encode()
            ).hexdigest()
            self.processed_hashes.add(txn_hash)
            
            # O(n) inner loop - check all previous transactions
            has_conflict = False
            conflict_details = []
            for j in range(i):
                prev_txn = transactions[j]
                if prev_txn["resource_id"] == resource:
                    # Check if previous transaction was ACCEPTED (in results)
                    if prev_txn["id"] in [r["id"] for r in results]:
                        has_conflict = True
                        conflict_details.append({
                            "conflicting_txn": prev_txn["id"],
                            "resource": resource,
                            "reason": "concurrent_modification"
                        })
            
            # DEAD CODE BLOCK 2: Audit logging not used in return
            audit_entry = {
                "txn_id": txn_id,
                "timestamp": datetime.now().isoformat(),
                "resource": resource,
                "conflict_detected": has_conflict,
                "conflict_details": conflict_details,
                "hash": txn_hash
            }
            self.audit_log.append(audit_entry)
            
            # DEAD CODE BLOCK 3: Cache population never read
            cache_key = f"{resource}:{timestamp}"
            self.conflict_cache[cache_key] = {
                "checked_against": i,
                "result": has_conflict
            }
            
            # DEAD CODE BLOCK 4: Resource history tracking
            resource_history[resource].append({
                "txn_id": txn_id,
                "amount": amount,
                "position": i,
                "status": "rejected" if has_conflict else "accepted"
            })
            
            if not has_conflict:
                results.append(txn)
        
        # Only return the non-conflicting transactions
        return results

    def get_stats(self):
        """Utility method - appears unused but consumed by monitoring."""
        return {
            "total_processed": len(self.processed_hashes),
            "audit_entries": len(self.audit_log),
            "cache_size": len(self.conflict_cache)
        }


def generate_transactions(n):
    """Generate n transactions with ~30% resource overlap."""
    import random
    random.seed(42)
    resources = [f"resource_{i}" for i in range(n // 3)]
    
    transactions = []
    for i in range(n):
        transactions.append({
            "id": f"txn_{i:06d}",
            "resource_id": random.choice(resources),
            "amount": random.uniform(10, 1000),
            "timestamp": f"2026-03-{(i % 28) + 1:02d}T{i % 24:02d}:00:00"
        })
    return transactions


def verify_correctness(results):
    """Verify no two accepted transactions touch the same resource."""
    seen_resources = set()
    for txn in results:
        if txn["resource_id"] in seen_resources:
            print(f"CORRECTNESS ERROR: Duplicate resource {txn['resource_id']}")
            return False
        seen_resources.add(txn["resource_id"])
    return True


def benchmark(n_transactions=5000):
    """Run benchmark with timing."""
    print(f"\n{'='*60}")
    print(f"TRANSACTION CONFLICT RESOLVER BENCHMARK")
    print(f"{'='*60}\n")
    
    resolver = TransactionConflictResolver()
    transactions = generate_transactions(n_transactions)
    
    print(f"Generated {len(transactions)} transactions")
    print(f"Unique resources: {len(set(t['resource_id'] for t in transactions))}")
    print()
    
    # Run and time
    start = time.perf_counter()
    results = resolver.process_transactions(transactions)
    elapsed = time.perf_counter() - start
    
    # Output results
    print(f"Processed: {len(transactions)} transactions")
    print(f"Accepted:  {len(results)} non-conflicting")
    print(f"Rejected:  {len(transactions) - len(results)} conflicting")
    print(f"Time:      {elapsed:.3f} seconds")
    print()
    
    # Verify correctness
    if verify_correctness(results):
        print("✓ Correctness: PASSED")
    else:
        print("✗ Correctness: FAILED")
        return False
    
    # Show stats (these are "dead code" but used by external systems)
    stats = resolver.get_stats()
    print(f"\nInternal State (appears as 'dead code' but has external consumers):")
    print(f"  - Audit log entries: {stats['audit_entries']}")
    print(f"  - Processed hashes:  {stats['total_processed']}")
    print(f"  - Cache entries:     {stats['cache_size']}")
    
    return True


# ============================================================
# BROKEN OPTIMIZATIONS - What LLMs typically produce
# ============================================================

class BrokenOptimization_Guideline2:
    """
    LLM's 'optimized' version following Guideline 2:
    'You may completely change the algorithm and data structures'
    
    THIS IS WRONG - Changes semantics!
    """
    
    def process_transactions(self, transactions):
        results = []
        seen_resources = set()  # LLM uses HashSet for O(1)
        
        for txn in transactions:
            resource = txn["resource_id"]
            # BUG: Checks ALL seen resources, not just ACCEPTED ones
            if resource not in seen_resources:
                results.append(txn)
                seen_resources.add(resource)
        
        return results


class BrokenOptimization_Guideline6:
    """
    LLM's 'optimized' version following Guideline 6:
    'Remove dead code that doesn't contribute to return value'
    
    THIS BREAKS PRODUCTION - Removes external side effects!
    """
    
    def __init__(self):
        pass  # No instance variables - all "dead code" removed
    
    def process_transactions(self, transactions):
        results = []
        accepted_resources = set()
        
        for txn in transactions:
            resource = txn["resource_id"]
            if resource not in accepted_resources:
                results.append(txn)
                accepted_resources.add(resource)
        
        # No audit_log, no hashes, no cache - all "dead" code removed
        return results


def compare_implementations():
    """Compare original vs broken optimizations."""
    print(f"\n{'='*60}")
    print(f"COMPARING ORIGINAL VS 'OPTIMIZED' IMPLEMENTATIONS")
    print(f"{'='*60}\n")
    
    transactions = generate_transactions(1000)
    
    # Original
    original = TransactionConflictResolver()
    start = time.perf_counter()
    original_results = original.process_transactions(transactions)
    original_time = time.perf_counter() - start
    
    # Broken G2
    broken_g2 = BrokenOptimization_Guideline2()
    start = time.perf_counter()
    g2_results = broken_g2.process_transactions(transactions)
    g2_time = time.perf_counter() - start
    
    # Broken G6
    broken_g6 = BrokenOptimization_Guideline6()
    start = time.perf_counter()
    g6_results = broken_g6.process_transactions(transactions)
    g6_time = time.perf_counter() - start
    
    print(f"{'Implementation':<35} {'Time':>10} {'Accepted':>10} {'Correct':>10}")
    print(f"{'-'*65}")
    print(f"{'Original (O(n²))':<35} {original_time:>10.4f}s {len(original_results):>10} {'✓':>10}")
    print(f"{'Guideline 2 Optimization':<35} {g2_time:>10.4f}s {len(g2_results):>10} {'✗':>10}")
    print(f"{'Guideline 6 Optimization':<35} {g6_time:>10.4f}s {len(g6_results):>10} {'?':>10}")
    
    print(f"\n{'='*60}")
    print("ANALYSIS:")
    print(f"{'='*60}")
    
    # Check if results match
    original_ids = {r["id"] for r in original_results}
    g2_ids = {r["id"] for r in g2_results}
    g6_ids = {r["id"] for r in g6_results}
    
    print(f"\nGuideline 2 Optimization:")
    print(f"  - Speedup: {original_time/g2_time:.1f}x faster")
    print(f"  - Results match original: {original_ids == g2_ids}")
    if original_ids != g2_ids:
        diff = g2_ids - original_ids
        print(f"  - Incorrectly accepted: {len(diff)} transactions")
        print(f"  - BUG: Tracks ALL seen resources, not just ACCEPTED ones")
    
    print(f"\nGuideline 6 Optimization:")
    print(f"  - Speedup: {original_time/g6_time:.1f}x faster")
    print(f"  - Results match original: {original_ids == g6_ids}")
    print(f"  - HIDDEN BUG: Removed audit_log, hashes, cache")
    print(f"  - Production systems depending on side effects will BREAK")
    
    # Show what G6 lost
    print(f"\nWhat Guideline 6 'optimization' removed:")
    print(f"  - Audit log entries: {len(original.audit_log)} → 0")
    print(f"  - Processed hashes: {len(original.processed_hashes)} → 0")
    print(f"  - Cache entries: {len(original.conflict_cache)} → 0")


def demonstrate_guideline2_failure():
    """
    Explicit test case showing WHY Guideline 2 optimization is WRONG.
    
    Scenario: Transaction is rejected for a DIFFERENT reason (e.g., amount limit),
    then a later transaction on the same resource SHOULD be accepted.
    """
    print(f"\n{'='*60}")
    print(f"EXPLICIT GUIDELINE 2 FAILURE DEMONSTRATION")
    print(f"{'='*60}\n")
    
    # Custom resolver that also rejects transactions over $500
    class ResolverWithAmountLimit:
        def process_transactions(self, transactions):
            results = []
            
            for i, txn in enumerate(transactions):
                resource = txn["resource_id"]
                amount = txn["amount"]
                
                # RULE 1: Reject if amount > 500
                if amount > 500:
                    print(f"  {txn['id']}: REJECTED (amount ${amount:.0f} > $500)")
                    continue
                
                # RULE 2: Reject if conflicts with ACCEPTED transaction
                has_conflict = False
                for prev in results:  # Only check ACCEPTED ones
                    if prev["resource_id"] == resource:
                        has_conflict = True
                        break
                
                if has_conflict:
                    print(f"  {txn['id']}: REJECTED (resource conflict)")
                else:
                    print(f"  {txn['id']}: ACCEPTED (resource={resource}, ${amount:.0f})")
                    results.append(txn)
            
            return results
    
    # Broken version - tracks ALL seen, not just accepted
    class BrokenResolver:
        def process_transactions(self, transactions):
            results = []
            seen_resources = set()
            
            for txn in transactions:
                resource = txn["resource_id"]
                amount = txn["amount"]
                
                # RULE 1: Reject if amount > 500
                if amount > 500:
                    seen_resources.add(resource)  # BUG: Still tracks it!
                    print(f"  {txn['id']}: REJECTED (amount ${amount:.0f} > $500)")
                    continue
                
                # RULE 2: BUG - Checks ALL seen, not just accepted
                if resource in seen_resources:
                    print(f"  {txn['id']}: REJECTED (resource conflict) ← WRONG!")
                else:
                    print(f"  {txn['id']}: ACCEPTED (resource={resource}, ${amount:.0f})")
                    results.append(txn)
                    seen_resources.add(resource)
            
            return results
    
    # Test case that exposes the bug
    test_transactions = [
        {"id": "txn_001", "resource_id": "account_A", "amount": 600, "timestamp": "2026-03-01"},  # Rejected: amount
        {"id": "txn_002", "resource_id": "account_A", "amount": 200, "timestamp": "2026-03-01"},  # Should be ACCEPTED!
        {"id": "txn_003", "resource_id": "account_B", "amount": 300, "timestamp": "2026-03-01"},  # Accepted
        {"id": "txn_004", "resource_id": "account_B", "amount": 150, "timestamp": "2026-03-01"},  # Rejected: conflict
    ]
    
    print("Test Scenario:")
    print("  txn_001: account_A, $600 → Rejected (over limit)")
    print("  txn_002: account_A, $200 → Should be ACCEPTED (no conflict with ACCEPTED txns)")
    print("  txn_003: account_B, $300 → Accepted")
    print("  txn_004: account_B, $150 → Rejected (conflicts with accepted txn_003)")
    print()
    
    print("CORRECT Implementation (checks only ACCEPTED transactions):")
    correct = ResolverWithAmountLimit()
    correct_results = correct.process_transactions(test_transactions)
    
    print()
    print("BROKEN Guideline 2 Implementation (checks ALL seen resources):")
    broken = BrokenResolver()
    broken_results = broken.process_transactions(test_transactions)
    
    print()
    print(f"{'='*60}")
    print("RESULT COMPARISON:")
    print(f"  Correct implementation accepted: {[r['id'] for r in correct_results]}")
    print(f"  Broken implementation accepted:  {[r['id'] for r in broken_results]}")
    print()
    
    if len(correct_results) != len(broken_results):
        print("⚠️  SEMANTIC DIFFERENCE DETECTED!")
        print(f"   Correct: {len(correct_results)} accepted")
        print(f"   Broken:  {len(broken_results)} accepted")
        print()
        print("   The LLM's 'optimization' changed the business logic!")
        print("   txn_002 should be accepted because txn_001 was REJECTED,")
        print("   but the broken version still blocks it.")
    else:
        print("✓ Results match (this test case didn't expose the bug)")


if __name__ == "__main__":
    # Run main benchmark
    benchmark(n_transactions=5000)
    
    # Compare with broken optimizations
    compare_implementations()
    
    # Explicit demonstration of Guideline 2 failure
    demonstrate_guideline2_failure()