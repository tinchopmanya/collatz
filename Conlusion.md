# Conlusion dinamica

Ultima actualizacion: 2026-04-25 01:57:35 -03:00
Tema activo: Collatz - Cuarta Ola cerrada

## Conlusion ejecutiva

La cuarta ola convirtio el repo en un laboratorio computacional reproducible. Ya no estamos solo leyendo sobre Collatz: ahora hay codigo, tests, scripts de analisis y reportes.

El laboratorio reprodujo records hasta `n <= 1000000`: `837799` tiene el mayor tiempo total, `626331` el mayor stopping time y `704511` la mayor altura maxima. Esto confirma que duracion, primer descenso y crecimiento maximo deben analizarse como metricas distintas.

El analisis por residuos modulo `128`, `256` y `512` redetecto la familia `-1 mod 2^k` (`127`, `255`, `511`) como clase de promedio alto para pasos totales y stopping time. La auditoria mostro que esto no es un descubrimiento nuevo: esta alineado con Terras, Klee-Wagon, OEIS A324248 y literatura sobre clases residuales. El aporte propio es reproducirlo, cuantificarlo y conectarlo con paridad y excursion temprana.

El hallazgo operativo mas util es que `511 mod 512` tiene casi 20 pasos alternantes promedio y el mayor pico temprano promedio entre las clases comparadas. Eso sugiere el siguiente objetivo: formalizar un lemma pequeno sobre prefijos alternantes para `n == -1 mod 2^k`.

## Veredicto

No hay prueba de Collatz ni novedad revolucionaria todavia. Si hay un avance metodologico real: una base experimental honesta, actualizada y reproducible que permite separar senales conocidas, mediciones nuevas y posibles lemmas formalizables.

## Siguiente paso

Abrir una quinta ola teorica-computacional:

- formalizar el lemma de prefijo alternante para `2^k - 1`;
- derivar una cota inferior de excursion temprana;
- comparar formalmente contra `2^k - 2`;
- revisar como esto se conecta con Terras, Klee-Wagon y Mersenne tails;
- decidir si el resultado alcanza para una nota tecnica publicable.
