# Milestones

Fecha: 2026-04-25
Foco: Collatz Lab

## M0 - Higiene y auditoria

Estado: en progreso.

Objetivo: dejar claro que sabemos, que creemos y que falta verificar.

Definition of done:

- `AuditoriaFuentesCollatz.md` creado.
- Cada claim importante de las tres olas clasificado como `alta`, `media`, `baja` o `pendiente`.
- Fuentes base separadas por tipo: peer-reviewed, arXiv, proyecto, blog, claim no verificado.
- Claims dudosos marcados para correccion o descarte.

Salida esperada:

- Una base bibliografica confiable para no construir sobre arena.

## M1 - Motor Collatz minimo

Estado: completado en primera version.

Objetivo: implementar funciones correctas y testeadas para generar datos.

Definition of done:

- Carpeta `src/collatz/` creada.
- Funcion para paso clasico.
- Funcion para paso acelerado.
- Funcion para orbita completa con limite de seguridad.
- Funcion para metricas: pasos totales, stopping time, maximo, impares, prefijo de paridad.
- Tests para casos pequenos y conocidos.

Salida esperada:

- Un nucleo confiable para experimentos reproducibles.

## M2 - Dataset base y records

Estado: completado en primera version.

Objetivo: producir el primer dataset chico y una tabla de extremos.

Definition of done:

- Script para generar dataset hasta `n <= 1_000_000`.
- CSV o Parquet generado en carpeta ignorada por git.
- Tabla versionada de records principales.
- Primer reporte con records de tiempo total, stopping time y altura maxima.

Salida esperada:

- Primer mapa propio de orbitas extremas.

## M3 - Paridad y modelo aleatorio

Estado: completado en primera version.

Objetivo: comparar orbitas reales contra una heuristica aleatoria simple.

Definition of done:

- Medicion de densidad de impares.
- Distribucion de bloques pares e impares.
- Autocorrelacion simple de prefijos de paridad.
- Comparacion de orbitas extremas contra poblacion general.

Salida esperada:

- Una respuesta inicial a: las orbitas extremas tienen firma de paridad distinta?

## M4 - Residuos y familias anomalas

Estado: completado en primera version.

Objetivo: buscar clases modulares que concentren comportamientos extremos.

Definition of done:

- Analisis por modulo `2^k` para varios `k`.
- Ranking de clases residuales por promedio y cola de stopping time.
- Comparacion entre records y clases frecuentes.
- Lista de familias candidatas para investigar.

Salida esperada:

- Candidatos concretos, no solo intuiciones.

## M5 - Reporte de cuarta ola

Estado: completado.

Objetivo: cerrar un ciclo de investigacion con resultados propios.

Definition of done:

- `InvestigacionSobreCollatzCuartaOla.md` creado.
- `ResumenInvestigacionSobreCollatzCuartaOla.md` creado.
- `Conlusion.md` actualizada.
- Hallazgos separados en confirmados, negativos, dudosos y proximos experimentos.

Salida esperada:

- Una cuarta ola seria: reproducible, autocritica y util para decidir si escalar.

## M6 - Escalado o cambio de estrategia

Estado: completado en primera version.

Objetivo: decidir con evidencia si conviene escalar computo o cambiar de enfoque.

Definition of done:

- Revision de costo/beneficio del motor actual.
- Decision entre optimizar Python, agregar C/Rust, usar GPU o mantener escala chica.
- Lista de experimentos que justifican computo mayor.

Salida esperada:

- Un camino tecnico claro para la siguiente fase.

Decision tomada:

- No escalar computo todavia.
- Priorizar formalizacion local y estudio del mapa de salida del bloque alternante.
- Reabrir escalado solo si aparece una pregunta que requiera rangos mayores.

## M7 - Mapa de salida del bloque alternante

Estado: completado en primera version.

Objetivo: entender que ocurre despues del prefijo alternante formalizado.

Definition of done:

- Representar el bloque alternante como una estructura calculable.
- Medir `r = v2(3^s q - 1)` para impares hasta `n <= 1000000`.
- Medir el siguiente impar `m = (3^s q - 1) / 2^r`.
- Comparar la distribucion de `r` contra una geometrica `P(r = k) = 2^-k`.
- Generar reporte tecnico y sexta ola.

Salida esperada:

- Un modelo local de expansion y salida que habilite estudiar cadenas odd-to-odd.

Decision tomada:

- No escalar por fuerza bruta todavia.
- Pasar a modelar secuencias de bloques y correlaciones entre colas consecutivas.

## M8 - Cadena odd-to-odd y correlaciones

Estado: completado en primera version.

Objetivo: estudiar si la salida de un bloque realmente "resetea" la cola binaria o si hay sesgos aprovechables.

Definition of done:

