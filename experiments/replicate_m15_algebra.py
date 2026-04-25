from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_CSV = ROOT / "reports" / "m15_algebra_replica_summary.csv"
REPORT_MD = ROOT / "colaboradores" / "codex-hijo" / "ReplicaM15Algebra.md"

MAX_TAIL = 8
Q_MOD8_CLASSES = (1, 3, 5, 7)
Q_MOD4_CLASSES = (1, 3)
ODD_S_WEIGHT = Fraction(2, 3)
EVEN_S_WEIGHT = Fraction(1, 3)


def frac_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def frac_decimal(value: Fraction) -> str:
    return f"{float(value):.12f}"


def empty_distribution() -> dict[int | str, Fraction]:
    return {tail: Fraction(0) for tail in range(1, MAX_TAIL + 1)} | {
        f">{MAX_TAIL}": Fraction(0)
    }


def geometric_distribution() -> dict[int | str, Fraction]:
    probs = empty_distribution()
    for tail in range(1, MAX_TAIL + 1):
        probs[tail] = Fraction(1, 2**tail)
    probs[f">{MAX_TAIL}"] = Fraction(1, 2**MAX_TAIL)
    return probs


def source_distribution(a_mod8: int) -> dict[int | str, Fraction]:
    """Distribution of v2(odd_part(a - 1) + 1) for a fixed odd a mod 8.

    Here a = 3^s q. The enumeration is over 2-adic cylinders, not over
    observed Collatz orbits.
    """

    probs = empty_distribution()

    if a_mod8 == 3:
        # a = 3 mod 8 => odd_part(a - 1) = 1 mod 4.
        probs[1] = Fraction(1)
        return probs

    if a_mod8 in (1, 5):
        # a = 5 mod 8 fixes exit_v2 = 2; a = 1 mod 8 splits over
        # exit_v2 >= 3. In both cases the resulting odd part is uniform
        # among odd 2-adics, so next_tail is geometric.
        return geometric_distribution()

    if a_mod8 == 7:
        # a = 7 mod 8 => odd_part(a - 1) = 3 mod 4, so next_tail is at
        # least 2, with the geometric law conditioned on >= 2.
        for tail in range(2, MAX_TAIL + 1):
            probs[tail] = Fraction(1, 2 ** (tail - 1))
        probs[f">{MAX_TAIL}"] = Fraction(1, 2 ** (MAX_TAIL - 1))
        return probs

    raise ValueError(f"a_mod8 must be odd modulo 8, got {a_mod8}")


def mix_distributions(
    weighted: list[tuple[Fraction, dict[int | str, Fraction]]],
) -> dict[int | str, Fraction]:
    probs = empty_distribution()
    for weight, distribution in weighted:
        for tail, probability in distribution.items():
            probs[tail] += weight * probability
    return probs


def distribution_for_q_mod8(q_mod8: int) -> dict[int | str, Fraction]:
    # 3^s mod 8 is 3 for odd s and 1 for even s. For odd n sampled
    # 2-adically, P(s odd) = 2/3 and P(s even) = 1/3.
    odd_source = (3 * q_mod8) % 8
    even_source = q_mod8 % 8
    return mix_distributions(
        [
            (ODD_S_WEIGHT, source_distribution(odd_source)),
            (EVEN_S_WEIGHT, source_distribution(even_source)),
        ]
    )


def distribution_for_q_mod4(q_mod4: int) -> dict[int | str, Fraction]:
    residues = [q_mod4, q_mod4 + 4]
    return mix_distributions(
        [(Fraction(1, len(residues)), distribution_for_q_mod8(r)) for r in residues]
    )


def write_summary_csv() -> None:
    geometric = geometric_distribution()
    rows: list[dict[str, str]] = []

    for q_mod4 in Q_MOD4_CLASSES:
        dist = distribution_for_q_mod4(q_mod4)
        for tail, probability in dist.items():
            rows.append(
                {
                    "conditioning": "q_mod4",
                    "class": str(q_mod4),
                    "next_tail": str(tail),
                    "probability": frac_text(probability),
                    "probability_decimal": frac_decimal(probability),
                    "geometric_probability": frac_text(geometric[tail]),
                    "delta_vs_geometric": frac_text(probability - geometric[tail]),
                }
            )

    for q_mod8 in Q_MOD8_CLASSES:
        dist = distribution_for_q_mod8(q_mod8)
        for tail, probability in dist.items():
            rows.append(
                {
                    "conditioning": "q_mod8",
                    "class": str(q_mod8),
                    "next_tail": str(tail),
                    "probability": frac_text(probability),
                    "probability_decimal": frac_decimal(probability),
                    "geometric_probability": frac_text(geometric[tail]),
                    "delta_vs_geometric": frac_text(probability - geometric[tail]),
                }
            )

    SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "conditioning",
                "class",
                "next_tail",
                "probability",
                "probability_decimal",
                "geometric_probability",
                "delta_vs_geometric",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def q_mod8_formula_tail_ge_2(q_mod8: int) -> str:
    factors = {
        1: "1/3 * 2^-t",
        3: "2/3 * 2^-t",
        5: "5/3 * 2^-t",
        7: "4/3 * 2^-t",
    }
    return factors[q_mod8]


