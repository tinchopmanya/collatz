# Arquitectura de trabajo multiagente para Collatz

Fecha: 2026-04-25
Estado: propuesta operativa
Responsable de decision final: Codex Papa OrquestadorYTomaDeDecisiones

## Veredicto corto

La arquitectura propuesta conviene, pero no como "todos hacen todo en paralelo".
Conviene como una fabrica de decisiones con compuertas:

1. CodexInvestigadorWeb revisa papers y estado del arte antes de decisiones cientificas.
2. ClaudeSocioCritico audita las ideas y busca errores, sesgos y alternativas.
3. Codex Papa Orquestador decide el siguiente paso, integra evidencias y cuida el versionado.
4. CodexHijo1 ejecuta la tarea principal.
5. CodexHijo2 replica, falsifica o implementa una parte disjunta, no duplica trabajo sin motivo.

El objetivo no es ir mas rapido en lineas de codigo. El objetivo es reducir autoengano:
menos anchoring, menos senales post-hoc, menos claims ya conocidos y mas descarte limpio.

## Preguntas obligatorias antes y despues de cada iteracion cientifica

Antes de decidir:

- Estamos en algo potencialmente virgen?
- Alguien ya hizo esto en papers, libros, repositorios o notas recientes?
- Que seria realmente nuevo si sale bien?
- Que resultado destruiria la hipotesis?
- Que tan lejos estamos de un resultado publicable?
- Esta decision necesita web, algebra, experimento o revision critica?
- Estamos por usar holdout fresco o contaminado?

Despues de cada iteracion:

- Avanzamos o solo confirmamos algo conocido?
- La hipotesis quedo mas fuerte, mas debil o descartada?
- El resultado depende de una eleccion post-hoc?
- Hay una explicacion algebraica trivial?
- Hay evidencia independiente o replica?
- Que se debe hacer ahora: cerrar, reformular, escalar o publicar como nota interna?

## Roles

### Codex Papa OrquestadorYTomaDeDecisiones

Responsabilidades:

- Mantener `main` limpio y versionado.
- Elegir el milestone activo.
- Definir las tareas de los hijos.
- No ejecutar computo grande salvo glue minimo, revision o integracion.
- Leer resultados de CodexInvestigadorWeb y ClaudeSocioCritico antes de decisiones cientificas.
- Decidir si una pista se descarta, se reformula o pasa a experimento confirmatorio.
- Hacer cherry-pick, merge o rechazo de ramas.
- Escribir decisiones en `colaboradores/orquestador/`.

No debe:

- Enamorarse de una senal.
- Confirmar una hipotesis con el mismo dataset que la genero.
- Delegar tareas vagas.
- Permitir que un hijo edite `main` directamente.

### CodexHijo1_PrincipalEjecutor

Responsabilidades:

- Implementar la tarea principal definida por el orquestador.
- Trabajar en rama propia `codex-hijo/<milestone>-<tarea>`.
- Crear scripts reproducibles en `experiments/`.
- Guardar reportes en `colaboradores/codex-hijo/`.
- Guardar CSV livianos en `reports/`.
- Hacer commit y push de su rama.

Reglas:

- No toca `main`.
- No toca archivos centrales salvo permiso explicito.
- No mira holdout si la tarea es exploratoria.
- Su entrega debe incluir comando reproducible, archivos tocados, resultado y limites.

### CodexHijo2_ReplicaYFalsacion

Responsabilidades:

- Replicar calculos de CodexHijo1 de forma independiente.
- Buscar contraejemplos, errores de implementacion y contaminacion de datos.
- Implementar un test disjunto si el orquestador lo define.
- Trabajar en rama propia `codex-hijo/<milestone>-replica-<tarea>`.

Reglas:

- No debe copiar el script de CodexHijo1 si la tarea es replica conceptual.
- Debe intentar destruir el resultado antes de confirmarlo.
- Debe declarar si replica exacta, replica parcial o contradice.

### CodexInvestigadorWeb

Responsabilidades:

- Buscar papers, libros, arXiv, notas tecnicas y repositorios relevantes.
- Priorizar fuentes primarias: papers, libros, survey de Lagarias, trabajos de Terras, Everett, Wirsching, Tao, Oliveira e Silva, etc.
- Buscar si la idea ya existe, cuando aparece y con que nombre.
- Separar claramente:
  - conocido en literatura;
  - implicito pero no tabulado;
  - posiblemente nuevo como formulacion experimental;
  - no encontrado, pero no demostrado como nuevo.

Reglas:

- No implementa.
- No decide.
- No exagera novedad.
- Toda afirmacion importante debe tener cita o quedar marcada como no verificada.
- Su salida vive en `colaboradores/investigador-web/`.

### ClaudeSocioCritico

Responsabilidades:

- Auditar las ideas del orquestador.
- Criticar diseno experimental, algebra, sesgos y claims de novedad.
- Leer a CodexInvestigadorWeb antes de opinar sobre direccion cientifica.
- Proponer alternativas.
- Decir "no hagas esto" cuando vea riesgo.

Reglas:

- No responde ordenes del orquestador como subordinado.
- No implementa.
- No decide la direccion final.
- El usuario lo convoca con un prompt independiente.
- Su salida vive en `colaboradores/claude-socio/`.

## Flujo recomendado de una iteracion

1. Orquestador escribe una ficha de decision: pregunta, hipotesis, riesgo, criterio de exito y criterio de abandono.
2. CodexInvestigadorWeb busca si ya existe la idea y entrega un informe con fuentes.
3. ClaudeSocioCritico audita la ficha y el informe web.
4. Orquestador decide:
   - descartar;
   - reformular;
   - pedir algebra previa;
   - pedir implementacion exploratoria;
   - pedir experimento confirmatorio.
