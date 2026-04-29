# M19 Paso 17 - source-deps no resuelve Matchbox

Fecha: 2026-04-29

## Preguntas antes de la iteracion

- Estamos avanzando? Si: estamos convirtiendo intentos de CI en evidencia auditada, no en "verde" superficial.
- Estamos en terreno virgen? No como matematica de Collatz/rewrite; si en nuestro pipeline reproducible de gates para S1/S2.
- Alguien ya estuvo aca? Si: Yolcu-Aaronson-Heule y la comunidad de termination rewriting recorrieron esta zona. Nuestro punto diferencial es certificacion reproducible y puente con filtros low-bit.
- Que tan lejos estamos de algo publicable? Medio-largo. Falta un `YES` externo verificable, o una reduccion nueva que deje una familia residual claramente menor y certificable.
- Que destruye esta via? Que Matchbox no sea reconstruible sin una cadena creciente de parches historicos de Haskell.

## Resultado observado

Run de GitHub Actions: `25109605155`

Configuracion:

- `ghc_version=8.10.7`
- `cabal_version=3.10.3.0`
- `index_state=2021-09-01T00:00:00Z`
- `matchbox_ref=3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4`
- `use_source_deps=true`
- `build_boolector_c=true`
- `boolector_ref=3.2.4`
- `patch_haskell_boolector=true`
- `patch_wl_pprint_extras=true`
- `actual_build=true`

El gate de artefacto fallo correctamente:

- faltan `m19-matchbox-sha256.txt`, `m19-matchbox-ldd.txt` y `m19-matchbox-help.log`;
- no hay binario Matchbox construido;
- si existen logs, ambiente, revision Boolector y version Boolector.

La causa no fue Boolector ni `wl-pprint-extras`; fue resolucion de dependencias Haskell:

```text
cabal: Could not resolve dependencies:
rejecting: atto-lisp-0.2.2.3
conflict: base==4.14.3.0, atto-lisp => base>=4.9 && <4.13
rejecting: atto-lisp-0.2.2.2
conflict: attoparsec==0.14.1, atto-lisp => attoparsec>=0.10 && <0.14
```

## Interpretacion

`use_source_deps=true` queda descartado como salida facil para GHC 8.10.7. Cambia el fallo: ya no estamos en el parche local de Boolector/`wl-pprint-extras`, sino en una incompatibilidad `tpdb -> atto-lisp -> base/attoparsec`.

Esto refuerza una lectura conservadora: construir Matchbox historico desde Hackage/source-deps se esta transformando en arqueologia de ecosistema. Todavia puede valer una o dos pruebas acotadas si el otro run con `use_source_deps=false` y parches activos produce una frontera pequena, pero no conviene abrir una cadena ilimitada de parches.

## Preguntas despues de la iteracion

- Estamos avanzando? Si, por descarte limpio: sabemos que `source-deps` no era la llave.
- Estamos en terreno virgen? No en la herramienta; la novedad sigue dependiendo de encontrar una certificacion o reduccion reproducible sobre S1/S2/M22.
- Posibilidad cientifica fuerte alta? Baja para "reconstruir Matchbox historico" como aporte; media para usarlo como certificador si aparece un binario real; media-alta para M22 si el filtro low-bit reduce de forma formal una familia que las herramientas puedan cerrar.
- Siguiente decision: esperar el run `25109605130` (`use_source_deps=false`, Boolector C, parches Boolector y `wl-pprint-extras`). Si tambien falla en otra dependencia, limitar esta via y pasar a binario/container oficial o a M22 como via principal.
