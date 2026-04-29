# M22 kill criteria

Fecha: 2026-04-29
Agente: CodexHijo-M22-Critic
Rama: `codex-hijo/m22-kill-criteria`
Estado: revision critica; sin cambios de codigo

## Resumen critico

M22 todavia no es una prueba ni un resultado publicable fuerte. La senal
existente es una reduccion cuantitativa prometedora: los certificados low-bit de
M21 descargan una fraccion grande de las ramas residuales que M22 asocia con
los sistemas de reescritura de M19/Yolcu-Aaronson-Heule. La mejor fotografia
local es S2 con `k = 16`: `7814/8192` residuos de la rama `5 mod 8` quedan
certificados por descenso y el complemento congelado tiene `378` residuos
(`4.6142578125%`).

La debilidad central es semantica, no computacional. M22 mide cobertura de
residuos y congela complementos, pero aun no demuestra que una guarda por bits
bajos sobre esos complementos sea exactamente el subproblema operativo correcto
del SRS mixto binario/ternario. Hasta que esa traduccion sea auditada de forma
independiente, cualquier exito de termination seria solo una senal exploratoria.

## Base revisada

- `scripts/m21_angeltveit_lowbit_probe.py`: probe independiente pequeno del
  certificado low-bit/descent para el mapa acelerado `T`. En los artefactos
  locales relevantes reporta `max_false_positives = 0` y auditoria estratificada
  con `affine_failures = 0`.
- `scripts/m22_bridge_lowbit_rewriting.py`: cuantifica cuanto descargan los
  certificados low-bit dentro de las ramas S1/S2/S3 etiquetadas por residuos.
- `scripts/m22_freeze_s2_k16.py`: congela el complemento S2-k16 y sus hashes.
- `reports/m22_bridge_lowbit_rewriting.*`: evidencia de cobertura por rama y
  por `k`.
- `reports/m22_s2_k16_*`: complemento S2-k16 congelado; `uncovered_sha256 =
  bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210`.
- `colaboradores/codex-hijo/M22BridgeAngeltveitRewriting.md`: propuesta previa
  honesta: M22 como preprocesador/benchmark, no como prueba de Collatz.
- `colaboradores/orquestador/M21Paso1AngeltveitLowBitProbe.md`: contexto M21 y
  advertencia de que el probe no reproduce todavia el algoritmo completo de
  Angeltveit ni cotas grandes.

## Que tendria que pasar para que M22 sea publicable

Publicable aqui significa "nota tecnica reproducible sobre un puente
certificado entre low-bit descent y benchmarks guarded rewriting", no "prueba
de Collatz".

1. Lema semantico del puente. Debe existir una especificacion formal o
   semi-formal que diga exactamente que propiedad del SRS mixto queda
   representada por una guarda sobre residuos modulo `2^k`. Para S2-k16, el
   validador debe enumerar los `65536` residuos y reportar `0` discrepancias
   entre la rama operacional `bad -> d` / `tf* -> *`, el predicado `r mod 8 = 5`
   y el conjunto congelado.
2. Certificado low-bit auditado por una segunda implementacion. El resultado
   publicable no puede depender solo de importar `lowbit_certified_residues`.
   Debe haber un rechecker independiente que reproduzca para `k = 16`:
   `branch_residue_count = 8192`, `lowbit_certified_count = 7814`,
   `uncovered_count = 378`, los dos SHA-256 congelados, `0` falsos positivos y
   `0` fallos del invariante affine.
3. Artefacto guarded SRS/TPDB con checker de implicacion. El archivo generado
   debe venir con un checker que pruebe: clases certificadas por M21 descienden;
   clases no certificadas son exactamente las que el SRS guardado conserva; y
   el SRS guardado implica un subproblema de S2, no una propiedad artificial.
4. Comparacion pre-registrada contra M19. Con el mismo prover, misma version y
   misma grilla M19, S2-k16 guarded debe conseguir al menos uno de estos
   resultados: `QED/YES` donde S2 base tuvo `0 QED`, o una reduccion robusta de
   costo sin perder semantica. "Robusta" significa mediana de tiempo o CNF al
   menos `25%` menor en los puntos comparables, sin aumentar simultaneamente
   variables y clausulas mas de `10%`.
