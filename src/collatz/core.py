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


def _require_positive_integer(n: int) -> None:
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 1:
        raise ValueError("n must be a positive integer")


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
