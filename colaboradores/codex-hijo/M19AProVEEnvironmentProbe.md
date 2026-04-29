# M19 AProVE environment probe

Fecha: 2026-04-29
Agente: CodexHijo-AProVEEnv
Rama: main
Commit: no realizado
Milestone: M19
Tarea: distinguir bloqueo de entorno AProVE vs problema matematico S1/S2

## Comando reproducible

Probe local sin JAR, util para inventario de entorno y validacion de SRS:

```powershell
python scripts\m19_probe_aprove_environment.py --out-dir $env:TEMP\m19_aprove_environment_probe_local
```

Probe con AProVE cuando exista un JAR local:

```powershell
python scripts\m19_probe_aprove_environment.py `
  --jar C:\ruta\aprove.jar `
  --challenge-file reports\m19_rewriting_challenges\m19_collatz_S1_without_ff_end_to_0_end.aprove.srs `
  --challenge-file reports\m19_rewriting_challenges\m19_collatz_S2_without_tf_end_to_end.aprove.srs `
  --out-dir $env:TEMP\m19_aprove_environment_probe `
  --timeout 20 `
  --wall-timeout 45
```

CI manual nuevo:

```text
GitHub Actions -> M19 AProVE environment probe -> Run workflow
```

## Archivos creados o modificados

- `scripts/m19_probe_aprove_environment.py`
- `.github/workflows/m19-aprove-environment-probe.yml`
- `colaboradores/codex-hijo/M19AProVEEnvironmentProbe.md`

## Resultado central

Se agrego un probe separado del runner AProVE existente. No modifica `scripts/m19_run_aprove_challenges.py` ni el workflow AProVE previo.

El probe produce JSON, Markdown, CSV opcional y logs. Clasifica explicitamente:

- `ENV_YICES_E_INCOMPATIBLE`: AProVE intento usar `yices -e` y el binario no lo acepta.
- `ENV_MISSING_YICES`: falta `yices`.
- `ENV_MISSING_MINISAT2`: falta `minisat2`.
- `ENV_JAVA_OOM`: heap insuficiente.
- `INPUT_PARSE_ERROR`: problema de formato/input.
- `WST_*` o `WALL_TIMEOUT`: AProVE corrio, pero el resultado ya no es un bloqueo ambiental simple.

La corrida local sin JAR en esta maquina diagnostico:

```text
AProVE run skipped: no --jar provided
ENV: yices -e is not supported or yices is missing
ENV: minisat2 is missing from PATH
```

En el Markdown local generado:

- `java`: no encontrado.
- `yices`: no encontrado.
- `minisat2`: no encontrado.
- `minisat`: no encontrado.
- memoria fisica detectada: 32441 MB.
- S1 y S2 `.aprove.srs`: extension `.srs`, empiezan con `(RULES)`, 11 reglas cada uno.

## Investigacion local y web

Fuentes revisadas:

- AProVE usage: https://aprove.informatik.rwth-aachen.de/usage
- AProVE download/dependencies: https://aprove.informatik.rwth-aachen.de/download
- Yices 1 command line: https://yices.csl.sri.com/old/command_line.html
- Yices 1 download: https://yices.csl.sri.com/old/download-yices1.html

Hallazgos:

- AProVE documenta la llamada CLI base como `java -ea -jar aprove.jar -m wst example.ari`; para terminacion con `-m wst`, la primera linea esperada es `YES`, `NO`, `MAYBE`, `ERROR` o `TIMEOUT`.
- AProVE soporta entrada SRS con extension `*.srs`; el ejemplo oficial usa `(VAR x)` y `(RULES ...)`. Nuestros desafios sin variables, con `(RULES ...)`, son compatibles con la forma SRS que AProVE parsea por extension.
- AProVE declara dependencia en Yices 1, por ejemplo Yices 1.0.40, y dice explicitamente que no funciona con Yices 2.
- La documentacion de Yices 1 muestra que `-e` existe para forzar modelos/nucleos no satisfacibles. Eso explica por que AProVE 2026 puede llamar `yices -e`.
- Yices 1.0.40 es la ultima version de Yices 1 y no esta mantenida. Su descarga requiere aceptar licencia en el sitio de SRI; por eso no conviene automatizarla sin decision explicita.
- AProVE requiere MiniSat version 2 o superior. En Linux la documentacion habla de paquete `minisat2`; Ubuntu moderno suele ofrecer `minisat`, asi que el symlink `minisat2 -> minisat` es un candidato de entorno, no una prueba matematica.

## Preguntas

### Terreno virgen

