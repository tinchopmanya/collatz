# M19 certification gate

Fecha: 2026-04-29
Agente: CodexHijo-M19CertificationGate

## Objetivo

`scripts/m19_certificate_gate.py` es una compuerta chica para no confundir una corrida prometedora con una certificacion CPF/CeTA. No busca que AProVE, Matchbox o TTT2 encuentren `YES`; valida artefactos ya producidos por una corrida externa.

## Criterios que exige

- `YES` top-level: la primera linea no vacia de `--prover-output` debe ser exactamente `YES`.
- CPF presente: `--cpf` debe ser un archivo separado, no vacio, y contener raiz `certificationProblem`.
- CeTA certificado: `--ceta-log` debe contener una linea `CERTIFIED` y no debe contener marcadores de rechazo.
- Identidad reproducible: calcula SHA-256 de TRS, CPF, salida del prover, log CeTA y, si se pasa, binario/JAR del prover.
- Manifest opcional: si se pasa `--sha256sums`, cada hash listado para los artefactos existentes debe coincidir.

## Uso esperado

```bash
python scripts/m19_certificate_gate.py \
  --trs reports/m19_rewriting_challenges/m19_collatz_S1_without_ff_end_to_0_end.aprove.srs \
  --prover-output /tmp/m19_s1_aprove_cpf.out \
  --cpf /tmp/m19_s1_aprove.cpf \
  --ceta-log /tmp/m19_s1_ceta.log \
  --prover-binary tools/aprove/aprove.jar \
  --sha256sums /tmp/m19_s1_SHA256SUMS \
  --json /tmp/m19_s1_certificate_gate.json
```

La salida termina en `m19_certificate_gate=PASS` o `m19_certificate_gate=FAIL` y el codigo de salida es `0` solo si todos los checks pasan.

## Que rechaza explicitamente

- Logs internos donde aparece `YES` en una linea posterior pero no como veredicto top-level.
- Corridas con `CERTIFIED` textual pero sin CPF separado.
- CPF embebido usado como si fuera la misma salida top-level del prover.
- `MAYBE`, `TIMEOUT`, `ERROR`, `KILLED` o cualquier primera linea distinta de `YES`.
- Manifiestos SHA-256 incompletos o con mismatch para archivos listados.

## Limites

- No prueba terminacion por si misma; solo valida la forma minima de una certificacion externa.
- No invoca AProVE, Matchbox, TTT2 ni CeTA.
- No valida todo el esquema CPF; delega esa semantica a CeTA y solo comprueba la raiz `certificationProblem`.
- El manifest SHA-256 es opcional para permitir uso exploratorio, pero en CI deberia ser obligatorio.

## Integracion posterior en CI

1. Job productor: ejecutar el prover con flags CPF, separar `YES` y CPF, correr `ceta proof.cpf`, y generar `SHA256SUMS`.
2. Job gate: correr `python scripts/m19_certificate_gate.py ... --sha256sums SHA256SUMS --json gate.json`.
3. Publicar como artifacts: TRS, salida completa del prover, CPF, log CeTA, `SHA256SUMS`, `gate.json` y version/hash del prover.
4. Politica recomendada: el job puede ser manual o nightly, pero cualquier afirmacion de "M19 certificado" debe requerir que este gate pase.
