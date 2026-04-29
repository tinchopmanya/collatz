# M19 Haskell legacy route

Fecha: 2026-04-29
Agente: CodexHijo-M19HaskellLegacyRoute
Rama: `codex-hijo/m19-haskell-legacy-route`
Scope escrito: `.github/workflows/m19-matchbox-build-probe.yml`, `.github/workflows/m19-matchbox-challenge-search.yml`, `colaboradores/codex-hijo/M19HaskellLegacyRoute.md`.

## Bloqueo actual

La corrida `25108580421`, segun el contexto de la tarea, avanzo mas que la ruta Boolector C + patch local de `boolector-0.0.0.13`, pero fallo despues en `wl-pprint-extras-3.5.0.5` con:

```text
fail is not a visible method of class Monad
```

Inspeccion de la fuente Hackage `wl-pprint-extras-3.5.0.5`:

```haskell
instance Monad Doc where
  return = Effect
  ...
  fail _ = empty
```

Ese paquete fue subido en 2014 y declara `base == 4.*`, por lo que Cabal lo considera compatible con GHC modernos aunque la fuente ya no lo sea. El cambio relevante es la fase final de `MonadFail`: en `base-4.13.0.0` / GHC 8.8.1, `fail` salio de `Monad` y paso a `MonadFail`. La documentacion de `Control.Monad.Fail` para `base-4.12.0.0` recomienda el patron de transicion con `qualified Control.Monad.Fail as Fail`, `fail = Fail.fail` en `Monad` para bases viejas, e instancia `Fail.MonadFail`.

Fuentes primarias:

- Hackage `wl-pprint-extras-3.5.0.5`: https://hackage.haskell.org/package/wl-pprint-extras-3.5.0.5
- Upstream `ekmett/wl-pprint-extras`: https://github.com/ekmett/wl-pprint-extras
- `Control.Monad.Fail` en `base-4.12.0.0`: https://downloads.haskell.org/ghc/8.6.2/docs/html/libraries/base-4.12.0.0/Control-Monad-Fail.html
- Changelog de `base`, entrada `4.13.0.0`: https://hackage.haskell.org/package/base/changelog

## Opciones comparadas

| Opcion | Lectura | Riesgo | Veredicto |
| --- | --- | --- | --- |
| GHC `8.6.5` / `base-4.12` | Evita la fase final de `MonadFail`; deberia compilar mas codigo legacy sin parches. | Cambia la toolchain completa, puede reabrir conflictos de solver/librerias boot y la corrida anterior `8.6.5` fue cancelada, no concluyente. | Buena prueba de control, no la ruta minima principal. |
| Patch local de `wl-pprint-extras` | Mantiene GHC `8.10.7`, Cabal, index-state y versiones resueltas; toca solo la fuente legacy que falla. | Puede revelar otro paquete legacy despues, pero eso seria progreso incremental auditable. | Ruta minima recomendada e implementada. |
| `source-repository-package` alternativo | Seria limpio si existe fork/commit ya corregido. | Upstream `ekmett/wl-pprint-extras` `master` sigue definiendo `fail` dentro de `Monad`; apuntar al upstream no desbloquea. Requiere publicar y fijar fork. | Segunda opcion si queremos congelar un fork despues de validar el patch. |
| Constraints / `allow-newer` | Util para solver, no para errores de compilacion fuente. | `allow-newer` no arregla un metodo inexistente; `constraints: base < 4.13` es incompatible con GHC `8.10.7` y equivale a cambiar de compiler. | No resuelve este bloqueo. |

## Implementacion

Agregue el input `patch_wl_pprint_extras` con default `true` en ambos workflows M19. Cuando se intenta build real, el workflow hace:

```bash
cabal get wl-pprint-extras-3.5.0.5 --destdir=/tmp/m19-wl-pprint-extras
```

Luego parchea `src/Text/PrettyPrint/Free/Internal.hs` asi:

```haskell
{-# LANGUAGE CPP #-}
import qualified Control.Monad.Fail as Fail

instance Monad Doc where
  ...
#if !MIN_VERSION_base(4,13,0)
  fail = Fail.fail
#endif

instance Fail.MonadFail Doc where
  fail _ = empty
```

Finalmente agrega el paquete local a `cabal.project.local`:

```text
packages: . /tmp/m19-haskell-boolector/boolector-0.0.0.13 /tmp/m19-wl-pprint-extras/wl-pprint-extras-3.5.0.5
```

El cache del workflow `M19 Matchbox challenge search` se movio a `v3` e incluye `patch_wl_pprint_extras` para evitar mezclar builds previos.

## Comandos reproducibles

Validacion primaria del build:

```text
Actions -> M19 Matchbox build pinning probe -> Run workflow
ghc_version=8.10.7
cabal_version=3.10.3.0
index_state=2021-09-01T00:00:00Z
matchbox_ref=3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4
use_source_deps=false
build_boolector_c=true
boolector_ref=3.2.4
patch_haskell_boolector=true
patch_wl_pprint_extras=true
actual_build=true
```

Si produce `matchbox2015`, pasar a desafios:

```text
Actions -> M19 Matchbox challenge search -> Run workflow
challenge=both
experimental_build=true
binary_archive_url=
ghc_version=8.10.7
cabal_version=3.10.3.0
index_state=2021-09-01T00:00:00Z
matchbox_ref=3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4
build_boolector_c=true
boolector_ref=3.2.4
patch_haskell_boolector=true
patch_wl_pprint_extras=true
wall_timeout=180
```

Control alternativo, solo si la ruta principal falla por otro paquete legacy:

```text
Repetir el build probe con:
ghc_version=8.6.5
cabal_version=3.10.3.0
patch_haskell_boolector=true
patch_wl_pprint_extras=true
actual_build=true
```

## Evidencia que valida la via

- El log del paso `Patch wl-pprint-extras MonadFail legacy` muestra `instance Fail.MonadFail Doc where` y el `cabal.project.local` incluye `/tmp/m19-wl-pprint-extras/wl-pprint-extras-3.5.0.5`.
- El build ya no falla con `fail is not a visible method of class Monad` en `wl-pprint-extras-3.5.0.5`.
- El artifact del probe contiene `m19-matchbox-sha256.txt`, `m19-matchbox-ldd.txt` y `m19-matchbox-help.log`.
- En `M19 Matchbox challenge search`, `command -v matchbox2015` encuentra el binario y los logs S1/S2 contienen un veredicto top-level auditable.

## Evidencia que destruye o debilita la via

- El patch falla porque la fuente descargada de Hackage ya no contiene el patron esperado; eso indicaria que el paquete/version o index-state no son los asumidos.
- Cabal sigue compilando el paquete Hackage original en vez del paquete local; el `cabal.project.local` del artifact lo revelaria.
- Aparece el mismo error `fail is not a visible method of class Monad` en `wl-pprint-extras`; eso destruye este patch exacto.
- Aparece otro error legacy equivalente en otro paquete; no destruye la via, pero confirma que hacen falta mas parches locales o pasar a fork congelado.
- El build compila, pero `matchbox2015 --help` falla por runtime/linker; entonces el bloqueo ya no es Haskell legacy sino packaging/binario.

## Recomendacion

Primero correr la ruta implementada con GHC `8.10.7` y los dos parches locales (`boolector` y `wl-pprint-extras`). Si eso supera `wl-pprint-extras` pero descubre otro paquete legacy, repetir el mismo patron solo si el cambio es local y pequeno. Si aparecen dos o mas parches adicionales, conviene consolidar en forks `source-repository-package` pinneados por commit para congelar la evidencia.
