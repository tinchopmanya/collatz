# M19 Yices 1-compatible route for AProVE

Fecha: 2026-04-29
Agente: CodexHijo-YicesAProVE
Scope: ruta reproducible/legal para AProVE con Yices 1-compatible, o justificacion para no automatizar descarga.
Commit: no realizado.

## Resumen ejecutivo

La ruta tecnicamente correcta es:

```text
AProVE master_2026_02_15 + Java 25 + MiniSat/minisat2 + Yices 1.0.40 primero en PATH + archivos .aprove.srs
```

La ruta legalmente segura no debe descargar Yices 1 de forma automatica, porque SRI exige aceptacion manual de EULA antes de permitir acceso/uso. Por eso agregue un workflow manual opcional que no contiene URL de descarga de Yices 1 ni redistribuye el binario: acepta un Yices 1 ya provisto por cache, artefacto o path de runner, y exige una atestacion explicita de licencia antes de correr.

Archivo nuevo de infraestructura:

- `.github/workflows/m19-aprove-yices1-manual.yml`

## Fuentes exactas

### Web

- AProVE download/dependencies: https://aprove.informatik.rwth-aachen.de/download
  - Lineas 13, 21-23: AProVE pide instalar dependencias antes de usar.
  - Lineas 31-33: AProVE funciona con Yices 1, por ejemplo 1.0.40, pero no con Yices 2; Yices debe estar antes que cualquier otro `yices` en `PATH`.
  - Lineas 34-36, 50-55: AProVE requiere MiniSat version 2 o superior; en Linux documenta `minisat2` o renombrar el binario a `minisat`.
  - Linea 13 y 91-98: descargar AProVE implica aceptar su licencia.
- AProVE usage: https://aprove.informatik.rwth-aachen.de/usage
  - Lineas 381-389: AProVE soporta String Rewrite Systems con extension `*.srs`.
  - GitHub release page enlazada desde AProVE: https://github.com/aprove-developers/aprove-releases/releases
  - Lineas 178-185 y 207-216: release latest `master_2026_02_15`; flags importantes `-m wst`, `-p plain|html`, `-t 30`.
- Yices 1 download: https://yices.csl.sri.com/old/download-yices1.html
  - Lineas 3-12: Yices 1 ya no se mantiene; ultima version Yices 1.0.40, 2013-12-04.
  - Lineas 28-33: la descarga abre una pagina con terminos de licencia y requiere aceptar antes de descargar.
  - Lineas 10, 14, 17: se distribuye como binario sin fuente; requiere GMP, con builds estaticos disponibles.
- Yices 1 command line: https://yices.csl.sri.com/old/command_line.html
  - Lineas 18-26: el ejecutable esperado se llama `yices` y lee stdin/archivo.
  - Lineas 39-45: Yices 1 soporta la opcion `-e`.
- Yices license terms: https://yices.csl.sri.com/yices-newnewlicense.html
  - Lineas 23-30: EULA no comercial, requiere aceptar terminos antes de acceder/usar.
  - Lineas 30-33: licencia personal/no exclusiva/no transferible; no uso/distribucion comercial.
  - Lineas 34-37: SRI conserva titularidad y puede terminar licencia; al terminar se destruyen copias.
- GitHub Actions workflow syntax: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
  - Lineas 850-856: `workflow_dispatch` admite inputs tipados (`boolean`, `choice`, `string`, etc.).
- `actions/cache`: https://github.com/actions/cache
  - Lineas 393-407: inputs `key`, `path`, `restore-keys` y output `cache-hit`.
  - Lineas 410-414: cache scope por key/version/branch.
- GitHub artifact v4 blog: https://github.blog/news-insights/product-news/get-started-with-v4-of-github-actions-artifacts/
  - Lineas 553-555: `download-artifact` v4 puede descargar artefactos de otros runs/repos con token y `run-id`.

### Locales

- `colaboradores/codex-hijo/M19AProVEEnvironmentProbe.md`
  - Ya habia identificado la combinacion fuerte `AProVE master_2026_02_15 + Java + Yices 1.0.40 primero en PATH + minisat2 + .aprove.srs`.
  - Ya advertia que Yices 1.0.40 no debe descargarse automaticamente sin decision explicita de licencia.
- `colaboradores/orquestador/M19Paso6Web2026YAProVE.md`
  - Introdujo la via AProVE por CI y el release `master_2026_02_15`.
