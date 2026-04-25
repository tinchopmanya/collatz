# Formalizacion del prefijo alternante

Fecha: 2026-04-25
Estado: lemma local formalizado

## Definiciones

Sea `C` el mapa clasico de Collatz:

```text
C(n) = n / 2      si n es par
C(n) = 3n + 1    si n es impar
```

Sea `v2(m)` la valuacion 2-adica de `m`, es decir, el mayor exponente `s` tal que `2^s` divide a `m`.

Para un impar positivo `n`, definimos:

```text
s = v2(n + 1)
q = (n + 1) / 2^s
```

Entonces `q` es impar y:

```text
n = 2^s q - 1
```

## Lemma 1: forma cerrada del bloque inicial

Si `n` es impar positivo, `s = v2(n + 1)` y `q = (n + 1) / 2^s`, entonces para `0 <= j <= s`:

```text
C^(2j)(n) = 3^j 2^(s-j) q - 1
```

y para `0 <= j < s`:

```text
C^(2j+1)(n) = 3^(j+1) 2^(s-j) q - 2
```

## Prueba

Base `j = 0`:

```text
C^0(n) = n = 2^s q - 1
```

Como `n` es impar:

```text
C(n) = 3(2^s q - 1) + 1
     = 3 * 2^s q - 2
```

Esto coincide con la formula impar para `j = 0`.

Paso inductivo:

Supongamos que para algun `j < s`:

```text
C^(2j)(n) = 3^j 2^(s-j) q - 1
```

Como `j < s`, el termino `3^j 2^(s-j) q` es par, asi que `C^(2j)(n)` es impar. Aplicando el paso impar:

```text
C^(2j+1)(n)
= 3(3^j 2^(s-j) q - 1) + 1
= 3^(j+1) 2^(s-j) q - 2
```

Este numero es par. Dividiendo por 2:

```text
C^(2j+2)(n)
= (3^(j+1) 2^(s-j) q - 2) / 2
= 3^(j+1) 2^(s-j-1) q - 1
```

que es la formula para `j + 1`.

## Lemma 2: longitud exacta del prefijo alternante

Si `n` es impar positivo y `s = v2(n + 1)`, entonces la paridad de:

```text
n, C(n), C^2(n), ..., C^(2s-1)(n)
```

alterna exactamente como:

```text
impar, par, impar, par, ..., impar, par
```

y `C^(2s)(n)` es par. Por lo tanto, la longitud exacta del prefijo alternante inicial es:

```text
2 * v2(n + 1)
```

## Prueba

Por el Lemma 1, para `0 <= j < s`:

```text
C^(2j)(n) = 3^j 2^(s-j) q - 1
```

Como `s - j >= 1`, el primer termino es par, asi que `C^(2j)(n)` es impar.

Tambien por el Lemma 1:

```text
C^(2j+1)(n) = 3^(j+1) 2^(s-j) q - 2
```

Ese valor es par. Por lo tanto, hasta `2s - 1` la paridad alterna.

En `j = s`:

```text
C^(2s)(n) = 3^s q - 1
```

Como `3^s q` es impar, `3^s q - 1` es par. En el paso `2s`, el patron alternante esperaba un impar, pero aparece un par. Entonces el prefijo alternante termina exactamente ahi.

## Corolario 1: clases `-1 mod 2^k`

Si:

```text
n == -1 mod 2^k
```

y `n` es positivo, entonces:

```text
v2(n + 1) >= k
```

por lo tanto el prefijo alternante inicial tiene longitud al menos:

```text
2k
```

Si ademas:

```text
n != -1 mod 2^(k+1)
```

entonces:

```text
v2(n + 1) = k
```

y la longitud alternante exacta es:

```text
2k
```

## Corolario 2: promedio condicional esperado

Dentro de la clase `n == -1 mod 2^k`, escribimos:

```text
n + 1 = 2^k a
```

Entonces:

```text
v2(n + 1) = k + v2(a)
```

Para `a` distribuido por densidad natural entre enteros positivos:

```text
E[v2(a)] = 1
```

Asi, la longitud alternante promedio esperada dentro de la clase es:

```text
E[2 v2(n + 1)] = 2(k + 1)
```

Esto explica por que para `511 mod 512`, donde `k = 9`, el promedio observado fue casi:

```text
2(9 + 1) = 20
```

## Corolario 3: excursion temprana

Durante el bloque alternante, los valores en pasos impares son:

```text
C^(2j+1)(n) = 3^(j+1) 2^(s-j) q - 2
```

Estos valores crecen con `j`. El pico antes de romper el prefijo alternante ocurre en:

```text
C^(2s-1)(n) = 2(3^s q - 1)
```

Por lo tanto, el pico temprano exacto del bloque alternante es:

```text
P(n) = 2(3^s q - 1)
```

y su proporcion respecto al valor inicial es:

```text
P(n) / n = 2(3^s q - 1) / (2^s q - 1)
```

Esto cuantifica el crecimiento temprano inducido por una cola binaria larga de unos.

## Que demuestra esto

- Explica formalmente la longitud alternante medida por el laboratorio.
- Explica por que las clases `2^k - 1` tienen crecimiento temprano.
- Conecta la medicion computacional con `v2(n + 1)` y Mersenne tails.
- Da una pieza local verificable y reutilizable.

## Que no demuestra

- No prueba la conjetura de Collatz.
- No descarta orbitas divergentes.
- No descarta ciclos no triviales.
- No controla lo que ocurre despues del bloque alternante.
- No es original como familia estructural; encaja con literatura previa sobre clases residuales y stopping time.

## Uso para la siguiente etapa

Este lemma convierte una medicion experimental en una herramienta local. La pregunta nueva ya no es si `2^k - 1` es especial, sino:

> Que ocurre despues de que termina el bloque alternante, y se puede clasificar la salida de ese bloque?

Ese es el borde donde podria aparecer algo mas interesante.
