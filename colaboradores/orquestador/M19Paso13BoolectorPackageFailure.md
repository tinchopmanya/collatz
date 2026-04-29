# M19 paso 13 - Boolector package failure

Fecha: 2026-04-29
Responsable: Codex orquestador
Estado: Ubuntu `boolector` no alcanza; ruta Matchbox requiere Boolector C dev/source build

## Preguntas antes

- Estamos avanzando?
  - Si, pero en modo infraestructura. La pregunta era si instalar `boolector` desde Ubuntu Jammy resolvia el bloqueo nativo de Matchbox.
- Estamos en terreno virgen?
  - No. Boolector, Matchbox y rewriting termination son herramientas conocidas. Lo parcialmente nuevo para este repo es reconstruir una cadena reproducible 2026 para S1/S2.
- Podemos descubrir algo fuerte?
  - Todavia no. La posibilidad fuerte aparece solo si logramos ejecutar Matchbox y obtener `YES` top-level, idealmente con CPF/CeTA.
- Ya alguien estuvo buscando esto?
  - Si. Yolcu-Aaronson-Heule ya usaron/analizaron terminacion automatica para Collatz; Matchbox y Boolector son piezas historicas de ese ecosistema.
- Que puede destruir esta via?
  - Que no exista una forma reproducible y legal de compilar/proveer `matchbox2015`, o que luego no produzca `YES` certificable.

## Run auditado

Run: `25107130045`

Workflow:

```text
M19 Matchbox build pinning probe
GHC = 8.10.7
Cabal = 3.10.3.0
index-state = 2021-09-01T00:00:00Z
matchbox_ref = 3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4
actual_build = true
```

Cambio testeado:

```text
apt-get install ... boolector
dpkg -L boolector | grep -E 'boolector\.(h|a|so)' || true
```

Resultado:

```text
Failed to build boolector-0.0.0.13.
Missing header file: boolector.h
Missing C library: boolector
```

Lectura:

- El paquete Ubuntu `boolector` no provee lo que necesita el binding Haskell `boolector-0.0.0.13`.
- El dry-run de Cabal sigue siendo valioso: el plan Haskell resuelve.
- El bloqueo exacto es ahora nativo: necesitamos `boolector.h` y `libboolector`.
- La corrida Matchbox challenge `25107580035` fue cancelada deliberadamente porque estaba repitiendo esta construccion conocida como bloqueada.

## Evidencia externa relevante

- Hackage `boolector-0.0.0.13` declara Haskell bindings para Boolector y depende de `extra-libraries: boolector` e `includes: boolector.h`.
- El README de Boolector indica que el build desde fuente genera `libboolector.a`/`libboolector.so` en `build/lib` y que requiere construir BTOR2Tools y un SAT backend como Lingeling.
- El articulo de Yolcu-Aaronson-Heule confirma que el enfoque Collatz-as-rewriting es terreno ya recorrido, aunque no resuelto.

Fuentes:

- https://hackage.haskell.org/package/boolector
- https://raw.githubusercontent.com/PLSysSec/haskell-boolector/master/boolector.cabal
- https://raw.githubusercontent.com/Boolector/boolector/master/README.md
- https://link.springer.com/article/10.1007/s10817-022-09658-8

## Decision

No relanzar `M19 Matchbox challenge search` con `experimental_build=true` hasta que una de estas condiciones se cumpla:

1. El workflow construye Boolector C desde fuente y exporta `CPATH`/`LIBRARY_PATH`/`LD_LIBRARY_PATH`, o instala en `/usr/local` y corre `ldconfig`.
2. Se provee un binario reproducible `matchbox2015` con hash y origen verificable.
3. Se demuestra que Matchbox puede compilar sin el binding Haskell de Boolector.

## Preguntas despues

- Estamos avanzando?
  - Si. Cerramos una falsa salida barata: `apt install boolector` no basta.
- Estamos en algo virgen?
  - No matematicamente. Si hay aporte, sera como reproduccion/certificacion moderna.
- Podemos descubrir algo?
  - Si, pero despues de superar esta dependencia nativa. Antes de eso no estamos ejecutando la herramienta, solo preparandola.
- Que tan lejos estamos?
  - A una iteracion tecnica de saber si Boolector C source-build habilita Matchbox. Si falla tambien, la ruta pasa a binario/container o se enfria.
- Proxima accion?
  - Delegar/ejecutar `M19-Boolector-source-route`: construir Boolector desde fuente, fijar commit/tag, verificar `boolector.h`, `libboolector`, `ldd`, `sha256`, y recien entonces correr S1/S2.