def write_report() -> None:
    geometric = geometric_distribution()

    source_rows = []
    for source in Q_MOD8_CLASSES:
        dist = source_distribution(source)
        source_rows.append(
            f"| `{source}` | `{frac_text(dist[1])}` | `{frac_text(geometric[1])}` |"
        )

    q4_rows = []
    for q_mod4 in Q_MOD4_CLASSES:
        dist = distribution_for_q_mod4(q_mod4)
        q4_rows.append(
            f"| `{q_mod4}` | `{frac_text(dist[1])}` | `{frac_text(dist[2])}` | "
            f"`si` |"
        )

    q8_rows = []
    for q_mod8 in Q_MOD8_CLASSES:
        dist = distribution_for_q_mod8(q_mod8)
        q8_rows.append(
            f"| `{q_mod8}` | `{frac_text(dist[1])}` | "
            f"`{q_mod8_formula_tail_ge_2(q_mod8)}` |"
        )

    report = f"""# Replica M15 algebra

Fecha: 2026-04-25
Rama: `codex-hijo/m15-algebra-replica`

## Alcance

Replica independiente del calculo teorico de `P(next_tail | q mod 8)`.

No usa holdout, no usa rangos de datos, no busca variables nuevas y no afirma
ninguna prueba de Collatz.

Definiciones usadas:

```text
n = 2^s q - 1, con s = tail = v2(n + 1) y q impar
a = 3^s q
exit_v2 = v2(a - 1)
next_odd = (a - 1) / 2^exit_v2
next_tail = v2(next_odd + 1)
```

## Metodo

Para un impar `n` uniforme en sentido 2-adico:

```text
P(s = k) = 2^-k, k >= 1
P(s impar) = 2/3
P(s par) = 1/3
```

Condicionado por `q mod 8 = r`, la clase fuente
`a = 3^s q mod 8` es:

```text
s impar: a = 3r mod 8
s par:   a = r mod 8
```

Luego se enumera la clase fuente `a mod 8`:

| `a mod 8` | `P(next_tail = 1)` | geometrica |
| ---: | ---: | ---: |
{chr(10).join(source_rows)}

Detalles:

- `a = 3 mod 8`: `exit_v2 = 1` y el odd part es `1 mod 4`, entonces `next_tail = 1` siempre.
- `a = 7 mod 8`: `exit_v2 = 1` y el odd part es `3 mod 4`, entonces `next_tail = 1` nunca.
- `a = 5 mod 8`: `exit_v2 = 2`; el odd part queda uniforme impar, por eso la ley es geometrica.
- `a = 1 mod 8`: se suma sobre `exit_v2 >= 3`; condicionado por cada salida exacta, el odd part queda uniforme impar, por eso la ley vuelve a ser geometrica.

## Resultado por `q mod 4`

Agrupar modulo 4 promedia las dos clases modulo 8 y cancela el sesgo.

| `q mod 4` | `P(next_tail = 1)` | `P(next_tail = 2)` | coincide con geometrica |
| ---: | ---: | ---: | :---: |
{chr(10).join(q4_rows)}

Conclusion: si, `q mod 4` coincide con la ley geometrica
`P(next_tail = t) = 2^-t`.

## Resultado por `q mod 8`

| `q mod 8` | `P(next_tail = 1)` | para `t >= 2` |
| ---: | ---: | ---: |
{chr(10).join(q8_rows)}

En particular:

```text
q = 1 mod 8 -> P(next_tail = 1) = 5/6
q = 3 mod 8 -> P(next_tail = 1) = 2/3
q = 5 mod 8 -> P(next_tail = 1) = 1/6
q = 7 mod 8 -> P(next_tail = 1) = 1/3
```

Las cuatro predicciones son correctas bajo este modelo 2-adico local.

## Interpretacion

`q mod 8` no coincide con la geometrica clase por clase. La desviacion no
requiere datos: sale de que `3^s mod 8` depende de la paridad de `s`, y esa
paridad no pesa `1/2`-`1/2`, sino `2/3`-`1/3`.

`q mod 4` si coincide con la geometrica porque mezcla pares de clases modulo 8:

```text
q = 1 mod 4: promedio de 5/6 y 1/6 = 1/2
q = 3 mod 4: promedio de 2/3 y 1/3 = 1/2
```

El CSV derivado esta en:

```text
reports/m15_algebra_replica_summary.csv
```

## Comparacion con Codex hijo 1

Despues de cerrar esta replica, inspeccione:

```text
origin/codex-hijo/m15-algebra:experiments/analyze_m15_algebra.py
origin/codex-hijo/m15-algebra:colaboradores/codex-hijo/ResultadosM15Algebra.md
origin/codex-hijo/m15-algebra:reports/m15_algebra_summary.csv
```

Coincidencias:

- `q mod 4`: Codex hijo 1 reporta `K = 2`, `classes_deviating_from_geometric = 0 / 2`. Esta replica obtiene ley geometrica exacta para las dos clases.
- `q mod 8`: Codex hijo 1 reporta desviacion en `4 / 4` clases, con maximo `1/3` en residuo `1`, `next_tail = 1`. Esta replica obtiene la misma tabla baja:

```text
q = 1 mod 8 -> P(next_tail = 1) = 5/6
q = 3 mod 8 -> P(next_tail = 1) = 2/3
q = 5 mod 8 -> P(next_tail = 1) = 1/6
q = 7 mod 8 -> P(next_tail = 1) = 1/3
```

No encontre discrepancia en el resultado `q mod 8`. La diferencia es de
alcance: Codex hijo 1 tambien explora refinamientos `q mod 16..64` y
`n mod 2^K`; esta replica se limita al calculo pedido para `q mod 4` y
`q mod 8`.
"""

    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text(report, encoding="utf-8")


def main() -> None:
    write_summary_csv()
    write_report()


if __name__ == "__main__":
    main()
