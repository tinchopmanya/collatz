# M19 - Investigacion de terreno: rewriting/SAT para Collatz

Fecha: 2026-04-27
Pregunta: estamos en terreno virgen con la via Yolcu-Aaronson-Heule de Collatz como terminacion de sistemas de reescritura?

## Respuesta corta

No. El enfoque central ya esta recorrido.

La idea de reformular Collatz como terminacion de sistemas de reescritura, usar representaciones mixtas binario-ternarias, aplicar interpretaciones matriciales/arctic/tropical y buscar pruebas con SAT ya fue desarrollada por Yolcu, Aaronson y Heule. El trabajo existe como paper, version arXiv, articulo revisado y codigo asociado.

Lo que podria quedar como aporte no es "descubrir la via", sino:

- reproducirla de forma limpia;
- auditar sus pruebas y dependencias;
- portar la reproduccion a CI/Linux;
- buscar una extension pequena no listada en sus logs;
- conectar esa linea con formalizacion/certificacion.

## Fuentes primarias

### Yolcu-Aaronson-Heule

Fuente: "An Automated Approach to the Collatz Conjecture"

- arXiv: https://arxiv.org/abs/2105.14697
- Journal of Automated Reasoning: https://link.springer.com/article/10.1007/s10817-022-09658-8
- PDF CADE/short version: https://www.cs.cmu.edu/~mheule/publications/WST21.pdf
- Codigo asociado: https://github.com/emreyolcu/rewriting-collatz

Fechas verificadas:

- arXiv v1: 2021-05-31.
- arXiv v3: 2022-12-31.
- Journal of Automated Reasoning: publicado 2023-04-25.

Lo que cubre:

- construyen un sistema de reescritura que simula Collatz en representaciones mixtas binario-ternarias;
- prueban que la terminacion de ese sistema es equivalente a Collatz;
- prueban limitaciones de un sistema unary previo frente a interpretaciones matriciales naturales;
- implementan un prover minimo con interpretaciones natural/arctic;
- encuentran pruebas automaticas de debilitamientos no triviales de Collatz;
- no prueban Collatz.

Conclusion:

```text
La direccion M19 no es virgen; es una linea publicada.
```

### Busqueda web 2025-2026

Consulta realizada el 2026-04-27 sobre trabajos recientes de Collatz + rewriting + SAT + termination.

Resultado:

- no encontre una continuacion primaria mas reciente que desplace a Yolcu-Aaronson-Heule como referencia central de esta via;
- si aparecieron trabajos recientes de verificacion computacional de rangos, por ejemplo Barina 2025, pero pertenecen a otra familia: verificar convergencia hasta un limite, no buscar pruebas de terminacion por rewriting/SAT;
- aparecieron preprints y articulos divulgativos que dicen probar Collatz, pero no cambian el mapa de esta linea sin validacion fuerte por literatura reconocida.

Conclusion:

```text
A fines de abril de 2026, la referencia fuerte para M19 sigue siendo Yolcu-Aaronson-Heule; no estamos ante una via nueva descubierta por nosotros.
```

### Zantema y antecedentes de rewriting

El articulo de Springer referencia trabajos previos de Zantema y de terminacion por interpretaciones matriciales:

- Zantema, "Termination of string rewriting proved automatically", Journal of Automated Reasoning, 2005.
- Hofbauer-Waldmann, "Termination of string rewriting with matrix interpretations", RTA 2006.
- Endrullis-Waldmann-Zantema, "Matrix interpretations for proving termination of term rewriting", Journal of Automated Reasoning, 2008.
- Sabel-Zantema, "Termination of cycle rewriting by transformation and matrix interpretation", 2017.

Conclusion:

```text
Incluso las herramientas de base tampoco son nuevas; pertenecen a una literatura de terminacion automatica.
```

### Collatz Challenge

Fuente: https://ccchallenge.org/

El proyecto Collatz Challenge apunta a formalizar literatura existente de Collatz. Esto indica que una via seria con valor alto podria ser formalizacion/auditoria de resultados conocidos, no necesariamente nueva matematica.

Conclusion:

```text
El terreno formal tambien esta activo y recorrido, pero hay espacio para aportes de formalizacion reproducible.
```

## Evaluacion de novedad

| Candidato | Terreno virgen? | Nivel posible | Comentario |
| --- | --- | ---: | --- |
| Reproducir Yolcu-Aaronson-Heule | No | 1-2 | Reproduccion util, no novedad |
| Portar a CI/Linux reproducible | Parcial | 2-3 | Aporte de infraestructura si queda limpio |
| Auditar/certificar pruebas existentes | Parcial | 3 | Valor metodologico, no prueba de Collatz |
| Encontrar un debilitamiento nuevo probado por SAT | Posible | 3-4 | Requiere frontera clara y comparacion con logs existentes |
| Probar Collatz via rewriting | No evaluable | 5 | Altisimo ceiling, probabilidad muy baja |

## Respuesta a la pregunta del usuario

No estamos en terreno virgen si lo que decimos es:

```text
Collatz como terminacion de sistemas de reescritura.
```

Eso ya existe.

Podriamos estar en terreno parcialmente nuevo si formulamos algo mucho mas estrecho:

```text
Reproducir y extender automaticamente una clase residual/debilitamiento no cubierta por los logs de rewriting-collatz, con prueba SAT y parametros versionados.
```

Pero todavia no sabemos si esa extension existe. Primero hay que reproducir el baseline.

## Decision para M19

M19 sigue permitido solo como fase de reproduccion/auditoria.

No se debe narrar como "nueva via descubierta".

La frase correcta es:

```text
Estamos entrando a una linea existente con ceiling mas alto que la estadistica odd-to-odd, para ver si podemos reproducirla y quizas aportar una extension pequena.
```

## Criterio para seguir

Seguir si:

- reproducimos al menos una prueba base;
- entendemos los parametros del prover;
- comparamos contra todos los logs existentes;
- identificamos una extension concreta no cubierta.

Abandonar si:

- solo podemos reproducir resultados ya publicados;
- no hay entorno estable;
- cualquier extension requiere busqueda SAT abierta sin principio de parada;
- el trabajo se vuelve "otro intento de prueba" sin certificacion.
