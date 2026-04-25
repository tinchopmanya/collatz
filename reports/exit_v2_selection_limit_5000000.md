# Seleccion de muestra en `exit_v2 = 5` hasta 5000000

Fecha: 2026-04-25
Script: [experiments/analyze_exit_v2_selection.py](../experiments/analyze_exit_v2_selection.py)

Salidas CSV:

- [exit_v2_selection_limit_5000000_summary.csv](exit_v2_selection_limit_5000000_summary.csv)
- [exit_v2_selection_limit_5000000_tail_distribution.csv](exit_v2_selection_limit_5000000_tail_distribution.csv)
- [exit_v2_selection_limit_5000000_exit_distribution.csv](exit_v2_selection_limit_5000000_exit_distribution.csv)
- [exit_v2_selection_limit_5000000_decomposition.csv](exit_v2_selection_limit_5000000_decomposition.csv)

## Preguntas antes de iterar

```text
1. Estoy en algo virgen?
Respuesta: no en el marco general. Campbell 2025 ya trabaja bloques de Mersenne, salida r(x), mezcla y clases residuales modulo potencias de 2.

2. Alguien busco esto antes?
Respuesta: si a nivel de marco. Lo que habia que verificar era mas fino: si nuestra senal `exit_v2 = 5` era local o si aparecia por el modo de muestreo.

3. Que parte exacta podria ser nueva?
Respuesta: distinguir experimentalmente entre transicion local de todos los bloques y pares de cadenas sobrevivientes antes del primer descenso.

4. Que probabilidad real hay de descubrir algo relevante?
Respuesta: baja para una prueba, pero buena para limpiar el roadmap: confirmar si la pista `exit_v2 = 5` merece formalizacion o descarte.

5. Que evidencia haria que sigamos?
Respuesta: que `exit_v2 = 5` sesgue tambien la muestra local de todos los bloques.

6. Que evidencia haria que abandonemos?
Respuesta: que la muestra local vuelva al modelo geometrico y la senal solo aparezca en cadenas condicionadas por supervivencia.
```

## Comando reproducible

```powershell
python experiments\analyze_exit_v2_selection.py --limit 5000000 --max-blocks 256 --targets 1,2,3,4,5,6,7,8 --out-dir reports --prefix exit_v2_selection_limit_5000000
```

## Congruencia exacta

Sea un impar al inicio de bloque:

```text
n = 2^s q - 1
q impar
s = v2(n + 1)
```

La salida del bloque es:

```text
B(n) = (3^s q - 1) / 2^r
r = v2(3^s q - 1)
```

Entonces:

```text
r = 5
<=> 3^s q - 1 = 32 mod 64
<=> 3^s q = 33 mod 64
<=> q = 3^(-s) + 32 mod 64
```

Tabla de residuos para `s mod 16`:

| s mod 16 | q mod 64 si r = 5 |
| ---: | ---: |
| 1 | 11 |
| 2 | 25 |
| 3 | 51 |
| 4 | 17 |
| 5 | 27 |
| 6 | 9 |
| 7 | 3 |
| 8 | 1 |
| 9 | 43 |
| 10 | 57 |
| 11 | 19 |
| 12 | 49 |
| 13 | 59 |
| 14 | 41 |
| 15 | 35 |
| 0 | 33 |

Si `3^s q = 33 + 64h`, entonces:

```text
B(n) = 1 + 2h
B(n) + 1 = 2(h + 1)
v2(B(n) + 1) = 1 + v2(h + 1)
```

Por eso, si `h` queda mezclado de manera uniforme modulo potencias de 2, la cola siguiente vuelve a ser geometrica. La pregunta decisiva era si las orbitas reales rompen esa uniformidad.

## Comparacion principal

| Fuente | prev_exit_v2 | Pares | P siguiente expansion | Diff vs geometrico | Avg next_tail | Avg next_exit_v2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| local_all_starts | 5 | 78124 | 0.28628846 | 0.00001396 | 2.00011520 | 1.99953919 |
| chain_before_descent | 5 | 5385 | 0.25979573 | -0.02647877 | 1.92423398 | 1.96620241 |

Interpretacion:

- En la muestra local de todos los bloques, `exit_v2 = 5` no cambia la expansion siguiente.
- En cadenas antes del primer descenso, `exit_v2 = 5` si aparece con menor expansion siguiente.
- Por lo tanto, la senal de la decima ola no es una ley local de la clase `exit_v2 = 5`; es una senal de seleccion de muestra/orbita.

