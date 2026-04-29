# M23 frontera web/papers Collatz rewriting + low-bit, corte abril 2026

Fecha de corte: 2026-04-29
Agente: CodexInvestigadorWeb-M23
Worktree: `C:\dev\vert\collatz-m23-frontera-web-2026`
Rama: `codex-investigador/m23-frontera-web-2026`
Base sincronizada antes de escribir: `origin/main` observado en `1e4e8c6` por `git fetch` + `git merge --ff-only`

## Resumen ejecutivo

La frontera publica hasta fines de abril de 2026 separa con bastante claridad tres lineas:

1. Rewriting/termination para Collatz ya esta recorrido: Zantema codifico Collatz como terminacion de SRS en 2003/2005; Yolcu-Aaronson-Heule llevaron esto a sistemas mixtos binario/ternarios, SAT + matrix/arctic interpretations, y pruebas automaticas de debilitamientos no triviales.
2. Certificacion de terminacion tambien esta recorrido como infraestructura: AProVE, Matchbox, TTT2, CPF, CeTA/IsaFoR y TermComp son una comunidad madura. Lo nuevo no seria "usar AProVE/Matchbox/CeTA"; seria una instancia Collatz exacta, guardada y verificable que produzca `YES` top-level + CPF + CeTA.
3. Low-bit/descent computacional tambien esta recorrido: Barina empujo la verificacion hasta `2^71`; Angeltveit 2026 propone un algoritmo low-bit para verificar `n < 2^N` con crecimiento menor que `2x` por bit; Bonacorsi-Bordoni 2026 modela stopping times y confirma heterogeneidad modular baja, pero no aporta certificados ni rewriting.

No encontre una fuente primaria o repo publico que combine explicitamente:

```text
certificados low-bit/descent modulo 2^k
  + descarga de familias residuales
  + SRS/TRS guarded para las ramas residuales de Yolcu-Aaronson-Heule
  + eventual CPF/CeTA
```

Por eso, la novedad plausible de M22/M23 es media-alta solo si se mantiene acotada: "preprocesador certificado de descenso que genera benchmarks guarded rewriting residuales reproducibles". La novedad cae a baja si se presenta como otra prueba de Collatz, como una corrida mas de AProVE/Matchbox, o como un filtro low-bit sin puente semantico auditado.

## Tabla de fuentes clave

