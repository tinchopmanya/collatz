# M19 paso 11 - decision post AProVE y cinco agentes

Fecha: 2026-04-29
Responsable: Codex orquestador
Estado: ola multiagente integrada; AProVE-wrapper auditado; decisiones siguientes fijadas

## Preguntas antes

- Estamos avanzando?
  - Si. La ola dejo de ser lineal: hubo ejecucion CI, auditoria de herramienta, diseno de desafios, ruta legal Yices1, ruta Matchbox, ruta CPF/CeTA y evaluacion Angeltveit 2026.
- Estamos en terreno virgen?
  - No globalmente. Rewriting/termination de Collatz ya es terreno de Yolcu-Aaronson-Heule, AProVE, Matchbox y TermComp. El terreno parcialmente nuevo para este repo es la instancia exacta S1/S2 con artefactos modernos reproducibles y certificables.
- Podemos descubrir algo fuerte?
  - Si, pero la condicion es estricta: `YES` top-level sobre un SRS exacto, idealmente CPF aceptado por CeTA, o una reproduccion computacional 2026 tipo Angeltveit con auditoria independiente. Nada de esto aparecio todavia.
- Ya alguien estuvo buscando esto?
  - Si. La idea general esta recorrida; nuestra posible contribucion es convertir rutas dispersas en experimentos exactos, auditables, versionados y con criterios de abandono.
- Que tan lejos estamos?
  - Mas cerca de saber que no funciona barato. Todavia lejos de una prueba; cerca de una nota tecnica honesta sobre reproducibilidad, bloqueos y descartes.

## Resultado AProVE wrapper

Run: `25105972129`

Configuracion:

```text
workflow: M19 AProVE challenge search
challenge: both
timeout: 120
wall_timeout: 180
yices_mode: yices2-strip-e
```

Resultado:

```text
S1 -> KILLED, 123.404 s
S2 -> KILLED, 124.348 s
YES top-level -> 0
ENV_ERROR -> 0
```

Lectura:

- El wrapper `yices2-strip-e` elimina el bloqueo superficial `yices -e`, pero no produce prueba.
- Hay `YES` internos en subobligaciones de los logs, pero el veredicto global es `KILLED`.
- Por regla de evidencia M19, esos `YES` internos no cuentan como resultado matematico.
- AProVE con Yices2-wrapper queda como diagnostico, no como evidencia fuerte ni como ruta publicable.

Decision:

```text
Enfriar AProVE-wrapper.
Mantener AProVE-Yices1 real como unica ruta AProVE seria.
No relanzar mas AProVE con Yices2-wrapper salvo para diagnostico puntual.
```

## Resultado de los agentes

### Yices1/AProVE

Archivo: `colaboradores/codex-hijo/M19Yices1AProVERoute.md`

Decision:

- Integrar workflow manual `m19-aprove-yices1-manual.yml`.
- No descargar Yices1 desde CI.
- Exigir atestacion humana de licencia y binario ya provisto por cache, artefacto privado o runner self-hosted.
- Usar esta ruta solo si el equipo decide aceptar/proveer Yices1 legalmente.

Razon:

```text
AProVE documenta dependencia Yices1; Yices2 no es equivalente.
Automatizar descarga/licencia seria una mala evidencia y un riesgo legal.
```

### Matchbox build pinning

Archivo: `colaboradores/codex-hijo/M19MatchboxBuildPinning.md`

Decision:

- Integrar workflow manual `m19-matchbox-build-probe.yml`.
- Primer probe: GHC `8.10.7`, Cabal `3.10.3.0`, index-state `2021-09-01T00:00:00Z`, build `false`.
- Si resuelve dependencias, relanzar con build `true`.
- Si falla, probar fuente-deps y luego GHC `9.4.8` + index-state `2025-02-25T00:00:00Z`.

Razon:

```text
El fallo Matchbox previo no fue matematico: fue Cabal/GHC/base.
Todavia no probamos Matchbox real contra S1/S2.
```

