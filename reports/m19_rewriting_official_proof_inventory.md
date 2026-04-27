# M19 rewriting proof inventory

External repo: `rewriting-collatz@8a4dfda60f97a6d33ff0a24fdfa7a172d4bec340`

## Summary

- Proof runs declared in `proofs.sh`: 24
- Logs missing: 0
- Logs without SAT or QED: 0

## Largest CNFs

| Source | Variables | Clauses | SAT seconds |
| --- | ---: | ---: | ---: |
| `relative/farkas.srs` | 61145 | 401782 | 23.001 |
| `relative/collatz-T-3mod8.srs` | 21004 | 220377 | 0.26 |
| `relative/collatz-C-6mod8.srs` | 21025 | 186053 | 44.257 |
| `relative/collatz-T-1or7mod8.srs` | 11469 | 94483 | 0.066 |
| `relative/collatz-T-3mod4.srs` | 6386 | 44207 | 5.411 |

## Full Inventory

| Source | Log | Args | SAT | QED | Variables | Clauses |
| --- | --- | --- | --- | --- | ---: | ---: |
| `relative/zantema.srs` | `zantema.log` | `-i natural -d 2 -rw 4` | True | True | 1446 | 8537 |
| `relative/farkas.srs` | `farkas.log` | `-i arctic  -d 5 -rw 8` | True | True | 61145 | 401782 |
| `relative/collatz-T-01.srs` | `collatz-T-01.log` | `-i natural -d 3 -rw 4 -any` | True | True | 4224 | 25867 |
| `relative/collatz-T-02.srs` | `collatz-T-02.log` | `-i natural -d 1 -rw 2 -any` | True | True | 77 | 267 |
| `relative/collatz-T-03.srs` | `collatz-T-03.log` | `-i natural -d 4 -rw 2 -any` | True | True | 3023 | 12687 |
| `relative/collatz-T-04.srs` | `collatz-T-04.log` | `-i natural -d 1 -rw 3 -any` | True | True | 151 | 684 |
| `relative/collatz-T-05.srs` | `collatz-T-05.log` | `-i natural -d 1 -rw 2 -any` | True | True | 77 | 267 |
| `relative/collatz-T-06.srs` | `collatz-T-06.log` | `-i arctic  -d 3 -rw 4 -any` | True | True | 4035 | 17384 |
| `relative/collatz-T-07.srs` | `collatz-T-07.log` | `-i arctic  -d 4 -rw 3 -any` | True | True | 6043 | 22428 |
| `relative/collatz-T-08.srs` | `collatz-T-08.log` | `-i arctic  -d 2 -rw 5 -any` | True | True | 1771 | 8606 |
| `relative/collatz-T-09.srs` | `collatz-T-09.log` | `-i natural -d 2 -rw 2 -any` | True | True | 444 | 1745 |
| `relative/collatz-T-10.srs` | `collatz-T-10.log` | `-i natural -d 3 -rw 3 -any` | True | True | 2690 | 14191 |
| `relative/collatz-T-11.srs` | `collatz-T-11.log` | `-i arctic  -d 4 -rw 3 -any` | True | True | 6042 | 22388 |
| `relative/collatz-S-3mod4.srs` | `collatz-S-3mod4.log` | `-i natural -d 2 -rw 5` | True | True | 2088 | 13928 |
| `relative/collatz-C-0mod4.srs` | `collatz-C-0mod4.log` | `-i natural -d 3 -rw 4` | True | True | 4788 | 29510 |
| `relative/collatz-C-2mod4.srs` | `collatz-C-2mod4.log` | `-i natural -d 2 -rw 4` | True | True | 1566 | 9308 |
| `relative/collatz-T-1mod4.srs` | `collatz-T-1mod4.log` | `-i natural -d 2 -rw 4 -any` | True | True | 1568 | 9315 |
| `relative/collatz-T-3mod4.srs` | `collatz-T-3mod4.log` | `-i natural -d 3 -rw 5 -any` | True | True | 6386 | 44207 |
| `relative/collatz-C-2mod8.srs` | `collatz-C-2mod8.log` | `-i natural -d 3 -rw 4 -any` | True | True | 5737 | 35627 |
| `relative/collatz-C-4mod8.srs` | `collatz-C-4mod8.log` | `-i natural -d 3 -rw 4 -any` | True | True | 5926 | 36833 |
| `relative/collatz-C-6mod8.srs` | `collatz-C-6mod8.log` | `-i arctic  -d 3 -rw 12 -any` | True | True | 21025 | 186053 |
| `relative/collatz-T-3mod8.srs` | `collatz-T-3mod8.log` | `-i natural -d 3 -rw 11 -any` | True | True | 21004 | 220377 |
| `relative/collatz-T-1or5mod8.srs` | `collatz-T-1or5mod8.log` | `-i natural -d 2 -rw 4 -any` | True | True | 1809 | 10841 |
| `relative/collatz-T-1or7mod8.srs` | `collatz-T-1or7mod8.log` | `-i natural -d 3 -rw 7 -any` | True | True | 11469 | 94483 |