- Implementar iterador odd-to-odd basado en `alternating_block`.
- Medir correlacion entre `s_i = v2(n_i + 1)` y `s_{i+1}`.
- Medir productos locales `n_{i+1}/n_i`.
- Buscar numeros con varias expansiones consecutivas antes del primer descenso.
- Comparar contra un modelo independiente con colas geometricas.

Salida esperada:

- Evidencia para decidir si hay una estructura menos conocida que merezca reporte tecnico formal.

Decision tomada:

- La cola siguiente parece volver a promedio cercano a `2`.
- La duracion y la altura deben tratarse como metricas separadas.
- El siguiente paso es comparar contra un modelo estocastico, no solo ampliar limite.

## M9 - Modelo estocastico y trazas de records

Estado: completado en primera version.

Objetivo: comparar cadenas reales contra una cadena artificial con colas geometricas independientes.

Definition of done:

- Generar trazas legibles de records por duracion y altura.
- Medir sumas de log factores locales.
- Implementar simulador comparable con `P(s = k) = 2^-k`.
- Comparar distribucion de bloques hasta bajar.
- Buscar desviaciones sistematicas entre cadena real y modelo.

Salida esperada:

- Un criterio claro para saber si hay estructura no capturada por el modelo geometrico.

Decision tomada:

- El modelo geometrico independiente explica muy bien el cuerpo de la distribucion.
- El modelo sobreproduce extremos de bloques y altura.
- La proxima pregunta es si hay anti-persistencia real entre bloques expansivos.

## M10 - Anti-persistencia entre bloques

Estado: completado en primera version.

Objetivo: medir si la dinamica real reduce la probabilidad de concatenar bloques favorables respecto del modelo independiente.

Definition of done:

- Medir correlacion entre factores logaritmicos consecutivos.
- Medir rachas de bloques expansivos reales y modeladas.
- Condicionar por bloques con `s >= 8`.
- Comparar la distribucion del factor siguiente despues de eventos extremos.
- Buscar una afirmacion candidata formalizable.

Salida esperada:

- Decidir si la sobreproduccion extrema del modelo es ruido de rango/semilla o una senal aritmetica real.

Decision tomada:

- No aparece anti-persistencia simple despues de bloques expansivos.
- Las rachas expansivas reales se parecen mucho al modelo.
- La senal mas interesante esta condicionada por `exit_v2 >= 5`.

## M11 - Salidas con alta valuacion 2-adica

Estado: completado en primera version.

Objetivo: estudiar si `exit_v2` alto deja congruencias que reducen la expansion siguiente.

Definition of done:

- Medir condiciones `exit_v2 >= k` para varios `k`.
- Calcular intervalos de confianza de la diferencia real/modelo.
- Comparar siguiente cola, siguiente `exit_v2` y siguiente log factor.
- Derivar congruencias exactas para las clases de salida.
- Decidir si hay un lemma local candidato.

Salida esperada:

- Confirmar o descartar que `exit_v2` alto produce un sesgo aritmetico real.

Decision tomada:

- `exit_v2 >= 5` y `exit_v2 = 5` muestran menor expansion siguiente real que el modelo hasta `n <= 5000000`.
- La senal no es monotona para todos los `exit_v2` altos.
- El siguiente paso debe ser modular/formal, no solamente mas computo.

## M12 - Congruencia de `exit_v2 = 5`

Estado: completado en primera version.

Objetivo: derivar la clase modular exacta asociada a `exit_v2 = 5` y estudiar su efecto sobre el bloque siguiente.

Definition of done:

- Expresar `exit_v2 = 5` como congruencia sobre `s` y `q`.
- Traducir esa congruencia al siguiente impar.
- Medir la distribucion de `v2(next_odd + 1)` condicionada por esa clase.
- Comparar contra modelo y contra clases vecinas `exit_v2 = 4, 6, 7`.
- Decidir si hay lemma local candidato.

Salida esperada:

- Una explicacion aritmetica o descarte de la senal `exit_v2 = 5`.

Decision tomada:

- La congruencia exacta es simple: para `n = 2^s q - 1`, `exit_v2 = 5` equivale a `3^s q = 33 mod 64`.
- En la muestra local de todos los bloques hasta `n <= 5000000`, `exit_v2 = 5` vuelve al modelo geometrico: expansion siguiente `0.28628846` vs `0.28627450`.
- La senal de la decima ola aparece por seleccion de cadenas antes del primer descenso, donde `next_tail = 1` queda sobre-representado.
- Se abandona `exit_v2 = 5` como lemma local candidato.

## M13 - Sesgo de supervivencia orbital

Estado: completado en primera version.

Objetivo: explicar por que las cadenas que sobreviven antes del primer descenso no muestrean uniformemente las transiciones locales.

Definition of done:

