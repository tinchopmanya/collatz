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

Estado: pendiente.

Objetivo: decidir con evidencia si conviene escalar computo o cambiar de enfoque.

Definition of done:

- Revision de costo/beneficio del motor actual.
- Decision entre optimizar Python, agregar C/Rust, usar GPU o mantener escala chica.
- Lista de experimentos que justifican computo mayor.

Salida esperada:

- Un camino tecnico claro para la siguiente fase.

## Prioridad

Orden recomendado:

1. M0 - Higiene y auditoria.
2. M1 - Motor Collatz minimo.
3. M2 - Dataset base y records.
4. M3 - Paridad y modelo aleatorio.
5. M4 - Residuos y familias anomalas.
6. M5 - Reporte de cuarta ola.
7. M6 - Escalado o cambio de estrategia.

## Criterio de avance

Puedo avanzar autonomamente dentro de estos milestones si:

- el trabajo no borra informacion existente;
- no requiere gastar dinero;
- no requiere credenciales nuevas;
- no cambia la historia remota de git;
- no afirma haber probado Collatz;
- deja scripts, datos derivados y conclusiones reproducibles.
