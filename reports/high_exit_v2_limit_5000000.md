# Salidas con alta valuacion 2-adica hasta 5000000

Fecha: 2026-04-25
Script: [experiments/analyze_high_exit_v2.py](../experiments/analyze_high_exit_v2.py)
Salidas CSV:

- [high_exit_v2_limit_1000000_threshold_compare.csv](high_exit_v2_limit_1000000_threshold_compare.csv)
- [high_exit_v2_limit_1000000_exact_compare.csv](high_exit_v2_limit_1000000_exact_compare.csv)
- [high_exit_v2_limit_5000000_threshold_compare.csv](high_exit_v2_limit_5000000_threshold_compare.csv)
- [high_exit_v2_limit_5000000_exact_compare.csv](high_exit_v2_limit_5000000_exact_compare.csv)
- [high_exit_v2_limit_5000000_thresholds.csv](high_exit_v2_limit_5000000_thresholds.csv)
- [high_exit_v2_limit_5000000_exact.csv](high_exit_v2_limit_5000000_exact.csv)

## Preguntas antes de iterar

```text
1. Estoy en algo virgen?
Respuesta: no en el marco general. Bloques, salida, r(x), mezcla y modelos geometricos ya fueron estudiados, especialmente por Campbell 2025.

2. Alguien busco esto antes?
Respuesta: si a nivel general. Campbell 2025 trabaja r(x) y mezcla; Bonacorsi/Bordoni 2026 trabaja estructura modular; Chang 2026 explora dependencias y obstaculos con LLMs. No encontramos aun la tabla exacta exit_v2 >= k -> sesgo siguiente real/modelo con intervalos.

3. Que parte exacta podria ser nueva?
Respuesta: la medicion reproducible por umbrales exit_v2 >= k y por valores exactos exit_v2 = k, comparando contra modelo geometrico independiente.

4. Que probabilidad real hay de descubrir algo relevante?
Respuesta: baja para una prueba; moderada-baja para una nota experimental util si el sesgo persiste y no es ruido.

5. Que evidencia haria que sigamos?
Respuesta: diferencia real-modelo estable, con intervalo que no cruce cero, al subir rango.

6. Que evidencia haria que abandonemos?
Respuesta: efecto no monotono, cambio de signo o desaparicion al escalar.
```

## Comandos reproducibles

```powershell
python experiments\analyze_high_exit_v2.py --limit 1000000 --max-blocks 256 --seed 20260425 --out-dir reports --prefix high_exit_v2_limit_1000000
python experiments\analyze_high_exit_v2.py --limit 5000000 --max-blocks 256 --seed 20260425 --out-dir reports --prefix high_exit_v2_limit_5000000
```

Modelo:

```text
s ~ Geom(1/2)
r ~ Geom(1/2)
log factor = s log(3/2) - r log(2)
```

La comparacion toma pares de bloques consecutivos y condiciona por el `exit_v2` del bloque anterior.

## Resultado por umbral en 5000000

| Condicion previa | Pares reales | Pares modelo | P siguiente exp real | P siguiente exp modelo | Diferencia real-modelo | IC95 bajo | IC95 alto | z |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| exit_v2 >= 1 | 1861284 | 1862189 | 0.28591607 | 0.28627331 | -0.00035724 | -0.00127533 | 0.00056086 | -0.762654 |
| exit_v2 >= 2 | 442078 | 442636 | 0.28537724 | 0.28597990 | -0.00060266 | -0.00248531 | 0.00127999 | -0.627421 |
| exit_v2 >= 3 | 113185 | 113804 | 0.28393338 | 0.28477031 | -0.00083692 | -0.00454853 | 0.00287469 | -0.441956 |
| exit_v2 >= 4 | 29008 | 29138 | 0.27633756 | 0.28608690 | -0.00974933 | -0.01705760 | -0.00244107 | -2.614671 |
| exit_v2 >= 5 | 7128 | 7269 | 0.25968013 | 0.28201954 | -0.02233940 | -0.03685220 | -0.00782660 | -3.017007 |
| exit_v2 >= 6 | 1743 | 1769 | 0.25932301 | 0.28434144 | -0.02501843 | -0.05443342 | 0.00439657 | -1.667045 |
| exit_v2 >= 7 | 463 | 443 | 0.23110151 | 0.28668172 | -0.05558020 | -0.11256877 | 0.00140837 | -1.911562 |
| exit_v2 >= 8 | 131 | 123 | 0.32824427 | 0.27642276 | 0.05182151 | -0.06093096 | 0.16457399 | 0.900824 |

## Resultado exacto en 5000000

