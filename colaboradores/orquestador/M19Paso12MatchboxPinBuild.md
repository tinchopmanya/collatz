# M19 paso 12 - Matchbox pin build

Fecha: 2026-04-29
Responsable: Codex orquestador
Estado: dry-run resuelto; build fuente llego a bloqueo Boolector; workflows parcheados

## Preguntas antes

- Estamos avanzando?
  - Si. La via Matchbox paso de "no hay binario" a "Cabal resuelve con toolchain pinneada".
- Estamos en terreno virgen?
  - No. Matchbox y terminacion SRS son terreno recorrido. Lo nuevo para este repo es lograr un binario reproducible que pueda atacar S1/S2.
- Podemos descubrir algo fuerte?
  - Si, pero solo si Matchbox real produce `YES` top-level y luego CPF/CeTA. Por ahora no llegamos a ejecutar S1/S2.
- Ya alguien estuvo buscando esto?
  - Si. Yolcu-Aaronson-Heule mencionan Matchbox; el propio `matchbox.cabal` documenta salida CPF. Nuestro trabajo es reproducibilidad moderna.
- Que tan lejos estamos?
  - Mas cerca: la resolucion Haskell ya funciona. Falta resolver una dependencia C concreta.

## Runs

### Dry-run pinneado

Run: `25106442517`

Configuracion:

```text
GHC = 8.10.7
Cabal = 3.10.3.0
index-state = 2021-09-01T00:00:00Z
matchbox_ref = 3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4
actual_build = false
```

Resultado:

```text
Dependency solver dry-run: success
base = 4.14.3.0
plan includes matchbox-4.4.0 exe:matchbox2015
```

Lectura:

- El bloqueo Cabal original era evitable.
- La combinacion GHC 8.10.7 + index-state 2021 funciona como plan de dependencias.

### Build fuente

Run: `25106571514`

Resultado operacional: job `success`, pero el paso `Full build` era `continue-on-error`; el log muestra fallo real:

```text
Failed to build boolector-0.0.0.13
Missing header file: boolector.h
Missing C library: boolector
```

Lectura:

- No hay binario `matchbox2015` todavia.
- El problema ya no es Hackage/Cabal sino una dependencia C de `boolector`.
- El run de desafios `25106849842` fue cancelado deliberadamente porque iba a repetir este fallo.

## Cambio aplicado

Workflows modificados:

- `.github/workflows/m19-matchbox-build-probe.yml`
- `.github/workflows/m19-matchbox-challenge-search.yml`

Cambio:

```text
apt-get install ... boolector
dpkg -L boolector | grep -E 'boolector\.(h|a|so)' || true
```

Razon:

- Ubuntu Jammy publica paquete `boolector`.
- Necesitamos saber si ese paquete contiene header/libreria suficientes para el binding Haskell.
- Si no las contiene, el siguiente paso sera compilar Boolector C o buscar una version de `boolector` Haskell/source-deps que no requiera binding C.

## Preguntas despues

- Estamos avanzando?
  - Si. Redujimos el bloqueo a una dependencia nativa concreta.
- Estamos en algo virgen?
  - No. Es arqueologia reproducible de herramienta historica, no matematica nueva todavia.
- Podemos descubrir algo?
  - Todavia no en Collatz. Pero si conseguimos `matchbox2015`, pasamos a una busqueda real sobre S1/S2.
- Que tan lejos estamos?
  - A un probe de saber si Ubuntu `boolector` alcanza. Si alcanza, corremos S1/S2. Si no, toca build nativo de Boolector o abandonar build-from-source.

## Proximo paso

1. Commit/push del parche `boolector`.
2. Relanzar `M19 Matchbox build pinning probe` con `actual_build=true`.
3. Si aparece `matchbox2015`, lanzar `M19 Matchbox challenge search` con `experimental_build=true`.
4. Si vuelve a fallar por `boolector.h`, abrir subruta `M19-Boolector`: compilar Boolector C o usar contenedor/binario congelado.

## Fuente externa

- Ubuntu Jammy package `boolector`: https://launchpad.net/ubuntu/jammy/+package/boolector
