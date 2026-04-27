# Metodologia de descartes disciplinados

## Que es esto

Este documento resume la metodologia que el proyecto Collatz Lab desarrollo a lo largo de 18 milestones para investigar computacionalmente un problema matematico abierto sin producir claims inflados. Sirve como template reutilizable para cualquier investigacion computacional exploratoria.

El proyecto no probo ni refuto la conjetura de Collatz. Lo que si logro fue testear 6 hipotesis computacionales con rigor, descartarlas limpiamente cuando no generalizaron, y cerrar sin afirmaciones falsas. Este documento explica como.

## El problema que resuelve

La investigacion computacional exploratoria tiene un sesgo estructural: es facil encontrar patrones en datos suficientemente grandes, y es tentador interpretar cada patron como descubrimiento. Sin disciplina, un proyecto computacional genera una cadena de "hallazgos" que son artefactos estadisticos, efectos de finitud, o resultados conocidos reempaquetados.

Este proyecto enfrento ese problema directamente y lo resolvio con un protocolo de 5 componentes.

## Componente 1: Preguntas obligatorias antes y despues

Antes de cada experimento, responder por escrito:

1. Estamos en algo potencialmente virgen?
2. Alguien ya hizo esto? (requiere busqueda web, no solo intuicion)
3. Que seria nuevo si sale bien?
4. Que resultado destruiria la hipotesis?
5. Que tan lejos estamos de algo publicable?
6. Hay riesgo post-hoc? (estamos eligiendo la hipotesis despues de ver los datos?)
7. Hay explicacion algebraica trivial?

Despues del experimento:

1. La originalidad cambio?
2. La probabilidad de relevancia subio?
3. Senal robusta o descarte?
4. Que aprendimos?
5. Seguir o abandonar?

Las respuestas quedan versionadas en el repo. No se permiten respuestas retroactivas.

## Componente 2: Separacion train/holdout

Dividir los datos en rangos antes de mirar:

- **Train (quemado):** se usa para explorar, calibrar, buscar patrones. Una vez tocado, no sirve como evidencia.
- **Holdout (fresco):** se reserva para validacion. Solo se toca una vez, con hipotesis preregistrada.

En este proyecto:
- Train: n in [3, 5M] (quemado en M12-M16)
- Holdout parcial: n in [5M, 10M] (usado en M14)
- Holdout fresco: n in [15M, 25M] (reservado hasta M17)

Regla estricta: si una senal no sobrevive en holdout fresco, se descarta. Sin excepciones.

## Componente 3: Correccion por comparaciones multiples

Cada vez que se hacen N tests simultaneos, aplicar correccion de Bonferroni: el umbral de significancia se divide por N.

En este proyecto se usaron consistentemente 3 tests por milestone con alfa = 0.05/3 = 0.0167. Esto evita que 1 de 20 tests salga "significativo" por azar.

## Componente 4: Busqueda web antes de claims

Antes de afirmar que algo es nuevo, buscar en la web si ya existe. No basta con "no recuerdo haberlo visto"; hace falta una busqueda real con queries especificas.

Formulacion correcta: "no encontrado en la busqueda realizada" (no "nadie lo hizo").

En este proyecto, la busqueda web encontro a Bonacorsi-Bordoni (arXiv:2603.04479) que ya documentaban el fenomeno principal que estabamos estudiando. Sin esa busqueda, habriamos inflado el claim de novedad.

## Componente 5: Escala de novedad honesta

Clasificar cada resultado en una escala fija:

| Nivel | Descripcion |
|-------|-------------|
| 1 | Reproducir algo conocido |
| 2 | Formular algo conocido de forma propia sin informacion nueva |
| 2.5 | Identificar mecanismo propio para fenomeno ya observado |
| 3 | Resultado comunicable (nota tecnica, blog serio) |
| 4 | Resultado publicable (paper, arXiv) |
| 5 | Avance serio que requiere revision externa |

El proyecto alcanzo maximo 2.5. Lo importante no es el numero sino la honestidad de la evaluacion. Un proyecto que dice "2.5" cuando es 2.5 tiene mas valor que uno que dice "4" cuando es 2.

## Ejemplo concreto: los 6 descartes

