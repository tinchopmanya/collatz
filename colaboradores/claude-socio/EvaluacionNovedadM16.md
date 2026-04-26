# Evaluacion honesta de novedad - M16

Fecha: 2026-04-25
Agente: ClaudeSocio

## Que encontramos en M16

El modelo geometrico i.i.d. sobreproduce cadenas largas. La causa es que los bloques tardios de cadenas sobrevivientes tienen drift ~0.013 mas negativo que el primer bloque. Esto es un sesgo de supervivencia condicional por profundidad: E[exit_v2] sube a ~2.012 en bloques 8-10 mientras E[tail] baja a ~1.98. No hay autocorrelacion significativa en lags 1-5.

## Que dice la literatura

Busque en 5 rondas de web search. Resultado:

1. **Kontorovich-Lagarias (2009):** definen el modelo RRW y predicen constantes de extremos. Dicen que las predicciones "agree fairly well" con datos. No reportan ni discuten sobreproduccion de extremos del modelo vs realidad.

2. **Bonacorsi-Bordoni (2026):** su NB2-GLM y modelo generativo de bloques "mildly overestimate extreme right-tail mass" en el posterior predictive check. Documentan el fenomeno pero NO lo explican ni lo descomponen en causas. Tambien usan `n mod 8` como covariable.

3. **No encontrado en la busqueda realizada:** ni la medicion de drift condicional por profundidad de bloque dentro de cadenas sobrevivientes, ni la descomposicion del gap en componentes (drift, correlacion, finitud, profundidad), ni un modelo corregido por profundidad. Esto no equivale a que no exista; puede estar en literatura no indexada o bajo formulaciones equivalentes.

4. **El sesgo de supervivencia como concepto** es ubicuo en estadistica pero NO lo encontre aplicado especificamente a explicar la sobreproduccion de extremos en modelos estocasticos de Collatz.

## Evaluacion honesta de novedad

### Lo que NO es nuevo (nivel 0-1):
- Que el modelo geometrico i.i.d. es un buen baseline: conocido desde Lagarias-Weiss 1992.
- Que modelos estocasticos sobreestiman colas: observado por Bonacorsi-Bordoni 2026.
- Que los modelos de random walk predicen constantes de extremos: Kontorovich-Lagarias 2009.
- La conexion entre Collatz y random walks con drift negativo: conocido desde los 70s.

### Lo que PARECE ser propio del proyecto (nivel 2-3):
- Medir drift condicional por profundidad de bloque y mostrar que crece (se vuelve mas negativo).
- Identificar que E[exit_v2] sube en bloques tardios como mecanismo del sesgo.
- Descomponer el gap en: finitud (~40%), drift (~30%), residuo (~30%).
- Mostrar que autocorrelacion lag 1-5 es ~0, descartando correlaciones locales.
- Construir un modelo corregido por profundidad que reduce el gap 82% en k=20.

### Lo que NO podemos afirmar:
- Que descubrimos un fenomeno nuevo (la sobreproduccion ya estaba documentada).
- Que nuestra explicacion es la unica posible.
- Que el resultado es publicable como paper independiente.
- Que esto acerca la prueba de Collatz.

## Que tan cerca estamos de algo nuevo

**Respuesta honesta: estamos en nivel 2.5 de 5.**

- Nivel 1: reproducir algo conocido.
- Nivel 2: formular algo conocido de forma propia pero sin aportar informacion nueva.
- **Nivel 2.5 (nosotros): identificar un mecanismo especifico (sesgo de profundidad) para un fenomeno ya observado pero no explicado. La explicacion es propia y verificable, pero usa herramientas estandar.**
- Nivel 3: resultado local comunicable (nota tecnica publicable en un workshop o blog tecnico serio).
- Nivel 4: resultado publicable en revista o arXiv.
- Nivel 5: avance serio que requiere revision matematica externa.

Para subir a nivel 3, necesitariamos: (a) validar en holdout fresco que el modelo corregido funciona, (b) derivar algebraicamente por que E[exit_v2 | sobrevive d bloques] crece con d, y (c) comparar contra el modelo de Bonacorsi-Bordoni.

Para subir a nivel 4, necesitariamos: un resultado teorico, no solo empirico.

## Decision

Dado que estamos en nivel 2.5, las opciones realistas son:

**Opcion 1: Intentar subir a nivel 3.** Validar en holdout y derivar algebra. Costo: moderado. Riesgo: que el holdout no confirme, o que la algebra sea trivial.

**Opcion 2: Consolidar y cerrar.** Escribir reporte tecnico M12-M16, documentar el hallazgo como resultado interno, y buscar una pregunta con mas potencial de novedad.

**Mi decision: Opcion 2.** Razon: el costo de subir de 2.5 a 3 es moderado pero el valor marginal es bajo. Un resultado nivel 3 en Collatz no cambia el campo. Es mejor documentar limpiamente y, si el proyecto continua, buscar una pregunta con ceiling mas alto.