- Medir `next_tail` por profundidad de bloque antes del primer descenso.
- Separar cadenas por duracion total y altura maxima.
- Comparar distribuciones condicionadas por supervivencia contra el modelo geometrico independiente.
- Identificar si la sobre-representacion de `next_tail = 1` explica la sobreproduccion de extremos del modelo.
- Decidir si hay una formulacion de supervivencia formalizable.

Salida esperada:

- Un modelo de seleccion orbital que explique por que los extremos reales son menos frecuentes que en el modelo independiente.

Decision tomada:

- El modelo independiente explica casi perfectamente el sesgo global por posicion final/interior.
- Bloques finales: `tail=1` real `0.68311110` vs modelo `0.68213098`.
- Bloques interiores: `tail=1` real `0.38646876` vs modelo `0.38606060`.
- Sin embargo, queda un residuo localizado en `prev_exit_v2 = 5` seguido de bloque interior: `tail=1` real `0.45271454` vs modelo `0.40614137`, con IC95 de la diferencia `[0.02320157, 0.06994477]`.
- La siguiente linea debe descomponer esa condicion por residuos/margen/profundidad.

## M14 - Residuo interior despues de `prev_exit_v2 = 5`

Estado: completado como descarte.

Objetivo: confirmar o destruir la dependencia fina que queda despues de `prev_exit_v2 = 5` en bloques interiores antes de seguir descomponiendola.

Definition of done:

- Registrar que la senal actual es exploratoria y post-hoc.
- Contar subgrupos/metricas testeadas en M13 y en la descomposicion inicial del Codex hijo.
- Aplicar correccion conservadora por comparaciones multiples.
- Hacer permutation test o bootstrap robusto para `prev_exit_v2 = 5` + `interior_block`.
- Revisar si existe explicacion algebraica directa de la relacion entre `prev_exit_v2 = 5` y `next_tail = 1`.
- Solo si sobrevive, separar por margen, profundidad y residuos de `q` modulo potencias de 2.
- Decidir si la senal pasa a confirmada, queda como exploratoria o se descarta.

Salida esperada:

- Confirmar robustez estadistica/algebraica del residuo o descartarlo como ruido post-hoc/mezcla condicionada.

Decision tomada:

- En el rango original `n <= 5000000`, la senal sobrevive bootstrap/permutacion por cadena, pero no pasa el umbral estricto `p ajustado < 0.01` bajo Bonferroni.
- Con tests M13: `p ajustado = 0.01390268`.
- Con conteo conservador M13 + exploracion del Codex hijo: `p ajustado = 0.06519232`.
- En holdout independiente `5000001 <= n <= 10000000`, la diferencia cae a `0.00939612`, con `p = 0.43201832` y bootstrap CI95 `[-0.01423070, 0.03272495]`.
- La congruencia local para `prev_exit_v2 = 5` predice `P(next_tail = 1) = 0.5`, no una anomalia real-modelo.
- Se abandona `prev_exit_v2 = 5` + interior como pista principal.

## M15 - Busqueda confirmatoria con train/holdout desde el inicio

Estado: pendiente.

Objetivo: reemplazar barridos post-hoc por busquedas que separen descubrimiento y confirmacion desde el diseno.

Definition of done:

- Definir un rango train y un rango holdout antes de buscar senales.
- Limitar la cantidad de hipotesis candidatas por ola.
- Registrar numero de tests y correccion antes de interpretar.
- Integrar a Claude como revisor del diseno antes de correr.
- Usar Codex hijo solo para replicacion o ejecucion acotada despues del diseno.

Salida esperada:

- Una nueva pista o un descarte, pero sin repetir el error de confirmar con el mismo dataset que genero la hipotesis.

## Prioridad

Orden recomendado:

1. M0 - Higiene y auditoria.
2. M1 - Motor Collatz minimo.
3. M2 - Dataset base y records.
4. M3 - Paridad y modelo aleatorio.
5. M4 - Residuos y familias anomalas.
6. M5 - Reporte de cuarta ola.
7. M6 - Escalado o cambio de estrategia.
8. M7 - Mapa de salida del bloque alternante.
9. M8 - Cadena odd-to-odd y correlaciones.
10. M9 - Modelo estocastico y trazas de records.
11. M10 - Anti-persistencia entre bloques.
12. M11 - Salidas con alta valuacion 2-adica.
13. M12 - Congruencia de `exit_v2 = 5`.
14. M13 - Sesgo de supervivencia orbital.
15. M14 - Residuo interior despues de `prev_exit_v2 = 5`.
16. M15 - Busqueda confirmatoria con train/holdout desde el inicio.

## Criterio de avance

Puedo avanzar autonomamente dentro de estos milestones si:

- el trabajo no borra informacion existente;
- no requiere gastar dinero;
- no requiere credenciales nuevas;
- no cambia la historia remota de git;
- no afirma haber probado Collatz;
- deja scripts, datos derivados y conclusiones reproducibles.
