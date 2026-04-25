# Decision M15 tras algebra, replica y revision de Claude

Fecha: 2026-04-25
Estado: decision registrada

## Insumos

- Codex hijo 1: [ResultadosM15Algebra.md](../codex-hijo/ResultadosM15Algebra.md)
- Codex hijo 2: [ReplicaM15Algebra.md](../codex-hijo/ReplicaM15Algebra.md)
- Claude: [RevisionM15Algebra.md](../revisor-claude/RevisionM15Algebra.md)
- Scripts:
  - [analyze_m15_algebra.py](../../experiments/analyze_m15_algebra.py)
  - [replicate_m15_algebra.py](../../experiments/replicate_m15_algebra.py)

## Preguntas iniciales

```text
1. Estamos avanzando?
Respuesta: si. Pasamos de una pista post-hoc descartada a un resultado algebraico local verificado por dos implementaciones y por Claude.

2. Estamos en terreno virgen?
Respuesta: no en el mecanismo general. La dependencia modular baja es esperable desde dinamica 2-adica, Terras/Wagstaff/Wirsching/Lagarias. La tabla exacta `q mod 8 -> next_tail` puede ser una explicitacion util, pero no una novedad profunda.

3. Podemos encontrar algo importante?
Respuesta: baja probabilidad de una prueba. Moderada-baja probabilidad de una mejora concreta del modelo geometrico si el modelo modular reduce la sobreproduccion de cadenas largas.

4. Conviene delegar mas?
Respuesta: si, pero solo con roles cerrados. Claude revisa diseno y literatura. Codex hijos replican o ejecutan tareas acotadas. No conviene abrir buscadores libres de patrones.
```

## Resultado algebraico integrado

Codex hijo 1 encontro y Codex hijo 2 replico:

```text
q mod 4 coincide con la geometrica.
q mod 8 no coincide clase por clase.
```

Predicciones verificadas:

| q mod 8 | P(next_tail = 1) |
| ---: | ---: |
| 1 | 5/6 |
| 3 | 2/3 |
| 5 | 1/6 |
| 7 | 1/3 |

El promedio marginal vuelve a:

```text
P(next_tail = 1) = 1/2
```

por cancelacion entre clases.

## Decision clave

Acepto la critica de Claude:

```text
No debemos testear en holdout si la tabla q mod 8 es correcta.
```

La tabla es algebra local. Confirmarla estadisticamente seria gastar holdout en una identidad.

## Reformulacion oficial de H1

H1 deja de ser:

```text
q mod 8 predice next_tail?
```

y pasa a ser:

```text
H1-modelo: un modelo modular que usa P(next_tail | q mod 8) mejora la prediccion de supervivencia orbital frente al modelo geometrico independiente?
```

Pregunta operacional:

```text
El modelo modular reduce la sobreproduccion de cadenas largas documentada en M9?
```

## Criterio de exito para H1-modelo

H1-modelo avanza solo si:

- mejora contra el modelo geometrico en train y holdout;
- la mejora tiene la misma direccion;
- reduce la brecha real-modelo en cadenas largas (`blocks_to_descend >= k`);
- no requiere subir inmediatamente a `q mod 16`, `q mod 32`, etc.

## Criterio de abandono

H1-modelo se descarta si:

- el modelo modular produce la misma sobreproduccion de extremos que el geometrico;
- o mejora solo en train pero no en holdout;
- o solo mejora al subir a modulos mas altos sin principio de parada.

## Sobre mas hijos

Se puede trabajar en paralelo, pero solo con estos roles:

- Claude: auditor adversarial y literatura.
- Codex hijo 1: autor del calculo algebraico.
- Codex hijo 2: replica independiente.
- Codex hijo futuro: implementador de modelo modular, solo despues de pre-registro.

No se abren hijos para "buscar patrones".

## Proxima decision tecnica

Antes de programar holdout, hay que definir el modelo modular.

Opciones:

1. Modelo geometrico base:

```text
tail_i ~ Geom(1/2)
exit_v2_i ~ Geom(1/2)
```

2. Modelo modular minimo:

```text
q_i mod 8 evoluciona o se re-muestrea?
next_tail_i ~ P(. | q_i mod 8)
exit_v2_i ~ Geom(1/2)
```

Problema:

```text
Si q_i mod 8 se re-muestrea uniforme en cada bloque, el promedio marginal cancela y el modelo modular colapsa casi al geometrico.
```

Por lo tanto, la pregunta crucial es si las cadenas largas seleccionan residuos `q mod 8` de manera no uniforme o si hay dinamica de transicion de `q mod 8` entre bloques.

## Proxima tarea recomendada

No correr [15M, 25M] todavia.

Primero disenar:

```text
experiments/design_m15_modular_model.py
```

o documento equivalente que especifique:

- estado del modelo: `q mod 8`;
- transicion de estado;
- distribucion de `next_tail`;
- distribucion de `exit_v2`;
- metrica de comparacion contra datos reales;
- criterios train/holdout.

Despues Claude debe revisar ese diseno antes de ejecutar.