| Condicion previa | Pares reales | Pares modelo | P siguiente exp real | P siguiente exp modelo | Diferencia real-modelo | IC95 bajo | IC95 alto | z |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| exit_v2 = 1 | 1419206 | 1419553 | 0.28608391 | 0.28636479 | -0.00028088 | -0.00133250 | 0.00077073 | -0.523511 |
| exit_v2 = 2 | 328893 | 328832 | 0.28587413 | 0.28639853 | -0.00052440 | -0.00270893 | 0.00166013 | -0.470498 |
| exit_v2 = 3 | 84177 | 84666 | 0.28655096 | 0.28431720 | 0.00223376 | -0.00207469 | 0.00654220 | 1.016183 |
| exit_v2 = 4 | 21880 | 21869 | 0.28176417 | 0.28743884 | -0.00567467 | -0.01413109 | 0.00278174 | -1.315257 |
| exit_v2 = 5 | 5385 | 5500 | 0.25979573 | 0.28127273 | -0.02147700 | -0.03816197 | -0.00479203 | -2.522924 |
| exit_v2 = 6 | 1280 | 1326 | 0.26953125 | 0.28355958 | -0.01402833 | -0.04837162 | 0.02031496 | -0.800608 |
| exit_v2 = 7 | 332 | 320 | 0.19277108 | 0.29062500 | -0.09785392 | -0.16324166 | -0.03246617 | -2.933175 |
| exit_v2 = 8 | 85 | 93 | 0.21176471 | 0.29032258 | -0.07855787 | -0.20526553 | 0.04814978 | -1.215187 |

## Comparacion 1000000 vs 5000000

| Condicion | Diff en 1000000 | IC95 1000000 | Diff en 5000000 | IC95 5000000 |
| --- | ---: | --- | ---: | --- |
| exit_v2 >= 4 | -0.01723013 | [-0.03351203, -0.00094824] | -0.00974933 | [-0.01705760, -0.00244107] |
| exit_v2 >= 5 | -0.04477799 | [-0.07673244, -0.01282355] | -0.02233940 | [-0.03685220, -0.00782660] |
| exit_v2 >= 6 | -0.00814257 | [-0.07442103, 0.05813588] | -0.02501843 | [-0.05443342, 0.00439657] |
| exit_v2 >= 7 | 0.19246032 | [0.04624857, 0.33867207] | -0.05558020 | [-0.11256877, 0.00140837] |

Al escalar de un millon a cinco millones, la senal `>=5` se mantiene negativa, pero baja de tamano. La inversion en `>=7` del primer millon desaparece. Esto indica que la muestra de un millon era demasiado chica para umbrales altos.

## Lectura

Hay una senal real-modelo detectable para salidas con `exit_v2 >= 4` y `exit_v2 >= 5`: despues de esas salidas, la cadena real tiene menor probabilidad de que el siguiente bloque sea expansivo que el modelo independiente.

Pero la senal no es una ley monotona simple:

- `exit_v2 = 5` es negativa y con intervalo bajo cero.
- `exit_v2 = 6` es negativa pero no concluyente.
- `exit_v2 = 7` vuelve a ser negativa y concluyente en valor exacto, pero con solo `332` pares reales.
- `exit_v2 >= 8` ya no es confiable por muestra escasa.

Esto sugiere que la variable correcta podria no ser solamente "exit_v2 alto", sino una clase modular mas especifica asociada a ciertos valores de `exit_v2`.

## Preguntas despues de iterar

```text
1. La respuesta sobre originalidad cambio?
Respuesta: no mucho. Seguimos en una extension fina de ideas existentes, no en terreno virgen amplio.

2. La probabilidad de relevancia subio, bajo o quedo igual?
Respuesta: subio un poco respecto a la novena ola, porque el efecto exit_v2 >= 5 persiste al escalar a 5M. Pero sigue lejos de ser un resultado fuerte.

3. Se encontro una senal robusta o solo ruido?
Respuesta: senal moderada para exit_v2 >= 4/5; ruido o muestra insuficiente para umbrales mayores.

4. Que aprendimos que no sabiamos antes?
Respuesta: la diferencia no es "expansion despues de expansion"; esta mas ligada a ciertos exponentes de salida, especialmente 5.

5. Conviene seguir, escalar, formalizar o abandonar?
Respuesta: conviene una iteracion mas, pero no escalar ciegamente. Hay que derivar congruencias para exit_v2 = 5 y exit_v2 = 7.

6. Cual es la siguiente pregunta minima?
Respuesta: que clase modular exacta deja exit_v2 = 5, y por que esa clase reduce la expansion del siguiente bloque?
```

## Veredicto

No hay descubrimiento revolucionario. Si hay una grieta concreta:

```text
exit_v2 = 5 parece dejar al siguiente bloque menos expansivo que el modelo independiente.
```

La forma correcta de seguir no es "mas computo" sino "mas aritmetica": derivar la congruencia y ver si fuerza una distribucion distinta de la siguiente cola.
