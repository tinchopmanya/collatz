from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


StepFunction = Callable[[int], int]


@dataclass(frozen=True)
class CollatzMetrics:
    n: int
    total_steps: int
    stopping_time: int | None
    max_value: int
    odd_steps: int
    even_steps: int
    parity_prefix: str
    reached_one: bool
    terminal_value: int


@dataclass(frozen=True)
class AlternatingBlock:
    n: int
    tail_length: int
    odd_factor: int
    alternating_length: int
    exit_even: int
    exit_v2: int
    next_odd: int
    block_peak: int
    block_steps_to_next_odd: int


def _require_positive_integer(n: int) -> None:
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 1:
        raise ValueError("n must be a positive integer")


def two_adic_valuation(n: int) -> int:
    """Return v2(n), the exponent of the largest power of 2 dividing n."""
    _require_positive_integer(n)

    exponent = 0
    current = n
    while current % 2 == 0:
        exponent += 1
        current //= 2
    return exponent


def mersenne_tail_length(n: int) -> int:
    """Return the length of the trailing run of ones in an odd positive integer."""
    _require_positive_integer(n)
    if n % 2 == 0:
        raise ValueError("n must be odd")
    return two_adic_valuation(n + 1)


def odd_alternating_prefix_len(n: int) -> int:
    """Return the exact initial odd/even alternating prefix length for odd n."""
    return 2 * mersenne_tail_length(n)


def alternating_block(n: int) -> AlternatingBlock:
    """Return the exact first alternating block decomposition for odd n."""
    _require_positive_integer(n)
    if n % 2 == 0:
        raise ValueError("n must be odd")

    tail_length = mersenne_tail_length(n)
    odd_factor = (n + 1) >> tail_length
    exit_even = (3**tail_length) * odd_factor - 1
    exit_v2 = two_adic_valuation(exit_even)
    next_odd = exit_even >> exit_v2
    block_peak = 2 * exit_even

    return AlternatingBlock(
        n=n,
        tail_length=tail_length,
        odd_factor=odd_factor,
        alternating_length=2 * tail_length,
        exit_even=exit_even,
        exit_v2=exit_v2,
        next_odd=next_odd,
        block_peak=block_peak,
        block_steps_to_next_odd=2 * tail_length + exit_v2,
    )


def classic_step(n: int) -> int:
    """Return the standard Collatz step for a positive integer."""
    _require_positive_integer(n)
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


def accelerated_step(n: int) -> int:
    """Return the common accelerated step T(n)."""
    _require_positive_integer(n)
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


def orbit(
    n: int,
    *,
    step: StepFunction = classic_step,
    stop_at: int = 1,
    max_steps: int = 100_000,
) -> list[int]:
    """Return the orbit from n until stop_at is reached or max_steps is exceeded."""
    _require_positive_integer(n)
    _require_positive_integer(stop_at)
    if max_steps < 0:
        raise ValueError("max_steps must be non-negative")

    values = [n]
    current = n
    for _ in range(max_steps):
        if current == stop_at:
            return values
        current = step(current)
        values.append(current)

    if current == stop_at:
        return values
    raise RuntimeError(f"orbit did not reach {stop_at} within {max_steps} steps")


def compute_metrics(
    n: int,
    *,
    step: StepFunction = classic_step,
    max_steps: int = 100_000,
    parity_prefix_len: int = 128,
) -> CollatzMetrics:
    """Compute basic orbit metrics for one starting value."""
    _require_positive_integer(n)
    if max_steps < 0:
        raise ValueError("max_steps must be non-negative")
    if parity_prefix_len < 0:
        raise ValueError("parity_prefix_len must be non-negative")

    current = n
    max_value = n
    odd_steps = 0
    even_steps = 0
    stopping_time: int | None = None
    parity_bits: list[str] = []

    for step_index in range(max_steps):
        if current == 1:
            return CollatzMetrics(
                n=n,
                total_steps=step_index,
                stopping_time=stopping_time,
                max_value=max_value,
                odd_steps=odd_steps,
                even_steps=even_steps,
                parity_prefix="".join(parity_bits),
                reached_one=True,
                terminal_value=current,
            )

        if len(parity_bits) < parity_prefix_len:
            parity_bits.append("1" if current % 2 else "0")

        if current % 2:
            odd_steps += 1
        else:
            even_steps += 1

        current = step(current)
        if current > max_value:
            max_value = current
        if stopping_time is None and current < n:
            stopping_time = step_index + 1

    return CollatzMetrics(
        n=n,
        total_steps=max_steps,
        stopping_time=stopping_time,
        max_value=max_value,
        odd_steps=odd_steps,
        even_steps=even_steps,
        parity_prefix="".join(parity_bits),
        reached_one=current == 1,
        terminal_value=current,
    )