- `colaboradores/orquestador/M19Paso7AProVELocalDocker.md`
  - Corrida Docker local: `.tpdb` fallo por parser; `.aprove.srs` parseo; faltaban `yices` y `minisat2`; con Yices 2.6.4 aparecio `invalid option: -e`.
- Artefactos locales de CI:
  - `reports/m19_github_runs/artifacts/25105347516/m19-aprove-environment-probe-both/m19_aprove_environment_probe.md`: Yices 2.6.4 real devuelve `yices: invalid option: -e`; clasificacion `ENV_YICES_E_INCOMPATIBLE`.
  - `reports/m19_github_runs/artifacts/25105756825/m19-aprove-environment-probe-both/m19_aprove_environment_probe.md`: wrapper `yices2-strip-e` oculta el bloqueo `-e`, pero las corridas terminan `WST_KILLED`; no es prueba de compatibilidad Yices 1.
  - `reports/m19_github_runs/artifacts/25104952325/m19-aprove-challenge-search-both/m19_aprove_challenges.md`: S1 y S2 terminan `KILLED` con 120 s usando ruta Yices 2/wrapper.

## Preguntas obligatorias

### Terreno virgen?

No en Collatz, rewriting, SAT/SMT ni AProVE. Tampoco es virgen localmente: M19 ya probo AProVE con Docker/CI y aislo el bloqueo Yices 2 vs Yices 1. El terreno parcialmente nuevo seria muy estrecho: una corrida reproducible de S1/S2 con AProVE moderno, Yices 1 real, MiniSat resuelto, memoria suficiente y logs auditables. Si esa combinacion da `WST_YES` top-level para S1 o S2, recien ahi habria una senal candidata de resultado nuevo.

### Quien ya busco?

Localmente buscaron el orquestador M19 y CodexHijo-AProVEEnv. Externamente, la zona esta relacionada con la comunidad de terminacion, AProVE, Termination Competition y los trabajos tipo Yolcu-Aaronson-Heule sobre Collatz/rewrite/SAT. Los documentos M19 locales ya registran que el valor no esta en "usar AProVE" como idea nueva, sino en obtener una ejecucion exacta y auditable para nuestros desafios S1/S2.

### Que bloquea?

Bloqueos tecnicos:

- AProVE 2026 documenta dependencia en Yices 1 y no Yices 2.
- AProVE llama `yices -e`; Yices 1 documenta `-e`, Yices 2.6.4 en CI reporto `invalid option: -e`.
- AProVE requiere `minisat2` o equivalente; Ubuntu instala `minisat`, por lo que hace falta symlink o binario nombrado correctamente.
- El release actual de AProVE declara Java 25; workflows previos usaban Java 21, que puede funcionar o no segun build, pero la ruta nueva debe seguir el requisito documentado.
- S1/S2 con entorno incompleto terminan en `ENV_*`, `KILLED` o `WST_KILLED`, estados no matematicos.

Bloqueo legal/reproducibilidad:

- Yices 1 no debe descargarse por workflow sin que una persona/entidad acepte la EULA de SRI.
- Meter el binario en el repo seria mala idea: mezcla redistribucion, licencia no comercial/no transferible y posible exposicion publica.
- Un artefacto/cache compartido tambien puede ser redistribucion; solo conviene si el repositorio/organizacion y sus usuarios tienen derecho a usarlo y se documenta quien acepto terminos.

### Se puede automatizar legalmente?

Si, pero solo a medias. Se puede automatizar la verificacion y la corrida una vez que Yices 1 ya fue provisto legalmente; no conviene automatizar la descarga/aceptacion de licencia.

Ruta aceptable:

```text
operador acepta EULA fuera de CI -> coloca Yices 1.0.40 en path/cache/artefacto privado -> workflow manual verifica y corre AProVE
```

Ruta que no recomiendo:

```text
workflow descarga Yices 1 desde SRI con curl/wget o simula aceptar licencia
```

Motivo: la pagina de SRI dice que hay que aceptar los terminos antes de descargar/acceder/usar. Automatizar ese paso en CI borraria la evidencia de consentimiento humano y puede violar o, como minimo, volver ambigua la licencia.

## Infraestructura propuesta

Agregue `.github/workflows/m19-aprove-yices1-manual.yml`.

Caracteristicas:

