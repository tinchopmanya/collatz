# M19 paso 7 - AProVE local via Docker

Fecha: 2026-04-27
Responsable: Codex orquestador
Estado: ejecucion local realizada; sin prueba encontrada

## Preguntas antes

- Estamos en terreno virgen?
  - No en rewriting/SAT general. Seguimos en la frontera estrecha S1/S2.
- Podemos descubrir algo con esto?
  - Si AProVE diera `YES` para S1 o S2, seria una senal importante que exigiria auditoria/certificacion.
- Ya alguien estuvo buscando esto?
  - Si. Los autores reportaron miles de CPU-horas sin prueba para S1/S2.
- Que tan lejos estamos?
  - Ya no estamos solo preparando: corrimos una herramienta moderna localmente.

## Corridas realizadas

Se ejecuto AProVE `master_2026_02_15` dentro de Docker `ubuntu:24.04`.

Primer intento:

- input: archivos `.tpdb`;
- resultado: parse error;
- causa: AProVE elige parser por extension y no reconoce `.tpdb` como SRS.

Correccion:

- se generaron archivos `.aprove.srs` con el mismo contenido `(RULES ...)`;
- se actualizo el workflow AProVE para usar `.aprove.srs`.

Segundo intento:

- AProVE parseo los desafios;
- fallo por dependencias externas faltantes: `yices` y `minisat2`.

Tercer intento:

- se instalo `minisat` y se creo symlink `minisat2`;
- se instalo Yices 2.6.4 desde binario oficial SRI;
- AProVE avanzo mas, pero Yices 2 reporto `invalid option: -e`;
- AProVE termino en estado `KILLED`;
- no hubo `YES` top-level para S1 ni S2.

## Resultado observado

Resumen local:

```text
S1: KILLED / could not be shown
S2: KILLED / could not be shown
```

No debe interpretarse como:

```text
S1/S2 son falsos o no terminan.
```

Debe interpretarse como:

```text
AProVE 2026, con entorno Docker local limitado y Yices 2, no encontro prueba top-level en esta corrida.
```

## Hallazgos tecnicos

- AProVE requiere formato `.srs`, no `.tpdb`, para parsear como string rewriting.
- AProVE usa `minisat2`; Ubuntu instala `minisat`, por lo que se necesita symlink.
- AProVE intenta llamar `yices -e`, que Yices 2.6.4 no acepta.
- AProVE produjo subobligaciones internas con `YES`, pero el resultado top-level fue `KILLED`, no una prueba completa.
- Docker local tiene memoria limitada, lo cual afecta AProVE.

## Cambios hechos

- Se agregaron archivos `.aprove.srs` para S, S1 y S2.
- Se ajusto el workflow AProVE para:
  - instalar `minisat`;
  - crear `minisat2`;
  - descargar Yices 2.6.4;
  - usar `JAVA_TOOL_OPTIONS=-Xmx6g`.
- Se ajusto el clasificador del runner AProVE para no confundir `YES` internos con `YES` top-level.

## Preguntas despues

- Avanzamos?
  - Si. Convertimos AProVE de plan a ejecucion real y encontramos bloqueos especificos.
- Hay resultado matematico?
  - No.
- Estamos mas cerca de algo publicable?
  - Un poco mas cerca de una nota tecnica reproducible. No mas cerca de una prueba de Collatz.
- Que destruye esta via?
  - Que con entorno completo y memoria suficiente AProVE/Matchbox/CeTA sigan sin producir prueba ni certificado.
- Que toca?
  - Ejecutar el workflow AProVE en GitHub Actions; si tambien queda `KILLED/MAYBE`, pasar a Matchbox o buscar Yices 1 compatible.