5. CodexHijo1 ejecuta la tarea principal.
6. CodexHijo2 replica, falsifica o trabaja una parte disjunta.
7. Orquestador integra solo lo que pase revision.
8. Se actualiza `MILESTONES.md` y se crea una decision en `colaboradores/orquestador/`.

## Git y versionado

Reglas de ramas:

- `main`: solo lo toca el orquestador.
- `codex-hijo/<milestone>-<tarea>`: CodexHijo1.
- `codex-hijo/<milestone>-replica-<tarea>`: CodexHijo2.
- `codex-investigador/<tema>`: CodexInvestigadorWeb, si trabaja dentro del repo.
- `claude-socio/<tema>`: si ClaudeSocioCritico entrega cambios como archivo en rama propia.

Reglas de integracion:

- Cada hijo hace commit y push en su rama.
- El orquestador integra con cherry-pick o merge solo despues de revisar.
- Ningun hijo debe reescribir historia remota.
- Ningun hijo debe borrar archivos ajenos.
- Los datasets grandes no se versionan.
- Los reportes livianos y scripts si se versionan.

Regla practica:

- El orquestador gestiona `main`.
- Los hijos gestionan su propia rama, commit y push.
- Si una tarea es solo conversacional y no modifica archivos, no necesita rama.
- Si una tarea produce un informe que debe quedar en el repo, debe usar rama propia.
- Si un hijo no sabe si debe commitear, debe escribir el archivo, mostrar `git status` y esperar instrucciones del usuario/orquestador.

Plantilla minima de entrega:

```text
Rama:
Commit:
Comando reproducible:
Archivos creados/modificados:
Resultado central:
Que destruye este resultado:
Que no se debe concluir:
Riesgos o dudas:
Siguiente paso recomendado:
```

Formato obligatorio al entregar prompts:

```text
Agente:
Objetivo:
Bloqueante: si/no
Puede empezar ahora: si/no
Depende de:
Desbloquea a:
Rama sugerida:
Archivos permitidos:
Archivos prohibidos:
Git:
Salida esperada:
```

Definiciones:

- `Bloqueante: si` significa que el orquestador no debe tomar la siguiente decision cientifica hasta leer esa salida.
- `Bloqueante: no` significa que puede correr en paralelo sin frenar la decision actual.
- `Puede empezar ahora: no` significa que el usuario no deberia lanzar ese hilo todavia.
- `Desbloquea a` indica que otros agentes esperan ese resultado.

Archivos de plantilla disponibles:

- `colaboradores/orquestador/PlantillaDecisionOrquestador.md`
- `colaboradores/investigador-web/PlantillaInformeInvestigadorWeb.md`
- `colaboradores/claude-socio/PlantillaRevisionCritica.md`
- `colaboradores/codex-hijo/PlantillaEntregaCodexHijo.md`

## Cuando paralelizar y cuando no

Paralelizar si:

- Hay dos calculos independientes.
- Una tarea es implementacion y otra es replica.
- Una tarea es web/literatura y otra es preparacion tecnica sin mirar resultados.
- Las ramas tienen archivos disjuntos.

No paralelizar si:

- La pregunta conceptual todavia no esta definida.
- Dos agentes van a tocar los mismos scripts.
- Falta decidir train/holdout.
- La tarea podria contaminar un holdout.
- El costo de integrar sera mayor que el avance.

## Protocolo de novedad

Una idea no se trata como nueva hasta pasar cuatro filtros:

1. Busqueda web/papers por CodexInvestigadorWeb.
2. Auditoria critica por ClaudeSocioCritico.
3. Replica independiente por CodexHijo2 si hay computo o algebra.
4. Decision escrita por el orquestador con nivel de novedad:
   - Nivel 0: error o ruido.
   - Nivel 1: conocido y reproducido.
   - Nivel 2: conocido, pero util para nuestro modelo.
   - Nivel 3: formulacion propia de algo implicito.
   - Nivel 4: resultado local potencialmente comunicable.
   - Nivel 5: avance serio que requiere revision matematica externa.

## Aplicacion inmediata a M15

Estado actual:

- `q mod 8` predice algebraicamente `next_tail`.
- Eso es real, replicado y auditado.
- No es por si solo un resultado nuevo fuerte.
- La pregunta relevante es si el modelo modular mejora la prediccion de supervivencia orbital frente al modelo geometrico independiente.

Siguiente iteracion recomendada:

1. CodexInvestigadorWeb:
   - buscar literatura sobre modelos 2-adicos, stopping time probabilistico, Terras/Wagstaff/Wirsching y correcciones modulares al modelo geometrico;
   - responder si una comparacion `q mod 8` vs modelo geometrico para supervivencia ya existe.
2. ClaudeSocioCritico:
   - auditar si H1-modelo esta bien formulada o si es tautologica;
   - proponer criterio de exito y abandono.
3. CodexHijo1:
   - solo despues de esas dos entradas, disenar el script de comparacion modular sin tocar holdout.
4. CodexHijo2:
   - preparar replica/falsacion del diseno, no correr la misma cosa.
5. Orquestador:
   - decide si M15 pasa a experimento train/holdout o se descarta por conocido/tautologico.

## Mi recomendacion como orquestador

Usaria esta arquitectura, pero con una regla: no todos los agentes trabajan todo el tiempo.
El sistema ideal es una mesa chica que se activa por compuertas.

Para M15 ahora activaria:

- CodexInvestigadorWeb: si, inmediatamente.
- ClaudeSocioCritico: si, despues del informe web.
- CodexHijo1: todavia no, salvo para preparar esqueleto sin correr datos.
- CodexHijo2: todavia no, hasta que exista diseno que replicar o falsar.

Esto mantiene velocidad sin convertir el proyecto en una fabrica de archivos.