- `workflow_dispatch` manual.
- Input booleano `license_attestation`; si no es `true`, el job se corta antes de preparar nada.
- No hay URL de descarga de Yices 1 en el workflow.
- Acepta Yices 1 desde `cache`, `artifact` o `runner-path`.
- Permite seleccionar runner por `runner_labels_json`, por ejemplo `["ubuntu-latest"]` o `["self-hosted","linux","x64"]`.
- Restaura cache solo con `actions/cache/restore`, sin guardar cache nuevo.
- Descarga artefacto solo si se provee `artifact_run_id` y `artifact_name`.
- Instala dependencias publicas (`curl`, `minisat`, `unzip`) y crea `minisat2 -> minisat`.
- Descarga AProVE desde el release publico `master_2026_02_15`.
- Usa Java 25, acorde a la documentacion actual de AProVE.
- Corre `scripts/m19_probe_aprove_environment.py` sin editar scripts existentes.
- Publica artifact `m19-aprove-yices1-manual-{S1|S2|both}` con JSON/MD/CSV/logs.

Uso esperado con cache presembrada:

```text
GitHub Actions -> M19 AProVE Yices1 manual route
license_attestation=true
yices_source=cache
cache_key=manual-yices1-1.0.40-linux-x86_64
challenge=both
timeout=120
wall_timeout=180
runner_labels_json=["ubuntu-latest"]
```

Uso esperado con artefacto privado:

```text
GitHub Actions -> M19 AProVE Yices1 manual route
license_attestation=true
yices_source=artifact
artifact_run_id=<run que subio el binario autorizado>
artifact_name=manual-yices1
challenge=both
```

Uso esperado con path de runner self-hosted:

```text
GitHub Actions -> M19 AProVE Yices1 manual route
license_attestation=true
yices_source=runner-path
yices1_bin_dir=/opt/yices-1.0.40/bin
runner_labels_json=["self-hosted","linux","x64"]
challenge=both
```

Formato aceptado para cache/artefacto:

- directorio extraido que contiene `bin/yices`, o
- `.tar.gz`, `.tgz` o `.zip` que al extraerse contiene `bin/yices`.

## Experimento siguiente

1. Una persona autorizada acepta la EULA de Yices 1 en SRI y descarga Yices 1.0.40 Linux x86_64 fuera del workflow.
2. Esa persona decide el canal: runner privado con path local, cache privada presembrada o artifact privado de corta vida.
3. Ejecutar `M19 AProVE Yices1 manual route` con `challenge=both`, `timeout=120`, `wall_timeout=180`, `java_xmx=6g`.
4. Confirmar en el artifact:
   - `yices_version` muestra Yices 1.x, idealmente 1.0.40;
   - `yices -e supported: yes` sin wrapper;
   - `minisat2 on PATH: yes`;
   - no aparecen `ENV_*`.
5. Si no hay `ENV_*`, subir a corridas largas con `timeout=600`, `wall_timeout=900` o runner mayor. Si hace falta mas heap, conviene clonar este workflow a un perfil "large" en vez de mezclarlo con la prueba legal basica.

## Que resultado seria publicable?

Publicable como nota tecnica/reproducibilidad:

- Un artifact con entorno completo Yices 1 real, MiniSat, Java, commit del repo, release AProVE, comandos exactos, logs y `WST_MAYBE/TIMEOUT/KILLED` para S1/S2. Seria publicable como cierre negativo reproducible de infraestructura, no como resultado matematico.

Publicable como resultado candidato fuerte:

- `WST_YES` top-level para S1 o S2, con log completo, version exacta de AProVE/Yices/MiniSat/Java, input exacto, y preferiblemente certificado CPF o una traza verificable por CeTA/tercero. Sin certificado, seria solo "AProVE encontro una prueba candidata" y debe auditarse manualmente.

No publicable como avance:

- `YES` interno en subobligaciones si el top-level es `KILLED`, `MAYBE` o `TIMEOUT`.
- Corridas con Yices 2 o wrapper `yices2-strip-e`, porque no cumplen la dependencia documentada de AProVE.
- Corridas sin atestacion de licencia o con binario Yices 1 pegado al repo.

## Decision

Conviene automatizar el experimento, no la adquisicion de Yices 1. La infraestructura correcta es un workflow manual, con atestacion, que consume un binario ya autorizado y produce artefactos auditables. Si eso no es aceptable para el equipo, la alternativa mas limpia es documentar comandos locales y no poner Yices 1 en CI.
