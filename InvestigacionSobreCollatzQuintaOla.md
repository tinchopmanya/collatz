# Investigacion sobre Collatz - Quinta Ola: formalizacion del prefijo alternante

Fecha de cierre de esta ola: 2026-04-25 02:12:23 -03:00
Estado: quinta ola cerrada
Resumen asociado: [ResumenInvestigacionSobreCollatzQuintaOla.md](ResumenInvestigacionSobreCollatzQuintaOla.md)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)
Ola anterior: [Cuarta](InvestigacionSobreCollatzCuartaOla.md)

## 1. Objetivo

La cuarta ola midio computacionalmente que las clases `-1 mod 2^k`, especialmente `127`, `255` y `511`, tienen prefijos de paridad alternante y crecimiento temprano alto.

La quinta ola intenta convertir esa medicion en una pieza matematica local:

> Para un impar `n`, la longitud exacta del prefijo alternante inicial bajo el mapa clasico de Collatz es `2 * v2(n + 1)`.

Esta ola no busca probar Collatz. Busca formalizar una observacion reproducible y definir el borde siguiente de investigacion.

## 2. Resultado principal

Sea `C` el mapa clasico:

```text
C(n) = n / 2      si n es par
C(n) = 3n + 1    si n es impar
```

Sea `n` impar positivo. Escribimos:

```text
s = v2(n + 1)
q = (n + 1) / 2^s
```

Entonces `q` es impar y:

```text
n = 2^s q - 1
```

La formula cerrada del bloque inicial es:

```text
C^(2j)(n) = 3^j 2^(s-j) q - 1       para 0 <= j <= s
C^(2j+1)(n) = 3^(j+1) 2^(s-j) q - 2 para 0 <= j < s
```

De ahi se deduce que las paridades de:

```text
n, C(n), C^2(n), ..., C^(2s-1)(n)
```

alternan exactamente:

```text
impar, par, impar, par, ...
```

y que `C^(2s)(n)` es par, rompiendo el patron. Por lo tanto, la longitud exacta del prefijo alternante es:

```text
2s = 2 * v2(n + 1)
```

La formalizacion completa esta en [FormalizacionPrefijoAlternante.md](FormalizacionPrefijoAlternante.md).

## 3. Verificacion computacional

Se agregaron funciones al nucleo:

- `two_adic_valuation(n)`;
- `mersenne_tail_length(n)`;
- `odd_alternating_prefix_len(n)`.

Archivos:

- [src/collatz/core.py](src/collatz/core.py)
- [tests/test_core.py](tests/test_core.py)

Se agrego un test que compara la formula contra una medicion iterativa para todos los impares menores que `2000`.

Resultado:

```text
Ran 7 tests
OK
```

Esto no reemplaza la prueba, pero protege el codigo contra errores obvios de implementacion.

## 4. Conexion con la cuarta ola

La cuarta ola habia medido:

| Residuo mod 512 | Longitud alternante promedio | Pico temprano promedio |
| ---: | ---: | ---: |
| 511 | 19.993856 | 347.125344 |
| 510 | 18.993856 | 136.859853 |
| 255 | 16.000000 | 175.302741 |
| 127 | 14.000000 | 150.722211 |

La quinta ola explica esos valores.

Para `127 mod 512`, los numeros son `-1 mod 2^7` pero no `-1 mod 2^8`, asi que `v2(n + 1) = 7` y la longitud alternante es exactamente `14`.

Para `255 mod 512`, `v2(n + 1) = 8` y la longitud alternante es exactamente `16`.

Para `511 mod 512`, `v2(n + 1) >= 9`. Dentro de esa clase:

```text
n + 1 = 2^9 a
```

Como `E[v2(a)] = 1` por densidad natural, la longitud promedio esperada es:

```text
2(9 + 1) = 20
```

Esto coincide con el promedio observado `19.993856`.

## 5. Excursion temprana

La formula cerrada tambien da el pico temprano del bloque alternante.

Si `s = v2(n + 1)` y `q = (n + 1) / 2^s`, entonces el pico antes de romper la alternancia ocurre en:

```text
C^(2s-1)(n) = 2(3^s q - 1)
```

La proporcion respecto del inicio es:

```text
2(3^s q - 1) / (2^s q - 1)
```

Esto explica por que una cola binaria larga de unos produce crecimiento temprano. Tambien muestra por que el fenomeno es local: la formula controla el bloque inicial, no toda la orbita.

## 6. Control par: `2^k - 2`

La cuarta ola mostro que `510 mod 512` tiene alternancia larga pero stopping time promedio `1`.

La explicacion es simple:

```text
510 mod 512 = 2 * (255 mod 256)
```

Al primer paso, todo numero en esa clase se divide por `2`, y por lo tanto baja inmediatamente por debajo de su valor inicial. Despues hereda parte de la estructura alternante del impar resultante, pero el stopping time ya quedo fijado en `1`.

Esto aclara una separacion importante:

- alternancia larga no implica stopping time alto;
- crecimiento temprano no implica primer descenso tardio;
- los controles pares son necesarios para no confundir metricas.

## 7. Que se logro

- Se formalizo el patron alternante medido experimentalmente.
- Se explico por que `127`, `255` y `511` tienen las longitudes observadas.
- Se conecto la medicion con `v2(n + 1)` y Mersenne tails.
- Se agregaron funciones y tests al laboratorio.
- Se delimito el borde donde termina la explicacion local.

## 8. Que falta

Lo desconocido empieza despues del bloque alternante.

La pregunta siguiente es:

> Dado `n = 2^s q - 1`, que estructura tiene la salida `C^(2s)(n) = 3^s q - 1`?

Ese valor ya no conserva necesariamente una cola binaria larga de unos. La dinamica posterior depende de:

- `q`;
- la factorizacion de `3^s q - 1`;
- la nueva valuacion 2-adica;
- la interaccion con clases residuales posteriores.

Si hay lugar para aportar algo menos conocido, probablemente esta ahi: en clasificar la salida del bloque alternante, no en redescubrir el bloque.

## 9. Conclusion

La quinta ola transforma una medicion en un lemma local. Esto no es una prueba de Collatz, pero si es progreso disciplinado: una observacion experimental paso a una formula exacta, con prueba, codigo y tests.

La proxima ola deberia estudiar el mapa de salida:

```text
n = 2^s q - 1  ->  C^(2s)(n) = 3^s q - 1
```

Ese mapa concentra lo que el prefijo alternante no explica. Si buscamos algo menos conocido, conviene mirar ahi.
