# Roadmap Collatz

Fecha: 2026-04-25
Estado: propuesta operativa

## Recomendacion ejecutiva

Conviene seguir investigando, pero no como lectura abierta. Lo mas valioso ahora es convertir el repo en un laboratorio computacional reproducible sobre Collatz.

No recomiendo intentar una prueba directa como siguiente paso. Ese camino suele producir argumentos fragiles, dificiles de verificar y parecidos a muchas "pruebas" fallidas. Recomiendo apuntar a un aporte mas concreto:

> construir herramientas y datasets propios para estudiar orbitas raras, tiempos de parada, vectores de paridad, clases residuales y desviaciones respecto del modelo aleatorio.

El objetivo seria encontrar patrones medibles, refutar intuiciones debiles y dejar resultados reproducibles. Si aparece una idea teorica fuerte, que nazca de datos limpios y de una formulacion precisa.

## Por que este camino

Collatz sigue abierto. La verificacion computacional publicada llega hasta `2^71` en el trabajo de David Barina de 2025, y el resultado teorico moderno mas fuerte sigue siendo el de Terence Tao: casi todas las orbitas, en densidad logaritmica, alcanzan valores casi acotados. Eso deja una zona natural para aportar desde computacion experimental:

- estudiar casos extremos, no casos promedio;
- medir donde falla la heuristica de independencia de paridades;
- buscar familias con tiempos de parada anormalmente altos;
- comparar residuos modulares y firmas binarias;
- reproducir y auditar afirmaciones existentes antes de construir sobre ellas.

## Tesis de trabajo

La pregunta practica no sera "probamos Collatz?". La pregunta sera:

> que estructura tienen las orbitas que mas se apartan del comportamiento promedio?

Si conseguimos responder eso con datos, graficos, tablas y scripts reproducibles, ya hay un aporte real. El valor no esta en calcular mas alto que todos, sino en mirar mejor.

## Linea donde podemos aportar

La mejor linea inicial es:

> atlas computacional de orbitas extremas y familias anomalas.

Esto combina cuatro objetos:

- tiempo total de parada;
- altura maxima alcanzada;
- vector de paridad;
- clase residual/modular del numero inicial.

La apuesta es que las orbitas extremas no son completamente aleatorias: pueden tener firmas detectables en prefijos binarios, residuos modulo potencias de 2, estructura de bloques impares/pares o patrones de aceleracion.

## Roadmap de 6 semanas

### Semana 1: auditoria y base reproducible

Entregables:

- `AuditoriaFuentesCollatz.md`
- lista de afirmaciones fuertes por nivel de confianza;
- decision tecnica del lenguaje principal: Python para analisis, C/Rust opcional para motor rapido.

Tareas:

- separar fuentes revisadas por pares, arXiv, paginas de proyecto y notas no verificadas;
- auditar especialmente la tercera ola antes de usarla como base;
- fijar convenciones: mapa acelerado, mapa clasico, tiempo de parada y tiempo total de parada;
- crear una carpeta `src/` y una carpeta `data/` ignorada o parcialmente versionada.

### Semana 2: motor Collatz y tests

Entregables:

- implementacion de funciones basicas;
- tests de casos conocidos;
- exportador CSV/Parquet para rangos chicos;
- notebook o script de inspeccion.

Metricas:

- `n`;
- pasos totales;
- pasos hasta bajar de `n`;
- maximo alcanzado;
- cantidad de pasos impares;
- prefijo de paridad;
- residuo modulo `2^k`, `3^k` y combinaciones pequenas.

### Semana 3: atlas de extremos

Entregables:

- tabla de records por rango;
- graficos de tiempo de parada y altura maxima;
- lista de candidatos extremos por escala.

Preguntas:

- que numeros son records de tiempo total;
- que numeros son records de altura maxima;
- si los records comparten prefijos binarios o residuos;
- si hay familias que generan colas mas pesadas que lo esperado.

### Semana 4: paridades y modelo aleatorio

Entregables:

- analisis de vectores de paridad;
- comparacion contra modelo Bernoulli simple;
- mediciones de autocorrelacion, entropia y runs.

Preguntas:

- las orbitas extremas tienen sesgo de paridad temprano;
- los bloques impares aparecen con distribucion esperada;
- que patrones preceden a grandes subidas.

### Semana 5: residuos y mapas inversos

Entregables:

- exploracion por clases residuales;
- arbol inverso parcial;
- candidatos de familias anomalas.

Preguntas:

- que residuos modulo `2^k` concentran altos tiempos de parada;
- si hay clases que se vacian rapido;
- si el arbol inverso muestra cuellos de botella o ramas dominantes.

### Semana 6: reporte y decision

Entregables:

- `InvestigacionSobreCollatzCuartaOla.md`;
- `ResumenInvestigacionSobreCollatzCuartaOla.md`;
- `Conlusion.md` actualizada;
- reporte tecnico con hallazgos y limites.

Decision:

- si aparecen patrones fuertes, abrir una quinta ola teorica;
- si no aparecen, mejorar motor y escalar rangos;
- si aparecen errores en claims previos, corregir el mapa de investigacion.

## Primer bloque de trabajo de 6 a 8 horas

Si me siento varias horas ahora, haria esto:

1. Borrar ruido ajeno al tema y dejar el repo Collatz puro.
2. Auditar las fuentes de las tres olas ya existentes.
3. Crear `AuditoriaFuentesCollatz.md` con tres columnas: afirmacion, fuente, confianza.
4. Crear `src/collatz/` con funciones basicas.
5. Crear tests sobre ejemplos conocidos: `1`, `2`, `3`, `6`, `7`, `27`, potencias de 2 y algunos records.
6. Generar dataset chico para `n <= 1_000_000`.
7. Producir una primera tabla de records.
8. Cerrar con una conclusion honesta: que se confirmo, que se corrigio y que patron merece la proxima ola.

## Criterios de calidad

- Ninguna afirmacion fuerte sin fuente fuerte.
- No mezclar mapa clasico con mapa acelerado sin declararlo.
- No publicar una "prueba" sin formalizacion minima.
- Preferir resultados reproducibles antes que intuiciones lindas.
- Cada grafico debe responder una pregunta.
- Cada dataset debe poder regenerarse.

## Fuentes base confirmadas para arrancar

- David Barina, "Improved verification limit for the convergence of the Collatz conjecture" (2025): https://link.springer.com/article/10.1007/s11227-025-07337-0
- Terence Tao, "Almost all orbits of the Collatz map attain almost bounded values" (2022): https://doi.org/10.1017/fmp.2022.8
- Jeffrey C. Lagarias, "The 3x+1 Problem: An Overview": https://arxiv.org/abs/2111.02635
- Christian Hercher, "There are no Collatz m-Cycles with m <= 91": https://arxiv.org/abs/2201.00406
- Collatz Conjecture Challenge: https://ccchallenge.org/

## Veredicto

Seguir investigando si, pero ya con laboratorio. El aporte razonable no es prometer una prueba: es construir una base experimental confiable, descubrir estructura en los extremos y separar senales reales de ruido.
