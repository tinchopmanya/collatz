# M19 paso 15 - Matchbox gate failure

Fecha: 2026-04-29
Responsable: Codex orquestador
Estado: workflow verde, gate rojo; bloqueo nuevo en `wl-pprint-extras`

## Preguntas antes

- Estamos avanzando?
  - Si. El parche local de `boolector-0.0.0.13` supero el bloqueo `MonadFail` anterior y el build llego mas lejos.
- Estamos en terreno virgen?
  - No. Seguimos en reconstruccion de herramienta legacy. La posible novedad esta despues: correr Matchbox sobre S1/S2 y/o M22a.
- Podemos descubrir algo fuerte?
  - Todavia no. Sin binario `matchbox2015`, no hay experimento matematico.
- Ya alguien estuvo buscando esto?
  - Si. Matchbox y los sistemas Collatz de Yolcu-Aaronson-Heule son terreno recorrido. Lo nuevo aqui es reproducibilidad moderna y gating estricto.
- Que destruye esta via?
  - Una cascada interminable de dependencias Haskell incompatibles, o que al final Matchbox compile pero no ayude en S1/S2.

## Run auditado

Run: `25108580421`

Configuracion:

```text
GHC = 8.10.7
Cabal = 3.10.3.0
index-state = 2021-09-01T00:00:00Z
build_boolector_c = true
patch_haskell_boolector = true
actual_build = true
```

Resultado operacional:

```text
GitHub Actions conclusion = success
Full build step = success
```

Resultado del gate:

```text
m19_matchbox_artifact_gate=FAIL
missing m19-matchbox-sha256.txt
missing m19-matchbox-ldd.txt
missing m19-matchbox-help.log
```

Lectura:

- El workflow esta configurado con `continue-on-error` en el paso de build, por eso un fallo de Cabal puede dejar el job verde.
- El gate nuevo detecta correctamente que no hay binario probado.
- No se debe lanzar `M19 Matchbox challenge search` usando este artifact.

## Bloqueo nuevo

El log muestra:

```text
Failed to build wl-pprint-extras-3.5.0.5.
src/Text/PrettyPrint/Free/Internal.hs:794:3: error:
'fail' is not a (visible) method of class 'Monad'
```

Lectura:

- `boolector-0.0.0.13` ya no es el bloqueo visible en esta corrida.
- El nuevo bloqueo es otra incompatibilidad del ecosistema Haskell pre-`MonadFail`.
- Es razonable probar GHC `8.6.5` porque usa una version de `base` anterior al cambio que removio `fail` como metodo visible de `Monad`.
- Si GHC `8.6.5` no funciona, el siguiente parche local minimo seria sobre `wl-pprint-extras-3.5.0.5`, moviendo/removiendo la definicion `fail _ = empty` hacia una instancia `MonadFail`.

## Preguntas despues

- Estamos avanzando?
  - Si, pero seguimos antes de la ejecucion matematica. Subimos de bloqueo C a bloqueo Haskell legacy.
- Estamos en algo virgen?
  - No. Es recuperacion de toolchain.
- Que tan lejos estamos?
  - A una prueba GHC `8.6.5` o a un parche local adicional de saber si Matchbox puede compilar.
- Posibilidad cientifica fuerte?
  - Baja hasta tener binario; media si el binario corre y deja un resultado reproducible; alta solo con `YES` certificable.
- Que destruye la iteracion siguiente?
  - Que GHC `8.6.5` falle por otras dependencias, o que parchar una dependencia revele otra y otra sin converger.

## Proximo paso

Ya se lanzo run `25109052384` con:

```text
GHC = 8.6.5
build_boolector_c = true
patch_haskell_boolector = false
actual_build = true
```

Criterio de exito:

```text
artifact contiene m19-matchbox-sha256.txt, m19-matchbox-ldd.txt y m19-matchbox-help.log
scripts/m19_matchbox_artifact_gate.py devuelve PASS
```

Criterio de abandono parcial:

```text
GHC 8.6.5 no compila y la ruta de parches locales requiere mas de dos paquetes legacy adicionales.
```
