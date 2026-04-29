# M19 AProVE environment probe

## Environment

- Platform: `Linux-6.17.0-1010-azure-x86_64-with-glibc2.39`
- Python: `3.12.3 (main, Mar  3 2026, 12:15:18) [GCC 13.3.0]`
- CPU count: `4`
- Total memory MB: `15989`
- JAVA_TOOL_OPTIONS: `-Xmx6g`

## Tool Probe

| Tool check | Found | Path | Return | First output |
| --- | --- | --- | ---: | --- |
| `java_version` | yes | `/opt/hostedtoolcache/Java_Temurin-Hotspot_jdk/21.0.10-7/x64/bin/java` | `0` | `Picked up JAVA_TOOL_OPTIONS: -Xmx6g` |
| `yices_version` | yes | `/usr/local/bin/yices` | `0` | `Yices 2.6.4` |
| `yices_e_empty_stdin` | yes | `/usr/local/bin/yices` | `0` | `` |
| `minisat2_help` | yes | `/usr/local/bin/minisat2` | `1` | `ERROR! Unknown flag "help". Use '--help' for help.` |
| `minisat_help` | yes | `/usr/bin/minisat` | `1` | `ERROR! Unknown flag "help". Use '--help' for help.` |

## Derived Environment Classification

- `yices -e` supported: yes
- `minisat2` on PATH: yes
- `minisat` on PATH: yes

## SRS Inputs

| File | `.srs` suffix | Starts `(RULES` | Rule count |
| --- | --- | --- | ---: |
| `m19_collatz_S1_without_ff_end_to_0_end.aprove.srs` | yes | yes | 11 |
| `m19_collatz_S2_without_tf_end_to_end.aprove.srs` | yes | yes | 11 |

## AProVE Runs

| Challenge | Status | Return | Seconds | First output | Log |
| --- | --- | ---: | ---: | --- | --- |
| `m19_collatz_S1_without_ff_end_to_0_end.aprove.srs` | `WST_KILLED` | `0` | 37.641 | `Picked up JAVA_TOOL_OPTIONS: -Xmx6g` | `/tmp/m19_aprove_environment_probe/logs/m19_collatz_S1_without_ff_end_to_0_end.aprove.aprove-probe.log` |
| `m19_collatz_S2_without_tf_end_to_end.aprove.srs` | `WST_KILLED` | `0` | 29.746 | `Picked up JAVA_TOOL_OPTIONS: -Xmx6g` | `/tmp/m19_aprove_environment_probe/logs/m19_collatz_S2_without_tf_end_to_end.aprove.aprove-probe.log` |

## Interpretation

- `ENV_*` statuses are environment blockers, not mathematical evidence.
- `WST_MAYBE`, `WST_TIMEOUT`, `WST_KILLED`, or `WALL_TIMEOUT` mean no proof was found in this run.
- Only `WST_YES` is a candidate proof signal, and it still needs log/certificate audit.
