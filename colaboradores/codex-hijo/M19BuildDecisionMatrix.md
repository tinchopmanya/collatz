# M19 Build decision matrix

Fecha: 2026-04-29
Agente: CodexHijo-M19-BuildDecision
Rama: `codex-hijo/m19-build-decision-matrix`
Scope: artefactos `25107130045`, `25107937562`, `25108580421`, `25109052384`, `25109605155` y workflows `.github/workflows/m19-matchbox-build-probe.yml`, `.github/workflows/m19-matchbox-challenge-search.yml`.

## Decision corta

Los artefactos auditados no contienen un binario Matchbox validado. En los cinco casos faltan `m19-matchbox-sha256.txt`, `m19-matchbox-ldd.txt` y `m19-matchbox-help.log`; por lo tanto no hay evidencia de `matchbox2015` ejecutable, aunque varios runs hayan servido para descubrir bloqueos sucesivos.

Recomendacion: no abrir una ruta de arqueologia larga. Si se decide insistir en build fuente, permitir como maximo **1 parche mas**, y solo si es el parche acotado ya sugerido por evidencia para `satchmo-2.9.9.3` (`Satchmo/Polynomial.hs`, patron failable `f:fs`). Si ese parche descubre otro paquete legacy, un conflicto de solver o un fallo runtime, parar. No recomiendo gastar 2 parches mas. El camino principal debe pivotar ya a binario/container reproducible, o a otra herramienta si no aparece un binario Matchbox verificable.

## Matriz de fallos

| Run | Configuracion observada | Fallo principal | Causa raiz | Parche acotado tiene sentido? | Costo esperado | Riesgo de arqueologia | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `25107130045` | GHC `8.10.7`, Cabal `3.10.3.0`, `index-state=2021-09-01T00:00:00Z`, sin build C Boolector. | `boolector-0.0.0.13` falla en configure: falta `boolector.h` y `libboolector`. | El paquete Ubuntu `boolector` aporta ejecutable, no una libreria C de desarrollo usable por Cabal. | Si. Ya fue el parche correcto: compilar/instalar Boolector C `3.2.4` y pasar include/lib dirs. | Medio, pero cerrado. | Bajo. Era dependencia C concreta. | Parche consumido y validado parcialmente por runs posteriores. |
| `25107937562` | Igual, con `build_boolector_c=true`, Boolector C instalado. | `boolector-0.0.0.13` compila `Boolector.Foreign`, luego falla en `src/Boolector.hs:1327` por `Could not deduce (MonadFail m)` al usar `fail`. | Paquete Haskell antiguo con fuente no compatible con `base-4.14`/GHC `8.10.7`; el bound de Cabal no expresa esa incompatibilidad. | Si. Parche local minimo `fail` -> `error` en ese caso unreachable/BUG tiene sentido. | Bajo. | Medio: confirma que resolver C solo destapa Haskell legacy. | Parche consumido; no es razon para seguir indefinidamente. |
| `25108580421` | GHC `8.10.7`, Boolector C, patch local de `boolector`. | `wl-pprint-extras-3.5.0.5` falla en `Internal.hs:794`: `fail` no es metodo visible de `Monad`. | Paquete 2014 con `fail` dentro de `Monad`; incompatible con la fase final de `MonadFail` en `base >= 4.13`. | Si. El parche CPP con instancia `Control.Monad.Fail.MonadFail` es local y canonico. | Bajo. | Medio-alto: segundo paquete legacy consecutivo. | Parche consumido; despues de este punto la ruta fuente ya es una cinta transportadora probable. |
| `25109052384` | GHC `8.6.5`, Cabal `3.10.3.0`, Boolector C, sin patch Haskell Boolector. | `satchmo-2.9.9.3` falla en `Satchmo/Polynomial.hs:143`: patron failable `f:fs <- ...` exige `MonadFail`. | Codigo legacy usa patron failable dentro de `do` bajo contexto `MonadSAT m`; la fuente no declara/provee `MonadFail m`. | Tal vez. Es el unico parche extra defendible, porque el sitio exacto esta en el log. Debe hacerse solo como experimento final y no mezclado con source deps. | Medio: parche local + repetir build completo, probablemente 1 corrida CI larga. | Alto: `satchmo` tiene muchas superficies legacy y Matchbox aun no llego a compilar. | Maximo 1 parche mas si se decide agotar fuente; si aparece otro bloqueo, pivot inmediato. |
| `25109605155` | GHC `8.10.7`, Boolector C, patches `boolector` y `wl-pprint-extras`, `use_source_deps=true` para `satchmo`, `tpdb`, `wl-pprint-text`. | Solver falla antes de compilar: `atto-lisp` no puede satisfacer a la vez `base==4.14.3.0` y `attoparsec==0.14.1`; conflicto set incluye `atto-lisp`, `attoparsec`, `time`, `tpdb`. | La ruta `source-repository-package` cambia el grafo y arrastra constraints historicas incompatibles; ya no es un parche local, es arqueologia de solver. | No. Arreglar esto exige cambiar index-state, constraints, forks o parches en `tpdb`/`atto-lisp`, y puede destapar mas paquetes. | Alto. | Muy alto. | No invertir parches aqui. Descartar source deps como ruta principal. Pivot. |

