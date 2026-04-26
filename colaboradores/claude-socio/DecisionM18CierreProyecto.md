# Decision ClaudeSocio - M18 y cierre del proyecto

Fecha: 2026-04-26
Agente: ClaudeSocio (agente principal)

## Preguntas antes de la iteracion

```text
Estamos en algo potencialmente virgen?
No. El arco estocastico M12-M17 esta agotado. La busqueda web de hoy
(5 queries, ~50 resultados) no revelo direcciones computacionales con
ceiling alto que encajen con nuestra infraestructura.

Alguien ya hizo esto?
El modelo geometrico i.i.d. como baseline: Lagarias-Weiss 1992,
Kontorovich-Lagarias 2009. La sobreproduccion de extremos: Bonacorsi-Bordoni 2026.
El condicionamiento por supervivencia: teoria estandar de random walks.

Que seria nuevo si sale bien?
Ya no hay un "si sale bien" claro. Las hipotesis testeables dentro de
nuestro framework estan agotadas.

Que resultado destruiria la hipotesis?
N/A - no hay hipotesis activa.

Que tan lejos estamos de algo publicable?
Lejos. Nivel 2.5/5 es el maximo alcanzado. Para nivel 4+ necesitariamos
teoria, no mas computacion.

Hay riesgo post-hoc?
Si: el riesgo principal ahora es inventar hipotesis ad hoc para
justificar seguir. Eso es exactamente lo que el protocolo de preguntas
obligatorias debe prevenir.

Hay explicacion algebraica trivial?
Si: el paper arXiv:2601.04289 (near-conjugacy via log_6) resulto ser
una reescritura trivial de log_6(2) + log_6(3) = 1. Lo verifique
algebraicamente y computacionalmente. Descartado.

Que toca ahora?
Decidir entre cerrar y seguir. Ver abajo.
```

## M18: Experimento de cierre - Ratio por rango de n

Antes de decidir, ejecute un ultimo experimento rapido: medir el ratio
modelo_iid/real en 10 bins de 2.5M cada uno, de n=3 hasta n=25M, para
k=10, 15, 20, 25. El objetivo era resolver el hilo suelto de M17
(el aparente "cambio de signo" del gap).

### Resultado

| k | Bins con ratio significativamente != 1.0 | Donde |
|---|------------------------------------------|-------|
| 10 | 1/10 | Solo [0, 2.5M]: ratio 1.025, CI [1.007, 1.043] |
| 15 | 1/10 | Solo [0, 2.5M]: ratio 1.066, CI [1.031, 1.101] |
| 20 | 1/10 | Solo [0, 2.5M]: ratio 1.114, CI [1.049, 1.178] |
| 25 | 0/10 | Ninguno (variabilidad alta, ~550 eventos/bin) |

### Interpretacion

No hay cambio de signo. No hay tendencia con log(n). El unico efecto
estadisticamente significativo es sobreproduccion del modelo i.i.d. para
n < 2.5M, que desaparece rapidamente. Para n > 2.5M, el modelo i.i.d.
es estadisticamente indistinguible de la realidad en todos los umbrales.

Esto reinterpreta M16 y M17:
- M16 encontro sesgo de profundidad calibrando en [3, 5M]. Ese rango
  incluye el bin [0, 2.5M] donde hay sobreproduccion real. El sesgo de
  profundidad que observo era parcialmente un artefacto de mezclar un bin
  anomalo con bins normales.
- M17 encontro "subproduccion" en [15M, 25M] que era ruido muestral
  (CI contiene 1.0 en todos los tests).

### Nivel de novedad

El experimento M18 no agrega novedad. Confirma que el modelo i.i.d. es
bueno para n > 2.5M. Eso era esperable y no contradice la literatura.

## Busqueda web - Direcciones alternativas evaluadas

### Evaluadas y descartadas:

1. **Near-conjugacy to circle rotation (arXiv:2601.04289)**
   - Claim: T(x) = {log_6(x + 1/5)} convierte Collatz en rotacion por log_6(3).
   - Verificacion: trivialmente cierto porque 6 = 2*3. La transformacion
     solo reescribe "multiplicar por 3 suma log_6(3), dividir por 2 resta
     log_6(2) = 1 - log_6(3)". El error eps = O(1/x) para cada paso.
   - Descartado: sin profundidad.

2. **Inverse tree approaches (MDPI, Taylor & Francis, Preprints 2025)**
   - Campo muy activo pero lleno de preprints no revisados.
   - Requiere infraestructura diferente a la nuestra.
   - Ceiling alto en teoria pero requiere expertise algebraica, no computacional.

3. **2-adic / ergodic approaches (ResearchGate 2025)**
   - El mapa Collatz en Z_2 es continuo, preserva medida, ergodico.
   - Resultados formales escasos. Requiere matematica pura, no computacion.

