# Reporte consolidado M12-M17: descartes disciplinados y sesgo de supervivencia

Fecha: 2026-04-25
Agente: ClaudeSocio (cierre autonomo)
Proyecto: Collatz Lab

## Resumen ejecutivo

Seis milestones (M12-M17) buscaron explicar por que el modelo geometrico independiente discrepa con datos reales en las colas de `blocks_to_descend`. Cuatro pistas fueron descartadas limpiamente. La quinta (M16) observo un sesgo de supervivencia condicional por profundidad en el rango de calibracion (n <= 5M). La sexta (M17) intento validar en holdout fresco [15M,25M] y obtuvo resultado negativo: 0/3 tests significativos para mejora del modelo corregido, y la tendencia de los ratios (aunque no significativa) apunta en direccion opuesta al train. El modelo cuantitativo no generaliza.

## Cronologia de descartes

### M12: Congruencia de `exit_v2 = 5`
- **Hipotesis:** `exit_v2 = 5` produce un sesgo aritmetico real en la expansion siguiente.
- **Resultado:** la congruencia `3^s q = 33 mod 64` es correcta, pero en la muestra completa (no condicionada por supervivencia) `exit_v2 = 5` vuelve al modelo geometrico.
- **Veredicto:** descartado. La senal venia de seleccion de cadenas, no de aritmetica local.

### M13: Sesgo de supervivencia orbital
- **Hipotesis:** las cadenas que sobreviven antes del primer descenso no muestrean uniformemente las transiciones locales.
- **Resultado:** el modelo independiente explica casi perfectamente el sesgo global por posicion final/interior. Queda un residuo en `prev_exit_v2 = 5` + `interior_block`.
- **Veredicto:** el fenomeno general (sesgo por posicion) queda explicado. El residuo pasa a M14.

### M14: Residuo interior despues de `prev_exit_v2 = 5`
- **Hipotesis:** la celda `prev_exit_v2 = 5` + `interior_block` tiene una dependencia real no capturada.
- **Resultado:** en holdout independiente (`5M-10M`), la diferencia cae a 0.009 con p = 0.43. No sobrevive.
- **Veredicto:** descartado. Senal post-hoc que no replica.

### M15: Modelo modular `q mod 8`
- **Hipotesis:** `q mod 8` tiene memoria suficiente entre bloques para mejorar prediccion de supervivencia orbital.
- **Resultado:** `q mod 8` predice `next_tail` (algebra esperable), pero la matriz de transicion mezcla casi uniforme en un paso (max TV = 0.00006).
- **Veredicto:** descartado/enfriado. Sin memoria marginal para cadenas completas.

### M16: Sobreproduccion de extremos y sesgo de profundidad
- **Hipotesis:** el gap modelo/real en colas de `blocks_to_descend` tiene una causa mecanica identificable.
- **Resultado:**
  - Gap significativo: ratio modelo/real = 1.09 en k=20 (p=0.0005 tras Bonferroni).
  - Autocorrelacion lag 1-5 ~ 0.
  - Bloque 1: drift exacto con teorico (-0.57536).
  - Bloques 8-10: drift ~0.013 mas negativo. E[exit_v2] sube a 2.012.
  - Modelo corregido por profundidad reduce gap 82% en k=20 (train), pero sobrecompensa en validacion split.
- **Veredicto:** hallazgo cualitativo. La causa es sesgo de supervivencia por profundidad, no correlacion local.

## Hallazgo principal

La sobreproduccion de extremos del modelo geometrico i.i.d. se descompone en:

| Componente | Contribucion estimada | Mecanismo |
| --- | ---: | --- |
| Finitud del rango | ~40% | Ruido de muestreo en colas con pocos eventos |
| Sesgo de drift global | ~30% | E[exit_v2] empirico ligeramente > 2 |
| Sesgo de profundidad | ~30% | Bloques tardios tienen drift mas negativo |

No es correlacion temporal (autocorrelacion ~0 en lags 1-5) sino condicionamiento global por supervivencia.

## Nivel de novedad

| Aspecto | Nivel | Justificacion |
| --- | :---: | --- |
| Modelo geometrico como baseline | 1 | Lagarias-Weiss 1992, Kontorovich-Lagarias 2009 |
| Sobreproduccion de extremos | 1.5 | Documentado por Bonacorsi-Bordoni 2026 |
| Descomposicion del gap | 2.5 | No encontrado en literatura |
| Sesgo de profundidad como causa | 2.5 | No encontrado en literatura |
| Modelo corregido por profundidad | 2 | Funciona en train, sobrecompensa en validacion |

**Nivel global: 2.5.** Identificacion propia de un mecanismo para un fenomeno ya observado. No publicable como paper independiente; util como resultado interno.

## Activos metodologicos

El valor principal de M12-M16 no es cientifico sino metodologico:

1. **Protocolo de preguntas antes/despues** de cada iteracion: evita autoengano.
2. **Compuertas de decision:** algebra antes que datos, web antes que claims, holdout separado de exploracion.
3. **Disciplina de descarte:** cuatro pistas abandonadas sin aferrarse.
4. **Correccion por comparaciones multiples:** Bonferroni aplicado consistentemente.
5. **Replica independiente:** CodexHijo2 replico algebra y transicion exactamente.

## Que no se logro

- No se probo ni refuto Collatz.
- No se encontro un modelo predictivo superior robusto (el corregido sobrecompensa).
- No se derivo algebraicamente por que E[exit_v2 | sobrevive d bloques] crece con d.
- No se alcanzo nivel de novedad publicable (4+).

## M17: Validacion en holdout fresco (resultado negativo)

M17 fue el test critico: validar el modelo depth-corrected en n in [15M, 25M], rango nunca tocado.

- 3 tests preregistrados (k=15,20,25), Bonferroni alfa = 0.017.
- **Resultado: 0/3 significativos para mejora del modelo corregido.**
- **Observacion:** la tendencia de los ratios i.i.d. apunta en direccion opuesta entre train (>1.0) y holdout (<1.0 para k>=20). Sin embargo, los CI del i.i.d. contienen 1.0 en los 3 tests, asi que el cambio de tendencia no es estadisticamente significativo.
- El modelo corregido tiene sesgo significativo de subproduccion en k=20 (CI [0.917, 0.984] no contiene 1.0), indicando que la correccion bootstrap no generaliza.
- La diferencia en escala es ln(5) ~= 1.6 (log natural) entre los rangos medios.
- **Implicacion:** el sesgo de profundidad de M16 se observa en el rango de calibracion pero no es transferible como correccion cuantitativa universal.

## Recomendacion para el futuro del proyecto

El arco de modelos estocasticos (M12-M17) queda cerrado. Opciones:

1. **Investigar la dependencia gap~log(n).** Por que el gap pasa de positivo a negativo? Esto podria tener una explicacion en terminos del overshoot del random walk, pero requiere teoria, no solo empiria. Ceiling: 3-4 si sale limpio.

2. **Cambio de direccion completo.** Inverse trees, potential cycles, L-functions, o formulaciones algebraicas.

3. **Cerrar el proyecto.** Documentar el repo como ejemplo de investigacion computacional disciplinada: hipotesis pequenas, controles negativos, holdout fresco, replicas y descartes sin inflar claims.

## Cierre

El resultado final de M12-M17 no es una pista fuerte hacia una prueba de Collatz. Es una mejora de metodo: el proyecto aprendio a convertir intuiciones prometedoras en experimentos falsables y a abandonar senales cuando no generalizan.

Si el trabajo continua, la proxima etapa deberia empezar con una pregunta nueva, no con una extension automatica de los modelos estocasticos ya cerrados.
