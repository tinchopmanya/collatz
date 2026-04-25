# Resumen de la investigacion sobre Collatz - Quinta Ola

Fecha de cierre de esta ola: 2026-04-25 02:12:23 -03:00
Investigacion completa: [InvestigacionSobreCollatzQuintaOla.md](InvestigacionSobreCollatzQuintaOla.md)
Conclusion dinamica: [Conlusion.md](Conlusion.md)

## Resumen fuerte corto

La quinta ola formalizo una observacion experimental de la cuarta ola. Se habia medido que las clases `-1 mod 2^k`, como `127`, `255` y `511`, tienen prefijos de paridad alternante y crecimiento temprano alto. Ahora se demostro la razon local exacta.

Si `n` es impar positivo y `s = v2(n + 1)`, entonces la longitud exacta del prefijo alternante inicial bajo el mapa clasico de Collatz es:

```text
2 * v2(n + 1)
```

Escribiendo `n = 2^s q - 1`, con `q` impar, se obtiene:

```text
C^(2j)(n) = 3^j 2^(s-j) q - 1
C^(2j+1)(n) = 3^(j+1) 2^(s-j) q - 2
```

Esto prueba que las paridades alternan hasta `2s - 1` y que el patron se rompe en `2s`. Tambien da el pico temprano exacto:

```text
C^(2s-1)(n) = 2(3^s q - 1)
```

El resultado explica por que `511 mod 512` tuvo longitud alternante promedio casi `20`: dentro de esa clase, `v2(n + 1) = 9 + v2(a)`, y el promedio esperado de `v2(a)` es `1`.

No es una prueba de Collatz. Es un lemma local. Lo importante es que ahora sabemos donde termina la explicacion conocida: despues del bloque alternante, en la salida `3^s q - 1`.

## Resumen fuerte ampliado

La quinta ola tuvo un objetivo concreto: convertir una medicion del laboratorio en una afirmacion matematica local. En la cuarta ola vimos que las clases residuales `-1 mod 2^k`, especialmente `127`, `255` y `511`, tenian prefijos de paridad alternante y crecimiento temprano alto. Tambien verificamos que esa familia no era un descubrimiento nuevo, sino una redeteccion de una estructura conectada con clases residuales, stopping time, Terras, Klee-Wagon, OEIS y Mersenne tails. La pregunta entonces paso a ser: podemos formalizar exactamente que esta midiendo el laboratorio?

La respuesta es si. Sea `C` el mapa clasico de Collatz. Si `n` es impar positivo y `s = v2(n + 1)`, entonces `n` puede escribirse como `n = 2^s q - 1`, con `q` impar. A partir de ahi se demuestra por induccion que:

```text
C^(2j)(n) = 3^j 2^(s-j) q - 1
C^(2j+1)(n) = 3^(j+1) 2^(s-j) q - 2
```

para los rangos correspondientes de `j`. La consecuencia inmediata es que los primeros `2s` terminos de la orbita alternan paridad: impar, par, impar, par, hasta que en `C^(2s)(n) = 3^s q - 1` aparece un par donde el patron esperaba un impar. Por lo tanto, la longitud exacta del prefijo alternante inicial es `2 * v2(n + 1)`.

Esto explica los datos. En la clase `127 mod 512`, la valuacion `v2(n + 1)` es exactamente `7`, por eso la longitud alternante es `14`. En `255 mod 512`, es `8`, por eso la longitud es `16`. En `511 mod 512`, la valuacion es al menos `9` y puede ser mayor; por densidad natural, el termino extra tiene esperanza `1`, dando una longitud promedio esperada de `20`, que coincide con el valor observado `19.993856`.

La formula tambien explica la excursion temprana. El pico antes de romper el bloque alternante ocurre en `C^(2s-1)(n) = 2(3^s q - 1)`, con proporcion exacta `2(3^s q - 1) / (2^s q - 1)` respecto de `n`. Esto muestra por que una cola binaria larga de unos fuerza crecimiento temprano: durante ese bloque, las multiplicaciones por 3 y divisiones por 2 quedan organizadas en un patron rigido.

La ola tambien aclaro el papel de los controles pares. Por ejemplo, `510 mod 512` hereda alternancia larga porque al dividir por 2 cae en una clase tipo `255 mod 256`, pero su stopping time es `1` porque baja inmediatamente. Esto evita una confusion importante: alternancia larga, crecimiento temprano y primer descenso son fenomenos relacionados, pero no equivalentes.

El resultado no prueba Collatz y no controla la orbita completa. Su valor esta en delimitar el borde: la parte conocida y formalizable es el bloque alternante; lo que sigue siendo interesante es la salida `C^(2s)(n) = 3^s q - 1`. Si buscamos algo mas original, la siguiente investigacion deberia estudiar esa salida y sus nuevas valuaciones 2-adicas.
