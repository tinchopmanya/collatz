# M19 CPF and certification route

Fecha: 2026-04-29
Agente: CodexHijo-CPFAndCertificationRoute
Scope: comandos concretos para obtener CPF/CeTA o equivalentes desde AProVE/TTT2/Matchbox en problemas de string rewriting, sin tocar workflows existentes.

## Resumen ejecutivo

La ruta certificable mas realista para M19 es:

1. AProVE 2026 como primer productor de CPF, con `-C ceta -p cpf`.
2. CeTA como verificador externo del CPF.
3. Matchbox como segunda via si hay binario reproducible y `--cpf`.
4. TTT2 solo como via historica/auxiliar, porque el comando CPF existe en literatura y usos academicos, pero hay que confirmarlo contra el binario concreto con `./ttt2 --help`.

El orquestador no debe tratar un `YES` textual como certificado. Debe exigir, como minimo, `YES` top-level, CPF separado, `ceta proof.cpf` con `CERTIFIED`, hashes SHA-256 y comandos/versiones.

## Fuentes verificadas

- AProVE usage oficial documenta SRS, CLI base `java -ea -jar aprove.jar -m wst example.ari`, `-C ceta`, `-p cpf`, `-t`, `-w` y `-Z`: https://aprove.informatik.rwth-aachen.de/index.php/usage
- AProVE download oficial: AProVE es Java 25; dependencias relevantes Z3, Yices 1, MiniSat; CeTA >= 2.22 para GUI: https://aprove.informatik.rwth-aachen.de/index.php/download
- GitHub releases de AProVE: latest actual `master_2026_02_15`, asset `aprove.jar`, digest `sha256:8b9ee0c9255cbde2c514306997fb9347afc3bb6d9c39b18763053088f671178a`: https://github.com/aprove-developers/aprove-releases/releases/tag/master_2026_02_15
- Termination certified categories: herramientas imprimen `YES/NO/MAYBE`; si `YES` o `NO`, imprimen CPF despues; certifiers corren sobre CPF: https://termination-portal.org/wiki/Termination_Competition_Certified_Categories_Competition
- CPF paper: CPF es formato comun para certificados de terminacion, confluencia, complejidad y completion: https://arxiv.org/abs/1410.8220
- CeTA paper/system descriptions: CeTA verifica CPF y responde `CERTIFIED` o `REJECTED`: https://arxiv.org/abs/1208.1591 y https://arxiv.org/abs/1505.01337
- Matchbox cabal/README historico: entrada TPDB plain/XTC, salida textual o CPF, ejemplo `matchbox --cpf data/z002.srs | tail -n +2 | ceta /dev/stdin`: https://raw.githubusercontent.com/jwaldmann/matchbox/master/matchbox.cabal
- Matchbox README historico: prueba terminacion de rewriting systems, usa GLPK/minisat, salida proof trace textual/CPF: https://raw.githubusercontent.com/jwaldmann/matchbox/master/README.md
- pure-matchbox 2022 reimplemento CPF output en MR `421-re-implement-cpf-output`; esto indica actividad posterior, pero no reemplaza validar el binario usado: https://git.imn.htwk-leipzig.de/waldmann/pure-matchbox/-/merge_requests/39
- TTT2 Termination Portal: herramienta LFU Innsbruck, homepage y publicacion: https://termination-portal.org/wiki/Tools%3ATTT2
- TTT2 paper: CLI general `./ttt2 [options] <file> [timeout]`, `--help`, `-s`, `-c`: https://www.researchgate.net/publication/221220733_Tyrolean_Termination_Tool_2

## AProVE 2026: comando recomendado

Version objetivo:

```bash
APROVE_URL="https://github.com/aprove-developers/aprove-releases/releases/download/master_2026_02_15/aprove.jar"
APROVE_SHA256="8b9ee0c9255cbde2c514306997fb9347afc3bb6d9c39b18763053088f671178a"
```

Requisitos:

- Java 25.
- Yices 1.x, idealmente 1.0.40, antes que cualquier Yices 2 en `PATH`.
- MiniSat 2 resoluble como `minisat2` o wrapper compatible.
- AProVE `aprove.jar` versionado o descargado con hash verificado.

Comando base para buscar veredicto y CPF:

```bash
java -ea -Xmx6g -jar tools/aprove/aprove.jar \
  -m wst \
  -C ceta \
  -p cpf \
  -t 300 \
  reports/m19_rewriting_challenges/m19_collatz_S1_without_ff_end_to_0_end.aprove.srs \
  > /tmp/m19_s1_aprove_cpf.out \
  2> /tmp/m19_s1_aprove_cpf.err
```

Repetir para S2:

```bash
java -ea -Xmx6g -jar tools/aprove/aprove.jar \
  -m wst \
  -C ceta \
  -p cpf \
  -t 300 \
  reports/m19_rewriting_challenges/m19_collatz_S2_without_tf_end_to_end.aprove.srs \
  > /tmp/m19_s2_aprove_cpf.out \
  2> /tmp/m19_s2_aprove_cpf.err
```

