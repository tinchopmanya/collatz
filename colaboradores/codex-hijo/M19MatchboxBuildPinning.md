# M19 Matchbox build pinning

Fecha: 2026-04-29
Agente: CodexHijo-MatchboxPin
Scope escrito: `colaboradores/codex-hijo/M19MatchboxBuildPinning.md` y probe separado `.github/workflows/m19-matchbox-build-probe.yml`.
Commit: no realizado.

## Diagnostico del fallo CI

El run `25105375622` de `M19 Matchbox challenge search` no produjo evidencia matematica sobre S1/S2. Fallo antes: el build experimental no genero `matchbox2015` y luego el runner clasifico ambos desafios como `ERROR` por binario ausente.

Evidencia local guardada:

- `reports/m19_github_runs/artifacts/25105375622/m19-matchbox-challenge-search-both/m19_matchbox_challenges.md`
- `reports/m19_github_runs/artifacts/25105375622/m19-matchbox-challenge-search-both/logs/*.matchbox.log`

Evidencia de `gh run view 25105375622 --log`:

```text
cabal update
The index-state is set to 2026-04-29T08:56:57Z.
cabal v2-build exe:matchbox2015
Could not resolve dependencies
...
conflict: semigroupoids => base>=4.3 && <4.18
deepseq => base==4.22.0.0/installed-8900
template-haskell => base==4.22.0.0/installed-8900
...
matchbox2015: command not found
```

Lectura: el workflow instala `ghc`/`cabal-install` por apt, pero Cabal termino resolviendo contra un GHC moderno ya presente en el runner (`base==4.22.0.0`, familia GHC 9.14), no contra el `ghc 8.8.4` que apt instalo. Ademas, el build usa Hackage al estado actual de 2026-04-29 y `jwaldmann/matchbox` sin pin de commit. Por eso el fallo es de entorno/resolucion Cabal, no de Matchbox contra los desafios.

## Que se puede fijar

Si se intenta seguir con build fuente, hay que fijar cuatro cosas juntas:

- Commit de Matchbox: `jwaldmann/matchbox@3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4` era `master` al investigar.
- GHC real en `PATH`: usar `haskell-actions/setup@v2` o contenedor, y registrar `which ghc`, `ghc --numeric-version`, `ghc-pkg field base version`.
- Cabal: usar una version explicita moderna que pueda instalar GHC viejo, por ejemplo `3.10.3.0`, pero no dejar que seleccione el GHC del runner.
- Hackage `index-state`: no usar el estado del dia. Probar primero `2021-09-01T00:00:00Z` con GHC `8.10.7`, porque ya existia `boolector` en Hackage y queda antes de muchas revisiones modernas; si falla, probar `2025-02-25T00:00:00Z` con GHC `9.4.8`, que aun satisface `base <4.18`.

Fuentes revisadas:

- Matchbox README/cabal: `matchbox` acepta TPDB plain/XTC, emite texto/CPF y su ejecutable historico es `matchbox2015`: https://github.com/jwaldmann/matchbox y https://raw.githubusercontent.com/jwaldmann/matchbox/master/matchbox.cabal
- `build-all.sh` historico advierte que varias dependencias se tomaban de GitHub y no solo de Hackage: https://raw.githubusercontent.com/jwaldmann/matchbox/master/build-all.sh
- `haskell-actions/setup` permite fijar `ghc-version` y `cabal-version`: https://github.com/haskell-actions/setup
- Cabal documenta `index-state` en `cabal.project`: https://cabal.readthedocs.io/en/stable/cabal-project-description-file.html
- Docker Hub mantiene imagen oficial `haskell` con GHC/Cabal, util para contenedor reproducible: https://hub.docker.com/_/haskell/

## Probe separado agregado

Archivo agregado: `.github/workflows/m19-matchbox-build-probe.yml`.

Es manual (`workflow_dispatch`) y no toca el workflow existente. Objetivo: distinguir rapido si el camino viable es:

- Hackage + GHC/Cabal/index-state pinneados.
- Hackage + source deps pinneadas (`satchmo`, `tpdb`, `wl-pprint-text`) si el plan Hackage puro falla.
- Abandono del build fuente y uso de binario/container.

Parametros principales:

- `ghc_version`: default `8.10.7`.
- `cabal_version`: default `3.10.3.0`.
- `index_state`: default `2021-09-01T00:00:00Z`.
- `matchbox_ref`: default `3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4`.
- `use_source_deps`: default `false`; si se activa, agrega repos Git pinneados para dependencias directas.
- `actual_build`: default `false`; primero hace dry-run/plan, luego opcionalmente compila.

