# M25 C3 preregistration

Fecha: 2026-04-29
Agente: CodexHijo-M25-C3-PreregistrationCritic
Worktree: `C:\dev\vert\collatz-m25-c3-preregistration`
Rama: `codex-hijo/m25-c3-preregistration`
Estado: preregistro documental/critico; sin implementacion C3; sin prover

## Veredicto operativo

Este documento bloquea cualquier corrida C3 no preregistrada. Desde M25, un
resultado C3 solo puede contarse como evidencia confirmatoria si:

- usa exactamente los inputs congelados aqui;
- declara antes de correr el artefacto, checker, prover, flags, timeouts,
  semillas y hardware;
- reporta todas las metricas permitidas para C3 y para S2 base;
- no cambia reglas, guardas, residuos, `k`, encoding ni prover despues de ver
  salidas.

Cualquier corrida C3 que no cumpla esto queda degradada automaticamente a
exploratoria/no citable como evidencia confirmatoria. Un resultado cuyo
timestamp sea anterior al commit de este preregistro tampoco puede usarse como
confirmatorio.

## Hipotesis exacta

Hipotesis confirmatoria M25-C3-minimo-r8189-v1:

> Si se construye un benchmark C3 minimo que conserva solo la microfamilia
> congelada `G_8189 = { r mod 2^16 : r mod 2^13 = 8189 }`, y un checker prueba
> que ese benchmark es un subproblema operacional correcto de la rama
> `bad -> d` / `tf* -> *` sin aceptar residuos certificados ni residuos fuera
> de S2, entonces C3 minimo sera objetivamente mas tratable que S2 base bajo la
> misma configuracion preregistrada.

La tratabilidad objetiva solo puede significar una de estas dos cosas:

- Exito fuerte: algun prover preregistrado devuelve `YES` para C3 minimo donde
  S2 base no devuelve `YES`, y ese `YES` produce CPF que CeTA verifica.
- Exito debil: si no hay `YES`, C3 minimo reduce costo frente a S2 base en los
  puntos comparables preregistrados: mediana de tiempo o CNF al menos `25%`
  menor, sin que variables y clausulas crezcan simultaneamente mas de `10%` y
  sin que reglas/estados superen `2x` S2 base.

La hipotesis no afirma Collatz, no afirma terminacion de `S`, no afirma
terminacion de todo `U_16`, y no afirma que el guardado sea novedoso hasta que
la literatura/repo oficial sigan sin mostrar una familia equivalente.

## Inputs congelados

Base local usada para este preregistro:

```text
origin: https://github.com/tinchopmanya/collatz.git
origin/main observado: 7dc70c894b54a2398e51e0baf6db6e8c65b220e6
```

Documentos normativos leidos:

```text
colaboradores/orquestador/DecisionM24DesbloqueoC3Minimo.md
colaboradores/codex-hijo/M24MicroGuardDesign.md
colaboradores/codex-hijo/M24SRSSemanticAudit.md
colaboradores/codex-hijo/M22KillCriteria.md
colaboradores/codex-investigador/M23FronteraWeb2026.md
```

Artefactos congelados para C3 minimo:

```text
reports/m22_residual_stats_candidate_subfamilies.csv
reports/m22_s2_k16_uncovered_residues.csv
reports/m22_c1_rechecker.certified_residues.csv
reports/m24_microguard_8189.guard.txt
reports/m24_microguard_8189_summary.csv
reports/m19_rewriting_challenges/m19_collatz_S2_without_tf_end_to_end.srs
reports/m19_rewriting_challenges/m19_collatz_S_full.srs
```

Hashes semanticos congelados por M22/M24:

```text
U_16 uncovered_sha256 = bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210
C_16 certified_sha256 = 0e8d2a804d7cc129a5fc6eec295250fd2a57786c25f2764e1bbd5100be01c7fa
G_8189 accepted_sha256 = de4100dcb707ee6d42acf0fc6af8b8bb8d2a70852b1a2af461d64e4926eb281c
```

Hashes de archivos locales relevantes:

