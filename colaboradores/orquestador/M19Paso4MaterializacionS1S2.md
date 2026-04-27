# M19 paso 4 - materializacion exacta de S1/S2

Fecha: 2026-04-27
Responsable: Codex orquestador
Estado: desafio publicado convertido a archivos reproducibles

## Preguntas antes

- Estamos en terreno virgen?
  - Parcialmente. La linea rewriting/SAT no es virgen, pero los desafios S1/S2 son explicitamente abiertos en el paper si no hubo resolucion posterior.
- Podemos descubrir algo con esto?
  - No por generar archivos. Si por usarlos para probar herramientas modernas o certificar un resultado nuevo.
- Ya alguien estuvo buscando esto?
  - Si. Yolcu-Aaronson-Heule reportan miles de CPU-horas sin encontrar interpretaciones para S1/S2.
- Que tan lejos estamos?
  - Un paso mas cerca: ya no hablamos de S1/S2 en abstracto; ahora tenemos archivos concretos y verificables.

## Verificacion de notacion

Se descargo el PDF de Yolcu-Aaronson-Heule y se extrajo el texto para verificar la correspondencia entre la notacion del paper y el alfabeto ASCII del repo `rewriting-collatz`.

Mapa confirmado:

| ASCII | Paper |
| --- | --- |
| `a` | `f` |
| `b` | `t` |
| `c` | marcador izquierdo |
| `d` | marcador final |
| `e` | `0` |
| `f` | `1` |
| `g` | `2` |

Con ese mapa:

| Paper | ASCII |
| --- | --- |
| `ff* -> 0*` | `aad -> ed` |
| `tf* -> *` | `bad -> d` |
| `t* -> 2*` | `bd -> gd` |

El archivo generado `m19_collatz_S_full.srs` fue comparado contra `rules/collatz-S.srs` del repo externo y no hubo diferencias.

## Archivos generados

Script:

```text
scripts/m19_generate_rewriting_challenges.py
```

Salida:

```text
reports/m19_rewriting_challenges/
```

Archivos principales:

- `m19_collatz_S_full.srs`
- `m19_collatz_S_full.tpdb`
- `m19_collatz_S1_without_ff_end_to_0_end.srs`
- `m19_collatz_S1_without_ff_end_to_0_end.tpdb`
- `m19_collatz_S2_without_tf_end_to_end.srs`
- `m19_collatz_S2_without_tf_end_to_end.tpdb`
- `README.md`

## Importancia

Antes, el riesgo era hablar de "S1/S2" sin saber si estabamos apuntando al objeto exacto.

Ahora la frontera quedo materializada:

```text
S1 = S sin aad -> ed
S2 = S sin bad -> d
```

Esto permite:

- correr herramientas externas contra archivos TPDB;
- comparar resultados entre provers;
- documentar fallos de forma reproducible;
- preparar un intento serio de certificacion si alguna herramienta encuentra prueba.

## Preguntas despues

- Avanzamos?
  - Si, de investigacion bibliografica a artefacto reproducible.
- Es un descubrimiento?
  - No. Es preparacion rigurosa de una frontera abierta publicada.
- Estamos en algo virgen?
  - Solo en el sentido estrecho: buscar una prueba moderna para S1/S2 sigue siendo una zona potencialmente abierta.
- Que destruye esta ruta?
  - Que herramientas modernas tampoco encuentren nada, o que exista una resolucion posterior no detectada.
- Que toca?
  - Ejecutar el workflow CI y despues probar los TPDB S1/S2 con herramientas de terminacion modernas.
