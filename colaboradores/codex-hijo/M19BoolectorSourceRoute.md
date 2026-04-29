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

## Evidencia CI obtenida

Run: https://github.com/tinchopmanya/collatz/actions/runs/25107937562

Configuracion:

```text
ghc_version=8.10.7
cabal_version=3.10.3.0
index_state=2021-09-01T00:00:00Z
matchbox_ref=3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4
use_source_deps=false
build_boolector_c=true
boolector_ref=3.2.4
actual_build=true
```

Resultado:

- El paso `Build and install Boolector C library` paso.
- El artifact contiene `m19-boolector-source-rev.txt = 393cdfba3735d334bb4e6525500b8a0280dd41e6`.
- El artifact contiene `m19-boolector-version.txt = 3.2.4`.
- El artifact contiene `m19-libboolector-ldd.txt` sin dependencias faltantes: solo `libm`, `libc` y loader.
- El build Haskell avanzo mas alla del bloqueo anterior: `boolector-0.0.0.13` ya no falla en configure por header/libreria; ahora configura, preprocesa y compila `Boolector.Foreign`.

Nuevo bloqueo, distinto de la libreria C:

```text
Failed to build boolector-0.0.0.13.
Configuring library for boolector-0.0.0.13..
Preprocessing library for boolector-0.0.0.13..
Building library for boolector-0.0.0.13..
[1 of 2] Compiling Boolector.Foreign
[2 of 2] Compiling Boolector
src/Boolector.hs:1327:10: error:
Could not deduce (MonadFail m) arising from a use of 'fail'
```

Lectura: esta rama resuelve el bloqueo `boolector.h/libboolector`; no produce todavia `matchbox2015` con GHC `8.10.7` porque aparece una incompatibilidad fuente del paquete Haskell `boolector-0.0.0.13` con `MonadFail`.

Tambien lance una prueba con `ghc_version=8.6.5` para evitar la fase final de `MonadFail`, pero fue cancelada externamente antes de terminar: https://github.com/tinchopmanya/collatz/actions/runs/25108397131. No debe contarse como evidencia a favor ni en contra.

## Evidencia que valida la via Boolector C

La via Boolector C queda validada porque el artifact del probe contiene:

- `m19-boolector-source-rev.txt` con `393cdfba3735d334bb4e6525500b8a0280dd41e6`.
- `m19-boolector-version.txt` con `3.2.4`.
- `m19-libboolector-ldd.txt` sin dependencias faltantes.

La via completa Matchbox queda pendiente. Para validarla faltan `m19-matchbox-sha256.txt`, `m19-matchbox-ldd.txt` y `matchbox2015 --help` sin error. La via matematica M19 se valida solo despues: `M19 Matchbox challenge search` debe producir `YES` top-level sobre los `.tpdb` S1/S2 y, para una prueba publicable, habria que repetir con CPF/CeTA.

## Evidencia que destruye o debilita la via

- Boolector C compila e instala, pero `cabal v2-build` vuelve a fallar en `boolector-0.0.0.13` por simbolos/API incompatibles.
- `libboolector.so` queda instalada pero `ldd` muestra dependencias no resueltas.
- El smoke test C falla al enlazar o ejecutar con `#include "boolector.h"` y `-lboolector`.
- Matchbox compila, pero `matchbox2015 --help` falla por loader/runtime.
- Matchbox corre sobre S1/S2 pero solo devuelve `MAYBE`, `TIMEOUT` o errores de parser.

## Riesgos

- El build fuente agrega tiempo a CI. Si funciona, conviene congelar un artifact binario con `sha256sum`, `ldd`, `cabal.project.freeze`, version de GHC/Cabal y version de Boolector.
- `setup-lingeling.sh` y `setup-btor2tools.sh` descargan tarballs de GitHub aunque los commits esten pinneados. Si GitHub rate-limitea o cambia disponibilidad de archives, puede fallar el CI.
- No pude ejecutar el build Linux local en esta maquina Windows; la evidencia fuerte usada aqui viene de GitHub Actions.
- Esta ruta solo resuelve la dependencia C. No garantiza que Matchbox encuentre una prueba para S1/S2.

## Proximo bloqueo tecnico

Opciones precisas:

- Probar de nuevo `ghc_version=8.6.5` con `actual_build=true`, porque GHC 8.8 implemento la fase final de `MonadFail` y el error actual puede desaparecer con base/GHC anterior.
- Si GHC 8.6.5 no resuelve dependencias o no compila, usar un `source-repository-package` para `boolector` Haskell con un parche minimo: reemplazar el `fail` de `lookupSort` por un error monomorfico compatible, o agregar `MonadFail m` donde corresponda y propagar la restriccion.
- Si se usa parche, fijar commit/fork y repetir el probe hasta obtener `matchbox2015`, `sha256sum`, `ldd` y `--help`.

## Estado

Solucion Boolector C validada en CI. No reclamo exito de Matchbox completo todavia: `cabal v2-build exe:matchbox2015` ya supera el bloqueo `boolector.h/libboolector`, pero falla despues por `MonadFail` en `boolector-0.0.0.13`.
