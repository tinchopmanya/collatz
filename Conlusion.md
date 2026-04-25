# Conlusion dinamica

Ultima actualizacion: 2026-04-25
Tema activo: Collatz Lab - motor minimo y records iniciales

## Conlusion ejecutiva

La mejor forma de seguir no es intentar una prueba directa de la conjetura de Collatz ni seguir acumulando lectura sin salida. El repo ya empezo a convertirse en un laboratorio computacional reproducible.

Ya existe un motor Collatz minimo con tests y un primer script de records. Para `n <= 1000000`, los records iniciales muestran que las metricas no coinciden: el mayor tiempo total aparece en `837799`, el mayor stopping time en `626331` y la mayor altura maxima en `704511`. Eso confirma que conviene estudiar cada metrica por separado.

El analisis por residuos modulo `128`, `256` y `512` para `n <= 1000000` muestra una senal candidata estable: la familia `-1 mod 2^k` queda primera por promedio de pasos totales y por promedio de stopping time en los tres niveles (`127`, `255`, `511`). Ademas, `511 mod 512` contiene el record de altura maxima del rango. Todavia es exploratorio, pero ya es el primer patron propio del laboratorio que merece una ola dedicada.

Antes de construir encima de las olas anteriores, conviene auditar las fuentes y separar afirmaciones fuertes de hipotesis o notas no verificadas. La base confiable inicial es: Lagarias para panorama, Tao para el avance teorico mayor, Barina para verificacion hasta `2^71`, Hercher para ciclos y el Collatz Conjecture Challenge como mapa de literatura/formalizacion.

## Siguiente paso

Arrancar el roadmap de [RoadmapCollatz.md](RoadmapCollatz.md):

- agregar analisis de prefijos de paridad;
- medir prefijos de paridad de la familia `-1 mod 2^k`;
- completar la auditoria de fuentes de la tercera ola;
- cerrar una cuarta ola con hallazgos, limites y proxima hipotesis.