```text
reports/m19_rewriting_challenges/m19_collatz_S2_without_tf_end_to_end.srs
sha256 = 728a023cf391419303e146cfae8987d0fe8d65c0b81cb2a5108186faddb5b2d2

reports/m19_rewriting_challenges/m19_collatz_S_full.srs
sha256 = 383367f1c9644eb8e6ea742d4ce27cdad9cea6ad947acdaf969a21c6ef05a06c

reports/m24_microguard_8189.guard.txt
sha256 = 640d963e860bca199a5321761529f81a1312b4c44b049007df03d9c7fc5a846f

reports/m24_microguard_8189_summary.csv
sha256 = 3fc2e338873145abcae71db42a0c112542bce30b64489468c58bcff10d0b805e
```

Microfamilia congelada:

```text
k = 16
modulus = 65536
selector = r mod 2^13 = 8189
accepted_count = 8
certified_overlap_count = 0
outside_s2_count = 0
accepted residues =
  8189
  16381
  24573
  32765
  40957
  49149
  57341
  65533
```

No esta preregistrado usar `U_16` completo de `378` residuos, cambiar `k`,
probar S1/S3, elegir otra microfamilia, minimizar otra guarda, cambiar
orientacion de bits, o introducir certificados dentro del SRS guardado.

## Alcance permitido

El experimento C3 minimo tiene tres fases y ninguna fase posterior puede
empezar si la anterior falla:

1. Artefacto y checker: generar un C3 textual/SRS/TPDB y un checker que pruebe
   la implicacion entre guarda, rama operacional `tf*`, complemento congelado y
   exclusion de certificados.
2. Medicion estructural: medir C3 minimo y S2 base antes del prover, con las
   mismas reglas de conteo.
3. Prover/certificacion: correr solo las configuraciones preregistradas contra
   C3 minimo y S2 base.

La fase 1 debe probar, como minimo:

- el checker reevalua `65536/65536` residuos, no confia solo en archivos CSV;
- `guard(r) => r in U_16`;
- `guard(r) => r not in C_16`;
- `guard(r) => r mod 8 = 5`;
- la insercion de la guarda no cambia el problema ni crea una propiedad
  artificial;
- las clases certificadas quedan descargadas fuera del SRS guardado, no
  embeddeadas como una negacion gigante.

## Metricas permitidas

Solo estas metricas pueden decidir exito o abandono:

- Reglas: cantidad de reglas SRS/TRS generadas para C3 minimo y S2 base.
- Estados: estados de automata/guard/frontend, si existen.
- CNF: variables, clausulas y tiempo de generacion CNF, si hay frontend SAT.
- Tiempo: wall-clock y/o CPU time, con timeout exacto y hardware reportado.
- Resultado de prover: `YES`, `NO`, `MAYBE`, `TIMEOUT` o `ERROR`.
- CPF: existencia, hash, tamano y comando exacto que lo genero.
- CeTA: resultado `CERTIFIED`/rechazado, version y comando exacto.

Metricas internas como memoria, numero de conflictos SAT, decisiones, learned
clauses, logs parciales, trazas de heuristicas o tamanos intermedios solo
pueden reportarse como diagnostico si fueron guardadas, pero no pueden definir
exito post hoc.

## Criterios de exito

Exito semantico minimo, obligatorio antes de cualquier claim:

- hashes `U_16`, `C_16` y `G_8189` coinciden con los congelados;
- `accepted_count = 8`;
- `certified_overlap_count = 0`;
- `outside_s2_count = 0`;
- el checker de implicacion pasa sin excepciones;
- C3 minimo se identifica como subproblema de S2, no como problema nuevo.

Exito fuerte de benchmark:

- la misma configuracion preregistrada se corre sobre S2 base y C3 minimo;
- S2 base no obtiene `YES`;
- C3 minimo obtiene `YES`;
- el `YES` exporta CPF;
- CeTA verifica ese CPF;
- se reportan reglas, estados, CNF y tiempo para ambos lados.

Exito debil de benchmark:

- no hay `YES` certificado;
- no hay fallos semanticos;
- mediana de tiempo o CNF baja al menos `25%` frente a S2 base en los puntos
  comparables preregistrados;
- variables y clausulas no crecen simultaneamente mas de `10%`;
- reglas/estados no superan `2x` S2 base.