Separacion robusta del resultado top-level y el CPF:

```bash
head -n 1 /tmp/m19_s1_aprove_cpf.out > /tmp/m19_s1_aprove_result.txt
awk 'BEGIN{s=0} /^<\?xml/ || /^<certificationProblem/ {s=1} s {print}' \
  /tmp/m19_s1_aprove_cpf.out > /tmp/m19_s1_aprove.cpf
```

Validacion minima antes de CeTA:

```bash
test "$(cat /tmp/m19_s1_aprove_result.txt)" = "YES"
test -s /tmp/m19_s1_aprove.cpf
grep -q "certificationProblem" /tmp/m19_s1_aprove.cpf
```

Verificacion CeTA:

```bash
ceta /tmp/m19_s1_aprove.cpf > /tmp/m19_s1_ceta.log 2>&1
grep -q "^CERTIFIED" /tmp/m19_s1_ceta.log
```

Hashes:

```bash
sha256sum \
  reports/m19_rewriting_challenges/m19_collatz_S1_without_ff_end_to_0_end.aprove.srs \
  /tmp/m19_s1_aprove_cpf.out \
  /tmp/m19_s1_aprove.cpf \
  /tmp/m19_s1_ceta.log \
  tools/aprove/aprove.jar \
  > /tmp/m19_s1_SHA256SUMS
```

Notas:

- `-C ceta` es importante: restringe AProVE a tecnicas certificables y genera prueba legible por CeTA.
- `-p cpf` es el formato de prueba; `-m wst` deja el veredicto como primera linea.
- Si AProVE imprime `MAYBE`, `TIMEOUT`, `ERROR` o no imprime XML CPF, no hay certificado.
- `-Z DIRECTORY_NAME` puede usarse para logging de online-certification de pasos problematicos, pero no reemplaza un CPF completo aceptado por CeTA.

## AProVE 2026 en GitHub Actions

Viabilidad: media-alta, si se resuelven dependencias.

Perfil operacional sugerido:

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-java@v4
    with:
      distribution: temurin
      java-version: '25'
  - run: |
      mkdir -p tools/aprove
      curl -L "$APROVE_URL" -o tools/aprove/aprove.jar
      echo "$APROVE_SHA256  tools/aprove/aprove.jar" | sha256sum -c -
```

Riesgos de CI:

- Java 25 puede no estar disponible en la distribucion elegida del runner; probar `temurin`, y si falla usar una accion/distribucion que publique JDK 25.
- Yices 1.0.40 no debe bajarse automaticamente sin aceptar licencia y pinning; preferir cache privada, artifact manual o imagen Docker interna.
- Ubuntu moderno instala `minisat`; AProVE puede buscar `minisat2`. Si el binario es compatible, crear wrapper `minisat2` en `$GITHUB_WORKSPACE/bin`; si no, compilar MiniSat 2.
- Runner `ubuntu-latest` puede matar AProVE por memoria. Usar `-Xmx6g` y timeouts externos; si aparece `KILLED`, no inferir dificultad matematica.
- El asset AProVE tiene licencia no-comercial. Para CI publico, confirmar que el uso y redistribucion por cache/artifacts cumple la licencia.

## Matchbox: comando recomendado si hay binario

Binario historico: `matchbox2015` o `matchbox`.

Primero validar flags:

```bash
matchbox2015 --help | tee /tmp/matchbox_help.txt
grep -E -- "--cpf|cpf" /tmp/matchbox_help.txt
```

Comando historico documentado en `matchbox.cabal`:

```bash
matchbox2015 --cpf reports/m19_rewriting_challenges/m19_collatz_S1_without_ff_end_to_0_end.tpdb \
  > /tmp/m19_s1_matchbox_cpf.out \
  2> /tmp/m19_s1_matchbox_cpf.err
tail -n +2 /tmp/m19_s1_matchbox_cpf.out > /tmp/m19_s1_matchbox.cpf
ceta /tmp/m19_s1_matchbox.cpf > /tmp/m19_s1_matchbox_ceta.log 2>&1
```

Pipeline directo, equivalente al ejemplo historico:

```bash
matchbox2015 --cpf reports/m19_rewriting_challenges/m19_collatz_S1_without_ff_end_to_0_end.tpdb \
  | tail -n +2 \
  | ceta /dev/stdin
