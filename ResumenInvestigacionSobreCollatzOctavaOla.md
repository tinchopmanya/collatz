# Resumen de la investigacion sobre Collatz - Octava Ola

Fecha de cierre de esta ola: 2026-04-25 02:40:15 -03:00
Investigacion completa: [InvestigacionSobreCollatzOctavaOla.md](InvestigacionSobreCollatzOctavaOla.md)
Conclusion dinamica: [Conlusion.md](Conlusion.md)
Reporte tecnico: [reports/geometric_model_limit_1000000.md](reports/geometric_model_limit_1000000.md)

## Resumen fuerte corto

La octava ola construyo un modelo nulo para las cadenas odd-to-odd. En el modelo, cada bloque elige independientemente:

```text
s ~ Geom(1/2)
r ~ Geom(1/2)
log factor = s log(3/2) - r log(2)
```

La cadena se detiene cuando la suma logaritmica cae por debajo de `0`, imitando el primer descenso. Se compararon `499999` cadenas reales (`3 <= n <= 1000000`) contra `499999` simuladas con semilla fija.

El resultado fue fuerte: el modelo explica muy bien el cuerpo de la distribucion. La media de bloques fue `1.742153` real contra `1.746125` modelo; p90 fue `3` en ambos; p99 fue `10` en ambos; p999 fue `20` real contra `21` modelo.

La diferencia aparece en extremos. El maximo real fue `41` bloques, mientras el modelo produjo `54`. El mayor pico real fue `107860.689285` veces el inicio, mientras el modelo produjo `2429179.311905`. Para eventos `max pico/n >= 100000`, el modelo produjo 13 veces mas casos que la dinamica real observada.

La lectura prudente es que Collatz real se parece mucho al modelo geometrico en escala gruesa, pero podria tener anti-persistencia en extremos: la aritmetica real parece menos permisiva que un modelo que reelige colas y salidas independientemente. Todavia no es una prueba ni una afirmacion formal, pero es una direccion clara para la siguiente ola.

## Resumen fuerte ampliado

La septima ola habia mostrado que, despues de un bloque odd-to-odd, la siguiente cola binaria `v2(n_{i+1} + 1)` vuelve a promedio cercano a `2`. La octava ola puso a prueba esa idea construyendo un modelo independiente. Si las colas realmente se mezclan, entonces una cadena artificial con `s` y `r` geometricos independientes deberia parecerse a la cadena real, al menos en la distribucion de bloques hasta el primer descenso.

El modelo fue deliberadamente simple. En cada bloque se toma `s` con probabilidad `P(s = k) = 2^-k`, se toma `r` con la misma distribucion, y se suma el factor logaritmico `s log(3/2) - r log(2)`. Cuando la suma acumulada baja de cero, se considera que la cadena descendio por debajo del inicio. Este modelo ignora congruencias, valores exactos de `q`, efectos de rango y dependencias aritmeticas entre bloques. Justamente por eso es util como modelo nulo.

La comparacion fue llamativa. Para `499999` muestras reales y `499999` simuladas, la media, mediana, p90 y p99 quedaron casi iguales. Esto significa que gran parte del comportamiento odd-to-odd no necesita una estructura fina para ser predicho: la heuristica geometrica explica bastante.

Pero el modelo falla hacia los extremos. Produce mas cadenas de `40` o mas bloques, mas picos superiores a `100000` veces el inicio, y un maximo mucho mayor que el real en esta escala. Esto sugiere que la independencia pura exagera la posibilidad de concatenar muchos bloques favorables. En Collatz real, podria haber restricciones aritmeticas que actuen como freno despues de episodios expansivos.

Tambien se generaron trazas detalladas de records. `626331` y `667375` fueron records de duracion con `41` bloques; `159487` fue record de altura relativa con solo `14` bloques; `270271`, `288615` y `405407` combinaron duracion alta con altura alta. Esto confirma que no hay una sola nocion de "dificultad": una orbita puede ser larga, alta, ambas, o ninguna.

El avance principal de esta ola es metodologico. A partir de ahora, cualquier patron candidato debe compararse contra el modelo geometrico. Si el modelo ya lo explica, probablemente no sea una veta nueva. Si el modelo falla de forma estable, especialmente en extremos, ahi podria haber un fenomeno formalizable.