## Distribucion de cola siguiente para `exit_v2 = 5`

| Fuente | next_tail | Fraccion | Geometrico | Diff |
| --- | ---: | ---: | ---: | ---: |
| local_all_starts | 1 | 0.50000000 | 0.50000000 | 0.00000000 |
| local_all_starts | 2 | 0.25003840 | 0.25000000 | 0.00003840 |
| local_all_starts | 3 | 0.12496800 | 0.12500000 | -0.00003200 |
| local_all_starts | 4 | 0.06249040 | 0.06250000 | -0.00000960 |
| chain_before_descent | 1 | 0.54447539 | 0.50000000 | 0.04447539 |
| chain_before_descent | 2 | 0.21708449 | 0.25000000 | -0.03291551 |
| chain_before_descent | 3 | 0.11977716 | 0.12500000 | -0.00522284 |
| chain_before_descent | 4 | 0.06035283 | 0.06250000 | -0.00214717 |

La diferencia nace casi toda en la cola siguiente:

```text
P(next_tail = 1 | exit_v2 = 5, chain_before_descent) = 0.54447539
P(next_tail = 1 | exit_v2 = 5, local_all_starts)     = 0.50000000
```

Como `next_tail = 1` nunca produce un bloque expansivo, esta sobre-representacion baja la expansion total.

## Descomposicion de la expansion

Para `exit_v2 = 5`:

| Fuente | Real | Geometrico | Cola observada + exit geometrico | Cola geometrica + exit observado | Producto marginal observado |
| --- | ---: | ---: | ---: | ---: | ---: |
| local_all_starts | 0.28628846 | 0.28627450 | 0.28627991 | 0.28628648 | 0.28629189 |
| chain_before_descent | 0.25979573 | 0.28627450 | 0.26158600 | 0.28958020 | 0.26452212 |

Lectura:

- En la muestra local, todo coincide con el modelo.
- En la muestra de cadenas sobrevivientes, reemplazar solo la cola por la cola observada ya baja la expansion a `0.26158600`, muy cerca del real `0.25979573`.
- El `exit_v2` siguiente observado no explica la caida; de hecho, con cola geometrica daria `0.28958020`.

## Preguntas despues de iterar

```text
1. La respuesta sobre originalidad cambio?
Respuesta: si, a la baja para esta pista. La clase `exit_v2 = 5` no parece contener un mecanismo local nuevo.

2. La probabilidad de relevancia subio, bajo o quedo igual?
Respuesta: bajo para una nota sobre `exit_v2 = 5`; subio para una pregunta diferente: como se sesgan las colas en cadenas sobrevivientes.

3. Se encontro una senal robusta o solo seleccion?
Respuesta: la senal local desaparece. La senal de cadenas sobrevivientes es real, pero no debe interpretarse como propiedad local de `exit_v2 = 5`.

4. Que aprendimos que no sabiamos antes?
Respuesta: condicionar por "antes del primer descenso" cambia la distribucion de la cola siguiente; ahi esta el efecto.

5. Conviene seguir, escalar, formalizar o abandonar?
Respuesta: abandonar `exit_v2 = 5` como lemma local candidato. Seguir con una pregunta de seleccion/supervivencia si queremos entender por que el modelo sobreproduce extremos.

6. Cual es la siguiente pregunta minima?
Respuesta: que filtro de supervivencia deforma `next_tail` hacia 1, y si esa deformacion explica la menor frecuencia de extremos reales frente al modelo.
```

## Veredicto

La hipotesis optimista:

```text
exit_v2 = 5 fuerza localmente menor expansion siguiente.
```

queda descartada en esta escala.

La hipotesis nueva, mas prudente, es:

```text
Las cadenas que sobreviven antes del primer descenso no muestrean uniformemente las transiciones locales; sobre-representan next_tail = 1 despues de ciertos eventos.
```

Esto no prueba Collatz, pero si corrige el rumbo: la brecha entre modelo y realidad parece estar menos en la aritmetica local estatica y mas en el condicionamiento orbital por supervivencia.

## Fuente externa usada para situar originalidad

- [Mersenne Block Dynamics: A Framework for the Collatz Conjecture, Stephen R. Campbell, 2025](https://ai.vixra.org/pdf/2512.0068v1.pdf)
