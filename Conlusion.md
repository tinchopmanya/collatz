# Conlusion dinamica

Ultima actualizacion: 2026-04-25
Tema activo: Collatz - M17 completado (resultado negativo), arco M12-M17 cerrado
Revision: incorpora feedback del revisor critico externo

## Preguntas antes de la iteracion (M17)

```text
Estoy en algo virgen?
No. El hallazgo M16 (sesgo profundidad) es propio pero nivel 2.5/5. La busqueda web
no encontro la descomposicion drift-por-profundidad como tal, pero el fenomeno subyacente
(sobreproduccion de extremos) ya esta documentado por Bonacorsi-Bordoni (2026), y el
mecanismo (condicionamiento por supervivencia cambia el drift) es conocido en random walks.

Puedo descubrir algo con esto?
Solo si el modelo corregido funciona en holdout fresco [15M,25M].

Ya alguien estuvo buscando esto?
No encontrado en la busqueda realizada. Eso no equivale a "nadie lo hizo".

Que tan lejos estoy de descubrir algo?
A un experimento de distancia: holdout fresco.
```

## Observacion principal de M17

En holdout [15M,25M], la tendencia observada de los ratios i.i.d. apunta a subproduccion (ratios < 1.0 para k >= 20), mientras que en train (n <= 5M) apuntaba a sobreproduccion (ratios > 1.0).

| Rango | ratio_iid k=20 | ratio_corr k=20 | Tendencia observada |
| --- | --- | --- | --- |
| Train (n <= 5M) | 1.041 | 1.023 | Sobreproduccion |
| Holdout (15M-25M) | 0.967 | 0.949 | Subproduccion |

**Matiz importante:** en los tests preregistrados (k=15,20,25), los CI del modelo i.i.d. contienen 1.0 en los tres casos. Por lo tanto, el cambio de tendencia es sugestivo pero **no estadisticamente significativo**. No se puede afirmar como hecho robusto.

El modelo depth-corrected tiene un sesgo significativo de subproduccion en k=20 (CI [0.917, 0.984] no contiene 1.0), lo que indica que la correccion bootstrap no generaliza al holdout.

## M16 se reinterpreta

El sesgo por profundidad observado en M16 (bloques tardios con drift mas negativo) es un fenomeno observable en el rango de calibracion. Pero no constituye una correccion universal. El mecanismo subyacente (condicionamiento por supervivencia) es conocido en la teoria de random walks; lo propio del proyecto fue medirlo en el contexto Collatz concreto.

## Arco completo M12-M17

| Milestone | Hipotesis | Resultado |
| --- | --- | --- |
| M12 | exit_v2=5 congruencia | Algebra local, descartado |
| M13 | Sesgo supervivencia posicional | Explicado por posicion, no memoria |
| M14 | prev_exit_v2=5 + interior | Fallo holdout, descartado |
| M15 | q mod 8 marginal como memoria | Mezcla en 1 paso, cerrado |
| M16 | Sesgo profundidad explica gap | Observable en train, no universal |
| M17 | Validacion holdout fresco | Negativo. Tendencia cambia, no significativa |

## Preguntas despues de la iteracion (M17)

```text
La originalidad cambio?
No. Se mantiene en 2.5/5. M17 es un resultado negativo limpio.

La probabilidad de relevancia subio?
No. El modelo no generaliza.

Senal robusta o descarte?
El sesgo de profundidad se observa en su rango. El modelo cuantitativo es descartable.
La tendencia gap~log(n) es una observacion en dos puntos, no un hallazgo.

Que aprendimos?
Que la relacion modelo/real parece depender del rango de n. Los ratios i.i.d. son > 1
en train y < 1 en holdout, pero la diferencia no es significativa en holdout. Esto
podria ser variabilidad muestral o un efecto real que requiere mas rangos para confirmar.

Seguir o abandonar?
Cerrar el arco estocastico. El proyecto puede continuar con direccion nueva o cerrarse.
```

## Estado del proyecto

El activo principal del proyecto es la metodologia de descarte disciplinado: preregistro, holdout separado, preguntas obligatorias, descarte limpio. 6 milestones de hipotesis testeadas y descartadas o limitadas, sin afirmaciones infladas.

## Opciones futuras

1. Investigar tendencia gap~log(n) con mas rangos de n (requiere teoria, no solo datos).
2. Cambio de direccion: inverse trees, 2-adicos, L-functions, potential cycles.
3. Cierre de proyecto con documento metodologico.
