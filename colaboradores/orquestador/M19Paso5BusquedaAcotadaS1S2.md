# M19 paso 5 - busqueda acotada S1/S2

Fecha: 2026-04-27
Responsable: Codex orquestador
Estado: infraestructura de busqueda preparada

## Preguntas antes

- Estamos en terreno virgen?
  - Parcialmente. S1/S2 son desafios explicitamente abiertos por Yolcu-Aaronson-Heule, pero la tecnica general ya esta recorrida.
- Podemos descubrir algo con esto?
  - Si, si una herramienta encuentra una prueba para S1 o S2 con parametros no reportados. Seria un avance real en un subproblema publicado, no una prueba de Collatz.
- Ya alguien estuvo buscando esto?
  - Si. Los autores reportaron miles de CPU-horas sin encontrar interpretaciones para estos dos subsistemas.
- Que tan lejos estamos?
  - Ahora estamos a una ejecucion CI de hacer una busqueda reproducible pequena. Todavia lejos de un resultado fuerte.

## Accion

Se agrego un runner:

```text
scripts/m19_run_rewriting_challenge_grid.py
```

Y un workflow manual:

```text
.github/workflows/m19-rewriting-challenge-search.yml
```

El workflow:

- clona `rewriting-collatz` en el commit auditado;
- instala Python/NumPy;
- compila CaDiCaL en commit pinneado;
- copia los archivos S1/S2 generados en M19 paso 4;
- ejecuta una grilla acotada de interpretaciones, dimensiones y result-widths;
- guarda logs por celda;
- produce `m19_challenge_grid.csv` y `m19_challenge_grid.md`;
- corta temprano si encuentra `QED`.

## Defaults prudentes

```text
challenge: both
interpretations: natural,arctic
dimensions: 1-3
result_widths: 2-5
solver_timeout: 30
wall_timeout: 60
workers: 4
tries: 1
remove_any: true
```

Estos defaults no intentan competir con miles de CPU-horas. Solo validan que la tuberia funciona y buscan una prueba chica si existe.

## Criterio de exito

Exito fuerte:

```text
status = QED
```

para S1 o S2 en una celda no trivial.

Exito tecnico:

```text
logs + CSV + Markdown generados sin errores
```

aunque no haya QED.

## Criterio de abandono

Abandonar esta micro-ruta si:

- no podemos ejecutar CI;
- el workflow no logra reproducir entorno CaDiCaL;
- todas las celdas pequenas fallan y no hay razon teorica para ampliar;
- ampliar significaria repetir "miles de CPU-horas" sin insight nuevo.

## Preguntas despues

- Avanzamos?
  - Si: pasamos de archivos S1/S2 a una busqueda reproducible acotada.
- Hay resultado matematico?
  - No todavia.
- Es terreno virgen?
  - No la tecnica; si el borde especifico S1/S2 sigue abierto.
- Que toca?
  - Ejecutar primero `M19 rewriting reproduction` con `proof_set=zantema`. Si pasa, ejecutar `M19 rewriting challenge search` con defaults.
