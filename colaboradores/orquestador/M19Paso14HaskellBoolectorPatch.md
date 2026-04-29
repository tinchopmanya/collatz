# M19 paso 14 - Haskell Boolector patch

Fecha: 2026-04-29
Responsable: Codex orquestador
Estado: Boolector C validado; bloqueo nuevo en binding Haskell `boolector-0.0.0.13`

## Preguntas antes

- Estamos avanzando?
  - Si. El build fuente de Boolector C en CI paso el smoke test y produjo `boolector --version = 3.2.4`.
- Estamos en terreno virgen?
  - No. Esto sigue siendo arqueologia reproducible de herramienta. Lo valioso es recuperar una cadena Matchbox ejecutable para benchmarks Collatz.
- Podemos descubrir algo fuerte?
  - Todavia no. Un resultado fuerte empieza si `matchbox2015` corre sobre S1/S2 y devuelve `YES` top-level, idealmente luego certificable.
- Ya alguien estuvo buscando esto?
  - Si. Matchbox/Boolector/rewriting termination son terreno recorrido. La instancia moderna reproducible contra nuestros S1/S2 es lo especifico del repo.
- Que destruye esta via?
  - Que el binding Haskell no pueda compilarse sin un fork grande, o que Matchbox compile pero no ejecute/parsee los desafios.

## Run auditado

Run: `25107937562`

Workflow usado: `M19 Matchbox build pinning probe` desde la rama `codex-hijo/m19-boolector-source-route`.

Resultado bueno:

```text
Build and install Boolector C library: success
Boolector version: 3.2.4
Boolector source rev: 393cdfba3735d334bb4e6525500b8a0280dd41e6
```

Resultado bloqueante:

```text
Failed to build boolector-0.0.0.13.
src/Boolector.hs:1327:10: error:
Could not deduce (MonadFail m) arising from a use of fail
```

Lectura:

- El bloqueo `boolector.h/libboolector` quedo superado.
- El siguiente bloqueo es una incompatibilidad Haskell moderna, no un fallo matematico ni de API C.
- La linea problematica es un fallback interno imposible en `lookupSort`; el paquete ya importa `Control.Monad.Fail` y la monada concreta deriva `MonadFail`, pero una funcion polimorfica conserva solo `MonadBoolector m`.

## Cambio aplicado

Agregue `patch_haskell_boolector=true` a:

- `.github/workflows/m19-matchbox-build-probe.yml`
- `.github/workflows/m19-matchbox-challenge-search.yml`

Cuando esta activo, CI descarga localmente `boolector-0.0.0.13` desde Hackage, aplica un parche minimo:

```text
fail "BUG: should really have the sort in the cache"
->
error "BUG: should really have the sort in the cache"
```

y fuerza a Cabal a usar ese paquete local agregandolo al campo `packages` de `cabal.project.local`.

Razon:

- No cambia la semantica normal del solver; solo cambia un camino de error interno.
- Evita agregar restricciones `MonadFail` que podrian propagarse por la API publica.
- Mantiene la dependencia Hackage con una modificacion textual pequena y auditable.

## Preguntas despues

- Estamos avanzando?
  - Si. Ahora la ruta Matchbox esta bloqueada por una incompatibilidad puntual que ya tiene parche minimo.
- Estamos en algo virgen?
  - No en herramientas; si en la trazabilidad moderna de esta cadena exacta dentro del repo.
- Que tan lejos estamos?
  - A una corrida CI de saber si `matchbox2015` se produce. Si aparece `m19-matchbox-sha256.txt`, pasamos a correr S1/S2.
- Posibilidad cientifica fuerte?
  - Media como benchmark/reproducibilidad; alta solo si Matchbox produce `YES` y luego conseguimos CPF/CeTA o evidencia equivalente.
- Que destruye la iteracion siguiente?
  - Que el build falle despues en otro error Haskell profundo, en runtime loader, o que `matchbox2015 --help` no ejecute.

## Proximo paso

1. Commit/push del parche.
2. Relanzar `M19 Matchbox build pinning probe` con:

```text
actual_build=true
build_boolector_c=true
patch_haskell_boolector=true
boolector_ref=3.2.4
```

3. Aceptar exito solo si el artifact contiene:

```text
m19-matchbox-sha256.txt
m19-matchbox-ldd.txt
m19-matchbox-help.log
```

4. Si pasa, lanzar `M19 Matchbox challenge search` contra S1/S2.
