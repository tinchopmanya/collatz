# Resumen de la investigacion sobre Collatz - Sexta Ola

Fecha de cierre de esta ola: 2026-04-25 02:24:36 -03:00
Investigacion completa: [InvestigacionSobreCollatzSextaOla.md](InvestigacionSobreCollatzSextaOla.md)
Conclusion dinamica: [Conlusion.md](Conlusion.md)
Reporte tecnico: [reports/exit_map_limit_1000000.md](reports/exit_map_limit_1000000.md)

## Resumen fuerte corto

La sexta ola estudio que pasa inmediatamente despues del prefijo alternante formalizado en la quinta ola. Si `n` es impar y `n = 2^s q - 1`, con `s = v2(n + 1)`, entonces el bloque alternante termina en:

```text
C^(2s)(n) = 3^s q - 1
```

Definimos `r = v2(3^s q - 1)` y `m = (3^s q - 1) / 2^r`, donde `m` es el siguiente impar. La medicion hasta `n <= 1000000` mostro que `r` tiene distribucion casi geometrica:

```text
P(r = k) ~= 2^-k
E[r] ~= 2
```

Esto tiene una explicacion 2-adica natural: para `s` fijo, `3^s` es invertible modulo potencias de `2`, asi que la condicion `3^s q == 1 mod 2^k` selecciona una clase residual entre los `q` impares.

El hallazgo central es que las colas largas de unos producen expansion local, pero la salida suele tener una valuacion 2-adica pequena. Por eso:

```text
E[m/n | s] ~= (3/2)^s / 3
```

Para `s = 9`, la prediccion es aproximadamente `12.814` y la medicion fue `12.820983`.

No es una prueba de Collatz. Es una pieza de mecanismo: una cola larga genera explosion local, pero la siguiente cola `v2(m + 1)` vuelve a promedio cercano a `2`, como si el sistema se mezclara de nuevo. El proximo borde es estudiar cadenas odd-to-odd y ver si ese "reseteo" es real, si tiene sesgos, y si los records conocidos nacen de varias expansiones locales encadenadas.

## Resumen fuerte ampliado

La sexta ola tomo el borde exacto que habia dejado la quinta. Ya sabiamos que, para un impar `n`, la longitud del prefijo alternante inicial es `2 * v2(n + 1)`. Tambien sabiamos que si `n = 2^s q - 1`, el valor en el que termina ese bloque es `3^s q - 1`. La pregunta nueva fue: que estructura tiene esa salida?

Para medirlo, se agrego al laboratorio la funcion `alternating_block(n)`, que devuelve la descomposicion del bloque inicial: la longitud de cola `s`, el factor impar `q`, el valor par de salida `e = 3^s q - 1`, la valuacion `r = v2(e)`, el siguiente impar `m = e / 2^r`, el pico local y la cantidad de pasos hasta `m`. Luego se creo `experiments/analyze_exit_map.py` y se ejecuto hasta un millon.

El resultado mas claro fue que `r` se distribuye casi exactamente como una geometrica: la mitad de los casos tienen `r = 1`, un cuarto tienen `r = 2`, un octavo tienen `r = 3`, y asi sucesivamente. El promedio queda cerca de `2` para todas las longitudes de cola `s`. Esto no parece una coincidencia experimental; se explica porque `3^s` es invertible modulo `2^k`, y por lo tanto la congruencia que fuerza divisibilidad por `2^k` selecciona una proporcion esperada de los `q` impares.

La consecuencia dinamica es importante. El bloque alternante produce un pico aproximado `2 * (3/2)^s` veces el valor inicial. Despues, al dividir por `2^r`, el siguiente impar queda aproximadamente en `(3/2)^s / 2^r` veces el valor inicial. Como la esperanza de `2^-r` bajo esa distribucion es `1/3`, se obtiene la regla empirica `E[m/n | s] ~= (3/2)^s / 3`. Esto coincide muy bien con los datos: para `s = 9`, la prediccion es `12.814` y la medicion fue `12.820983`.

La lectura prudente es doble. Por un lado, esto explica por que las clases tipo `511 mod 512` crecen tanto: una cola binaria larga de unos no solo alarga el patron alternante, sino que normalmente sale con pocas divisiones por `2`, por lo que la expansion sobrevive hasta el siguiente impar. Por otro lado, la siguiente cola `v2(m + 1)` vuelve a promedio cercano a `2`; es decir, el bloque expansivo no parece conservar automaticamente una cola larga para el siguiente bloque.

El avance no prueba la conjetura ni descarta ciclos. Pero si convierte el fenomeno en un modelo local mas preciso: expansion por cola larga, salida 2-adica casi geometrica, y aparente reseteo de la cola. La siguiente investigacion deberia estudiar la cadena de saltos entre impares, medir correlaciones entre colas consecutivas, comparar contra un modelo independiente y buscar numeros que encadenen varias expansiones antes del primer descenso.
