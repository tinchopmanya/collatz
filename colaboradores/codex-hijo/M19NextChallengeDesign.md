# M19 next challenge design

Fecha: 2026-04-29
Responsable: CodexHijo
Scope: diseno de la proxima ola de desafios SRS para `rewriting-collatz`, sin ejecutar AProVE/Matchbox y sin tocar scripts existentes.

## Resumen

La ola actual M19 ya materializo y probo una grilla chica para:

- `S1 = S \ {aad -> ed}`, equivalente a quitar `ff* -> 0*`.
- `S2 = S \ {bad -> d}`, equivalente a quitar `tf* -> *`.

La grilla `rewriting-collatz` chica dio 0 `QED` para S1/S2 con natural/arctic, `d <= 3`, `rw <= 5`; AProVE queda condicionado por Yices 1 real; Matchbox queda condicionado por conseguir binario reproducible. Por eso esta siguiente ola no debe ser "mas de lo mismo" sobre S1/S2. Debe separar si la dificultad viene de una regla dinamica especifica, de interacciones entre reglas dinamicas, o de los desafios modulo 8 del paper.

La recomendacion es publicar como maximo seis nuevos desafios, en este orden de prioridad.

## Desafio 1: S3 sin `t* -> 2*`

Nombre sugerido: `M19N1_S3_without_t_end_to_2_end`

Regla removida:

```text
bd -> gd
```

Hipotesis: la tercera regla dinamica de `S`, asociada a `t* -> 2*` y al caso residual `3 mod 4`, puede tener una prueba mas accesible que S1/S2 o revelar que S1/S2 no eran especiales sino parte de una familia de tres removals duros.

Por que no es redundante con S1/S2: S1 y S2 remueven las reglas dinamicas `aad -> ed` y `bad -> d`. Este desafio remueve la unica regla dinamica restante, que no fue materializada como challenge M19 actual. Sirve tambien como control: si cae rapido, S1/S2 son excepcionales; si no cae, la frontera dinamica completa es dura.

Herramienta que lo puede intentar: primero `rewriting-collatz` con la misma grilla chica para comparabilidad; despues AProVE con Yices 1 real; despues Matchbox si aparece binario reproducible.

Criterio de exito: `QED` en `rewriting-collatz` o `YES` top-level en AProVE/Matchbox sobre el SRS exacto, idealmente seguido de CPF/CeTA si la herramienta lo permite.

Criterio de abandono: abandonar si `rewriting-collatz` da `UNSAT` hasta `d <= 3`, `rw <= 5`, y AProVE/Matchbox no dan `YES` en presupuestos comparables a S1/S2. No escalar a busqueda abierta salvo que los CNF sean mucho mas chicos o aparezca una senal estructural nueva.

Riesgo Yolcu-Aaronson-Heule: alto. El inventario oficial ya contiene `relative/collatz-S-3mod4.srs` con prueba, que puede estar muy cerca conceptualmente. Antes de reclamar novedad hay que comparar si este S3 es simplemente una reformulacion de ese caso.

## Desafio 2: S12 sin las dos reglas abiertas S1/S2

Nombre sugerido: `M19N2_S12_without_ff_and_tf_end`

Reglas removidas:

```text
aad -> ed
bad -> d
```

Hipotesis: quitar simultaneamente las dos reglas abiertas puede producir un sistema mas debil y, por tanto, mas facil de certificar. Si no cae, sugiere que la dificultad no esta solo en cada regla individual sino en la estructura auxiliar que queda.

Por que no es redundante con S1/S2: S1 y S2 son remociones unitarias. Este desafio mide la interaccion entre las dos reglas que el paper dejo abiertas. Un `QED` aqui no resuelve S1 ni S2, pero daria un benchmark intermedio claro entre los desafios abiertos y subsistemas demasiado triviales.

Herramienta que lo puede intentar: `rewriting-collatz` como prueba de sensibilidad; AProVE/Matchbox para buscar un `YES` top-level; auditor CPF/CeTA solo si hay prueba candidata.

Criterio de exito: prueba automatica con parametros no mayores que los de las pruebas oficiales medianas, por ejemplo CNF y tiempos comparables a `collatz-T-1or5mod8` o `collatz-S-3mod4`, no a una busqueda masiva.

