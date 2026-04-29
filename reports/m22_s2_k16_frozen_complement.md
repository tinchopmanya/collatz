# M22a S2-k16 frozen complement

This freezes the M22 candidate complement for the S2 branch before any guarded
rewriting-system construction. It is a data artifact, not a proof.

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
- The LSB-first trie is the relevant first guess because the guard is low-bit driven.
- The next step is semantic, not computational: prove that a guard over these bitstrings really matches the mixed binary/ternary SRS branch.