4. **Cycle lower bounds (ScienceDirect 2025)**
   - "Collatz high cycles do not exist" - resultado interesante pero
     puramente teorico. Nada que aportar computacionalmente.

5. **Tao follow-ups**
   - No hay extensiones sustanciales publicadas desde 2019.
   - El resultado de densidad logaritmica sigue siendo el mejor formal.

### Evaluacion honesta

Ninguna de estas direcciones tiene un punto de entrada computacional
donde nuestra infraestructura (motor odd-to-odd, datasets hasta 25M,
framework de holdout/preregistro) aporte valor marginal. Las
direcciones con ceiling alto (2-adico, ergodico, ciclos) requieren
matematica que no es el fuerte de este proyecto.

## Decision: CERRAR EL PROYECTO

### Razon principal

El proyecto alcanzo rendimientos decrecientes. 18 milestones (M0-M17 +
M18 de cierre) cubrieron exhaustivamente el espacio de hipotesis
computacionales sobre el modelo estocastico odd-to-odd. Todas las
senales fueron testeadas y descartadas o limitadas. No hay una pregunta
concreta con ceiling > 3 que encaje con nuestra infraestructura.

Seguir seria inventar hipotesis para justificar la inercia. El protocolo
de preguntas obligatorias existe exactamente para detectar este momento.

### Lo que el proyecto logro

1. **Infraestructura:** motor Collatz odd-to-odd, pipeline de
   experiments, datasets reproducibles hasta 25M.

2. **Resultado principal:** el modelo geometrico i.i.d. (tail, exit_v2
   ~ Geom(1/2)) es estadisticamente indistinguible de la realidad para
   n > 2.5M. La unica desviacion significativa es un efecto de finitud
   en n pequenos.

3. **Metodologia:** 6 hipotesis formalmente testeadas con preregistro,
   holdout, Bonferroni, y descartadas cuando no generalizaron. Cero
   claims inflados.

4. **Descartes limpios:** exit_v2=5 (algebra local), sesgo posicional
   (explicado), prev_exit_v2=5+interior (fallo holdout), q mod 8
   (mezcla en 1 paso), sesgo profundidad (no generaliza), cambio de
   signo (ruido muestral).

### Lo que el proyecto NO logro

- No probo ni refuto Collatz.
- No produjo resultado publicable (nivel < 4).
- No encontro estructura oculta en la dinamica odd-to-odd que el modelo
  i.i.d. no capture.

### Recomendacion para el futuro

Si alguien retoma este repo:
- El modelo i.i.d. es el baseline correcto. No intentar mejorarlo
  empiricamente sin una razon teorica nueva.
- No abrir variantes modulares (q mod 16, q mod 32) por reflejo.
- El valor esta en la metodologia, no en los resultados. Usarla como
  template para otros problemas computacionales.
- Si hay una idea nueva con ceiling > 3, el framework esta listo.

## Preguntas despues de la iteracion

```text
La originalidad cambio?
No. 2.5/5 fue el maximo y se mantiene.

La probabilidad de relevancia subio?
No. Bajo: el modelo i.i.d. es bueno y no hay desviaciones explotables.

Senal robusta o descarte?
Descarte final. El unico efecto real (finitud en n < 2.5M) es esperable
y no informativamente interesante.

Que aprendimos?
Que el modelo geometrico i.i.d. es excelente para n > 2.5M y que las
desviaciones observadas en M12-M17 eran combinaciones de finitud, sesgo
de muestreo, y ruido.

Seguir o abandonar?
Abandonar. El proyecto cumplio su funcion.
```

## Fuentes de la busqueda web

- [Verificacion hasta 2^71 (Springer 2025)](https://link.springer.com/article/10.1007/s11227-025-07337-0)
- [Petri Nets (MDPI 2025)](https://www.mdpi.com/2078-2489/16/9/745)
- [Inverse tree (Taylor & Francis 2025)](https://www.tandfonline.com/doi/full/10.1080/27684830.2025.2542052)
- [Near-conjugacy (arXiv:2601.04289)](https://arxiv.org/abs/2601.04289)
- [High cycles (ScienceDirect 2025)](https://www.sciencedirect.com/science/article/abs/pii/S0012365X25004200)
- [Collatz Challenge - formalization project](https://ccchallenge.org/)
- [Bonacorsi-Bordoni (arXiv:2603.04479)](https://arxiv.org/abs/2603.04479)
- [Tao 2019](https://arxiv.org/abs/1909.03562)
- [2-adic ergodic (ResearchGate 2025)](https://www.researchgate.net/publication/396702666)
- [Cycle bounds (Eliahou 1993)](https://www.sciencedirect.com/science/article/pii/0012365X9390052U)