Criterio de abandono: abandonar si no hay prueba chica y el desafio queda solo como weakening artificial sin lectura matematica adicional. No ampliar si el unico plan es repetir la busqueda S1/S2 con menos reglas.

Riesgo Yolcu-Aaronson-Heule: medio. Es muy probable que los autores exploraran debilitamientos parecidos, aunque no necesariamente este doble-removal como archivo separado. El valor seria de benchmark reproducible, no de novedad fuerte, salvo certificado moderno.

## Desafio 3: S13 sin `ff* -> 0*` y `t* -> 2*`

Nombre sugerido: `M19N3_S13_without_ff_and_t_to_2`

Reglas removidas:

```text
aad -> ed
bd -> gd
```

Hipotesis: comparar S13 contra S12 y S23 separa si la regla `bad -> d` es la principal fuente de dificultad o si la dificultad aparece cuando queda aislada una sola rama dinamica.

Por que no es redundante con S1/S2: no intenta resolver S1 ni S2 directamente. Es una prueba de interaccion entre una regla abierta (`aad -> ed`) y la regla dinamica no materializada (`bd -> gd`). Puede ayudar a decidir que rama dinamica conviene estudiar con herramientas externas.

Herramienta que lo puede intentar: `rewriting-collatz` para una grilla chica uniforme; Matchbox si se consigue binario, porque SRS pequenas con menos reglas son buen objetivo; AProVE solo despues de resolver Yices 1.

Criterio de exito: `QED` o `YES` con parametros significativamente menores que S1/S2, o al menos una diferencia clara de dificultad frente a S12/S23.

Criterio de abandono: abandonar si los tres pairwise removals son todos `UNSAT` en la grilla chica y ninguna herramienta externa da top-level `YES`. En ese caso no aportan frontera, solo confirman que los removals combinatorios son mala direccion.

Riesgo Yolcu-Aaronson-Heule: medio-alto. Los pairwise removals son naturales y pudieron haber sido probados informalmente. Mantenerlo como diagnostico interno salvo que aparezca certificado nuevo.

## Desafio 4: S23 sin `tf* -> *` y `t* -> 2*`

Nombre sugerido: `M19N4_S23_without_tf_and_t_to_2`

Reglas removidas:

```text
bad -> d
bd -> gd
```

Hipotesis: si S23 cae pero S13 no, la regla `aad -> ed` conserva suficiente estructura para orientar una prueba; si ocurre al reves, la rama `bad -> d` merece prioridad. Esta comparacion da informacion que S1/S2 por separado no dan.

Por que no es redundante con S1/S2: aunque incluye la regla removida de S2, el objeto no es S2 sino un sistema con solo una regla dinamica principal restante. Es una prueba de "rama sobreviviente", no una busqueda directa sobre el desafio abierto original.

Herramienta que lo puede intentar: igual que S13: primero prover oficial, luego Matchbox/AProVE, con clasificacion conservadora de top-level `YES`.

Criterio de exito: prueba chica o patron de dificultad asimetrico frente a S12/S13. El resultado seria util incluso si solo sirve para priorizar que rama atacar despues.

Criterio de abandono: abandonar si no discrimina nada frente a S12/S13 o si la prueba, en caso de existir, es una consecuencia trivial de un subsistema oficial ya inventariado.

Riesgo Yolcu-Aaronson-Heule: medio-alto. Es un weakening combinatorio obvio. Debe presentarse como mapa de dificultad, no como descubrimiento matematico fuerte.

## Desafio 5: SRS de evitacion `5 or 7 mod 8`

Nombre sugerido: `M19N5_mod8_avoid_5or7`

Objeto a materializar: un SRS relativo que codifique la negacion operacional de la conjetura 4.14 del paper: una trayectoria no convergente que evita simultaneamente las clases `5 mod 8` y `7 mod 8`, en el alfabeto y estilo de `rewriting-collatz`.

Hipotesis: la familia modulo 8 es una frontera mas prometedora que seguir variando S1/S2, porque el propio paper marco conjeturas residuales explicitas y el repo oficial ya prueba varios casos cercanos (`2,4,6 mod 8`, `3 mod 8`, `1or5`, `1or7`).