El exito debil solo permite decir "senal de benchmark mas tratable"; no permite
decir terminacion, prueba ni certificacion.

## Criterios de abandono

Abandonar C3 minimo como via confirmatoria si ocurre cualquiera de estos casos:

- algun hash congelado no coincide y no hay nuevo preregistro antes de correr;
- el checker acepta al menos un residuo fuera de `U_16`;
- el checker acepta al menos un residuo certificado en `C_16`;
- el checker acepta algun residuo fuera de `r mod 8 = 5`;
- no se puede especificar donde se inserta la guarda respecto de `bad -> d` y
  las reglas auxiliares `X`;
- el SRS guardado cambia el problema o prueba una propiedad artificial;
- la unica configuracion exitosa surge despues de ajustar flags/provers viendo
  resultados;
- reglas/estados superan `2x` S2 base antes del prover;
- CNF o tiempo medianos son peores que S2 base por mas de `25%` sin `YES`;
- C3 obtiene `YES` pero no puede producir CPF;
- CeTA rechaza el CPF por una razon no superficial;
- aparece una familia equivalente en el repo oficial o literatura previa.

Si C3 mejora costos pero falla CPF/CeTA, el resultado queda como exploratorio.
Si C3 obtiene logs positivos con una configuracion no preregistrada, esos logs
no pueden convertirse retroactivamente en exito confirmatorio.

## Resultados que NO se pueden reclamar

Aunque C3 minimo tenga exito, no se puede reclamar:

- prueba de la conjetura de Collatz;
- terminacion del sistema completo `S`;
- terminacion del complemento completo `U_16` de `378` residuos;
- validez para `k != 16`;
- validez para S1, S3 u otra rama;
- reproduccion completa de Angeltveit o Barina;
- novedad absoluta sin nueva busqueda bibliografica;
- que `YES` sin CPF/CeTA sea prueba fuerte;
- que menor tiempo en una configuracion tuneada post hoc sea evidencia;
- que una reduccion de CNF pruebe significado matematico por si sola.

La unica formulacion defendible, si todo pasa, es acotada:

```text
La microfamilia G_8189, congelada por certificados low-bit y validada por un
checker de implicacion, genera un benchmark C3 minimo de la rama S2 que es mas
tratable/certificable que S2 base bajo la configuracion preregistrada.
```

## Higiene anti p-hacking

Antes de la primera llamada a Matchbox, AProVE, TTT2, CeTA o cualquier prover,
debe existir un manifiesto C3 commiteado que incluya:

- id del preregistro: `M25-C3-minimo-r8189-v1`;
- commit exacto del repo;
- hashes de inputs y outputs generados;
- comando exacto de generacion C3;
- comando exacto del checker;
- lista cerrada de provers/frontends;
- versiones exactas;
- flags completos;
- timeouts;
- semillas o declaracion de determinismo;
- hardware/OS;
- orden de corrida;
- numero de repeticiones;
- regla de agregacion, por ejemplo mediana si hay repeticiones.

Reglas anti cherry-picking:

- todo prover/flag preregistrado debe correrse tanto en S2 base como en C3;
- no se puede agregar un prover despues de ver `MAYBE`/`TIMEOUT`;
- no se puede subir timeout solo para C3;
- no se puede cambiar orientacion LSB/MSB despues de ver CNF;
- no se puede cambiar encoding de la guarda despues de ver tiempos;
- no se puede reportar solo el mejor seed;
- no se puede ocultar `ERROR` o `TIMEOUT`;
- si se exploran nuevas flags, deben etiquetarse como exploratorias y exigir
  un nuevo preregistro antes de contar como evidencia.

El baseline obligatorio es S2 base medido en el mismo entorno y con la misma
configuracion. No alcanza comparar C3 contra un resultado historico de M19 si
versiones, flags, hardware o timeout no son identicos y verificables.

## Gate final

M25 no autoriza todavia ningun prover. Autoriza solo el siguiente paso: generar
un artefacto C3 minimo y un checker de implicacion para `G_8189`, ambos
alineados con este preregistro. La primera corrida de prover que no pueda
apuntar a este documento y a un manifiesto previo queda automaticamente fuera
del registro confirmatorio.
