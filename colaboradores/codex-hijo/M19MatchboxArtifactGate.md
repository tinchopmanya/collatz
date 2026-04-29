# M19 Matchbox artifact gate

Fecha: 2026-04-29
Agente: CodexHijo-M19MatchboxArtifactGate

## Objetivo

`scripts/m19_matchbox_artifact_gate.py` es una compuerta chica para auditar artefactos de build Matchbox M19. Su punto central es evitar que un workflow exitoso se interprete como "hay binario Matchbox probado" cuando solo produjo logs de entorno/build.

## Criterios que exige

- Directorio de artefacto existente.
- `m19-matchbox-sha256.txt` no vacio, con hash SHA-256 de 64 hex y nombre `matchbox`/`matchbox2015`.
- `m19-matchbox-ldd.txt` no vacio, sin `command not found`, `No such file` ni bibliotecas `not found`.
- `m19-matchbox-help.log` no vacio, sin errores de ejecucion, y con senales de salida `matchbox`/`usage`/`options`/`--help`.
- `m19-matchbox-build.log` no vacio y sin `Failed to build`, `cabal: Failed`, `command not found` ni `No such file or directory`.
- `environment.txt` con pinnings para `ghc_version`, `cabal_version`, `index_state` y `matchbox_ref`; rechaza valores sueltos como `latest`, `master`, `main` o `head`.
- `m19-boolector-source-rev.txt` con revision/version no suelta.
- `m19-boolector-version.txt` con version parseable.

## Uso

```bash
python scripts/m19_matchbox_artifact_gate.py \
  reports/m19_github_runs/artifacts/<run-id>/m19-matchbox-build-probe-ghc-8.10.7 \
  --json /tmp/m19_matchbox_artifact_gate.json
```

La salida termina en `m19_matchbox_artifact_gate=PASS` o `m19_matchbox_artifact_gate=FAIL`; el codigo de salida es `0` solo si todos los checks pasan.

## Caso que bloquea explicitamente

El gate falla si el workflow fue `success` pero no produjo evidencia del binario probado. En particular, no alcanza con `environment.txt`, `cabal.project.local`, logs de dry-run o un build log parcial: deben existir `m19-matchbox-sha256.txt`, `m19-matchbox-ldd.txt` y `m19-matchbox-help.log`.

## Verificacion hecha

- `python -m py_compile scripts\m19_matchbox_artifact_gate.py tests\test_m19_matchbox_artifact_gate.py`: OK.
- `python -m unittest tests.test_m19_matchbox_artifact_gate`: OK, 6 tests.
- Sanity check contra `reports/m19_github_runs/artifacts/25107937562/m19-matchbox-build-probe-ghc-8.10.7`: FAIL esperado por ausencia de `m19-matchbox-sha256.txt`, `m19-matchbox-ldd.txt`, `m19-matchbox-help.log` y presencia de `Failed to build`.

## Limites

- No compila Matchbox ni ejecuta desafios S1/S2; solo audita artefactos ya emitidos.
- No verifica que el hash corresponda a un archivo binario presente en el mismo directorio, porque el artefacto minimo pedido solo incluye el manifest `m19-matchbox-sha256.txt`.
- No modifica workflows ni reportes existentes.