5. Reproducibilidad externa minima. Un comando limpio debe regenerar los
   artefactos desde cero, y un segundo entorno debe obtener exactamente los
   mismos counts y hashes. Si hay nondeterminismo de solver, debe reportarse
   semilla, timeout y distribucion de resultados.
6. Reclamo acotado y honesto. El texto publicable debe decir explicitamente
   que M22 reduce un benchmark condicionado por certificados de descenso. No
   debe presentarse como prueba de Collatz ni como reproduccion completa de
   Angeltveit.

## Que destruiria la via M22

- Un solo falso positivo: existe `n > 0` descargado por M21/M22 tal que el
  certificado usado no fuerza `T^k(n) < n`.
- Una discrepancia semantica: alguna palabra/rama del SRS mixto cae fuera del
  predicado de residuos usado, o alguna guarda low-bit acepta/rechaza una clase
  que no corresponde a la rama que se esta debilitando.
- Inestabilidad del complemento: al regenerar S2-k16 no se obtiene
  `uncovered_count = 378` y SHA-256
  `bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210`.
- Inflacion del benchmark: el SRS/TPDB guardado produce CNF consistentemente
  mas grandes que S2 base, o tiempos peores, sin un nuevo `QED/YES`.
- Exito artificial: el prover termina porque el guardado cambio el problema,
  no porque resolvio el complemento operacional de S2.
- No-reproducibilidad: otro checkout limpio no puede regenerar counts, hashes y
  resultados principales con los comandos documentados.
- Falta de novedad: se confirma que el mismo guardado/residuo ya existe en la
  literatura o en el repo oficial bajo otra formulacion equivalente.

## Cinco riesgos epistemicos mayores

1. Brecha de traduccion. El mayor riesgo es confundir una clase de residuos
   modulo `2^k` con una condicion correcta sobre el alfabeto mixto del SRS. Una
   tabla de cobertura no prueba equivalencia operacional.
2. Sesgo por elegir `k = 16`. Los datos no son monotonicamente mejores para
   S1/S2/S3 al subir `k`; S2 cae de `0.953857421875` en `k = 16` a
   `0.928268432617` en `k = 20`. Elegir el mejor `k` despues de mirar puede
   sobreestimar la fuerza estructural de la via.
3. Confundir cobertura con cierre. Que `95.39%` de S2-k16 descienda no dice que
   el `4.61%` restante sea terminable por el SRS, ni que sea mas facil. El
   complemento puede concentrar exactamente la dificultad.
4. Circularidad de implementacion. M22 importa el generador M21; si un bug vive
   en la definicion compartida de certificado, los scripts pueden estar de
   acuerdo entre si sin ser correctos.
5. Benchmark engineering sin significado matematico. Un DFA/trie puede reducir
   o aumentar el problema por detalles de codificacion, heuristicas SAT o
   timeouts, no por una reduccion conceptual valida.

## Experimentos confirmatorios vs exploratorios

Confirmatorios:

- Rechecker independiente de M21/M22 para S2-k16. Debe reproducir counts,
  hashes, `0` falsos positivos y `0` fallos affine sin importar los modulos de
  M21/M22.
- Validador semantico de puente. Debe enumerar exhaustivamente `2^16` residuos
  y probar `0` discrepancias entre predicado low-bit, rama S2 y complemento
  congelado.
- Generacion guarded SRS/TPDB con checker de implicacion. Debe certificar que
  cada clase descargada esta cubierta por descenso y que cada clase conservada
  pertenece al complemento congelado.
- Comparacion solver pre-registrada contra S2 base. Debe usar la grilla M19,
  mismos timeouts y metricas fijadas antes de mirar resultados.

Exploratorios:

- Probar S1, S3 o varios `k` buscando una configuracion mas amable.
- Cambiar DFA, trie LSB-first/MSB-first, minimizacion o formato TPDB.
- Ajustar parametros del prover, pesos, dimensiones, dominios natural/arctic o
  tropical despues de ver fallos.
- Usar muestras de residuos no cubiertos para intuir patrones.
- Comparar contra otros filtros de Angeltveit todavia no implementados, como
  mod 9 o merging, antes de tener un checker independiente.