Por que no es redundante con S1/S2: no es una remocion de una regla dinamica de `S`. Es un desafio de evitacion de clases residuales, conectado con las conjeturas abiertas modulo 8. Si se prueba, no seria "S1/S2 con otro parametro", sino evidencia sobre una frontera distinta.

Herramienta que lo puede intentar: primero `rewriting-collatz`, porque ya tiene convenciones para archivos `collatz-T-*mod8.srs`; luego AProVE/Matchbox sobre TPDB/SRS generados. La herramienta ideal seria la que pueda producir CPF para hacerlo auditable.

Criterio de exito: `QED` o `YES` top-level para el SRS exacto de evitacion `5or7`, con traduccion documentada a la conjetura 4.14. Exito fuerte solo si ademas hay certificado o revision independiente de la traduccion.

Criterio de abandono: abandonar si la formalizacion requiere introducir tantas reglas auxiliares que ya no se pueda auditar su relacion con la conjetura 4.14, o si reproduce exactamente un archivo oficial existente bajo otro nombre.

Riesgo Yolcu-Aaronson-Heule: alto. El paper menciona explicitamente estas conjeturas y el repo oficial ya contiene casos `1or5` y `1or7`. El riesgo de terreno recorrido es alto; el punto nuevo debe ser la instancia exacta `5or7` si no aparece en el inventario oficial.

## Desafio 6: SRS de evitacion `1 mod 8`

Nombre sugerido: `M19N6_mod8_avoid_1`

Objeto a materializar: un SRS relativo para la conjetura 4.11: toda trayectoria no convergente debe encontrar algun valor `1 mod 8`. El desafio codifica la existencia de una trayectoria que evita `1 mod 8`.

Hipotesis: el caso `1 mod 8` puede ser menos combinado que `5or7` y servir como primer puente desde los archivos oficiales modulo 8 hacia una conjetura marcada como abierta.

Por que no es redundante con S1/S2: S1 remueve `ff* -> 0*`, que el manifiesto M19 asocia a residuo `1 mod 8`, pero no equivale por si solo a una evitacion global de la clase `1 mod 8`. Este desafio debe codificar una propiedad de trayectoria/residuo, no quitar una regla local.

Herramienta que lo puede intentar: `rewriting-collatz` si la codificacion se mantiene en su formato; AProVE/Matchbox como validacion cruzada; auditor de artefactos si aparece un candidato.

Criterio de exito: prueba automatica con una traduccion clara desde la conjetura 4.11 al SRS. Una prueba sin traduccion matematica revisada debe clasificarse solo como benchmark tecnico.

Criterio de abandono: abandonar si al intentar materializarlo se descubre que es equivalente a S1, o si depende de supuestos de alcanzabilidad que el SRS no expresa. Tambien abandonar si solo se obtiene una familia de archivos demasiado parametrica sin un problema exacto.

Riesgo Yolcu-Aaronson-Heule: alto. Es una conjetura explicita del paper y probablemente fue explorada por los autores. La novedad solo seria una prueba/certificado moderno o una formulacion reproducible que no exista en los logs oficiales.

## Orden recomendado

1. Generar primero S3, S12, S13 y S23, porque son cambios mecanicos sobre las 12 reglas ya auditadas y permiten comparar dificultad sin inventar semantica nueva.
2. Generar despues `avoid_5or7` y `avoid_1` solo si se puede documentar la traduccion desde las conjeturas modulo 8 sin ambiguedad.
3. No ampliar S1/S2 directamente hasta resolver Yices 1 real o Matchbox reproducible; la grilla chica ya descarto el primer escalon.

## Guardrails

- No llamar "resultado Collatz" a ningun `QED`/`YES`; como maximo es terminacion del SRS exacto o avance sobre una conjetura/debilitamiento.
- No aceptar `SAT`, `QED` interno, `YES` interno o `KILLED` como prueba top-level.
- No gastar presupuestos de miles de CPU-horas sin una asimetria clara entre los nuevos desafios.
- Si un desafio coincide con un archivo oficial de `rewriting-collatz`, reclasificarlo como reproduccion/control y quitarlo de la ola nueva.
- Si aparece top-level `YES`, congelar input, hashes, comando, versiones y pasar inmediatamente a CPF/CeTA o auditoria equivalente.