### M12: exit_v2 = 5 como congruencia especial
- Hipotesis: exit_v2 = 5 produce sesgo aritmetico real.
- Realidad: algebra local correcta (3^s q = 33 mod 64), pero en muestra completa el efecto desaparece.
- Mecanismo de descarte: al descondicionar por supervivencia, la senal se disuelve.
- Leccion: condicionar por supervivencia puede crear senales donde no las hay.

### M13: Sesgo de supervivencia posicional
- Hipotesis: las cadenas sobrevivientes no muestrean uniformemente.
- Realidad: el modelo independiente explica el sesgo por posicion (final vs interior).
- Mecanismo de descarte: el modelo simple es suficiente.
- Leccion: antes de buscar explicaciones complejas, verificar que la simple no baste.

### M14: Residuo prev_exit_v2 = 5 + interior
- Hipotesis: esta celda tiene dependencia real no capturada.
- Realidad: en holdout [5M, 10M], la diferencia cae a 0.009 con p = 0.43.
- Mecanismo de descarte: holdout independiente.
- Leccion: si la senal no replica, no es senal.

### M15: q mod 8 como memoria entre bloques
- Hipotesis: q mod 8 tiene memoria suficiente para mejorar prediccion.
- Realidad: la matriz de transicion mezcla casi uniforme en 1 paso (max TV = 0.00006).
- Mecanismo de descarte: algebra (la transicion borra la memoria).
- Leccion: verificar algebraicamente antes de computar.

### M16: Sesgo de profundidad explica sobreproduccion
- Hipotesis: bloques tardios tienen drift mas negativo, explicando el gap.
- Realidad: correcto en train, pero el modelo corregido sobrecompensa en validacion.
- Mecanismo de descarte: split validation muestra sobrecompensacion.
- Leccion: un mecanismo cualitativo correcto no implica un modelo cuantitativo util.

### M17+M18: Validacion en holdout fresco y ratio por rango
- Hipotesis: el modelo corregido mejora en holdout; el gap cambia de signo con n.
- Realidad: 0/3 tests significativos en holdout. 0/36 tests significativos en 10 bins. El unico efecto es finitud en n < 2.5M.
- Mecanismo de descarte: holdout fresco + multiples rangos.
- Leccion: dos data points no son una tendencia.

## Cuando cerrar un proyecto

El protocolo tiene una compuerta de cierre implicita. Cerrar cuando:

1. Las preguntas obligatorias no pueden identificar una hipotesis con ceiling > 3.
2. La busqueda web no revela direcciones compatibles con la infraestructura.
3. El holdout fresco no confirma ninguna senal.
4. Seguir requeriria inventar hipotesis post-hoc para justificar la inercia.

Cerrar no es fracasar. 6 descartes limpios en un problema famoso, sin una afirmacion inflada, es un resultado metodologico valioso.

## Como reutilizar esto

Para aplicar esta metodologia a otro problema computacional:

1. Copiar las preguntas obligatorias a un archivo en el repo.
2. Definir rangos de train y holdout ANTES de mirar datos.
3. Fijar el numero de tests por milestone y aplicar Bonferroni.
4. Antes de cada claim, hacer busqueda web con queries especificas.
5. Usar la escala de novedad en cada reporte.
6. Versionar todas las decisiones (no editar retroactivamente).
7. Establecer criterios de abandono antes de empezar cada experimento.

## Creditos y contexto

Proyecto: Collatz Lab, 18 milestones (M0-M17 + M18 de cierre), 2026.
Agentes: Codex orquestador, Codex hijos, ClaudeSocio (agente principal desde M16).
Infraestructura: Python, motor odd-to-odd, datasets hasta 25M impares.
Resultado principal: el modelo geometrico i.i.d. es baseline correcto y suficiente.

## Referencias recientes verificadas

- Bonacorsi-Bordoni, "Bayesian Modeling of Collatz Stopping Times", arXiv:2603.04479.
- "An Explicit Near-Conjugacy Between the Collatz Map and a Circle Rotation", arXiv:2601.04289.

Estas referencias no convierten el proyecto en un resultado publicable; sirven para ubicar honestamente el nivel de novedad y evitar claims inflados.