Notas de evidencia:

- Todos los dry-runs muestran el warning de `index-state` y Cabal cae al estado `2021-08-31T21:49:42Z`. No es el fallo central, pero conviene registrar que el pin efectivo no es exactamente el texto de entrada.
- El run `25109605155` no tiene `Failed to build` porque falla en solver; por eso un check textual limitado puede subestimar el build log. Aun asi, el gate de artefacto falla por falta de binario/hash/help/ldd.

## Auditoria de workflows

`m19-matchbox-build-probe.yml` es un probe manual, no una compuerta de exito de binario. Tiene `continue-on-error: true` tanto en `Dependency solver dry-run` como en `Full build`, y siempre recolecta artefactos. Esto es util para diagnostico, pero un workflow verde no debe leerse como "Matchbox compilo".

`m19-matchbox-challenge-search.yml` tambien es deliberadamente blando en la fase experimental: el build fuente es `continue-on-error`, el probe de comando no bloquea, y el runner clasifica un binario ausente como `ERROR` en artefactos. Esto evita falsos `YES`, pero tambien significa que el estado de GitHub Actions no certifica que hubo busqueda matematica real.

Brecha menor detectada y no modificada: el gate existente marca correctamente `FAIL` por ausencia de `m19-matchbox-sha256.txt`, `m19-matchbox-ldd.txt` y `m19-matchbox-help.log`, pero su subcheck `build_log_no_failed_build` no captura `Error: cabal: Could not resolve dependencies` en `25109605155`. No cambie scripts porque el resultado global sigue siendo `FAIL` y la tarea pide decision, no parche de gate. Si se toca luego, agregar patrones para `Could not resolve dependencies`, `rejecting:` y `fail (backjumping)`.

## Presupuesto de parches

| Opcion | Que implica | Veredicto |
| --- | --- | --- |
| `0` parches mas | Congelar la evidencia actual y pivotar ya a binario/container. | Ruta recomendada si el objetivo es avanzar M19 con menor riesgo. |
| `1` parche mas | Parche local, aislado y reversible para `satchmo-2.9.9.3`, solo si una corrida Hackage-pura con los parches actuales reproduce ese bloqueo. | Maximo aceptable. Debe tener criterio de muerte: cualquier nuevo paquete legacy o solver conflict termina la via. |
| `2` parches mas | Parchear `satchmo` y luego otro paquete/constraint que aparezca despues. | No recomendado. La evidencia ya muestra treadmill de paquetes legacy. |
| Pivot binario | Conseguir/publicar tar/zip con `matchbox2015`, `sha256sum`, `ldd`, `--help`, toolchain y `cabal.project.freeze`; usar `binary_archive_url`. | Mejor ajuste con el workflow actual. |
| Pivot container | Construir una imagen/artefacto cerrado una vez y extraer binario o correr challenges dentro del container. | Buena fabrica reproducible si Docker/CI esta disponible. |
| Pivot herramienta | Si Matchbox no entrega binario verificable, priorizar AProVE/CPF/CeTA/Yices/otras rutas ya documentadas. | Preferible a seguir arreglando Haskell historico sin evidencia matematica. |

Decision operativa propuesta: **maximo 1 parche mas, pero el trabajo principal debe pivotar ahora**. El parche permitido no debe tocar workflows de produccion salvo como probe manual y debe venir con artefacto que pruebe `matchbox2015 --help`, `sha256sum` y `ldd`. Sin esos tres archivos, no hay avance de decision.

## Siguiente paso recomendado

1. Intentar conseguir un binario Matchbox historico o construirlo en un container cerrado fuera del workflow de challenge.
2. Publicar un archivo `tar.gz`/`zip` con `matchbox2015`, `m19-matchbox-sha256.txt`, `m19-matchbox-ldd.txt`, `m19-matchbox-help.log`, versiones GHC/Cabal/Boolector y `cabal.project.freeze`.
3. Correr `m19-matchbox-challenge-search.yml` con `binary_archive_url` y una matriz pequena de flags tomada de `--help`.
4. Solo si falta binario y se autoriza una ultima prueba fuente, parchear `satchmo` una vez. Si no produce los tres artefactos de binario, cerrar la ruta fuente.

## Verificacion

- Leidos los cinco artefactos solicitados y sus `environment.txt`, `cabal.project.local`, `m19-matchbox-build-dry-run.log` y `m19-matchbox-build.log`.
- Leidos `.github/workflows/m19-matchbox-build-probe.yml` y `.github/workflows/m19-matchbox-challenge-search.yml`.
- Ejecutado `python scripts\m19_matchbox_artifact_gate.py` sobre los cinco directorios de artefactos; todos dieron `m19_matchbox_artifact_gate=FAIL`, esperado por falta de binario/hash/help/ldd.
- No se modificaron workflows ni scripts.
