# M21 Angeltveit low-bit stratified audit

Deterministic second-layer audit for the low-bit certificate. It samples certified
and uncertified residue strata, then checks the affine invariant
`T^k(r + a 2^k) = T^k(r) + 3^f a` on low/mid/high lifts.

This raises reproducibility and catches implementation mistakes; it is not a new
Collatz proof and not a reproduction of the full Angeltveit GPU search.

| k | residue samples C/U | n samples | max lift | affine failures | certified false positives | uncertified sampled descents | min contraction slack | min descent slack |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 48/36 | 252 | 65535 | 0 | 0 | 10 | 13 | 1 |
| 10 | 48/48 | 288 | 16383 | 0 | 0 | 2 | 295 | 1 |
| 12 | 48/48 | 288 | 4095 | 0 | 0 | 2 | 1909 | 1 |
| 14 | 48/48 | 288 | 1023 | 0 | 0 | 2 | 9823 | 1 |
| 16 | 48/48 | 288 | 255 | 0 | 0 | 2 | 6487 | 1 |
| 18 | 48/48 | 288 | 63 | 0 | 0 | 2 | 84997 | 1 |
| 20 | 48/48 | 288 | 15 | 0 | 0 | 2 | 517135 | 1 |