Comando recomendado en GitHub Actions:

```text
Actions -> M19 Matchbox build pinning probe -> Run workflow
ghc_version=8.10.7
cabal_version=3.10.3.0
index_state=2021-09-01T00:00:00Z
use_source_deps=false
actual_build=false
```

Si el dry-run resuelve, repetir con `actual_build=true`. Si no resuelve por `tpdb`, `satchmo` o APIs antiguas, repetir con `use_source_deps=true`. Si falla por `base`, `template-haskell` o `containers` no reinstalable, probar:

```text
ghc_version=9.4.8
cabal_version=3.10.3.0
index_state=2025-02-25T00:00:00Z
use_source_deps=false
actual_build=false
```

## Container/Docker recomendado

La ruta con mas chance de reproducibilidad no es apt sobre `ubuntu-22.04`, sino contenedor con toolchain cerrado. En esta maquina `docker --version` existe, pero el daemon no esta activo (`dockerDesktopLinuxEngine` ausente), asi que no pude validar localmente el build dentro de Docker.

Dockerfile minimo propuesto para probar fuera del workflow actual:

```Dockerfile
FROM haskell:8.10.7

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git ca-certificates libgmp-dev libglpk-dev glpk-utils minisat \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/jwaldmann/matchbox.git /opt/matchbox \
    && cd /opt/matchbox \
    && git checkout 3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4 \
    && printf '%s\n' \
      'packages: .' \
      'index-state: 2021-09-01T00:00:00Z' \
      'allow-newer: false' \
      > cabal.project.local \
    && cabal v2-update \
    && cabal v2-build exe:matchbox2015 \
    && install -D "$(cabal list-bin exe:matchbox2015)" /usr/local/bin/matchbox2015

ENTRYPOINT ["matchbox2015"]
```

Comandos esperados:

```bash
docker build -t m19-matchbox2015:ghc8.10.7 .
docker run --rm -v "$PWD:/work" -w /work m19-matchbox2015:ghc8.10.7 \
  reports/m19_rewriting_challenges/m19_collatz_S1_without_ff_end_to_0_end.tpdb
```

Si esto compila, congelar el artefacto binario es preferible a recompilar en cada corrida: publicar un tar con `matchbox2015`, `matchbox2015 --help`, `ldd`, `sha256sum`, `ghc --version`, `cabal --version` y el `cabal.project.freeze`, y correr el workflow existente con `binary_archive_url`.

## Respuestas directas

Terreno virgen?

No para Matchbox ni terminacion de SRS. Si es terreno relativamente virgen dentro de este repo: no hay todavia un `matchbox2015` reproducible, pinneado y auditado contra los `.tpdb` S1/S2 locales.

Ya buscado?

Si parcialmente. El documento `M19MatchboxRoute.md` ya habia marcado que compilar Matchbox era fragil y que el workflow aceptaba binario externo o build experimental no bloqueante. El run `25105375622` confirma esa fragilidad con un fallo Cabal concreto, pero no agota la via porque no pinneo toolchain ni index-state.

Posibilidad fuerte?

Media. Hay una posibilidad razonable de obtener binario reproducible con contenedor `haskell:8.10.7` o `haskell-actions/setup` + GHC `8.10.7`/`9.4.8` + `index-state`. La posibilidad fuerte no es que el build actual funcione con apt; ese camino ya quedo debil. La posibilidad fuerte es construir una vez, fijar hash del binario, y despues usar `binary_archive_url`.

Abandono?

No aun. Abandonaria el build fuente solo despues de dos probes negativos:

- `GHC 8.10.7 + index-state 2021-09-01 + Hackage puro/source deps` falla por APIs incompatibles.
- `GHC 9.4.8 + index-state 2025-02-25 + Hackage puro/source deps` falla tambien.

Si ambos fallan, la recomendacion pasa a `abandonar compilacion desde fuente en CI` y mantener solo dos vias: binario historico verificable o contenedor preconstruido con hash. No abandonaria Matchbox como buscador hasta probar un binario real sobre S1/S2.

## Verificacion hecha

- `gh run view 25105375622 --log`: OK; se extrajo el fallo Cabal y `matchbox2015: command not found`.
- `docker --version`: OK; daemon local no disponible, por lo que no se valido build Docker local.
- `git ls-remote` para refs actuales de `matchbox`, `satchmo`, `haskell-tpdb`, `wl-pprint-text`: OK.
- Check de texto local sobre markdown/workflow: OK; sin tabs ni CRLF.
- No se ejecuto el probe en GitHub Actions en este turno y no habia `actionlint`/`PyYAML` instalado para validacion YAML local.
