# M19 rewriting challenge files

Date: 2026-04-27

These files materialize the two explicit S-system challenges from Yolcu-Aaronson-Heule in the ASCII alphabet used by `rewriting-collatz`.

## Symbol Map

| ASCII | Paper symbol |
| --- | --- |
| `a` | `f` |
| `b` | `t` |
| `c` | `left marker` |
| `d` | `end marker` |
| `e` | `0` |
| `f` | `1` |
| `g` | `2` |

## Generated Files

| Challenge | Prover SRS | TPDB | AProVE SRS | Removed rule | Meaning |
| --- | --- | --- | --- | --- | --- |
| `S_full` | `m19_collatz_S_full.srs` | `m19_collatz_S_full.tpdb` | `m19_collatz_S_full.aprove.srs` | `none` | full S |
| `S1_without_ff_end_to_0_end` | `m19_collatz_S1_without_ff_end_to_0_end.srs` | `m19_collatz_S1_without_ff_end_to_0_end.tpdb` | `m19_collatz_S1_without_ff_end_to_0_end.aprove.srs` | `aad -> ed` | ff* -> 0* |
| `S2_without_tf_end_to_end` | `m19_collatz_S2_without_tf_end_to_end.srs` | `m19_collatz_S2_without_tf_end_to_end.tpdb` | `m19_collatz_S2_without_tf_end_to_end.aprove.srs` | `bad -> d` | tf* -> * |

## Rule Inventory

| ASCII rule | Paper meaning | Role |
| --- | --- | --- |
| `aad -> ed` | ff* -> 0* | dynamic S, residue 1 mod 8 |
| `bad -> d` | tf* -> * | dynamic S, residue 5 mod 8 |
| `bd -> gd` | t* -> 2* | dynamic S, residue 3 mod 4 |
| `ae -> ea` | f0 -> 0f | auxiliary A |
| `af -> eb` | f1 -> 0t | auxiliary A |
| `ag -> fa` | f2 -> 1f | auxiliary A |
| `be -> fb` | t0 -> 1t | auxiliary A |
| `bf -> ga` | t1 -> 2f | auxiliary A |
| `bg -> gb` | t2 -> 2t | auxiliary A |
| `ce -> cb` | left 0 -> left t | auxiliary B |
| `cf -> caa` | left 1 -> left ff | auxiliary B |
| `cg -> cab` | left 2 -> left ft | auxiliary B |

## Research Status

- These files do not prove termination.
- They only make the two published open challenges concrete and reproducible.
- Next step: run established termination tools against the TPDB files before inventing custom search.
