import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collatz import (  # noqa: E402
    accelerated_step,
    classic_step,
    compute_metrics,
    mersenne_tail_length,
    odd_alternating_prefix_len,
    orbit,
    two_adic_valuation,
)


def measured_alternating_prefix_len(n: int, max_len: int = 256) -> int:
    current = n
    expected = current % 2
    length = 0
    for _ in range(max_len):
        if current % 2 != expected:
            break
        length += 1
        current = classic_step(current)
        expected = 1 - expected
    return length


class CollatzCoreTests(unittest.TestCase):
    def test_classic_step(self) -> None:
        self.assertEqual(classic_step(1), 4)
        self.assertEqual(classic_step(2), 1)
        self.assertEqual(classic_step(3), 10)
        self.assertEqual(classic_step(10), 5)

    def test_accelerated_step(self) -> None:
        self.assertEqual(accelerated_step(1), 2)
        self.assertEqual(accelerated_step(2), 1)
        self.assertEqual(accelerated_step(3), 5)
        self.assertEqual(accelerated_step(10), 5)

    def test_orbit_for_27(self) -> None:
        values = orbit(27, max_steps=200)
        self.assertEqual(values[0], 27)
        self.assertEqual(values[-1], 1)
        self.assertEqual(len(values) - 1, 111)
        self.assertEqual(max(values), 9232)

    def test_metrics_for_known_values(self) -> None:
        one = compute_metrics(1)
        self.assertEqual(one.total_steps, 0)
        self.assertIsNone(one.stopping_time)
        self.assertEqual(one.max_value, 1)
        self.assertTrue(one.reached_one)

        three = compute_metrics(3)
        self.assertEqual(three.total_steps, 7)
        self.assertEqual(three.stopping_time, 6)
        self.assertEqual(three.max_value, 16)
        self.assertTrue(three.reached_one)

        twenty_seven = compute_metrics(27)
        self.assertEqual(twenty_seven.total_steps, 111)
        self.assertEqual(twenty_seven.stopping_time, 96)
        self.assertEqual(twenty_seven.max_value, 9232)
        self.assertTrue(twenty_seven.reached_one)

    def test_two_adic_and_mersenne_tail_lengths(self) -> None:
        self.assertEqual(two_adic_valuation(1), 0)
        self.assertEqual(two_adic_valuation(2), 1)
        self.assertEqual(two_adic_valuation(512), 9)
        self.assertEqual(mersenne_tail_length(7), 3)
        self.assertEqual(mersenne_tail_length(511), 9)
        self.assertEqual(odd_alternating_prefix_len(511), 18)

    def test_odd_alternating_prefix_formula(self) -> None:
        for n in range(1, 2_000, 2):
            self.assertEqual(
                measured_alternating_prefix_len(n),
                odd_alternating_prefix_len(n),
                msg=f"n={n}",
            )

    def test_rejects_invalid_inputs(self) -> None:
        for value in (0, -1):
            with self.assertRaises(ValueError):
                classic_step(value)
            with self.assertRaises(ValueError):
                compute_metrics(value)

        with self.assertRaises(TypeError):
            classic_step(1.5)  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            mersenne_tail_length(2)


if __name__ == "__main__":
    unittest.main()
