# M19 Boolector source route

Fecha: 2026-04-29
Agente: CodexHijo-M19BoolectorSourceRoute
Rama: `codex-hijo/m19-boolector-source-route`

## Diagnostico

El build pinneado de Matchbox ya no esta bloqueado por Cabal. El dry-run con GHC `8.10.7`, cabal-install `3.10.3.0`, `index-state=2021-09-01T00:00:00Z` y `matchbox_ref=3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4` resuelve `matchbox-4.4.0 exe:matchbox2015`.

El build completo falla en la dependencia Haskell `boolector-0.0.0.13`:

```text
Missing (or bad) header file: boolector.h
Missing (or bad) C library: boolector
```

La causa es concreta: el paquete Ubuntu `boolector` de Jammy provee el ejecutable, pero no una libreria de desarrollo usable por Cabal. La libreria Haskell de Hackage declara bindings sobre el solver SMT Boolector y, en su `boolector.cabal` descargado localmente, contiene:

```text
extra-libraries:  boolector
includes:         boolector.h
```

Por eso no alcanza con `/usr/bin/boolector`; Cabal necesita que el compilador C vea `boolector.h` y que el linker vea `libboolector.so` o `libboolector.a`.

## Ruta implementada en CI

Modifique los dos workflows M19 para agregar una ruta fuente reproducible:

- `boolector_ref`: default `3.2.4`.
- `build_boolector_c`: default `true`.
- Build C solo cuando se intenta compilar Matchbox (`actual_build=true` en el probe, `experimental_build=true` sin binario en challenge-search).

Comandos centrales agregados:

```bash
git clone --depth 1 --branch "$boolector_ref" https://github.com/Boolector/boolector.git /tmp/m19-boolector-src
cd /tmp/m19-boolector-src
./contrib/setup-lingeling.sh
./contrib/setup-btor2tools.sh
./configure.sh --prefix /usr/local --shared --only-lingeling --no-testing
cmake --build build --parallel "$(nproc)"
sudo cmake --install build
sudo ldconfig
```

Luego Cabal se invoca con:

```bash
cabal v2-build exe:matchbox2015 \
  -w "$(command -v ghc)" \
  --jobs=2 \
  --extra-include-dirs=/usr/local/include/boolector \
  --extra-lib-dirs=/usr/local/lib
```

El detalle importante es el include-dir: Boolector instala `boolector.h` bajo `/usr/local/include/boolector/`, mientras que `boolector-0.0.0.13` incluye `"boolector.h"` directamente.

## Pinnings y fuentes

- Boolector `3.2.4` resuelve al commit `393cdfba3735d334bb4e6525500b8a0280dd41e6` (`git ls-remote refs/tags/3.2.4`).
- El script upstream `setup-lingeling.sh` de Boolector `3.2.4` pinnea Lingeling en `7d5db72420b95ab356c98ca7f7a4681ed2c59c70`.
- El script upstream `setup-btor2tools.sh` de Boolector `3.2.4` pinnea BTOR2Tools en `037f1fa88fb439dca6f648ad48a3463256d69d8b`.
- La documentacion upstream de Boolector indica que para Linux se deben construir dependencias SAT y BTOR2Tools, luego `./configure.sh && cd build && make`, y que las librerias salen en `boolector/build/lib`.
- El `src/CMakeLists.txt` de Boolector `3.2.4` instala `libboolector` en `lib` y headers en `include/boolector`.

Links:

- Boolector build upstream: https://github.com/Boolector/boolector
- Boolector C API usa `#include "boolector.h"`: https://boolector.github.io/docs/cboolector.html
- Hackage `boolector-0.0.0.13` docs: https://hackage.haskell.org/package/boolector-0.0.0.13/docs/Boolector.html
- Ubuntu Jammy `boolector`: https://launchpad.net/ubuntu/jammy/+package/boolector
- Script Lingeling pinneado: https://raw.githubusercontent.com/Boolector/boolector/3.2.4/contrib/setup-lingeling.sh
- Script BTOR2Tools pinneado: https://raw.githubusercontent.com/Boolector/boolector/3.2.4/contrib/setup-btor2tools.sh
- Instalacion CMake Boolector: https://raw.githubusercontent.com/Boolector/boolector/3.2.4/src/CMakeLists.txt

## Comando reproducible recomendado

Primero validar que el binario Matchbox se produce:

```text
Actions -> M19 Matchbox build pinning probe -> Run workflow
ghc_version=8.10.7
cabal_version=3.10.3.0
index_state=2021-09-01T00:00:00Z
matchbox_ref=3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4
use_source_deps=false
build_boolector_c=true
boolector_ref=3.2.4
actual_build=true
```

Si produce `matchbox2015`, pasar a desafio:

```text
Actions -> M19 Matchbox challenge search -> Run workflow
challenge=both
experimental_build=true
build_boolector_c=true
boolector_ref=3.2.4
ghc_version=8.10.7
cabal_version=3.10.3.0
index_state=2021-09-01T00:00:00Z
matchbox_ref=3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4
wall_timeout=180
```

## Evidencia que valida la via

La via queda validada si el artifact del probe contiene:

- `m19-boolector-source-rev.txt` con `393cdfba3735d334bb4e6525500b8a0280dd41e6` o el commit exacto del `boolector_ref` usado.
- `m19-boolector-version.txt` producido por `/usr/local/bin/boolector --version`.
- `m19-libboolector-ldd.txt` sin dependencias faltantes.
- `m19-matchbox-sha256.txt` y `m19-matchbox-ldd.txt`.
- `matchbox2015 --help` ejecutado sin `command not found`.

La via matematica M19 se valida solo despues: `M19 Matchbox challenge search` debe producir `YES` top-level sobre los `.tpdb` S1/S2 y, para una prueba publicable, habria que repetir con CPF/CeTA.

## Evidencia que destruye o debilita la via

- Boolector C compila e instala, pero `cabal v2-build` vuelve a fallar en `boolector-0.0.0.13` por simbolos/API incompatibles.
- `libboolector.so` queda instalada pero `ldd` muestra dependencias no resueltas.
- El smoke test C falla al enlazar o ejecutar con `#include "boolector.h"` y `-lboolector`.
- Matchbox compila, pero `matchbox2015 --help` falla por loader/runtime.
- Matchbox corre sobre S1/S2 pero solo devuelve `MAYBE`, `TIMEOUT` o errores de parser.

## Riesgos

- El build fuente agrega tiempo a CI. Si funciona, conviene congelar un artifact binario con `sha256sum`, `ldd`, `cabal.project.freeze`, version de GHC/Cabal y version de Boolector.
- `setup-lingeling.sh` y `setup-btor2tools.sh` descargan tarballs de GitHub aunque los commits esten pinneados. Si GitHub rate-limitea o cambia disponibilidad de archives, puede fallar el CI.
- No pude ejecutar el build Linux local en esta maquina Windows. La validacion fuerte debe venir de GitHub Actions.
- Esta ruta solo resuelve la dependencia C. No garantiza que Matchbox encuentre una prueba para S1/S2.

## Estado

Solucion preparada, no reclamo exito todavia. El bloqueo `boolector.h/libboolector` queda atacado con build fuente pinneado y smoke test C en CI. Falta correr el workflow actualizado para confirmar si `cabal v2-build exe:matchbox2015` produce el binario.
