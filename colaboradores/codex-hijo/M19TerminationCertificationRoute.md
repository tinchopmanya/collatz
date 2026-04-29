# M19 termination certification route

Fecha: 2026-04-29
Responsable: CodexHijo-Certificacion
Scope: CPF/CeTA/TTT2/AProVE/Matchbox para cualquier eventual prueba de terminacion.

## Resumen ejecutivo

No necesitamos una prueba hoy. Necesitamos una vara clara para no confundir `YES`, `QED` o logs de solver con una prueba publicable.

La evidencia fuerte aceptable es:

1. Instancia exacta: archivo de problema versionado, con traduccion documentada desde el sistema Collatz/SRS que se afirma probar.
2. Prueba de herramienta: salida top-level `YES` o equivalente de AProVE, TTT2 o Matchbox, no solo `YES` internos de subobligaciones.
3. Certificado CPF: archivo XML CPF que contenga el problema y la prueba exportada por la herramienta.
4. Verificacion CeTA: log de CeTA/IsaFoR con resultado `CERTIFIED` sobre ese CPF exacto.
5. Versionado completo: nombre y version/release de herramienta, comandos, sistema operativo, solver externo, commits de inputs/scripts.
6. Hashes: SHA-256 de problema, CPF, logs, binarios o jars descargados, y manifiesto `SHA256SUMS` o sidecars `.sha256`.
7. Reproduccion independiente: workflow o instrucciones que regeneren el resultado en entorno limpio.

Sin CPF verificado por CeTA, el resultado puede ser un candidato importante, pero no debe llamarse certificado. Sin top-level `YES`, son solo logs negativos/inconclusos aunque contengan `SAT`, `QED` o `YES` internos.

## Escala de evidencia

| Nivel | Evidencia | Lectura |
| --- | --- | --- |
| 0 | Sin artefactos | Nada auditable. |
| 1 | Logs de busqueda o reproduccion | Utiles para diagnostico, no certifican terminacion. |
| 2 | Top-level `YES` de AProVE/TTT2/Matchbox | Candidato serio, pero dependemos de la herramienta. |
| 3 | CPF exportado para el mismo problema | Prueba machine-readable, todavia no validada externamente. |
| 4 | CPF + CeTA `CERTIFIED` + hashes + versiones | Evidencia fuerte para paper/nota tecnica. |
| 5 | Nivel 4 + reproduccion independiente + revision externa | Publicable y auditable. |

## Ruta tecnica recomendada

1. Congelar el problema: usar archivos SRS/TPDB exactos de `reports/m19_rewriting_challenges/`, registrar hash y explicar la correspondencia con la notacion del paper.
2. Buscar top-level `YES`: correr AProVE primero por disponibilidad de jar; luego Matchbox y TTT2 si AProVE queda en `MAYBE`, `TIMEOUT` o `KILLED`.
3. Exportar certificado: si aparece `YES`, rerun con modo certificable/CPF. En AProVE la documentacion publica opciones para restringir a tecnicas certificables por CeTA y para imprimir salida CPF.
4. Verificar con CeTA: ejecutar CeTA sobre el CPF y guardar stdout/stderr completo. El unico resultado fuerte es `CERTIFIED`; un rechazo tambien es un artefacto valioso.
5. Empaquetar evidencia: problema, CPF, log de herramienta, log de CeTA, comandos, versiones, hashes y workflow.
6. Reproducir en CI: correr `m19-termination-artifact-audit.yml` sobre los artefactos descargados o versionados.

## Tooling minimo creado

Se agrega `scripts/m19_audit_termination_artifacts.py`.

El runner:

- escanea raices de artefactos, por defecto `reports`;
- detecta candidatos CPF, logs de herramienta, logs de certificador, inventarios y manifiestos de hash;
- calcula SHA-256 de cada artefacto;
- verifica sidecars `.sha256` y archivos `SHA256SUMS` si existen;
- clasifica el bundle como `certified_top_level`, `cpf_present_unchecked_top_level`, `cpf_present_unchecked`, `top_level_uncertified`, `uncertified_logs_only`, `candidate_files_only` o `no_artifacts`;
- genera CSV, JSON y Markdown.

Se agrega `.github/workflows/m19-termination-artifact-audit.yml`.

El workflow compila el script, ejecuta auditoria sobre raices configurables y sube los reportes. Por defecto no falla si no hay certificado, porque M19 todavia esta en investigacion. Puede fallar con `require_certified=true` cuando queramos usarlo como gate de publicacion.

## Respuestas directas

Terreno virgen?

No en la linea general. Collatz como terminacion de rewriting/SAT ya fue trabajado por Yolcu-Aaronson-Heule, y la comunidad de Termination Competition mantiene herramientas y categorias relacionadas. La zona parcialmente virgen seria una combinacion concreta: S1/S2 materializados en este repo, herramientas 2026, CPF y certificacion CeTA reproducible.

Quien ya trabaja en esto?

Externamente: Yolcu-Aaronson-Heule para mixed-base rewriting de Collatz; AProVE/RWTH Aachen; Matchbox/Johannes Waldmann; TTT2 e Innsbruck; CeTA/IsaFoR; comunidad TermComp. Localmente: el orquestador M19 ya preparo reproduccion de `rewriting-collatz`, archivos S1/S2 y workflow AProVE; esta tarea agrega la ruta de certificacion y auditoria.

Posibilidad fuerte?

Fuerte solo condicionalmente. Si AProVE/Matchbox/TTT2 devuelve top-level `YES` para S1/S2 y eso se convierte a CPF aceptado por CeTA, hay una contribucion tecnica publicable. Sin certificado, la posibilidad de una prueba fuerte es baja-media; con solo logs inconclusos, baja.

Criterio de publicacion:

- afirmacion acotada, por ejemplo terminacion de S1/S2 o de una variante exacta, no "Collatz probado" salvo equivalencia formal completa;
- problema, comandos, versiones, solvers y commits fijados;
- top-level `YES` y CPF correspondiente;
- CeTA `CERTIFIED` sobre el CPF;
- hashes SHA-256 y reproduccion CI;
- revision humana de la traduccion matematica desde Collatz/SRS al archivo auditado.

Criterio de abandono:

- ninguna herramienta produce top-level `YES` bajo presupuestos razonables;
- solo hay logs con subobligaciones `YES`, `SAT` o `QED`, sin prueba top-level;
- no se puede exportar CPF o CeTA rechaza por tecnica no soportada;
- aparecen mismatches de hash, versiones no fijadas o artefactos imposibles de reproducir;
- la traduccion del problema auditado no corresponde exactamente a la afirmacion matematica;
- avanzar exige busqueda SAT abierta sin principio de parada ni insight teorico nuevo.

## Fuentes base

- AProVE usage: https://aprove.informatik.rwth-aachen.de/index.php/usage
- Termination Competition 2026: https://termination-portal.org/wiki/Termination_Competition_2026
- CPF paper: https://arxiv.org/abs/1410.8220
- CeTA paper: https://arxiv.org/abs/1208.1591
- CeTA/CPF confluence system description: https://arxiv.org/abs/1505.01337
- Termination Portal tools: https://termination-portal.org/wiki/Category%3ATools
- Local: `colaboradores/orquestador/M19Paso3MapaFronteraRewriting.md`
- Local: `colaboradores/orquestador/M19Paso6Web2026YAProVE.md`
- Local: `colaboradores/orquestador/M19Paso7AProVELocalDocker.md`
- Local: `colaboradores/orquestador/M19Paso8Web2026Orientacion.md`
