# Forma de trabajo multiagente para Collatz

Estado: v1.0, revisado despues de respuesta de Claude
Fecha: 2026-04-25
Repo: `collatz`

## Objetivo

Organizar una investigacion colaborativa sobre Collatz sin perder trazabilidad, sin mezclar intuiciones con evidencia y sin convertir varios modelos en ruido.

La idea central:

```text
Un solo repositorio, varias voces, una integracion controlada.
```

Codex actua como orquestador tecnico y custodio de `main`. Claude actua como revisor/critico/proponente. Otros hilos o agentes pueden trabajar en ramas y carpetas separadas con tareas acotadas.

## Principios

1. Ningun agente afirma haber probado Collatz sin una demostracion formal revisada.
2. Toda hipotesis debe responder antes y despues: "estoy en algo virgen?", "alguien ya lo intento?", "que tan lejos estoy de algo relevante?".
3. Los experimentos deben ser reproducibles con script, comando, parametros y salida versionada.
4. Las conclusiones deben distinguir entre prueba, lemma, senal experimental, intuicion y descarte.
5. `main` solo recibe trabajos cerrados, verificados y explicados.
6. Los agentes no pisan archivos centrales sin coordinacion.
7. La literatura externa se revisa antes de vender una idea como nueva.
8. Las olas exploratorias y confirmatorias se separan cuando hay muchas comparaciones.
9. Todo candidato post-hoc necesita una prueba de destruccion antes de convertirse en milestone fuerte.

## Roles

### Usuario

Responsabilidades:

- Define ambicion, tolerancia a riesgo y direccion general.
- Decide si se suman agentes externos.
- Aprueba cambios grandes de estrategia.
- Puede pedir pausa, cambio de foco o auditoria.

No tiene que hacer trabajo mecanico de integracion.

### Codex orquestador

Responsabilidades:

- Mantener `main` limpio.
- Crear y actualizar roadmap, milestones, conclusiones y mapa de investigacion.
- Disenar experimentos reproducibles.
- Validar resultados antes de integrarlos.
- Hacer commits y push de olas cerradas.
- Leer aportes de Claude u otros agentes y convertirlos en tareas concretas.
- Actuar como filtro epistemico: bajar el entusiasmo cuando la evidencia no alcanza.

Archivos bajo control principal:

- `Investigacion.md`
- `InvestigacionMapa.md`
- `Conlusion.md`
- `MILESTONES.md`
- `README.md`
- `reports/*.md`
- `experiments/*.py`
- `src/`
- `tests/`

### Claude

Rol recomendado: critico externo y estratega de investigacion.

Responsabilidades:

- Revisar si el protocolo multiagente es razonable.
- Auditar rigor estadistico: comparaciones multiples, tamanio de muestra, correlacion intra-cadena y seleccion post-hoc.
- Detectar sesgos, saltos logicos o sobreinterpretaciones.
- Buscar si una idea ya existe en papers o preprints.
- Proponer hipotesis alternativas.
- Sugerir experimentos, pero no tocar `main` directamente.
- Escribir sus aportes versionables en la carpeta `colaboradores/revisor-claude/`.
- Usar `Claude/` solo como carpeta local/scratch si hace falta; esta ignorada por git.

Archivos sugeridos:

- `colaboradores/revisor-claude/ConsultaFormaDeTrabajoMultiagente.md`
- `colaboradores/revisor-claude/RespuestaFormaDeTrabajoMultiagente.md`
- `colaboradores/revisor-claude/RevisionM14.md`
- `colaboradores/revisor-claude/NotasLiteratura.md`

### Codex hijo

Rol recomendado: ejecutor tecnico acotado.

Responsabilidades:

- Trabajar una pregunta concreta en una rama propia.
- No modificar archivos centrales salvo que se le asigne.
- Entregar script, CSV y reporte breve.
- No cambiar la historia git.
- No hacer afirmaciones globales sin evidencia.

Ejemplos de tareas:

- Analizar solo `prev_exit_v2 = 5` + `interior_block` por residuos modulo `2^k`.
- Comparar una subpoblacion real contra modelo.
- Optimizar un script sin cambiar el significado del experimento.

## Estructura de carpetas

```text
colaboradores/
  revisor-claude/
    ConsultaFormaDeTrabajoMultiagente.md
    RespuestaFormaDeTrabajoMultiagente.md
    RevisionM14.md
    NotasLiteratura.md
  codex-hijo/
    TareaActual.md
    Resultados.md
    Riesgos.md

Claude/
  ConsultaFormaDeTrabajoMultiagente.md
  RespuestaFormaDeTrabajoMultiagente.md
  RevisionM14.md
  NotasLiteratura.md
```

La carpeta `colaboradores/revisor-claude/` es el espacio versionado de Claude.

La carpeta `Claude/` ya existe, pero esta ignorada por git y se conserva solo como espacio local o importado.

La carpeta `colaboradores/codex-hijo/` se crea solo cuando abramos un hilo hijo operativo.

## Ramas

Rama estable:

```text
main
```

Ramas recomendadas:

```text
codex/m14-residuo-interior
claude/revision-forma-trabajo
claude/revision-m14
codex-hijo/m14-residuos
```

Reglas:

- `main` debe quedar siempre reproducible.
- Claude y agentes hijos trabajan en ramas propias o en archivos asignados.
- Codex orquestador integra a `main` despues de validar.
- No se usa `git reset --hard`.
- No se reescribe historia remota.

## Ciclo de una iteracion

Cada iteracion nueva debe tener tres bloques.

### 1. Antes

Responder por escrito:

```text
1. Estoy en algo virgen?
2. Alguien ya busco esto?
3. Que parte exacta podria ser nueva?
4. Puedo descubrir algo con esto?
5. Que tan lejos estoy de algo relevante?
6. Que evidencia haria que siga?
7. Que evidencia haria que abandone?
```

### 2. Trabajo

Hacer una unidad pequena:

- leer literatura o contexto;
- escribir script;
- correr experimento;
- generar CSV/MD;
- interpretar con cuidado.

No mezclar demasiadas hipotesis en una sola ola.

### 3. Despues

Responder por escrito:

```text
1. La originalidad cambio?
2. La probabilidad de relevancia subio, bajo o quedo igual?
3. Se encontro senal robusta, ruido o descarte?
4. Que aprendimos que no sabiamos antes?
5. Conviene seguir, escalar, formalizar o abandonar?
6. Cual es la siguiente pregunta minima?
```

Despues se actualizan:

- `Investigacion.md`
- `InvestigacionMapa.md`
- `Conlusion.md`
- `MILESTONES.md` si cambia el roadmap
- reporte largo en `reports/`
- resumen fuerte de la ola

## Olas exploratorias y confirmatorias

Una ola es exploratoria cuando:

- busca senales en muchos subgrupos;
- prueba varias particiones;
- elige una celda despues de mirar los datos;
- usa el mismo dataset para generar la hipotesis.

Una ola es confirmatoria cuando:

- pre-registra una hipotesis antes de correr el test;
- define exito y abandono numericamente;
- controla comparaciones multiples;
- usa muestra independiente, permutation test o bootstrap/cluster robust;
- no cambia la hipotesis durante el analisis.

Regla:

```text
Una senal exploratoria no se integra como hallazgo fuerte hasta sobrevivir una ola confirmatoria.
```

## Prueba de destruccion

Antes de escalar o formalizar una senal favorita, debe intentarse destruirla.

Pruebas minimas:

- comparar contra hipotesis nula agresiva;
- contar subgrupos testeados;
- aplicar correccion por comparaciones multiples;
- revisar si hay correlacion intra-cadena;
- buscar explicacion algebraica trivial;
- buscar explicacion por mezcla de subpoblaciones.

Si una senal no sobrevive, se documenta como descarte limpio.

## Protocolo para aportes de Claude

Claude debe responder en:

```text
colaboradores/revisor-claude/RespuestaFormaDeTrabajoMultiagente.md
```

