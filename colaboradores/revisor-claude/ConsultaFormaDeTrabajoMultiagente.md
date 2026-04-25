# Consulta para Claude - Forma de trabajo multiagente

Fecha: 2026-04-25
Estado: pendiente de respuesta de Claude
Archivo base a revisar: [../../FormaDeTrabajoMultiagente.md](../../FormaDeTrabajoMultiagente.md)

## Contexto

Estamos investigando Collatz en el repo `collatz`.

Codex viene actuando como orquestador: crea experimentos, reportes, conclusiones dinamicas, commits y push.

El usuario quiere sumar a Claude como participante real en la eleccion de la forma de trabajo, no solo como ejecutor.

La propuesta actual es:

```text
Codex = orquestador, integrador y custodio de main.
Claude = critico externo, estratega, auditor de literatura y generador de hipotesis alternativas.
Codex hijo = ejecutor acotado en ramas/carpetas separadas.
```

## Estado tecnico actual

Ultimo resultado cerrado:

```text
M13 / Duodecima Ola - sesgo de supervivencia orbital
```

Lectura vigente:

```text
El modelo independiente explica la supervivencia global, pero queda una dependencia residual despues de `prev_exit_v2 = 5` en bloques interiores.
```

Siguiente milestone:

```text
M14 - Residuo interior despues de `prev_exit_v2 = 5`
```

Pregunta minima:

```text
Dentro de `prev_exit_v2 = 5` + `interior_block`, que variable explica el exceso de `next_tail = 1`?
```

## Lo que se pide a Claude

Claude debe revisar la forma de trabajo propuesta y responder si conviene:

- aceptar el protocolo tal como esta;
- cambiar roles;
- cambiar carpetas o ramas;
- cambiar criterios de evidencia;
- proponer otra forma de colaboracion;
- sugerir primera tarea para M14.

## Preguntas obligatorias

1. Esta division Codex/Claude/Codex-hijo mejora la investigacion o agrega ruido?
2. Que rol deberia tener Claude para aportar mas valor?
3. Que cosas no deberia hacer Claude?
4. Que archivos deberia poder modificar Claude?
5. Conviene que Claude trabaje en rama propia o solo escriba notas?
6. Como evitamos que varios agentes dupliquen trabajo?
7. Que criterio minimo deberia exigirse para integrar un aporte a `main`?
8. Cual deberia ser la primera tarea de Claude para M14?

## Formato de respuesta esperado

Crear o completar:

```text
colaboradores/revisor-claude/RespuestaFormaDeTrabajoMultiagente.md
```

Con este formato:

```text
# Respuesta de Claude - Forma de trabajo multiagente

## Veredicto

Aprobar / aprobar con cambios / rechazar.

## Riesgos principales

1.
2.
3.

## Cambios propuestos al protocolo

1.
2.
3.

## Como deberia participar Claude

1.
2.
3.

## Que no deberia hacer Claude

1.
2.
3.

## Archivos o carpetas que Claude puede tocar

1.
2.
3.

## Archivos o carpetas que Claude no debe tocar sin permiso

1.
2.
3.

## Primera tarea recomendada para M14

Descripcion concreta, con criterio de exito y abandono.

## Preguntas para Codex orquestador

1.
2.
3.
```

## Restricciones

Claude no debe afirmar que hay prueba de Collatz.

Claude debe clasificar cada propuesta como:

```text
intuicion / experimento / lemma candidato / revision literatura / descarte
```

Claude debe favorecer tareas chicas, verificables y con salida escrita.

Claude debe evitar recomendaciones vagas como:

```text
investigar mas
usar IA
buscar patrones
```

sin convertirlas en una tarea concreta.
