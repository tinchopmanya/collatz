# Decision de orquestacion M15 tras revision de Claude

Fecha: 2026-04-25
Estado: decision registrada

## Insumo revisado

- [RevisionDisenoM15.md](../revisor-claude/RevisionDisenoM15.md)

## Preguntas iniciales

```text
1. Estamos avanzando?
Respuesta: si, pero el avance principal es metodologico. M14 nos enseno a no perseguir senales post-hoc sin holdout.

2. Estamos en algo virgen?
Respuesta: no en el marco general. El terreno de modelos geometricos, paridad, stopping times y dinamica 2-adica ya existe. Lo potencialmente util seria una desviacion reproducible con motivacion algebraica.

3. Podemos descubrir algo con M15?
Respuesta: si, pero solo si dejamos de buscar celdas y pasamos a hipotesis pre-registradas con algebra previa.

4. Que tan lejos estamos de algo publicable?
Respuesta: lejos de una prueba; cerca de una nota metodologica o experimental si encontramos un resultado train/holdout robusto o un descarte fuerte.

5. Conviene delegar?
Respuesta: si, pero no para buscar patrones. Claude revisa diseno. Codex hijo ejecuta una tarea algebraica acotada en rama propia. Codex orquestador conserva `main`.
```

## Veredicto

Acepto la recomendacion central de Claude:

```text
M15 debe empezar por algebra antes que datos.
```

No vamos a correr un nuevo barrido estadistico hasta saber si las variables modulares tienen una prediccion teorica distinta de la geometrica.

## Diseno oficial M15 v0.1

Pregunta:

```text
Existe una variable observable al inicio de un bloque que prediga la transicion siguiente mejor que el modelo geometrico independiente, de forma reproducible en holdout?
```

Rangos:

```text
Train:   impares 3 <= n <= 5000000
Holdout: impares 15000001 <= n <= 25000000
Reserva: impares 10000001 <= n <= 15000000
```

El rango `5000001 <= n <= 10000000` queda contaminado como holdout de M14 y no se usa para confirmar M15.

## Orden obligatorio

1. Calculo algebraico previo para `P(next_tail | n mod 2^k)` o una formulacion equivalente.
2. Revision de Claude del resultado algebraico.
3. Pre-registro de hipotesis finales.
4. Experimento train.
5. Sin cambiar hipotesis, experimento holdout.
6. Revision de Claude.
7. Integracion o descarte por Codex orquestador.

## Hipotesis candidatas permitidas

Maximo inicial: 6 tests.

Prioridad:

- H1: prediccion modular de `next_tail` por clases residuales de bajo modulo, si la algebra muestra efecto teorico.
- H2: sobreproduccion de cadenas largas por el modelo.
- H3: autocorrelacion de log-factores consecutivos.
- H4: dependencia global entre `exit_v2` y `next_tail`, como un solo test de independencia, no como celdas aisladas.

H5-H6 quedan reservadas. No se usan sin justificacion previa.

## Variables prohibidas o peligrosas

Prohibidas como hipotesis aisladas:

- `prev_exit_v2 = 5`;
- combinaciones de 3 o mas variables;
- variables derivadas del futuro de la orbita;
- `duration` como predictora;
- residuos modulo `2^k` con `k > 6` sin justificacion algebraica.

Peligrosas, solo como control o descripcion:

- profundidad alta;
- margen logaritmico.

## Criterio de exito

Una hipotesis cuenta como confirmada si cumple todo:

- p ajustado por Bonferroni menor que `0.05` en holdout;
- misma direccion en train y holdout;
- efecto holdout al menos `50%` del efecto train;
- bootstrap por cadena con IC95 que no cruza cero.

## Criterio de abandono

M15 se cierra como descarte si:

- ninguna hipotesis alcanza p ajustado menor que `0.10` en holdout;
- o todos los efectos holdout son menores a `0.01` en proporcion;
- o la algebra muestra que la estructura modular coincide con la prediccion geometrica.

## Decision sobre delegacion

Delegar ahora si, pero solo una tarea:

```text
Codex hijo: calculo algebraico previo de H1.
```

Claude no ejecuta; revisa.

Codex orquestador:

- mantiene `main`;
- revisa ramas;
- integra o descarta;
- actualiza conclusiones.

## Git

Codex hijo debe trabajar en:

```text
codex-hijo/m15-algebra
```

No debe tocar:

- `main`;
- `Conlusion.md`;
- `Investigacion.md`;
- `InvestigacionMapa.md`;
- `MILESTONES.md`;
- `README.md`.

Puede crear:

- `experiments/analyze_m15_algebra.py`;
- `reports/m15_algebra_*.csv`;
- `colaboradores/codex-hijo/ResultadosM15Algebra.md`.

Codex orquestador hara merge o no despues de revisar.