Formato obligatorio:

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

## Primera tarea recomendada para M14

Descripcion concreta.

## Preguntas para Codex orquestador

1.
2.
3.
```

Codex orquestador luego debe:

- leer la respuesta;
- aceptar, rechazar o modificar cada cambio propuesto;
- registrar la decision en este archivo o en un apendice;
- integrar solo lo que mejore trazabilidad, rigor o velocidad.

## Protocolo para Codex hijo

Antes de abrir un hilo hijo, Codex orquestador debe crear:

```text
colaboradores/codex-hijo/TareaActual.md
```

Debe incluir:

```text
Objetivo:
Archivos que puede tocar:
Archivos que no puede tocar:
Comando esperado:
Formato de salida:
Criterio de exito:
Criterio de abandono:
```

El hijo debe entregar:

- script o patch si corresponde;
- reporte breve;
- CSV si hay datos;
- lista de archivos cambiados;
- interpretacion conservadora.

## Criterios de integracion

Un aporte se integra si cumple al menos uno:

- mejora reproducibilidad;
- descarta una hipotesis;
- encuentra una senal con control razonable;
- confirma una senal exploratoria con correccion por comparaciones multiples o test pre-registrado;
- mejora el protocolo;
- conecta con literatura de forma verificable;
- reduce riesgo de sobreinterpretacion.

Un aporte no se integra si:

- solo agrega especulacion;
- no tiene comando reproducible;
- duplica trabajo existente;
- afirma novedad sin busqueda;
- confirma una hipotesis con el mismo dataset que la genero sin advertirlo;
- ignora comparaciones multiples cuando se exploraron muchos subgrupos;
- mezcla demasiadas hipotesis;
- modifica archivos centrales sin permiso.

## Protocolo de evidencia

Niveles:

```text
Nivel 0: intuicion
Nivel 1: observacion manual
Nivel 2: experimento reproducible chico
Nivel 3: experimento reproducible escalado
Nivel 4: lemma formal local
Nivel 5: resultado conectado con literatura
Nivel 6: prueba formal revisada
```

Por defecto, nuestras senales actuales estan en Nivel 2 o 3.

Nada se llama "avance revolucionario" antes de Nivel 5, y nada se llama "demostracion" antes de Nivel 6.

## Comparaciones multiples

Todo reporte que busque senales en subgrupos debe incluir:

```text
Numero de subgrupos testeados:
Numero de metricas testeadas:
Correccion aplicada:
P-valor crudo si corresponde:
P-valor ajustado si corresponde:
```

Bonferroni es aceptable como criterio conservador inicial. Benjamini-Hochberg puede agregarse para exploracion, pero no reemplaza el criterio conservador cuando se decide avanzar de milestone.

## Correlacion intra-cadena

Las transiciones dentro de una misma orbita no deben tratarse automaticamente como independientes.

Cuando una senal depende de muchas transiciones por cadena, se debe usar al menos uno:

- permutation test a nivel de cadena;
- bootstrap por cadena;
- error estandar cluster-robust;
- validacion en muestra independiente.

## Estado actual de la investigacion

Ultima ola cerrada:

```text
Duodecima Ola / M13 - sesgo de supervivencia orbital
```

Hallazgo vigente:

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

Variables candidatas:

- profundidad;
- margen logaritmico antes del bloque;
- residuo de `q` modulo `2^k`;
- residuo del siguiente impar;
- combinacion con duracion total;
- mezcla de subpoblaciones.

## Decision pendiente

Claude respondio en:

```text
colaboradores/revisor-claude/RespuestaFormaDeTrabajoMultiagente.md
```

Decision de Codex orquestador:

```text
Aceptar los cambios metodologicos principales: olas exploratorias vs confirmatorias, prueba de destruccion, comparaciones multiples y cautela por correlacion intra-cadena.
```

Registro especifico para M14:

```text
colaboradores/orquestador/DecisionM14TrasRevisionClaudeYCodexHijo.md
```
