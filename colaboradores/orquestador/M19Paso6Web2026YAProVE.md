# M19 paso 6 - web 2026 y via AProVE

Fecha: 2026-04-27
Responsable: Codex orquestador
Estado: investigacion web actualizada y nueva via CI preparada

## Preguntas antes

- Estamos en terreno virgen?
  - No en Collatz general ni en rewriting/SAT. Si hay terreno parcialmente nuevo, esta en S1/S2, certificacion y prueba con herramientas modernas.
- Podemos descubrir algo relevante?
  - Si, si AProVE/Matchbox/CeTA/Cetera encuentran o certifican algo para S1/S2 que no este reportado.
- Ya alguien estuvo buscando esto?
  - Si. Los autores de Yolcu-Aaronson-Heule, la comunidad de Termination Competition y herramientas como AProVE/Matchbox.
- Que tan lejos estamos?
  - Ya tenemos archivos S1/S2 y workflows. Falta ejecucion real de CI y evaluacion de logs.

## Web 2026: estado Collatz

### Collatz sigue abierto

No encontre una prueba aceptada de Collatz a fines de abril de 2026. Si aparecen claims recientes, deben tratarse como no establecidos hasta pasar auditoria formal/peer review.

Fuentes relevantes:

- Collatz Challenge: https://ccchallenge.org/
- Angeltveit 2026: https://arxiv.org/abs/2602.10466
- Barina verification: https://pcbarina.fit.vutbr.cz/

Lectura:

- Collatz Challenge lista literatura y formalizaciones, pero muestra 0 papers formalizados completamente y varias piezas en proceso/auditoria.
- Angeltveit 2026 propone un algoritmo mejorado para verificar Collatz hasta `n < 2^N`; es importante para verificacion computacional, no para prueba teorica directa.
- Barina reporta verificacion de convergencia hasta `2^71` con fecha 2025-01-15.

### Claims recientes

Aparecen claims 2026 en preprints, blogs, Lean/Isabelle y sitios no revisados.

Decision:

```text
No usar estos claims como base salvo que haya auditoria externa fuerte.
```

Motivo:

- Collatz atrae muchas pruebas falsas;
- nuestro criterio requiere fuente primaria fuerte, reproduccion, o formalizacion verificable por terceros;
- el proyecto no debe desviarse por claims no auditados.

## Web 2026: herramientas de terminacion

### AProVE

Fuente principal:

- Release repo: https://github.com/aprove-developers/aprove-releases
- Release latest detectado: `master_2026_02_15`
- Asset: `aprove.jar`
- Workflow/talk WST 2025: https://www.imn.htwk-leipzig.de/~waldmann/WST2025/accepted/

Hallazgo:

- AProVE tiene releases publicos recientes;
- WST 2025 indica "AProVE: Becoming Open Source and Recent Improvements";
- hay un `aprove.jar` publico publicado el 2026-02-15;
- la documentacion de AProVE muestra ejecucion tipo:

```text
java -ea -jar aprove.jar -m wst file -p plain -t 30
```

Decision:

```text
AProVE debe entrar como via CI separada para correr TPDB S1/S2.
```

### Matchbox

Fuentes:

- Termination Portal: https://termination-portal.org/wiki/Tools%3AMatchbox
- GitHub: https://github.com/jwaldmann/matchbox

Hallazgo:

- Matchbox es publico;
- acepta entrada TPDB;
- produce trazas textuales/CPF;
- usa matrix interpretations natural/arctic, dependency pairs y compresion;
- requiere stack Haskell/solvers (`glpk`, `minisat`) para construir localmente.

Decision:

```text
Matchbox es candidato fuerte, pero primero AProVE es mas facil porque tiene jar publico.
```

### Termination Competition 2025

Fuente:

- https://termcomp.github.io/Y2025/

Hallazgo:

- SRS Relative sigue existiendo como categoria;
- hubo problemas tecnicos con dos instancias SRS Relative excluidas;
- la comunidad sigue activa.

Decision:

```text
Nuestros S1/S2 TPDB deben pensarse como instancias estilo TermComp.
```

## Accion nueva

Se agrego:

```text
scripts/m19_run_aprove_challenges.py
.github/workflows/m19-aprove-challenge-search.yml
```

El workflow:

- usa Java 21;
- descarga `aprove.jar` desde release `master_2026_02_15`;
- corre AProVE en modo `wst`;
- prueba S1, S2 o ambos usando los archivos `.aprove.srs`;
- guarda logs, CSV y Markdown.

## Secuencia recomendada

1. Ejecutar `M19 rewriting reproduction` con `proof_set=zantema`.
2. Si pasa, ejecutar `M19 rewriting challenge search` con defaults.
3. Ejecutar `M19 AProVE challenge search` con `challenge=both`, `timeout=120`.
4. Si AProVE retorna `YES`, guardar artifact y auditar manualmente el log.
5. Si AProVE retorna `MAYBE/TIMEOUT`, probar Matchbox como siguiente herramienta.

## Preguntas despues

- Avanzamos?
  - Si. Ya no solo tenemos el prover minimo del paper; agregamos una segunda herramienta moderna.
- Hay resultado matematico?
  - No todavia.
- Estamos en algo virgen?
  - No en general. Si un `YES` aparece para S1/S2 y no esta publicado, podria ser avance real.
- Que destruye esta via?
  - AProVE y el prover minimo fallan/timeout en grillas razonables; Matchbox tampoco produce certificado; ampliar compute no trae insight.
- Que toca ya?
  - Correr los tres workflows manuales en GitHub Actions.