No en Collatz, rewriting ni AProVE. La zona interesante sigue siendo estrecha: correr S1/S2 con una herramienta moderna, entorno correcto y logs auditables. Un `YES` top-level seria potencialmente nuevo, pero solo despues de auditar salida/certificado.

### Ya buscado

Si. Los documentos M19 previos ya registran que Yolcu-Aaronson-Heule y herramientas de terminacion exploraron este tipo de frontera; tambien consta una corrida local Docker con AProVE `master_2026_02_15` que avanzo hasta bloqueos `yices -e`, `minisat2` y memoria/`KILLED`.

### Posibilidad fuerte

La posibilidad fuerte no es "AProVE 2026 + Yices 2", porque esa combinacion esta rota por dependencia. La posibilidad fuerte es:

```text
AProVE master_2026_02_15 + Java con heap suficiente + Yices 1.0.40 primero en PATH + minisat2 resoluble + .aprove.srs
```

Si bajo ese entorno S1/S2 dan `MAYBE`, `TIMEOUT`, `KILLED` o wall-timeout, recien ahi el resultado empieza a decir algo sobre dificultad de herramienta/instancia y no sobre ambiente.

### Bloqueos

- Local actual: falta Java, Yices, MiniSat/MiniSat2 y JAR AProVE.
- CI actual de reproduccion negativa: instala Yices 2.6.4 para demostrar incompatibilidad `-e`; no pretende ser el entorno final.
- Yices 1.0.40 no debe descargarse automaticamente sin decidir como manejar licencia y pinning.
- Memoria: el workflow permite `JAVA_TOOL_OPTIONS=-Xmx6g`, pero un `KILLED` todavia puede ser OOM de runner o timeout externo.

### Proximo experimento

1. Ejecutar el workflow nuevo `M19 AProVE environment probe` con defaults para obtener artifact que confirme el bloqueo Yices 2 en GitHub Actions.
2. Preparar, sin tocar el runner actual, una variante de entorno donde Yices 1.0.40 este preinstalado o provisto manualmente y aparezca antes que cualquier Yices 2 en PATH.
3. Repetir el probe con S1/S2. Solo si `yices -e supported: yes` y `minisat2 on PATH: yes`, pasar a corridas largas con el workflow AProVE existente o con una recomendacion de perfil nuevo.

## Verificacion

- `python -m py_compile scripts\m19_probe_aprove_environment.py`: OK.
- `python scripts\m19_probe_aprove_environment.py --out-dir $env:TEMP\m19_aprove_environment_probe_local`: OK; diagnostico ambiental local, sin JAR.
- `python scripts\m19_probe_aprove_environment.py --jar C:\tmp\missing-aprove.jar --dry-run --out-dir $env:TEMP\m19_aprove_environment_probe_dry`: OK; genera comandos sin ejecutar JAR.
- `git diff --check -- scripts\m19_probe_aprove_environment.py .github\workflows\m19-aprove-environment-probe.yml`: OK, sin salida. Nota: los archivos nuevos estan sin stage, por lo que este check cubre diferencias tracked aplicables y no sustituye revision visual de untracked.

## Que destruye este resultado

- Un artifact de CI con Yices 1 correcto, `minisat2` correcto, heap suficiente y aun asi `WST_YES` para S1/S2: destruiria la hipotesis de que solo habia bloqueo ambiental y abriria auditoria matematica.
- Un artifact con `yices -e supported: yes`, `minisat2 on PATH: yes`, sin OOM y resultado `WST_MAYBE/TIMEOUT/KILLED`: confirma que el problema restante es de herramienta/instancia, no de dependencia basica.

## Que no se debe concluir

- No se probo ni refuto terminacion de S1/S2.
- No se encontro prueba de Collatz.
- No se debe interpretar `KILLED`, `MAYBE`, `TIMEOUT` o `WALL_TIMEOUT` como contraejemplo.
- No se debe usar Yices 2 como entorno valido para AProVE si aparece `invalid option: -e`.

## Riesgos o dudas

- El nombre exacto esperado por AProVE para MiniSat puede depender de plataforma, pero el fallo observado y la documentacion apuntan a `minisat2`.
- `minisat` moderno via symlink puede ser suficiente, pero debe validarse con AProVE real, no solo con `-help`.
- El probe clasifica por texto de logs; si AProVE cambia mensajes, puede requerir ajuste.

## Siguiente paso recomendado

Conseguir una ruta reproducible para Yices 1.0.40 con licencia aceptada fuera del repo, ejecutar el probe, y recien despues gastar tiempo en corridas largas S1/S2.
