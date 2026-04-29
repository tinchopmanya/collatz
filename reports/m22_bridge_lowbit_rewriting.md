# M22 low-bit to rewriting branch bridge

This prototype measures whether M21 low-bit descent certificates can act as a
preprocessor for the M19/Yolcu-Aaronson-Heule dynamic S branches. It does not
generate a sound guarded SRS yet; it quantifies the residue slices that such a
guarded benchmark would need to keep after low-bit discharge.

| k | Branch | Removed rule | Predicate | Certified | Uncovered | Certified fraction |
| ---: | --- | --- | --- | ---: | ---: | ---: |
| 8 | `S1_without_ff_end_to_0_end` | `aad -> ed` | `mod8_eq_1` | 23/32 | 9 | 0.718750000000 |
| 8 | `S2_without_tf_end_to_end` | `bad -> d` | `mod8_eq_5` | 31/32 | 1 | 0.968750000000 |
| 8 | `S3_without_t_end_to_2_end` | `bd -> gd` | `mod4_eq_3` | 40/64 | 24 | 0.625000000000 |
| 10 | `S1_without_ff_end_to_0_end` | `aad -> ed` | `mod8_eq_1` | 98/128 | 30 | 0.765625000000 |
| 10 | `S2_without_tf_end_to_end` | `bad -> d` | `mod8_eq_5` | 120/128 | 8 | 0.937500000000 |
| 10 | `S3_without_t_end_to_2_end` | `bd -> gd` | `mod4_eq_3` | 163/256 | 93 | 0.636718750000 |
| 12 | `S1_without_ff_end_to_0_end` | `aad -> ed` | `mod8_eq_1` | 381/512 | 131 | 0.744140625000 |
| 12 | `S2_without_tf_end_to_end` | `bad -> d` | `mod8_eq_5` | 466/512 | 46 | 0.910156250000 |
| 12 | `S3_without_t_end_to_2_end` | `bd -> gd` | `mod4_eq_3` | 638/1024 | 386 | 0.623046875000 |
| 14 | `S1_without_ff_end_to_0_end` | `aad -> ed` | `mod8_eq_1` | 1485/2048 | 563 | 0.725097656250 |
| 14 | `S2_without_tf_end_to_end` | `bad -> d` | `mod8_eq_5` | 1816/2048 | 232 | 0.886718750000 |
| 14 | `S3_without_t_end_to_2_end` | `bd -> gd` | `mod4_eq_3` | 2510/4096 | 1586 | 0.612792968750 |
| 16 | `S1_without_ff_end_to_0_end` | `aad -> ed` | `mod8_eq_1` | 7098/8192 | 1094 | 0.866455078125 |
| 16 | `S2_without_tf_end_to_end` | `bad -> d` | `mod8_eq_5` | 7814/8192 | 378 | 0.953857421875 |
| 16 | `S3_without_t_end_to_2_end` | `bd -> gd` | `mod4_eq_3` | 12911/16384 | 3473 | 0.788024902344 |
| 18 | `S1_without_ff_end_to_0_end` | `aad -> ed` | `mod8_eq_1` | 27823/32768 | 4945 | 0.849090576172 |
| 18 | `S2_without_tf_end_to_end` | `bad -> d` | `mod8_eq_5` | 30827/32768 | 1941 | 0.940765380859 |
| 18 | `S3_without_t_end_to_2_end` | `bd -> gd` | `mod4_eq_3` | 50643/65536 | 14893 | 0.772750854492 |
| 20 | `S1_without_ff_end_to_0_end` | `aad -> ed` | `mod8_eq_1` | 109293/131072 | 21779 | 0.833839416504 |
| 20 | `S2_without_tf_end_to_end` | `bad -> d` | `mod8_eq_5` | 121670/131072 | 9402 | 0.928268432617 |
| 20 | `S3_without_t_end_to_2_end` | `bd -> gd` | `mod4_eq_3` | 199140/262144 | 63004 | 0.759658813477 |

Interpretation:

- `S1` corresponds to the dynamic branch `aad -> ed` / `ff* -> 0*`, tagged in M19 as residue `1 mod 8`.
- `S2` corresponds to `bad -> d` / `tf* -> *`, tagged as residue `5 mod 8`.
- `S3` is the natural third dynamic branch `bd -> gd` / `t* -> 2*`, tagged as residue `3 mod 4`.
- A guarded rewriting benchmark would need an independently checked translation from binary low-bit guards to the mixed binary/ternary SRS alphabet before any termination result is claimed.
