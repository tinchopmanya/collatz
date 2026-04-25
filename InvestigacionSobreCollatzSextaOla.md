# Investigacion sobre Collatz - Sexta Ola: mapa de salida del bloque alternante

Fecha de cierre de esta ola: 2026-04-25 02:24:36 -03:00
Estado: sexta ola cerrada
Resumen asociado: [ResumenInvestigacionSobreCollatzSextaOla.md](ResumenInvestigacionSobreCollatzSextaOla.md)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)
Ola anterior: [Quinta](InvestigacionSobreCollatzQuintaOla.md)
Reporte tecnico: [reports/exit_map_limit_1000000.md](reports/exit_map_limit_1000000.md)

## 1. Objetivo

La quinta ola dejo un borde claro. Para todo impar positivo `n`, si:

```text
s = v2(n + 1)
q = (n + 1) / 2^s
n = 2^s q - 1
```

entonces el prefijo alternante inicial termina exactamente en:

```text
C^(2s)(n) = 3^s q - 1
```

La sexta ola estudia esa salida. La pregunta ya no es cuanto dura el bloque alternante, sino que tan grande queda el siguiente impar despues de salir del bloque.

## 2. Definicion del mapa de salida

Definimos:

```text
e = 3^s q - 1
r = v2(e)
m = e / 2^r
```

Entonces:

- `e` es el primer valor par despues del bloque alternante;
- `r` es la cantidad de divisiones por `2` forzadas al salir;
- `m` es el siguiente impar;
- los pasos desde `n` hasta `m` son `2s + r`;
- el pico local del bloque es `2e`.

En codigo, esto quedo representado por `AlternatingBlock` y `alternating_block(n)` en [src/collatz/core.py](src/collatz/core.py).

## 3. Resultado experimental

Se agrego el script:

```text
experiments/analyze_exit_map.py
```

y se ejecuto:

```powershell
python experiments\analyze_exit_map.py --limit 1000000 --out-dir reports --prefix exit_map_limit_1000000
```

El reporte completo esta en [reports/exit_map_limit_1000000.md](reports/exit_map_limit_1000000.md).

Los resultados principales fueron:

- `r = v2(3^s q - 1)` tiene promedio cercano a `2` para casi todo `s`.
- La distribucion de `r` es practicamente geometrica: `P(r = k) ~= 2^-k`.
- La siguiente cola `v2(m + 1)` tambien vuelve a promedio cercano a `2`.
- La razon promedio `m/n` crece aproximadamente como `(3/2)^s / 3`.
- La fraccion de casos donde `m > n` crece con `s`: para colas largas, la expansion local casi siempre sobrevive hasta el siguiente impar.

## 4. Explicacion 2-adica de la distribucion de salida

El patron de `r` no parece accidental.

Para `s` fijo, `3^s` es impar e invertible modulo `2^k`. Por lo tanto, la condicion:

```text
3^s q == 1 mod 2^k
```

selecciona una clase residual entre los `q` impares modulo `2^k`. Por densidad natural:

```text
P(r >= k) = 2^-(k-1)
P(r = k) = 2^-k
E[r] = 2
```

Esto coincide con la medicion hasta `n <= 1000000`:

| r | Fraccion medida |
| ---: | ---: |
| 1 | 0.500002 |
| 2 | 0.249992 |
| 3 | 0.125000 |
| 4 | 0.062506 |
| 5 | 0.031252 |
| 6 | 0.015626 |

La salida del bloque alternante, vista por `r`, se comporta como un impar generico respecto de su divisibilidad por potencias de `2`.

## 5. Expansion local esperada

Durante el bloque, el pico local satisface:

```text
pico/n ~= 2 * (3/2)^s
```

El siguiente impar cumple:

```text
m/n ~= (3/2)^s / 2^r
```

Usando la distribucion geometrica de `r`:

```text
E[2^-r] = 1/3
```

asi que:

```text
E[m/n | s] ~= (3/2)^s / 3
```

Ejemplo para `s = 9`:

```text
(3/2)^9 / 3 ~= 12.814
medicion: 12.820983
```

Esto explica por que las clases `511 mod 512` y similares son tan expansivas al comienzo: no solo tienen un bloque largo; ademas la division de salida suele ser demasiado pequena para cancelar el crecimiento acumulado.

## 6. Lo mas importante

La sexta ola separa dos hechos:

- las colas largas de unos generan expansion local muy fuerte;
- la salida de esa expansion parece resetear la cola a una distribucion casi generica.

Eso evita una lectura equivocada. El bloque alternante no parece crear automaticamente una cadena infinita de bloques alternantes largos. Mas bien produce una explosion local y luego devuelve el sistema a una zona mezclada. La dificultad global esta en medir si esos episodios raros de expansion quedan compensados por los bloques genericos posteriores.

## 7. Que se agrego al repositorio

- `AlternatingBlock` en el nucleo del laboratorio.
- `alternating_block(n)` para calcular `s`, `q`, `r`, siguiente impar, pico y pasos.
- Tests que comparan la formula contra iteracion exacta.
- `experiments/analyze_exit_map.py` para medir la salida del bloque.
- CSVs agregados en `reports/`.
- Reporte tecnico [reports/exit_map_limit_1000000.md](reports/exit_map_limit_1000000.md).

## 8. Que falta

El siguiente paso no deberia ser simplemente subir el limite. Primero conviene estudiar la dinamica por bloques odd-to-odd:

```text
n_i -> n_{i+1}
```

donde cada salto resume un bloque alternante inicial y su salida.

Preguntas concretas:

- Cuanta correlacion hay entre `s_i = v2(n_i + 1)` y `s_{i+1} = v2(n_{i+1} + 1)`?
- Es real el "reseteo" de cola o hay sesgos detectables?
- Que numeros encadenan varias expansiones locales antes de bajar?
- Los records conocidos se explican por secuencias de muchos bloques expansivos?
- Hay una cota util para el producto de varios cocientes `n_{i+1}/n_i`?

## 9. Veredicto

No se probo Collatz. Pero ya se paso de una familia conocida (`-1 mod 2^k`) a una descripcion cuantitativa del mecanismo de salida.

La parte potencialmente publicable, si madura, seria un informe sobre dinamica por bloques: como las colas binarias largas producen expansion, como la salida se distribuye 2-adicamente, y que correlaciones reales quedan despues de ese aparente reseteo.
