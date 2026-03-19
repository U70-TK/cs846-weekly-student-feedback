import time
import random
from conflict_resolver import TransactionConflictResolver


def generate_transactions(n, resource_ratio=3):
    random.seed(42)
    resources = [f"resource_{i}" for i in range(n // resource_ratio)]
    return [
        {
            "id": f"txn_{i:06d}",
            "resource_id": random.choice(resources),
            "amount": random.uniform(10, 1000),
        }
        for i in range(n)
    ]


def run_benchmark(n=3000):
    print(f"Generating {n} transactions...")
    txns = generate_transactions(n)
    
    resolver = TransactionConflictResolver()
    
    print("Running benchmark...")
    start = time.perf_counter()
    results = resolver.process_transactions(txns)
    elapsed = time.perf_counter() - start
    
    print(f"\nResults:")
    print(f"  Processed: {n} transactions")
    print(f"  Accepted:  {len(results)}")
    print(f"  Rejected:  {n - len(results)}")
    print(f"  Time:      {elapsed:.3f} seconds")
    
    stats = resolver.get_stats()
    print(f"\nSide Effects:")
    print(f"  Audit entries: {stats['audit_entries']}")
    print(f"  Hashes:        {stats['total_processed']}")
    print(f"  Cache entries: {stats['cache_size']}")


if __name__ == "__main__":
    run_benchmark()
