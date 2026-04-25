# Resumen de la investigacion sobre Collatz - Septima Ola

Fecha de cierre de esta ola: 2026-04-25 02:32:13 -03:00
Investigacion completa: [InvestigacionSobreCollatzSeptimaOla.md](InvestigacionSobreCollatzSeptimaOla.md)
Conclusion dinamica: [Conlusion.md](Conlusion.md)
Reporte tecnico: [reports/odd_chain_limit_1000000.md](reports/odd_chain_limit_1000000.md)

## Resumen fuerte corto

La septima ola paso de estudiar un solo bloque alternante a estudiar cadenas de bloques entre impares. Para cada impar `n_i`, se aplica el salto:

```text
n_i = 2^s q - 1
n_{i+1} = (3^s q - 1) / 2^r
r = v2(3^s q - 1)
```

La cadena se detiene cuando llega a `1`, baja por debajo del impar inicial o supera el limite de bloques. Se midieron todos los impares `3 <= n <= 1000000` con limite de `256` bloques. Ningun caso agoto el limite; el maximo observado fue `41` bloques odd-to-odd hasta bajar.

El resultado mas importante fue el "reseteo" de cola: condicionado por la cola actual `v2(n_i + 1)`, el promedio de la siguiente cola `v2(n_{i+1} + 1)` queda muy cerca de `2` para casi todos los valores medidos. Esto refuerza la idea de que una cola larga causa expansion local, pero no fabrica automaticamente otra cola larga.

Tambien se separaron dos dificultades distintas. El record de duracion fue `626331`, con `41` bloques, pero el mayor pico relativo fue `159487`, con solo `14` bloques y `max pico/n ~= 107860.689`. Esto indica que "orbita dificil" no es una sola propiedad: una orbita puede ser larga sin ser la mas alta, o muy alta sin ser la mas larga.

La ola no prueba Collatz. Pero deja un camino mas serio: comparar cadenas reales contra un modelo geometrico independiente y buscar desviaciones sistematicas en las secuencias de colas y factores locales.

## Resumen fuerte ampliado

La septima ola tomo el mecanismo local de la sexta ola y lo encadeno. En vez de estudiar solamente la salida de `n = 2^s q - 1`, se itero el salto entre impares `n_i -> n_{i+1}`. Cada salto resume un bloque alternante inicial mas las divisiones por dos necesarias hasta llegar al siguiente impar. Esta compresion permite medir la dinamica de Collatz por bloques, no paso a paso.

La corrida principal cubrio todos los impares entre `3` y `1000000`, con maximo de `256` bloques por numero. Todos los casos bajaron por debajo del impar inicial o llegaron a `1` antes del limite. El maximo observado fue `41` bloques, alcanzado por `626331` y `667375`. Esto no es una prueba global, pero muestra que en esta escala el primer descenso aparece rapido cuando se mira en unidades odd-to-odd.

La medicion central fue la transicion entre colas binarias. Si la cola actual es `s_i = v2(n_i + 1)`, se midio el promedio de `s_{i+1} = v2(n_{i+1} + 1)`. Para colas actuales de `1` a `12`, el promedio de la siguiente cola quedo casi siempre alrededor de `2`. Esto es exactamente lo que uno esperaria de un impar generico. La interpretacion prudente es que el bloque alternante puede expandir mucho, pero la salida tiende a mezclar la informacion 2-adica y no conserva facilmente una cola larga.

La cola inicial sigue importando: a mayor `s`, suben el promedio de bloques antes del descenso y la excursion promedio. Por ejemplo, con `s = 1`, todos los casos bajan en un bloque; esto incluso tiene una prueba corta. Si `n = 2q - 1`, con `q` impar y `q > 1`, entonces el siguiente impar `m` cumple `m <= (3q - 1)/2 < n`. Pero para colas mayores el efecto se vuelve probabilistico: hay expansion local fuerte, seguida de mezcla.

Un hallazgo practico fue separar duracion y altura. `626331` fue record de bloques en la corrida, pero no de altura. `159487`, en cambio, alcanzo el mayor pico relativo con muchos menos bloques. Esto sugiere que las busquedas futuras deberian clasificar orbitas por perfiles: largas, altas, con muchos bloques expansivos, con colas largas repetidas, etc.

La siguiente etapa deberia trazar los records y compararlos contra un modelo de colas geometricas independientes. Si las cadenas reales se comportan casi igual que el modelo, el resultado seria una buena explicacion negativa. Si aparecen correlaciones persistentes, ahi podria estar una contribucion mas original.
