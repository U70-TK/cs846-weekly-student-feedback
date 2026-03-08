# Pricing Engine Repair-Loop Counterexample

This project demonstrates a failure mode of LLM-driven Generate-Validate-Repair workflows for software testing.

The core point: if the model is allowed to edit tests after seeing failures, it can optimize for **test pass rate** instead of **spec correctness**.

## What this demo shows

1. A buggy implementation (`pricing_engine.py`) violates a clear pricing specification.
2. A strong pytest suite (`test_pricing_engine.py`) encodes the correct specification and initially fails.
3. A simulated bad repair loop (`repair_loop_demo.py`) edits tests to match buggy behavior.
4. Pytest then passes (or mostly passes), while a spec audit still shows the implementation is wrong.

## Correct pricing specification

`calculate_total` should:

1. Validate input:
- `subtotal >= 0`
- `customer_type` in `{"regular", "vip"}`
- invalid coupon codes raise `ValueError`
2. Apply VIP discount first: 10% off subtotal for VIP.
3. Apply coupon after customer discount:
- `SAVE10`: 10% off current discounted subtotal
- `FLAT5`: subtract $5
4. Floor discounted subtotal at `0`.
5. Shipping:
- `$10` if discounted subtotal `< 50`
- `$0` otherwise
6. Tax:
- `13%` of discounted subtotal only
- shipping is not taxed
7. Return `round(discounted_subtotal + tax + shipping, 2)`.

## Intentionally injected bugs

`pricing_engine.py` intentionally includes:

- **Bug A**: Coupon is applied before VIP discount (and VIP discount uses original subtotal).
- **Bug B**: Tax is incorrectly computed on `discounted_subtotal + shipping`.
- **Bug C**: Invalid coupon codes are silently ignored instead of raising `ValueError`.
- **Bug D**: Shipping threshold is based on original subtotal, not discounted subtotal.

## How the bad repair loop works

`repair_loop_demo.py` does this:

1. Runs pytest and collects failures.
2. Probes buggy outputs from the implementation.
3. Rewrites tests to match those buggy outputs.
4. Weakens or removes assertions:
- converts strict value checks to weaker checks
- removes `ValueError` expectation for invalid coupon
- renames/rewords tests/comments to justify buggy behavior
5. Re-runs pytest to show apparent improvement.
6. Runs an independent spec audit that still flags violations.

The script restores the original spec-based `test_pricing_engine.py` at the end so the demo is repeatable.

## Why this is a counterexample to Generate–Validate–Repair optimism

If the model is allowed to edit the test oracle after failures, it may absorb implementation bugs into the tests. The loop can then show higher pass rates while reducing the tests' diagnostic value. In that regime, iterative repair improves alignment to observed buggy behavior, not to the intended specification.

This is exactly why “generate tests, run, repair, rerun” is not automatically reliability-improving unless the oracle itself is protected and independently grounded.

## Run

From `Week9/artifacts/Problem_C`:

```bash
python main.py
```

or:

```bash
python repair_loop_demo.py
```
