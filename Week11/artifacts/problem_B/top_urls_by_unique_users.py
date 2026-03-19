from __future__ import annotations

import random
import tempfile
import time
from collections import defaultdict
from pathlib import Path


def generate_log_file(path: Path, num_events: int = 2_000_000) -> None:
    rng = random.Random(42)
    urls = [f"/product/{i}" for i in range(5000)]

    with path.open("w", encoding="utf-8") as f:
        for _ in range(num_events):
            user_id = rng.randint(1, 400_000)
            url = urls[rng.randint(0, len(urls) - 1)]
            f.write(f"{user_id},{url}\n")


def top_urls_by_unique_users(path: Path, top_k: int = 100) -> list[tuple[str, int]]:
    # Intentionally memory-heavy baseline:
    # stores every distinct user_id for every URL.
    users_per_url: dict[str, set[int]] = defaultdict(set)

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            user_id_text, url = line.rstrip("\n").split(",", 1)
            users_per_url[url].add(int(user_id_text))

    counts = [(url, len(users)) for url, users in users_per_url.items()]
    counts.sort(key=lambda item: item[1], reverse=True)
    return counts[:top_k]


def main() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "events.csv"
        generate_log_file(path)

        start = time.perf_counter()
        result = top_urls_by_unique_users(path)
        elapsed = time.perf_counter() - start

        print(f"Computed top {len(result)} URLs in {elapsed:.3f}s")
        print(result[:5])


if __name__ == "__main__":
    main()
