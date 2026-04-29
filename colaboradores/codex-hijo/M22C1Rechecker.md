# M22-C1 rechecker independiente S2-k16

Fecha: 2026-04-29
Agente: CodexHijo-M22-C1-Rechecker
Rama/worktree: `codex-hijo/m22-c1-rechecker` en `C:\dev\vert\collatz-m22-c1-rechecker`

## Resumen

Se implemento un rechecker independiente para la ventana S2-k16. La logica central esta en:

```text
scripts/m22_c1_rechecker.py
```

El script no importa los scripts M21/M22 previos. Reimplementa directamente:

```text
T(n) = n/2       si n es par
T(n) = (3n+1)/2 si n es impar
T^k(r + a 2^k) = T^k(r) + 3^f a
```

La certificacion low-bit marca un residuo cuando `3^f < 2^k` y el prefijo de longitud `k` desciende en el residuo base. Para M22-C1 solo se congela la rama S2, es decir `r mod 8 = 5`.

## Comando ejecutado

```powershell
python -m py_compile scripts\m22_c1_rechecker.py tests\test_m22_c1_rechecker.py
python -m unittest tests.test_m22_c1_rechecker
python scripts\m22_c1_rechecker.py --k 16 --validation-power 20 --audit-max-power 24 --audit-residue-strata 32 --audit-residues-per-stratum 3 --audit-lifts-per-residue 3 --out-dir reports --prefix m22_c1_rechecker
```

## Artefactos

```text
reports/m22_c1_rechecker.csv
reports/m22_c1_rechecker.md
reports/m22_c1_rechecker.uncovered_residues.csv
reports/m22_c1_rechecker.certified_residues.csv
reports/m22_c1_rechecker.audit.csv
reports/m22_c1_rechecker.validation.csv
```

## Resultado numerico

| Campo | Valor |
| --- | ---: |
| `branch_residue_count` | `8192` |
| `lowbit_certified_count` | `7814` |
| `uncovered_count` | `378` |
| `uncovered_sha256` | `bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210` |
| `certified_sha256` | `0e8d2a804d7cc129a5fc6eec295250fd2a57786c25f2764e1bbd5100be01c7fa` |
| `false_positives` | `0` |
| `affine_failures` | `0` |
| `audit_sampled_numbers` | `576` |
| `max_lift_seen` | `255` |

La validacion exhaustiva cubrio `1 <= n < 2^20` para los residuos certificados de la rama S2-k16 y reviso `125024` candidatos. No se observaron falsos positivos.

La auditoria estratificada uso `32` estratos, `3` residuos por estrato y `3` lifts por residuo, con `576` numeros muestreados. No se observaron fallas del invariante afin.

## Alcance

Este resultado congela y revalida la data finita S2-k16. No es una prueba de Collatz ni una prueba de terminacion del sistema de reescritura. El uso sano es como insumo independiente para comparar o auditar un experimento guardado posterior sobre los `378` residuos no certificados.
