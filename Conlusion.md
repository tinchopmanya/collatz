# Conlusion dinamica

Ultima actualizacion: 2026-04-27
Tema: Collatz - arco estadistico cerrado; M19 reabierto solo para busqueda high-ceiling

## Estado final

El proyecto se cierra tras 18 milestones (M0-M17 + M18 de cierre). El arco estocastico M12-M17 queda cerrado como descarte disciplinado. M18 resolvio el ultimo hilo suelto y confirmo que no hay direccion computacional con ceiling suficiente para continuar.

## Reapertura condicionada M19

A pedido del usuario, se busco una posibilidad cientifica mas fuerte. La conclusion no reabre el arco estadistico: mas mediciones odd-to-odd tienen ceiling bajo. La unica via con potencial relativamente alto y compatible con trabajo computacional es cambiar de marco hacia sistemas de reescritura y pruebas automaticas de terminacion.

Decision M19:

```text
Reabrir solo para auditar y reproducir mixed-base rewriting / SAT termination.
```

Esto no afirma una prueba de Collatz. El objetivo realista es reproducir pruebas automaticas de debilitamientos no triviales y evaluar si existe una extension pequena, verificable y nueva.

## Resultado principal

El modelo geometrico i.i.d. (tail, exit_v2 ~ Geom(1/2), independientes por bloque) es estadisticamente indistinguible de la dinamica real Collatz odd-to-odd para n > 2.5M, en todos los umbrales testeados (k=10, 15, 20, 25).

La unica desviacion significativa es un efecto de finitud en n < 2.5M donde el modelo sobreproducce cadenas largas (~11% mas en k=20). Este efecto desaparece rapidamente y es esperable desde la teoria de random walks.

## Arco completo M12-M18

| Milestone | Hipotesis | Resultado |
| --- | --- | --- |
| M12 | exit_v2=5 congruencia | Algebra local, descartado |
| M13 | Sesgo supervivencia posicional | Explicado por posicion, no memoria |
| M14 | prev_exit_v2=5 + interior | Fallo holdout, descartado |
| M15 | q mod 8 marginal como memoria | Mezcla en 1 paso, cerrado |
| M16 | Sesgo profundidad explica gap | Observable en train con bin anomalo |
| M17 | Validacion holdout fresco | Negativo. Sin mejora |
| M18 | Ratio por rango de n | Sin tendencia. Efecto solo en n < 2.5M |

## Que se lleva el proyecto

1. **Infraestructura:** motor odd-to-odd, pipeline de experiments, datasets hasta 25M.
2. **Metodologia:** preregistro, holdout, Bonferroni, preguntas obligatorias, descarte limpio. 6 hipotesis formalmente testeadas y descartadas.
3. **Resultado negativo limpio:** no hay estructura oculta en la dinamica odd-to-odd que el modelo i.i.d. no capture, al menos en el rango computacionalmente accesible.
4. **Nivel de novedad final:** 2.5/5 (identificacion propia de mecanismo para fenomeno ya observado, con las salvedades documentadas).

## Que NO logro el proyecto

- No probo ni refuto Collatz.
- No produjo resultado publicable (nivel < 4).
- No encontro dependencia explotable entre bloques odd-to-odd consecutivos.

## Leccion principal

El modelo geometrico i.i.d. es tan bueno como baseline que romperlo requiere teoria, no mas computacion. Las 6 hipotesis computacionales testeadas fueron todas absorbidas por el modelo o por efectos de finitud. El proyecto demostro que es posible hacer investigacion computacional disciplinada sobre un problema famoso sin inflar claims.

## Proxima linea permitida

M19 - Auditoria y reproduccion de mixed-base rewriting para Collatz.

Condicion: primero reproducir resultados existentes. Solo despues buscar extensiones.