| Tema | Fuente | Fecha relevante | Que aporta | Lectura para M22 |
| --- | --- | ---: | --- | --- |
| Rewriting Collatz | [Yolcu-Aaronson-Heule, arXiv:2105.14697](https://arxiv.org/abs/2105.14697) | v1 2021-05-31; v3 2022-12-31; JAR 2023 | SRS mixto binario/ternario; terminacion equivalente a Collatz; prover SAT con natural/arctic matrix interpretations; pruebas de debilitamientos | Base obligada; M22 debe hablar como extension/benchmark, no como terreno virgen |
| Codigo YA-Heule | [emreyolcu/rewriting-collatz](https://github.com/emreyolcu/rewriting-collatz) | HEAD observado 2026-04-29: `8a4dfda60f97a6d33ff0a24fdfa7a172d4bec340` | Reglas, prover, pruebas reproducibles, conversor TPDB | Comparar S1/S2/S3 contra repo oficial antes de reclamar novedad |
| Zantema SRS | [Zantema, Termination of String Rewriting Proved Automatically](https://pure.tue.nl/ws/files/1729598/200314.pdf) | report 2003; JAR 2005 | TORPA, relative termination, semantic labelling, Collatz como SRS chico | El encuadre "Collatz como terminacion SRS" no es nuevo |
| TermComp 2026 | [Termination Competition 2026](https://termination-portal.org/wiki/Termination_Competition_2026) | pagina editada 2026-04-27; full run 2026-07-13/17 | Reglas 2026; salida `YES/NO/MAYBE`; proof ASCII/HTML/CPF; categorias certificadas | Define estandar comunitario actual |
| AProVE | [AProVE usage](https://aprove.informatik.rwth-aachen.de/index.php/usage) | consultado 2026-04-29 | SRS `.srs`, TRS/ARI/XML, `-C ceta`, `-p cpf` | Ruta concreta para `YES` + CPF si el problema entra |
| CPF | [Sternagel-Thiemann, CPF, arXiv:1410.8220](https://arxiv.org/abs/1410.8220) | 2014-10-30 | Formato comun para pruebas de terminacion/confluencia/complejidad | M22 fuerte requiere CPF, no solo log |
| CeTA | [CeTA, arXiv:1208.1591](https://arxiv.org/abs/1208.1591) | 2012-08-08 | Certificador basado en IsaFoR/Isabelle/HOL | Verificador externo para prueba de termination |
| Matchbox certificado | [Certified Matchbox, WST 2022 proceedings](https://sws.cs.ru.nl/pmwiki/uploads/Main/wst2022proceedings.pdf) | 2022 | Matchbox en categoria certified SRS, certificados para CeTA, natural/arctic matrices, tiling | Matchbox es relevante, pero no novedoso por si solo |
| Benchmarks relative SRS | [Hofbauer-Waldmann, arXiv:2307.14149](https://arxiv.org/abs/2307.14149) | 2023-07-26 | Critica y enumeracion de benchmarks de relative SRS termination | M22 podria aportar benchmark nuevo si esta bien etiquetado |
| Angeltveit low-bit | [Angeltveit, arXiv:2602.10466](https://arxiv.org/abs/2602.10466) | 2026-02-11 | Algoritmo mejorado para verificar Collatz `n < 2^N`; costo menor que `2x` por bit | Fuente reciente para certificados low-bit/descent |
| Codigo Angeltveit | [vigleik0/collatz](https://github.com/vigleik0/collatz) | HEAD observado 2026-04-29: `f3f09248c7ae7299b8443e112f565f309d97f161` | CUDA/OpenCL; README indica RTX 3060 verifica hasta `2^60` en unas 24h | Reproduccion externa posible, pero GPL-3.0 segun auditoria local M21 |
| Barina 2025 | [Improved verification limit, J Supercomput](https://link.springer.com/article/10.1007/s11227-025-07337-0) | aceptado 2025-04-21; publicado 2025-05-02 | Verificacion hasta `2^71`; aceleracion total `1335x`; cuatro path records | Baseline computacional fuerte; no rewriting |
| Barina project | [pcbarina.fit.vutbr.cz](https://pcbarina.fit.vutbr.cz/) | generado 2026-04-29; log: `2^71` el 2025-01-15 | Estado publico y log de cotas | Fuente de actualidad para cota verificada |
| Codigo Barina | [xbarin02/collatz](https://github.com/xbarin02/collatz) | HEAD observado 2026-04-29: `29af989b7dd49f9b78e7a1098af973495c7b7796` | CPU/GPU 128-bit, ctz y tabla chica de potencias de 3, MIT | Reproducibilidad de verificacion, no certificacion de M22 |
| Bonacorsi-Bordoni | [arXiv:2603.04479](https://arxiv.org/abs/2603.04479) | 2026-03-04 | Modelado bayesiano de stopping times `n <= 10^7`; covariables `log n`, `n mod 8`; odd-block generators | Apoya importancia de modulo bajo; no prueba ni certificado |
| Orbit mixing 2026 | [Chang, arXiv:2603.25753](https://arxiv.org/abs/2603.25753) | 2026-03-24 | Reduccion a problema one-bit/orbit-mixing, mod 8/mod 32 | Cercano a low-bit/residual, pero no rewriting/CPF |

## Rewriting y termination: terreno recorrido

### Zantema

Hans Zantema ya habia mostrado que string rewriting es suficientemente expresivo para Collatz. En el reporte/paper "Termination of String Rewriting Proved Automatically", Zantema presenta TORPA, combina semantic labelling, polynomial interpretations, recursive path order y dependency pairs, y declara que en la seccion 7 representara Collatz como terminacion de un SRS chico. La misma linea es citada por Yolcu-Aaronson-Heule como el sistema unary de Zantema, con el teorema: el SRS `Z` termina si y solo si Collatz es cierto.

Lectura para M22:

- Recorrido: codificar Collatz como SRS/termination.
- Recorrido: usar relative termination, rule removal, reversal y semantic labelling.
- Frontera: no hay señal de que Zantema trabajara con certificados low-bit modulo `2^k` para descargar ramas residuales de un sistema mixto.

Nivel de novedad para M22 frente a Zantema: bajo si solo reescribimos Collatz; medio si generamos benchmarks residuales guardados no presentes en TORPA/TPDB; alto solo si hay certificado externo reproducible.

### Yolcu-Aaronson-Heule

El paper YA-Heule es la fuente central. En el abstract de arXiv, los autores dicen que exploran Collatz "through the lens of termination of string rewriting", construyen un sistema que simula Collatz en representaciones mixtas binario-ternarias, prueban equivalencia entre terminacion del sistema y Collatz, demuestran limitaciones de natural matrix interpretations para el sistema unary de Zantema, e implementan un prover minimo con natural/arctic matrix interpretations para pruebas automaticas de debilitamientos.

El repo oficial `rewriting-collatz` acompana el paper, contiene el prover, reglas, pruebas y scripts. El README indica que los sistemas usan formato no estandar de simbolos single-letter, y ofrece `tpdb-convert.py` para convertir a TPDB.

Lectura para M22:

- Recorrido: mixed-base rewriting, SAT para interpretaciones, natural/arctic/tropical, debilitamientos no triviales.
- Recorrido: interpretar reglas dinamicas como funciones tipo Collatz y probar subsistemas/debilitamientos.
- No encontrado en fuentes revisadas: una familia "guarded by low-bit certificate" construida desde Angeltveit/Barina para conservar solo complementos residuales modulo `2^k`.
- Riesgo: cualquier desafio S1/S2/S3 puede estar moralmente cerca de debilitamientos explorados por los autores. Por eso la novedad debe anclarse en artefactos exactos, hashes y comparacion con repo oficial.

Nivel de novedad para M22 frente a YA-Heule: medio-bajo para S1/S2 sin certificado; medio para benchmark guarded con traduccion nueva; medio-alto si ademas produce `YES`/CPF/CeTA.

## Matchbox, AProVE, CeTA, CPF: terreno recorrido y vara de evidencia

La infraestructura de terminacion automatica no es nueva y esta viva en 2026. La pagina de TermComp 2026, editada el 2026-04-27, anuncia WST/FLoC 2026, full run del 2026-07-13 al 2026-07-17, live run 2026-07-24/25, y reglas donde las herramientas emiten `YES/NO/MAYBE` y pruebas ASCII/HTML/CPF, con excepciones para categorias certificadas.

AProVE declara soporte para SRS `.srs`, TRS, ARI/XML, y en CLI documenta:

- `-C ceta`: restringir a tecnicas certificables por CeTA.
- `-p cpf`: imprimir pruebas en formato CPF.
- `-m wst`: salida estilo competition (`YES`, `NO`, `MAYBE`, `ERROR`, `TIMEOUT`).

CPF y CeTA dan la vara fuerte:

- CPF es formato comun de certificados para terminacion y otras propiedades de TRS/SRS.
- CeTA es un certifier basado en IsaFoR/Isabelle/HOL.
- Las categorias certificadas corren certifiers sobre CPFs generados por herramientas.

Matchbox sigue siendo relevante para SRS. En "Certified Matchbox" (WST 2022), Waldmann describe Matchbox participando en la categoria certified termination of string rewriting; explica su historia: matchbounds desde 2003, matrix interpretations desde 2006, sparse tiling desde 2019, y en 2022 certificados para CeTA con restricciones de tecnicas.

Lectura para M22:

- Recorrido: usar AProVE/Matchbox/TTT2/CeTA/CPF.
- Recorrido: natural/arctic matrix interpretations y tiling/semantic labelling en SRS.
- No encontrado: que esas herramientas ya incluyan un preprocesador Collatz low-bit/descent estilo Angeltveit que genere familias residuales guardadas.
- Vara minima de publicacion: `YES` top-level no basta; se necesita CPF separado, CeTA `CERTIFIED`, versiones, hashes, comandos y equivalencia matematica del input.

Nivel de novedad para M22:

- Bajo: "corrimos AProVE/Matchbox sobre S1/S2".
- Medio: "nuevo benchmark relative/guarded SRS con README de origen y comparacion".
- Alto condicional: "guarded SRS exacto de M22 obtiene top-level `YES`, exporta CPF y CeTA lo certifica".

## Angeltveit 2026 low-bit/descent

Angeltveit publica el 2026-02-11 "An improved algorithm for checking the Collatz conjecture for all n < 2^N". El abstract dice que describe un nuevo algoritmo para verificar Collatz para todo `n < 2^N`, y que verificar `2^{N+1}` toma menos de dos veces el tiempo de verificar `2^N`. La auditoria local M21 ya extrajo el nucleo que importa para M22: trayectorias por bits bajos, invariantes afines de la forma `T^k(r + a 2^k) = T^k(r) + 3^f a`, y certificados de descenso para residuos modulo `2^k`.

El repo `vigleik0/collatz` estaba publico al corte observado, con HEAD `f3f09248c7ae7299b8443e112f565f309d97f161`. El README visible dice que `collatz_cudav7.cu` verifica convergencia hasta `2^N`, que tambien hay OpenCL, y que con una RTX 3060 verificar hasta `2^60` toma unas 24 horas.

Lectura para M22:

- Recorrido: low-bit/descent como verificacion computacional de rangos.
- Recorrido: usar bits bajos para descargar familias infinitas de lifts.
- No encontrado: conectar estos certificados a SRS mixtos tipo YA-Heule ni a CPF/CeTA.
- Riesgo: Angeltveit no es prueba global y no reemplaza el lema semantico de puente M22.

Nivel de novedad para M22 frente a Angeltveit: bajo si solo reimplementa el sieve; medio-alto si usa certificados como preprocesador semantico para benchmarks rewriting.

## Barina y verificaciones computacionales

Barina es el baseline computacional fuerte. El articulo 2021 "Convergence verification of the Collatz problem" presenta un algoritmo que reemplaza tablas enormes `O(2^N)` por tablas chicas `O(N)`, con implementaciones CPU/OpenCL para 128-bit. El articulo 2025 "Improved verification limit for the convergence of the Collatz conjecture" fue aceptado el 2025-04-21, publicado el 2025-05-02, y reporta la verificacion hasta `2^71`, aceleracion total `1335x` desde el primer algoritmo CPU al mejor GPU, distribucion en supercomputers europeos y cuatro nuevos path records.

El sitio de proyecto `pcbarina.fit.vutbr.cz`, generado el 2026-04-29, registra:

- 2020-05-07: verificacion bajo `2^68`.
- 2021-12-10: bajo `2^69`.
- 2023-07-09: bajo `2^70`.
- 2023-11-03: bajo `1.5 * 2^70`.
- 2025-01-15: bajo `2^71`.

El repo `xbarin02/collatz`, HEAD observado `29af989b7dd49f9b78e7a1098af973495c7b7796`, declara un enfoque con `ctz`, tabla chica de potencias de tres y soporte 128-bit.

Lectura para M22:

- Recorrido: verificacion exhaustiva de convergencia hasta cotas enormes.
- Recorrido: optimizaciones CPU/GPU y sieves aritmeticos.
- No encontrado: salida en forma de certificados de residuos pensados para SRS/TRS guarded ni CPF/CeTA.
- Uso sano para M22: baseline externo para no confundir "descenso por bits bajos" con resultado nuevo.

Nivel de novedad para M22 frente a Barina: bajo en computacion bruta; medio si convierte verificacion local en certificados reutilizables por rewriting.

## Bonacorsi-Bordoni 2026

Bonacorsi y Bordoni publican en arXiv el 2026-03-04 "Bayesian Modeling of Collatz Stopping Times: A Probabilistic Machine Learning Perspective". El abstract estudia `tau(n)` para `n <= 10^7`, usa un NB2-GLM bayesiano con covariables `log n` y `n mod 8`, y un generador mecanistico por odd-block decomposition con `K(m)=v_2(3m+1)`. El resultado relevante para nosotros es que condicionar por estructura modular baja mejora el ajuste, y que la heterogeneidad aritmetica de bajo modulo es visible estadisticamente.

Lectura para M22:

- Recorrido: modelado estadistico de stopping times; modularidad baja `mod 8`; odd-block lengths.
- No recorrido por ellos: termination rewriting, certificados, CPF/CeTA, familias residuales guardadas.
- Utilidad indirecta: refuerza que separar ramas `mod 8` no es caprichoso, pero no certifica nada.

Nivel de novedad para M22 frente a Bonacorsi-Bordoni: medio, porque el solapamiento es solo modular/estadistico; la via M22 es formal/rewriting si se completa.

## Otros trabajos 2026 cercanos pero no equivalentes

Edward Y. Chang, arXiv:2603.25753, enviado el 2026-03-24, reduce Collatz a un problema de one-bit orbit-mixing con estructura `mod 8`/`mod 32`. Es relevante porque confirma que 2026 tiene actividad sobre "low-order bits" y residuos, pero no encontre en esa fuente rewriting, certificados de terminacion ni CPF/CeTA.

Tambien aparecieron resultados no primarios o menos confiables en ResearchGate, reddit, preprints.org, viXra y sitios personales con lenguaje de "proof", "certificate", "Lean" o "residual families". No los uso como evidencia de frontera porque no encontre en ellos una cadena auditable equivalente a paper/repo/certificador, y varios parecen depender de hipotesis no verificadas o claims no revisados. Sirven solo como ruido de busqueda: muestran que la palabra "certificate" aparece, no que exista la combinacion M22.

## Busquedas negativas realizadas

No encontre coincidencias sustantivas para la combinacion exacta mediante busquedas web focalizadas, incluyendo:

- `"low-bit" Collatz rewriting termination residual families`
- `"Collatz" "rewriting" "low bits"`
- `"Collatz" "low-bit" "termination" "rewriting"`
- `"Collatz" "residue" "string rewriting" "certificate"`
- `"Angeltveit" "rewriting" Collatz`
- `"Angeltveit" "Yolcu" Collatz`
- `"Barina" "rewriting" Collatz`
- `"Barina" "termination" "Collatz" "rewriting"`
- `site:github.com Collatz "rewriting" "low-bit"`
- `site:github.com Collatz "Angeltveit" "rewriting"`

Lo encontrado en esas busquedas cae en una de estas clases:

- YA-Heule o copias/citas del paper.
- Barina/Angeltveit como verificacion computacional.
- Bonacorsi-Bordoni/Chang como low-modular o estadistico.
- Repos o posts no relacionados con rewriting/low-bit Collatz.
- Claims no primarios sin artefactos certificables.

Conclusion negativa: hasta el corte 2026-04-29, no encontre evidencia publica de que alguien haya combinado certificados low-bit de descenso con familias residuales de rewriting tipo M22.

## Nivel de novedad por afirmacion posible

| Afirmacion | Nivel de novedad | Riesgo | Comentario |
| --- | --- | --- | --- |
| "Collatz como SRS/TRS termination" | Bajo | Alto de redundancia | Zantema y YA-Heule ya lo hicieron |
| "Usar natural/arctic matrix interpretations o SAT para Collatz-like SRS" | Bajo | Alto de redundancia | Nucleo de YA-Heule y herramientas de termination |
| "Correr AProVE/Matchbox/TTT2 sobre S1/S2" | Bajo-medio | Medio | Puede ser util como reproduccion, no como novedad fuerte |
| "Exigir CPF + CeTA para cualquier `YES`" | Bajo | Bajo | Es estandar comunitario, pero necesario |
| "Reproducir Angeltveit/Barina en pequeno" | Bajo-medio | Medio | Aporte de auditoria, no resultado teorico |
| "Usar certificados low-bit para descargar ramas residuales de YA-Heule" | Medio-alto | Alto | No encontrado publicamente; depende del puente semantico |
| "S2-k16 guarded benchmark con 378 residuos congelados y checker" | Medio-alto | Medio-alto | Podria ser benchmark nuevo si no esta en repo oficial |
| "S2-k16 guarded obtiene `YES` + CPF + CeTA" | Alto condicional | Alto | Resultado tecnico publicable si la traduccion es correcta |
| "Esto prueba Collatz" | Nulo/no defendible | Muy alto | No hay base para ese reclamo |

## Experimento que fortaleceria M22

El experimento que mas fortaleceria M22 no es escalar a muchos `k`, sino cerrar la brecha semantica y medir dificultad real:

```text
M22-C1/C2/C3:
  1. Rechecker independiente para S2-k16.
  2. Validador semantico de puente low-bit -> rama S2 del SRS mixto.
  3. SRS/TPDB guarded de los 378 residuos no certificados.
  4. Comparacion preregistrada contra S2 base con la grilla M19.
  5. Si aparece YES: exportar CPF y verificar con CeTA.
```

Fortalece la via si se cumplen todos estos puntos:

- `0` falsos positivos en certificados low-bit.
- `0` fallos del invariante affine.
- `0` discrepancias entre predicado residual y rama S2.
- El guarded SRS no infla reglas/CNF de forma peor que S2 base.
- Al menos un `QED/YES` donde S2 base no lo tenia, o reduccion robusta de costo.
- Si hay `YES`, CPF separado y CeTA `CERTIFIED`.

Un resultado fuerte y honesto seria:

```text
Un certificado de descenso por bits bajos descarga 7814/8192 clases de la rama S2.
El complemento de 378 clases genera un benchmark SRS guardado.
Ese benchmark es semanticamente un subproblema de S2 y es mas facil/certificable
para herramientas de termination.
```

## Experimento que destruiria M22

M22 debe abandonarse como via fuerte si ocurre cualquiera de estos eventos:

- Un solo residuo certificado produce algun lift positivo que no desciende como se afirma.
- El rechecker independiente no reproduce los counts/hashes congelados para S2-k16.
- El puente semantico falla: una clase `mod 2^16` no corresponde a la rama `bad -> d` / `tf* -> *` como se supone, o la guarda acepta clases fuera de S2.
- El guarded SRS conserva/descarga clases distintas de las `378` congeladas.
- El sistema guardado infla el problema: mas reglas/estados, CNF o tiempos que S2 base, sin obtener `YES`.
- Un resultado `YES` no puede exportarse a CPF o CeTA lo rechaza por una razon no superficial.
- Se encuentra en el repo oficial o literatura una familia equivalente de guardas low-bit ya probada bajo otro nombre.

El criterio de abandono mas limpio es:

```text
Si C1 o C2 fallan, cerrar M22 como diagnostico de cobertura residual.
Si C1/C2 pasan pero C3 empeora S2 base, cerrar M22 como benchmark engineering no util.
Si C3 mejora pero no certifica, mantenerlo como resultado exploratorio, no publicable fuerte.
```

## Recomendacion operativa

Seguir solo una iteracion confirmatoria: S2-k16. Es la rama local con mejor senal cuantitativa (`7814/8192` certificados, `378` no cubiertos), y coincide con la lectura M22/M22KillCriteria: el problema central ya no es encontrar mas cobertura, sino probar que la cobertura significa lo que creemos dentro del SRS mixto.

No recomiendo abrir todavia una familia grande S1/S2/S3 para varios `k`. Eso aumentaria el espacio de busqueda sin resolver el riesgo epistemico principal. La oportunidad M23 es estrecha pero real: si se logra un benchmark guarded S2-k16 semanticamente auditado y certificable por herramientas de termination, no encontre evidencia de que esa combinacion exista publicamente hasta abril de 2026.

## Fuentes consultadas

- [Yolcu, Aaronson, Heule, "An Automated Approach to the Collatz Conjecture", arXiv:2105.14697](https://arxiv.org/abs/2105.14697)
- [Yolcu personal page, publicaciones y charlas Collatz/rewrite](https://www.cs.cmu.edu/~eyolcu/research/rewriting-collatz.pdf)
- [Repositorio `emreyolcu/rewriting-collatz`](https://github.com/emreyolcu/rewriting-collatz)
- [README raw de `rewriting-collatz`](https://raw.githubusercontent.com/emreyolcu/rewriting-collatz/master/README.md)
- [Yolcu-Heule WST 2021 "Mixed Base Rewriting for the Collatz Conjecture"](https://www.cs.cmu.edu/~mheule/publications/WST21.pdf)
- [Zantema, "Termination of String Rewriting Proved Automatically"](https://pure.tue.nl/ws/files/1729598/200314.pdf)
- [Termination Competition 2026](https://termination-portal.org/wiki/Termination_Competition_2026)
- [Termination Competition Certified Categories](https://termination-portal.org/wiki/Termination_Competition_Certified_Categories_Competition)
- [AProVE usage](https://aprove.informatik.rwth-aachen.de/index.php/usage)
- [Termination Portal: AProVE](https://termination-portal.org/wiki/Tools%3AAProVE)
- [Termination Portal: Tools category](https://termination-portal.org/wiki/Category%3ATools)
- [Sternagel, Thiemann, "The Certification Problem Format", arXiv:1410.8220](https://arxiv.org/abs/1410.8220)
- [Sternagel, Thiemann, Winkler, Zankl, "CeTA", arXiv:1208.1591](https://arxiv.org/abs/1208.1591)
- [WST 2022 proceedings, CeTA and Certified Matchbox](https://sws.cs.ru.nl/pmwiki/uploads/Main/wst2022proceedings.pdf)
- [Hofbauer, Waldmann, "Old and New Benchmarks for Relative Termination of String Rewrite Systems", arXiv:2307.14149](https://arxiv.org/abs/2307.14149)
- [Angeltveit, "An improved algorithm for checking the Collatz conjecture for all n < 2^N", arXiv:2602.10466](https://arxiv.org/abs/2602.10466)
- [Repositorio `vigleik0/collatz`](https://github.com/vigleik0/collatz)
- [README raw de `vigleik0/collatz`](https://raw.githubusercontent.com/vigleik0/collatz/main/README.md)
- [Barina, "Convergence verification of the Collatz problem", J Supercomput 2021](https://link.springer.com/article/10.1007/s11227-020-03368-x)
- [Barina, "Improved verification limit for the convergence of the Collatz conjecture", J Supercomput 2025](https://link.springer.com/article/10.1007/s11227-025-07337-0)
- [Barina project page](https://pcbarina.fit.vutbr.cz/)
- [Repositorio `xbarin02/collatz`](https://github.com/xbarin02/collatz)
- [README raw de `xbarin02/collatz`](https://raw.githubusercontent.com/xbarin02/collatz/master/README.md)
- [Bonacorsi, Bordoni, "Bayesian Modeling of Collatz Stopping Times", arXiv:2603.04479](https://arxiv.org/abs/2603.04479)
- [Chang, "A Structural Reduction of the Collatz Conjecture to One-Bit Orbit Mixing", arXiv:2603.25753](https://arxiv.org/abs/2603.25753)
