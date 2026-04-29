# M19 Matchbox route

Fecha: 2026-04-29
Responsable: CodexHijo-Matchbox
Scope: ruta reproducible para probar M19 S1/S2 con Matchbox, sin exigir build local inmediato.

## Resumen ejecutivo

Matchbox es una via razonable pero fragil para M19. La via no esta virgen en el area general: Matchbox existe desde hace anos como prover de terminacion para SRS/TRS y fue usado en Termination Competition. Lo que si parece poco explorado en este repo es la instancia exacta S1/S2 materializada en `reports/m19_rewriting_challenges/` con una corrida moderna, logs guardados y eventual CPF/CeTA.

El runner nuevo no intenta compilar Matchbox. Ejecuta un comando configurable sobre los `.tpdb` de S1/S2, guarda logs completos y solo promueve `YES`, `NO`, `MAYBE`, `TIMEOUT` o `ERROR` si aparece como primera linea no vacia exacta. Esto evita falsos positivos por `YES` internos de subobligaciones, trazas CPF, mensajes SAT o logs complejos.

## Fuentes y CLI esperado

La referencia publica vieja de `jwaldmann/matchbox` dice que el programa prueba terminacion de sistemas de reescritura, acepta entrada en sintaxis TPDB plain o XTC, y emite traza textual o CPF. Tambien enumera metodos como interpretaciones matriciales, dependency pairs y compresion, y solvers externos GLPK/minisat. Fuente: [README de Matchbox](https://github.com/jwaldmann/matchbox) y [README raw](https://raw.githubusercontent.com/jwaldmann/matchbox/master/README.md).

El `matchbox.cabal` historico declara el ejecutable `matchbox2015`, sugiere `matchbox --help`, y muestra el ejemplo `matchbox --cpf data/z002.srs | tail -n +2 | ceta /dev/stdin`. El `run.sh` historico usa comandos del estilo `matchbox2015 --satchmo --bits 4 archivo.srs` y lee la primera linea de salida como resultado. Fuente: [matchbox.cabal raw](https://raw.githubusercontent.com/jwaldmann/matchbox/master/matchbox.cabal) y [run.sh raw](https://raw.githubusercontent.com/jwaldmann/matchbox/master/run.sh).

El build no es trivial: el propio cabal viejo dice que `cabal install` necesita versiones actuales de librerias desde GitHub, no solo Hackage, y `build-all.sh` instala minisat bindings, GLPK/hmatrix, satchmo, haskell-tpdb, CO4 y otras dependencias. Por eso el workflow queda manual y conservador: primero acepta un binario por URL o cache; solo despues ofrece un build experimental no bloqueante. Fuente: [build-all.sh raw](https://raw.githubusercontent.com/jwaldmann/matchbox/master/build-all.sh).

## Formato TPDB/SRS de S1/S2

Los desafios locales ya estan generados en:

| Desafio | Archivo Matchbox recomendado | Lectura |
| --- | --- | --- |
| S1 | `reports/m19_rewriting_challenges/m19_collatz_S1_without_ff_end_to_0_end.tpdb` | S sin `ff* -> 0*` |
| S2 | `reports/m19_rewriting_challenges/m19_collatz_S2_without_tf_end_to_end.tpdb` | S sin `tf* -> *` |

El formato local es TPDB plain viejo:

```text
(RULES
  b a d -> d ,
  ...
)
```

La especificacion historica de TPDB/SRS acepta una seccion `RULES` con reglas `word -> word`, separadas por comas, y Matchbox declara soporte para TPDB plain/XTC. Fuente adicional: [formato TPDB/SRS historico](https://www.lri.fr/~marche/tpdb/format.pdf).

## Runner reproducible

Archivo creado: `scripts/m19_run_matchbox_challenges.py`.

Uso minimo con un binario ya disponible:

```bash
python scripts/m19_run_matchbox_challenges.py \
  --matchbox-command "matchbox2015" \
  --challenge-file reports/m19_rewriting_challenges/m19_collatz_S1_without_ff_end_to_0_end.tpdb \
  --challenge-file reports/m19_rewriting_challenges/m19_collatz_S2_without_tf_end_to_end.tpdb \
  --out-dir /tmp/m19_matchbox_challenges \
  --wall-timeout 180
```

Uso con argumentos historicos de portfolio:

```bash
python scripts/m19_run_matchbox_challenges.py \
  --matchbox-command "matchbox2015" \
  --matchbox-arg=--satchmo \
  --matchbox-arg=--bits \
  --matchbox-arg=4 \
  --challenge-file reports/m19_rewriting_challenges/m19_collatz_S1_without_ff_end_to_0_end.tpdb \
  --out-dir /tmp/m19_matchbox_challenges
```

Artefactos generados:

- `m19_matchbox_challenges.csv`
- `m19_matchbox_challenges.json`
- `m19_matchbox_challenges.md`
- `logs/*.matchbox.log`

Regla de clasificacion:

- `TIMEOUT` si vence el timeout externo, o codigos/senales tipicas de timeout.
- `YES/NO/MAYBE/ERROR` solo si la primera linea no vacia, despues de quitar ANSI, es exactamente uno de esos tokens.
- `ERROR` si no hay veredicto top-level pero aparecen errores fatales/parsing/excepciones o return code no cero.
- `MAYBE` si no hay veredicto top-level ni error claro. Esto es conservador: nunca convierte una aparicion interna de `YES` en prueba.

## Workflow

Archivo creado: `.github/workflows/m19-matchbox-challenge-search.yml`.

Es un workflow manual (`workflow_dispatch`) con estas rutas:

- `binary_archive_url`: ruta preferida si conseguimos un tar/zip con `matchbox2015` o `matchbox`; se agrega al `PATH` y se corre el runner.
- `experimental_build=false`: default conservador; no compila Matchbox.
- `experimental_build=true`: intenta `cabal v2-build exe:matchbox2015` sobre `jwaldmann/matchbox`, con cache de `~/.cabal` y `/tmp/matchbox-install`, pero el paso es `continue-on-error` porque el build historico puede romper por dependencias antiguas.
- `matchbox_command` y `matchbox_args`: permiten probar `matchbox2015`, `matchbox`, `matchbox2015 --satchmo --bits 4`, o un wrapper local del archivo descargado.

El workflow siempre sube `/tmp/m19_matchbox_challenges` si llega a generarlo. Si el build falla antes de tener binario, el probe y el runner dejaran evidencia de `ERROR` o fallaran de forma auditable, sin tocar otros workflows.

## Respuestas directas

Terreno virgen?

No para Matchbox/SRS en general. Si para esta ruta exacta dentro del repo: S1/S2 concretos, Matchbox parametrizable, artefactos reproducibles y clasificacion sin falsos positivos.

Alguien ya busco?

Externamente, si: Matchbox fue herramienta historica de Termination Competition y aparece en literatura de SRS, sparse tiling, interpretaciones matriciales y certificacion. Localmente ya hay generador M19, grid `rewriting-collatz`, AProVE y auditoria de certificacion; no habia un runner/workflow Matchbox dedicado en el scope permitido.

Posibilidad fuerte?

Media como buscador de `YES` top-level, especialmente porque Matchbox fue fuerte en SRS. Baja como prueba publicable inmediata si no conseguimos binario estable o CPF verificable. Fuerte solo si obtenemos `YES` top-level sobre el `.tpdb` exacto y despues CPF aceptado por CeTA.

Que destruye la via?

- Matchbox no compila en GitHub Actions moderno sin pinning pesado de GHC/cabal/librerias.
- El binario disponible no acepta el TPDB plain local y exige XTC u otro formato.
- Solo aparecen `YES` internos, SAT de subproblemas o trazas parciales, sin primera linea top-level `YES`.
- El metodo que prueba `YES` no exporta CPF, o CeTA rechaza el CPF.
- S1/S2 requieren una tecnica fuera del portfolio historico y todo queda en `MAYBE/TIMEOUT`.

Proximo paso

Conseguir un binario reproducible de Matchbox o fijar una imagen/container externo. Luego ejecutar el workflow con `binary_archive_url` y una matriz chica de argumentos: default, `--satchmo --bits 4`, `--boolector --bits 4`, `--guarded-satchmo --bits 4` si esos flags estan presentes en `--help`. Si aparece `YES`, repetir con `--cpf` y pasar a la ruta CPF/CeTA.
