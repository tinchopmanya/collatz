# M19 termination artifact audit

## Summary

- Bundle classification: `uncertified_logs_only`
- Candidate artifacts: 75
- Missing roots: 0
- Hash failures: 0

## Artifact Counts

| Type | Count |
| --- | ---: |
| `inventory_or_report` | 21 |
| `tool_log` | 54 |

## Highest-Signal Artifacts

| Artifact | Type | Tool | Status | CeTA | Hash | Signals |
| --- | --- | --- | --- | --- | --- | --- |
| `m19_github_runs/artifacts/25104952228/m19-rewriting-challenge-search-both/m19_challenge_grid.csv` | `inventory_or_report` | rewriting-collatz | ERROR |  | `missing_sidecar` | qed |
| `m19_github_runs/artifacts/25104952228/m19-rewriting-challenge-search-both/m19_challenge_grid.md` | `inventory_or_report` | rewriting-collatz |  |  | `missing_sidecar` | qed |
| `m19_github_runs/artifacts/25104952325/m19-aprove-challenge-search-both/logs/m19_collatz_S1_without_ff_end_to_0_end.aprove.aprove.log` | `tool_log` | aprove | KILLED |  | `missing_sidecar` | versioned |
| `m19_github_runs/artifacts/25104952325/m19-aprove-challenge-search-both/logs/m19_collatz_S2_without_tf_end_to_end.aprove.aprove.log` | `tool_log` | aprove | KILLED |  | `missing_sidecar` | versioned |
| `m19_github_runs/artifacts/25104952325/m19-aprove-challenge-search-both/m19_aprove_challenges.csv` | `inventory_or_report` | aprove | KILLED |  | `missing_sidecar` |  |
| `m19_github_runs/artifacts/25105347516/m19-aprove-environment-probe-both/logs/m19_collatz_S1_without_ff_end_to_0_end.aprove.aprove-probe.log` | `tool_log` | aprove | KILLED |  | `missing_sidecar` | versioned |
| `m19_github_runs/artifacts/25105347516/m19-aprove-environment-probe-both/logs/m19_collatz_S2_without_tf_end_to_end.aprove.aprove-probe.log` | `tool_log` | aprove | KILLED |  | `missing_sidecar` | versioned |
| `m19_github_runs/artifacts/25105375622/m19-matchbox-challenge-search-both/m19_matchbox_challenges.csv` | `inventory_or_report` | matchbox | ERROR |  | `missing_sidecar` | contains-sha256 |
| `m19_rewriting_official_proof_inventory.csv` | `inventory_or_report` | rewriting-collatz |  |  | `missing_sidecar` | qed |
| `m19_rewriting_official_proof_inventory.md` | `inventory_or_report` | rewriting-collatz |  |  | `missing_sidecar` | qed,sat |
| `m19_rewriting_zantema_inventory.csv` | `inventory_or_report` | rewriting-collatz |  |  | `missing_sidecar` | qed |
| `m19_rewriting_zantema_inventory.md` | `inventory_or_report` | rewriting-collatz |  |  | `missing_sidecar` | qed,sat |

## Evidence Ladder

- `certified_top_level`: CPF certificate plus a successful CeTA/certifier artifact was found.
- `cpf_present_unchecked_top_level`: CPF and a top-level `YES` exist, but no successful certifier run was found.
- `top_level_uncertified`: a tool reports top-level `YES`, but no CPF/CeTA evidence was found.
- `uncertified_logs_only`: logs or reports exist, but there is no top-level certified proof artifact.
- `no_artifacts`: no candidate evidence was found in the scanned roots.
