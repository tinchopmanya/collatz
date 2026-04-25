# Investigacion sobre Collatz - Octava Ola: modelo geometrico independiente

Fecha de cierre de esta ola: 2026-04-25 02:40:15 -03:00
Estado: octava ola cerrada
Resumen asociado: [ResumenInvestigacionSobreCollatzOctavaOla.md](ResumenInvestigacionSobreCollatzOctavaOla.md)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)
Ola anterior: [Septima](InvestigacionSobreCollatzSeptimaOla.md)
Reporte tecnico: [reports/geometric_model_limit_1000000.md](reports/geometric_model_limit_1000000.md)

## 1. Objetivo

La septima ola encontro evidencia de reseteo de cola: despues de un bloque odd-to-odd, la nueva cola `v2(n_{i+1} + 1)` vuelve a promedio cercano a `2`.

La octava ola intenta responder:

> Esa mezcla alcanza para explicar la distribucion observada de bloques hasta descenso?

Para eso se construyo un modelo nulo independiente.

## 2. Modelo

El modelo artificial genera bloques con:

```text
s_i ~ Geom(1/2)
r_i ~ Geom(1/2)
P(k) = 2^-k
```

y usa:

```text
log(n_{i+1}/n_i) = s_i log(3/2) - r_i log(2)
```

La cadena se detiene cuando:

```text
sum log(n_{i+1}/n_i) < 0
```

Esto imita el primer descenso en escala odd-to-odd.

## 3. Scripts agregados

Se agregaron:

- [experiments/trace_odd_records.py](experiments/trace_odd_records.py)
- [experiments/compare_geometric_model.py](experiments/compare_geometric_model.py)

El primero genera trazas bloque por bloque para records reales. El segundo compara la poblacion real hasta `n <= 1000000` contra el modelo geometrico independiente.

## 4. Resultado principal

La comparacion principal uso `499999` muestras reales y `499999` simuladas:

| Fuente | Media bloques | p90 | p99 | p999 | Max bloques | Max pico/n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Real | 1.742153 | 3 | 10 | 20 | 41 | 107860.689285 |
| Modelo | 1.746125 | 3 | 10 | 21 | 54 | 2429179.311905 |

La coincidencia en el cuerpo de la distribucion es sorprendentemente fuerte. El modelo simple explica muy bien media, mediana, p90 y p99.

La diferencia aparece en los extremos: el modelo produce mas cadenas larguisimas y picos gigantes que la dinamica real observada.

## 5. Probabilidades de cola

| Evento | Real | Modelo | Lectura |
| --- | ---: | ---: | --- |
| Bloques >= 10 | 0.01246602 | 0.01273403 | casi igual |
| Bloques >= 20 | 0.00114400 | 0.00123400 | modelo apenas mayor |
| Bloques >= 30 | 0.00011600 | 0.00017400 | modelo 1.5x mayor |
| Bloques >= 40 | 0.00000600 | 0.00003800 | modelo 6.33x mayor |
| Max pico/n >= 100000 | 0.00000200 | 0.00002600 | modelo 13x mayor |

Esto sugiere una hipotesis nueva:

> El modelo independiente captura el comportamiento grueso, pero Collatz real podria tener anti-persistencia en extremos.

Anti-persistencia significa que despues de una serie de bloques favorables, la estructura aritmetica real podria hacer menos probable otra expansion extrema que en un modelo que reelige todo independientemente.

## 6. Records trazados

Los records reales trazados fueron:

| n | Perfil |
| ---: | --- |
| 626331 | record de duracion: 41 bloques |
| 667375 | record de duracion: 41 bloques |
| 704623 | 40 bloques y comparte cola final con 626331 |
| 159487 | record de altura relativa: max pico/n ~= 107860 |
| 270271 | duracion alta y altura alta |
| 288615 | duracion alta y altura alta |
| 704511 | cola inicial 14, altura alta, baja rapido |
| 405407 | duracion alta y altura alta |

La separacion se mantiene: altura y duracion no son la misma propiedad.

## 7. Que se logro

- Se construyo un modelo nulo reproducible.
- Se generaron trazas detalladas de records.
- Se comparo real contra modelo con la misma cantidad de muestras.
- Se encontro que el modelo explica casi todo el cuerpo de la distribucion.
- Se detecto una posible diferencia en extremos: el modelo independiente parece sobreproducir eventos muy raros.

## 8. Que no se logro

- No se probo Collatz.
- No se demostro anti-persistencia.
- No se descarta que la diferencia extrema sea efecto de rango finito o semilla.
- No se puede afirmar originalidad matematica todavia.

## 9. Veredicto

Esta ola cambia la estrategia. Ya no conviene buscar patrones raros sin compararlos contra el modelo geometrico, porque el modelo explica mucho.

La pregunta prometedora queda asi:

> Que dependencia aritmetica real reduce o modula los extremos que el modelo independiente sobreproduce?

Si esa diferencia se mantiene al escalar y puede formalizarse, podria ser una contribucion tecnica seria.