```

Notas:

- El ejemplo historico usa `tail -n +2`, lo que sugiere primera linea de veredicto y CPF despues.
- Si la primera linea no es `YES`, no pasar a afirmacion certificada aunque CeTA reciba algo.
- Matchbox historico declara TPDB plain/XTC y CPF, pero el build moderno es fragil. El reporte local `M19MatchboxRoute.md` ya propone usar binario precompilado o URL de artifact.
- pure-matchbox tiene trabajo de CPF en 2022, pero hay issues alrededor de tecnicas CPF/CeTA como unlabeling; validar cada CPF con CeTA es obligatorio.

Viabilidad GitHub Actions: media-baja sin binario fijado; media si se aporta `binary_archive_url` o imagen Docker.

## TTT2: ruta auxiliar a validar

CLI general documentado por el paper:

```bash
./ttt2 [options] <file> [timeout]
```

Comando CPF observado en material academico, no confirmado aqui contra binario actual:

```bash
./ttt2 -cpf xml reports/m19_rewriting_challenges/m19_collatz_S1_without_ff_end_to_0_end.tpdb 300 \
  > /tmp/m19_s1_ttt2_cpf.out \
  2> /tmp/m19_s1_ttt2_cpf.err
```

Validacion obligatoria antes de usar:

```bash
./ttt2 --help | tee /tmp/ttt2_help.txt
grep -E -- "-cpf|--cpf|cpf" /tmp/ttt2_help.txt
```

Si el help confirma `-cpf xml`, separar como en AProVE/Matchbox:

```bash
head -n 1 /tmp/m19_s1_ttt2_cpf.out > /tmp/m19_s1_ttt2_result.txt
awk 'BEGIN{s=0} /^<\?xml/ || /^<certificationProblem/ {s=1} s {print}' \
  /tmp/m19_s1_ttt2_cpf.out > /tmp/m19_s1_ttt2.cpf
test "$(cat /tmp/m19_s1_ttt2_result.txt)" = "YES"
ceta /tmp/m19_s1_ttt2.cpf > /tmp/m19_s1_ttt2_ceta.log 2>&1
grep -q "^CERTIFIED" /tmp/m19_s1_ttt2_ceta.log
```

Riesgos:

- TTT2 es historico y puede requerir OCaml/solvers antiguos.
- No hay evidencia suficiente, desde las fuentes revisadas en esta ronda, de un release moderno facil de instalar en GitHub Actions.
- Usarlo como productor primario puede consumir tiempo de orquestacion sin mejorar sobre AProVE/Matchbox.

## CeTA: criterio de aceptacion

Comando esperado:

```bash
ceta proof.cpf > ceta.log 2>&1
grep -q "^CERTIFIED" ceta.log
```

Comando historico equivalente visto en lista Termtools:

```bash
ceta-2.15 rt2-4.cpf
```

Lectura:

- `CERTIFIED`: evidencia fuerte si el CPF corresponde al problema exacto.
- `REJECTED`: no certificado; guardar log porque puede indicar tecnica no soportada o CPF invalido.
- `UNSUPPORTED`: no certificado; puede ser limitacion del certifier.
- Exit code cero sin `CERTIFIED` no debe aceptarse como certificado salvo documentacion del binario usado.

## Riesgos transversales

- CPF no equivale automaticamente a prueba de Collatz. Solo certifica el problema de rewriting exacto contenido en el CPF.
- AProVE puede tener `YES` internos en logs; solo vale el primer veredicto top-level.
- `-p cpf` con tecnica no certificable puede emitir CPF parcial, `unknownProof` o ser rechazado por CeTA.
- `NO` tambien puede tener CPF en categorias certificadas, pero para M19 la evidencia buscada es terminacion (`YES`).
- Entradas SRS `.aprove.srs` y `.tpdb` pueden no ser byte-a-byte equivalentes; registrar hashes y traduccion.
- CeTA valida el certificado, no la equivalencia entre M19/Collatz y el archivo si esa equivalencia no esta formalizada dentro del CPF.
- Dependencias antiguas, especialmente Yices 1 y MiniSat 2, son el principal bloqueo operativo de AProVE 2026.

## Recomendacion operacional para el orquestador

No crear un nuevo workflow global todavia. Usar esta ruta como playbook manual sobre los workflows/probes M19 existentes.

Orden recomendado:

1. Cerrar entorno AProVE: Java 25, AProVE `master_2026_02_15`, Yices 1.0.40, MiniSat 2.
2. Ejecutar S1/S2 normal con `-m wst` hasta obtener un top-level `YES` o descartar por `MAYBE/TIMEOUT/KILLED`.
3. Solo si hay `YES`, repetir con `-C ceta -p cpf` y guardar stdout/stderr completos.
4. Extraer CPF desde la primera linea XML, verificar con `ceta`, generar `SHA256SUMS`.
5. Si AProVE no produce `YES` o CeTA rechaza, probar Matchbox con binario fijado y `--cpf`.
6. Dejar TTT2 como tercera via, solo si hay binario ya disponible y `--help` confirma salida CPF.

Decision de publicacion:

- Publicable tecnicamente: `YES` top-level + CPF + `CERTIFIED` + hashes + versionado + reproduccion limpia.
- No publicable: `YES` sin CPF, CPF sin CeTA, CeTA rechazado, logs con subobligaciones, o equivalencia M19/Collatz no documentada.

## Archivos auxiliares

No cree scripts ni workflows nuevos en esta tarea. El archivo actual es deliberadamente un playbook operacional para no interferir con los workflows M19 ya existentes.