### CPF/CeTA

Archivo: `colaboradores/codex-hijo/M19CPFAndCertificationRoute.md`

Decision:

- No aceptar `YES` textual como suficiente.
- Si AProVE o Matchbox dan `YES`, repetir inmediatamente con CPF/CeTA.
- Criterio publicable minimo: `YES` top-level + CPF + `ceta` con `CERTIFIED` + hashes + versiones + input exacto.

Razon:

```text
Sin certificado, el resultado es candidato tecnico, no evidencia fuerte.
```

### Nuevos desafios SRS

Archivo: `colaboradores/codex-hijo/M19NextChallengeDesign.md`

Decision:

- No generar todavia los seis desafios.
- Priorizar primero herramientas: Yices1 real o Matchbox reproducible.
- Luego abrir ola M19-N con maximo seis desafios y criterios de abandono.

Razon:

```text
Mas desafios sin herramientas reales multiplican ruido.
La proxima mejora tiene que aumentar potencia de prueba, no solo cantidad de archivos.
```

### Angeltveit 2026

Archivo: `colaboradores/codex-hijo/M21AngeltveitVerificationRoute.md`

Decision:

- Abrir M21a como via paralela acotada.
- Objetivo: reproduccion/auditoria computacional independiente, no prueba teorica de Collatz.
- Primer experimento: prototipo CPU pequeno contra verificacion ingenua para `N <= 24`.

Razon:

```text
No es terreno virgen mundial, pero si es una via 2026 seria, con paper y codigo publico, donde el repo puede aportar auditoria reproducible.
```

## Preguntas despues

- Estamos avanzando?
  - Si, pero el avance principal hoy fue de infraestructura y descartes, no de teorema.
- Estamos en algo virgen?
  - No en el enfoque general. Parcialmente si en la combinacion exacta S1/S2 + CI moderno + certificacion reproducible dentro de este repo.
- Puedo descubrir algo con esto?
  - Si, si logramos un `YES` certificable o una reproduccion independiente robusta de Angeltveit. La probabilidad de una prueba completa sigue siendo baja; la probabilidad de una contribucion tecnica honesta es media.
- Ya alguien estuvo buscando esto?
  - Si. Por eso toda afirmacion debe ser "nuestra instancia/reproduccion/certificacion", no "nadie lo vio".
- Que tan lejos estoy de descubrir algo?
  - Lejos de demostrar Collatz; a una o dos iteraciones de saber si Matchbox o Yices1 abren una senal real. M21a podria dar una contribucion reproducible sin esperar a resolver la conjetura.

## Proxima decision operacional

Orden:

1. Commit/push de workflows manuales, artefactos AProVE-wrapper y reportes de agentes.
2. Ejecutar probe Matchbox dry-run despues de que el workflow exista en `main`.
3. No ejecutar workflow Yices1 hasta que una persona acepte/provea Yices1 legalmente.
4. Si Matchbox dry-run resuelve, relanzar build real y congelar binario/hash.
5. Si Matchbox falla en las dos toolchains propuestas, enfriar Matchbox build-from-source y pasar a binario/container.
6. Abrir M21a CPU pequeno como via paralela de alta seriedad cuando M19 no este bloqueado por git/CI.

## Criterio de abandono actualizado

Abandonar o congelar M19 como ruta fuerte si:

- AProVE con Yices1 real no supera `KILLED/MAYBE/TIMEOUT` en presupuestos razonables.
- Matchbox no puede compilarse ni obtenerse como binario reproducible.
- Ninguna herramienta produce `YES` top-level sobre S1/S2 o desafios M19-N.
- No aparece CPF/CeTA o auditoria equivalente para cualquier `YES`.

Mantener M19 como contribucion tecnica si:

- Documenta de forma reproducible que rutas modernas fallan o requieren dependencias historicas.
- Deja workflows, artefactos, hashes y criterios claros para que otro equipo pueda repetir.
