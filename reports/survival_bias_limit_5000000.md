# Sesgo de supervivencia orbital hasta 5000000

Fecha: 2026-04-25
Script: [experiments/analyze_survival_bias.py](../experiments/analyze_survival_bias.py)

Salidas principales:

- [survival_bias_limit_5000000_position.csv](survival_bias_limit_5000000_position.csv)
- [survival_bias_limit_5000000_position_compare.csv](survival_bias_limit_5000000_position_compare.csv)
- [survival_bias_limit_5000000_depth.csv](survival_bias_limit_5000000_depth.csv)
- [survival_bias_limit_5000000_depth_compare.csv](survival_bias_limit_5000000_depth_compare.csv)
- [survival_bias_limit_5000000_margin.csv](survival_bias_limit_5000000_margin.csv)
- [survival_bias_limit_5000000_margin_compare.csv](survival_bias_limit_5000000_margin_compare.csv)
- [survival_bias_limit_5000000_duration.csv](survival_bias_limit_5000000_duration.csv)
- [survival_bias_limit_5000000_duration_compare.csv](survival_bias_limit_5000000_duration_compare.csv)
- [survival_bias_limit_5000000_prev_exit.csv](survival_bias_limit_5000000_prev_exit.csv)
- [survival_bias_limit_5000000_prev_exit_compare.csv](survival_bias_limit_5000000_prev_exit_compare.csv)
- [survival_bias_limit_5000000_prev_exit_position.csv](survival_bias_limit_5000000_prev_exit_position.csv)
- [survival_bias_limit_5000000_prev_exit_position_compare.csv](survival_bias_limit_5000000_prev_exit_position_compare.csv)

## Preguntas antes de iterar

```text
1. Estoy en algo virgen?
Respuesta: no en el marco general. Terras/Everett/Lagarias ya conectan stopping time, vectores de paridad y modelos probabilisticos; Campbell 2025 trabaja bloques de Mersenne; Bonacorsi/Bordoni 2026 modelan stopping times con heterogeneidad modular.

2. Alguien busco esto antes?
Respuesta: si a nivel amplio. No encontramos aun esta medicion exacta por posicion de bloque, profundidad, margen logaritmico y `prev_exit_v2` en coordenadas de bloques Mersenne.

3. Que parte exacta podria ser nueva?
Respuesta: separar si el sesgo de `next_tail = 1` viene de bloques finales, profundidad/margen de supervivencia, o una dependencia residual despues de ciertos `prev_exit_v2`.

4. Que probabilidad real hay de descubrir algo relevante?
Respuesta: baja para una prueba; moderada para explicar por que el modelo independiente sobreproduce extremos.

5. Que evidencia haria que sigamos?
Respuesta: una diferencia real-modelo que sobreviva despues de separar final/interior.

6. Que evidencia haria que abandonemos?
Respuesta: que todo el sesgo quede explicado por posicion final/interior igual que en el modelo.
```

## Comando reproducible

```powershell
python experiments\analyze_survival_bias.py --limit 5000000 --max-blocks 256 --seed 20260425 --out-dir reports --prefix survival_bias_limit_5000000
```

Modelo:

```text
tail ~ Geom(1/2)
exit_v2 ~ Geom(1/2)
local_log = tail * log(3/2) - exit_v2 * log(2)
```

Se generan la misma cantidad de cadenas reales y modeladas:

```text
reales: impares 3 <= n <= 5000000
modelo: 2499999 cadenas independientes
```

Cada cadena se corta al primer bloque cuyo valor queda por debajo del valor inicial.

## Resultado 1: posicion final/interior

| Posicion | Real count | Modelo count | tail=1 real | tail=1 modelo | Diff | IC95 | Exp real | Exp modelo |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| only_block | 1784316 | 1784459 | 0.70054800 | 0.70110213 | -0.00055413 | [-0.00150428, 0.00039602] | 0.00000000 | 0.00000000 |
| first_block | 715683 | 715540 | 0.00000000 | 0.00000000 | 0.00000000 | [0.00000000, 0.00000000] | 1.00000000 | 1.00000000 |
| interior_block | 1145601 | 1146649 | 0.38646876 | 0.38606060 | 0.00040816 | [-0.00085247, 0.00166879] | 0.46453434 | 0.46491559 |
| final_block | 715683 | 715540 | 0.68311110 | 0.68213098 | 0.00098012 | [-0.00054502, 0.00250526] | 0.00000000 | 0.00000000 |

Lectura:

- El sesgo grueso de supervivencia lo explica casi perfectamente el modelo independiente.
- Los bloques finales tienen `tail=1` cerca de `0.683`, porque deben producir descenso.
- Los bloques interiores tienen `tail=1` cerca de `0.386`, porque deben seguir vivos.
- Real y modelo coinciden dentro de intervalos para estas posiciones globales.

Esto corrige una interpretacion excesiva de la ola anterior: gran parte del sesgo no es una rareza aritmetica, sino un efecto esperado de condicionar por supervivencia y por descenso.

## Resultado 2: profundidad

La profundidad tampoco muestra una gran ruptura global.

| Profundidad | Real count | Modelo count | tail=1 real | tail=1 modelo | Diff | IC95 | Exp real | Exp modelo |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| depth_10 | 31582 | 31746 | 0.50129821 | 0.50311850 | -0.00182030 | [-0.00960881, 0.00596822] | 0.27898803 | 0.28327978 |
| depth_15 | 9011 | 9259 | 0.50893353 | 0.49789394 | 0.01103958 | [-0.00346114, 0.02554031] | 0.27510820 | 0.28836807 |
| depth_20 | 2939 | 3107 | 0.49914937 | 0.50209205 | -0.00294268 | [-0.02815934, 0.02227398] | 0.29363729 | 0.28644995 |
| depth_21_plus | 12840 | 14223 | 0.51596573 | 0.49637910 | 0.01958663 | [0.00766010, 0.03151316] | 0.28130841 | 0.29079660 |