La regla de higiene: un experimento exploratorio puede sugerir el siguiente
confirmatorio, pero no debe contarse como evidencia final si sus umbrales no
fueron fijados antes.

## Proximos tres experimentos

### 1. M22-C1: rechecker independiente S2-k16

Objetivo: eliminar circularidad basica entre `m21_angeltveit_lowbit_probe.py` y
M22.

Procedimiento esperado: escribir un rechecker pequeno desde cero o en otro
lenguaje que no importe M21/M22, regenerar el conjunto certificado y el
complemento S2-k16, y comparar hashes contra `reports/m22_s2_k16_*`.

Criterio de exito:

- `branch_residue_count = 8192`
- `lowbit_certified_count = 7814`
- `uncovered_count = 378`
- `uncovered_sha256 =
  bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210`
- `certified_sha256 =
  0e8d2a804d7cc129a5fc6eec295250fd2a57786c25f2764e1bbd5100be01c7fa`
- `false_positives = 0` en validacion exhaustiva para `1 <= n < 2^20`
- `affine_failures = 0` en una auditoria estratificada con al menos `288`
  muestras y `max_lift_seen >= 255`

Criterio de abandono:

- Cualquier falso positivo.
- Cualquier hash distinto sin explicacion documental y regeneracion completa.
- Mas de `0` fallos affine.

### 2. M22-C2: validador semantico del puente S2

Objetivo: demostrar que el complemento low-bit congelado es realmente el
subproblema S2 que se pretende conservar.

Procedimiento esperado: especificar la lectura operacional de la rama
`bad -> d` / `tf* -> *`, enumerar todos los residuos modulo `2^16`, y verificar
que las guardas aceptan exactamente los `378` residuos no certificados dentro
de `r mod 8 = 5`.

Criterio de exito:

- `65536/65536` residuos evaluados.
- `8192/8192` residuos de la rama S2 clasificados por `r mod 8 = 5`.
- `378/378` residuos del complemento aceptados por la guarda.
- `0` residuos fuera de S2 aceptados.
- `0` residuos certificados enviados al SRS guardado.
- Documento de equivalencia con al menos una tabla de transiciones o reglas que
  conecte bits bajos con el alfabeto mixto.

Criterio de abandono:

- `>= 1` discrepancia entre rama S2 y predicado de residuos.
- `>= 1` clase certificada que todavia pueda activar la rama guardada.
- No poder escribir una especificacion local clara de la traduccion sin apelar
  a intuicion externa.

### 3. M22-C3: benchmark guarded S2-k16 contra S2 base

Objetivo: decidir si M22 reduce una frontera real o solo agrega maquinaria.

Procedimiento esperado: generar `S2_guarded_k16_uncovered.srs` y/o TPDB,
validarlo con M22-C2, y correr exactamente la grilla M19 contra S2 base y
S2-k16 guarded con el mismo timeout, version de prover y semillas.

Criterio de exito fuerte:

- Al menos `1` resultado `QED/YES` para S2-k16 guarded donde S2 base tiene
  `0 QED/YES` bajo la misma grilla.
- `0` fallos del checker de implicacion.

Criterio de exito debil:

- Sin `QED/YES`, pero mediana de tiempo o CNF al menos `25%` menor que S2 base
  en puntos comparables.
- Variables y clausulas no crecen mas de `10%` simultaneamente frente a S2
  base.
- El reporte identifica que el cuello queda en los `378` residuos congelados.

Criterio de abandono:

- CNF o tiempo medianos peores que S2 base por mas de `25%` y sin `QED/YES`.
- El guardado introduce mas de `2x` reglas/estados que S2 base antes de llegar
  al prover.
- El resultado solo depende de parametros elegidos despues de mirar la salida.

## Veredicto operativo

Continuar M22 solo hasta completar M22-C1 y M22-C2. No conviene invertir en una
familia grande de S1/S2/S3 ni en muchos `k` antes de cerrar la brecha semantica.
Si C1 o C2 fallan, M22 debe cerrarse como diagnostico util de cobertura, no como
via publicable. Si C1 y C2 pasan, C3 decide si hay una contribucion publicable
como benchmark guardado reproducible.
