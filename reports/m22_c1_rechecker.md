# M22-C1 independent S2-k16 rechecker

This artifact recomputes the S2 low-bit complement from first principles in
`scripts/m22_c1_rechecker.py`. The central logic does not import earlier M21/M22
scripts; earlier artifacts are useful only as external comparison material.

| Field | Value |
| --- | ---: |
| `k` | `16` |
| `modulus` | `65536` |
| `branch_residue_count` | `8192` |
| `lowbit_certified_count` | `7814` |
| `uncovered_count` | `378` |
| `certified_fraction` | `0.953857421875` |
| `uncovered_fraction` | `0.046142578125` |
| `lsb_first_trie_nodes` | `1473` |
| `msb_first_trie_nodes` | `3294` |

- Uncovered SHA-256: `bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210`
- Certified SHA-256: `0e8d2a804d7cc129a5fc6eec295250fd2a57786c25f2764e1bbd5100be01c7fa`
- Exhaustive validation: `1 <= n < 1048576`, `checked_candidates = 125024`, `false_positives = 0`.
- Stratified audit: `sampled_numbers = 576`, `affine_failures = 0`, `max_lift_seen = 255`.

Interpretation:

- The rechecker verifies the finite S2-k16 data slice; it is not a proof of Collatz.
- Certified residues are discharged by the low-bit descent condition `T^k(r + a 2^k) = T^k(r) + 3^f a`, with `3^f < 2^k` and descent at `r`.
- Uncovered residues are the remaining S2 branch residues to keep for any guarded rewriting experiment.