La cola `depth_21_plus` queda como pequena senal a vigilar: tiene mas `tail=1` real que el modelo y menor expansion, pero mezcla profundidades distintas y tamanos de muestra menores.

## Resultado 3: margen logaritmico

Por margen `log(current/start)` antes del bloque, real y modelo tambien coinciden bien.

| Margen | Real count | Modelo count | tail=1 real | tail=1 modelo | Diff | IC95 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| margin_0_0p25 | 3042169 | 3041940 | 0.50003534 | 0.50021368 | -0.00017834 | [-0.00097296, 0.00061627] |
| margin_0p25_0p5 | 148700 | 148596 | 0.50049765 | 0.50057875 | -0.00008110 | [-0.00367579, 0.00351358] |
| margin_0p5_1 | 515595 | 515318 | 0.50020074 | 0.50030467 | -0.00010393 | [-0.00203432, 0.00182646] |
| margin_1_2 | 416891 | 415823 | 0.50006357 | 0.50036434 | -0.00030077 | [-0.00244864, 0.00184710] |
| margin_2_4 | 205079 | 206164 | 0.50406429 | 0.50019887 | 0.00386542 | [0.00080908, 0.00692175] |
| margin_4_plus | 32849 | 34347 | 0.49520533 | 0.49058142 | 0.00462391 | [-0.00293822, 0.01218605] |

No aparece una ley simple tipo:

```text
mas margen => mucho mas/menos tail=1
```

## Resultado 4: residuo condicionado por `prev_exit_v2 = 5`

Aqui queda la senal mas interesante.

| Condicion | Real count | Modelo count | tail=1 real | tail=1 modelo | Diff tail=1 | IC95 tail=1 | Exp real | Exp modelo | Diff exp | IC95 exp |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
| prev_exit_v2_05 | 5385 | 5500 | 0.54447539 | 0.50345455 | 0.04102085 | [0.02227129, 0.05977041] | 0.25979573 | 0.28127273 | -0.02147700 | [-0.03816197, -0.00479203] |
| prev_exit_v2_05__final_block | 1959 | 2048 | 0.70495151 | 0.66748047 | 0.03747104 | [0.00876201, 0.06618006] | 0.00000000 | 0.00000000 | 0.00000000 | [0.00000000, 0.00000000] |
| prev_exit_v2_05__interior_block | 3426 | 3452 | 0.45271454 | 0.40614137 | 0.04657317 | [0.02320157, 0.06994477] | 0.40834793 | 0.44814600 | -0.03979807 | [-0.06316752, -0.01642863] |

Esto es el punto fino:

- Si solo fuera sesgo de bloque final, la diferencia desapareceria en `interior_block`.
- No desaparece.
- En bloques interiores despues de `prev_exit_v2 = 5`, el real tiene mas `tail=1` que el modelo y menor expansion.

Por lo tanto:

```text
La ola 12 descarto `exit_v2 = 5` como ley local estatica.
La ola 13 muestra que aun queda una dependencia orbital condicionada por supervivencia + prev_exit_v2 = 5.
```

No es una prueba ni un gran avance, pero si una pista mejor formulada.

## Preguntas despues de iterar

```text
1. La respuesta sobre originalidad cambio?
Respuesta: si, se volvio mas precisa. El sesgo global de supervivencia no es nuevo ni sorprendente; el residuo interior condicionado por `prev_exit_v2 = 5` es la parte que merece revision.

2. La probabilidad de relevancia subio, bajo o quedo igual?
Respuesta: subio ligeramente respecto del cierre de la ola 12, porque no todo se explico por bloque final/interior. Pero sigue siendo una senal experimental, no un theorem candidate.

3. Se encontro una senal robusta o solo seleccion?
Respuesta: ambas cosas. La seleccion global esta explicada por el modelo; queda una senal residual en `prev_exit_v2 = 5` incluso en bloques interiores.

4. Que aprendimos que no sabiamos antes?
Respuesta: el modelo independiente captura muy bien la geometria gruesa de supervivencia. La falla no esta en profundidad ni margen global, sino en dependencias condicionadas mas finas.

5. Conviene seguir, escalar, formalizar o abandonar?
Respuesta: no escalar ciegamente. Conviene aislar `prev_exit_v2 = 5` + bloque interior por residuos/margen/profundidad para ver si el efecto tiene causa modular.

6. Cual es la siguiente pregunta minima?
Respuesta: dentro de `prev_exit_v2 = 5` e interior, que variable explica el exceso de `next_tail = 1`: residuo de `q`, profundidad, margen o clase del siguiente impar?
```

## Veredicto

La hipotesis:

```text
el sesgo de la ola 12 era solamente mezcla de bloques finales/interiores
```

queda parcialmente confirmada, pero no completamente.

El resultado mas honesto es:

```text
El modelo independiente explica la supervivencia global casi perfecto, pero falla de forma localizada despues de `prev_exit_v2 = 5`, incluso entre bloques interiores.
```

La siguiente investigacion no debe vender esto como prueba. Debe tratarlo como una dependencia fina y buscar su causa modular.

## Fuentes externas usadas para situar originalidad

- [Mersenne Block Dynamics: A Framework for the Collatz Conjecture, Stephen R. Campbell, 2025](https://ai.vixra.org/pdf/2512.0068v1.pdf)
- [Bayesian Modeling of Collatz Stopping Times, Bonacorsi y Bordoni, arXiv:2603.04479, 2026](https://arxiv.org/abs/2603.04479)
