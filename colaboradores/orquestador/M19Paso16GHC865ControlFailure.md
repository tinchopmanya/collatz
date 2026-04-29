# M19 paso 16 - GHC 8.6.5 control failure

Fecha: 2026-04-29
Responsable: Codex orquestador
Estado: GHC viejo no resuelve toda la cadena legacy

## Preguntas antes

- Estamos avanzando?
  - Si. Probamos la hipotesis limpia: bajar a GHC `8.6.5` para evitar la fase final de `MonadFail`.
- Estamos en terreno virgen?
  - No. Es recuperacion de toolchain Haskell legacy.
- Podemos descubrir algo fuerte?
  - No todavia. Sin `matchbox2015`, no hay experimento sobre Collatz.
- Ya alguien estuvo buscando esto?
  - Si. Las herramientas y dependencias son publicas; lo nuestro es trazabilidad reproducible.
- Que podia destruir esta ruta?
  - Que GHC `8.6.5` tambien encontrara errores legacy en dependencias profundas.

## Run auditado

Run: `25109052384`

Configuracion:

```text
GHC = 8.6.5
Cabal = 3.10.3.0
index-state = 2021-09-01T00:00:00Z
build_boolector_c = true
patch_haskell_boolector = false
actual_build = true
```

Resultado del gate:

```text
m19_matchbox_artifact_gate=FAIL
missing m19-matchbox-sha256.txt
missing m19-matchbox-ldd.txt
missing m19-matchbox-help.log
```

Bloqueo:

```text
Failed to build satchmo-2.9.9.3
Satchmo/Polynomial.hs:143:28: error:
Could not deduce (Control.Monad.Fail.MonadFail m)
arising from a do statement with the failable pattern f : fs
```

## Lectura

- GHC `8.6.5` supera los bloqueos visibles de `boolector-0.0.0.13` y `wl-pprint-extras-3.5.0.5`, pero falla mas profundo en `satchmo-2.9.9.3`.
- Esto debilita la estrategia "bajar GHC es suficiente".
- No destruye Matchbox todavia, pero confirma que el ecosistema legacy tiene mas de un punto incompatible.
- La siguiente prueba natural es `use_source_deps=true`, porque el workflow ya conoce una fuente `jwaldmann/satchmo` pinneada.

## Preguntas despues

- Estamos avanzando?
  - Si, por descarte. Sabemos que GHC `8.6.5` no es salida limpia.
- Estamos en algo virgen?
  - No, pero estamos construyendo una auditoria util de reproducibilidad.
- Que tan lejos estamos?
  - Mas lejos de una prueba que de una herramienta. Nos falta todavia producir el binario.
- Posibilidad cientifica fuerte?
  - Baja hasta tener `matchbox2015`; media si logramos ejecutar S1/S2; alta solo con `YES` certificable.
- Que destruye la siguiente iteracion?
  - Que `use_source_deps=true` o el parche `wl-pprint-extras` revelen mas parches necesarios sin converger.

## Proximas corridas lanzadas

Se lanzaron dos runs en `main`:

```text
25109605130: GHC 8.10.7, parches boolector + wl-pprint-extras, use_source_deps=false
25109605155: GHC 8.10.7, parches boolector + wl-pprint-extras, use_source_deps=true
```

Criterio:

- Si alguna produce artifact con `m19-matchbox-sha256.txt`, pasar gate y correr S1/S2.
- Si ambas fallan en nuevos paquetes legacy, enfriar build-from-source y priorizar binario/container congelado.
