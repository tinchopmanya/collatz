# M19 Web 2026 - Estado publico de Collatz al 29 de abril de 2026

Autor: CodexHijo-Web2026
Fecha de corte: 2026-04-29
Scope: investigacion web y analisis. No se modificaron scripts, workflows ni archivos de otros colaboradores.

## Veredicto ejecutivo

No estamos en terreno virgen. La zona Collatz esta extremadamente explorada: bibliografias anotadas de Lagarias, verificacion computacional hasta potencias enormes, teoria de ciclos, suficiencia de progresiones aritmeticas, dinamica 2-adica, modelos de reescritura/terminacion, SAT/SMT/ATP, generalizaciones tipo Conway/Fractran y una iniciativa publica de formalizacion.

Si nuestra estrategia local usa clases residuales, vectores de paridad, prefijos/binario, bloques, arbol inverso, "descenso eventual" o terminacion por ranking, entonces alguien ya busco cerca. Eso no invalida el trabajo, pero exige que cada lema nuevo se compare contra los marcos conocidos y que evitemos reempaquetar la dificultad central como una hipotesis equivalente a Collatz.

Lo realmente nuevo y serio en 2026, segun fuentes primarias localizadas, no es una prueba de Collatz. Es:

- Vigleik Angeltveit, arXiv 2026: nuevo algoritmo de verificacion para todos los `n < 2^N`, con codigo publico y estimaciones de mejora 50-100x frente a algoritmos previos. Es computacional, no teorico-resolutivo.
- Kevin Knight, Discrete Mathematics 2026: prueba revisada por pares de que los "Collatz high cycles" racionales no pueden estar compuestos por enteros positivos. Es avance real en teoria de ciclos, pero no descarta todos los ciclos ni la divergencia.
- Kevin Knight, Complex Systems 2026: regla multiplicativa de 30 condiciones que simula Collatz sin `+1`. Es una representacion nueva/compacta, no una prueba.
- Collatz Conjecture Challenge: proyecto publico de formalizacion de literatura; al consultar, declara `0/358` papers formalizados, 3 en formalizacion y 3 listos para auditar. Es importante como infraestructura, no como teorema nuevo.

La cota publica fuerte de verificacion computacional sigue siendo Barina 2025: convergencia verificada hasta `2^71`. No encontre una fuente primaria posterior que anuncie una cota verificada mayor que `2^71` al 2026-04-29.

## Fuentes primarias y estado de confianza

| Fuente | Link primario | Tipo | Estado de confianza | Que cambia |
|---|---|---:|---:|---|
| Barina, "Improved verification limit for the convergence of the Collatz conjecture" | https://doi.org/10.1007/s11227-025-07337-0 | articulo revisado por pares, open access, Journal of Supercomputing, publicado 2025-05-02 | Alta para la cota computacional `2^71`; no es prueba general | Sube la frontera publica desde `2^68` a `2^71`; incluye arquitectura distribuida, GPU/CPU, sieves y cuatro nuevos path records |
| Angeltveit, "An improved algorithm for checking the Collatz conjecture for all n < 2^N" | https://arxiv.org/abs/2602.10466 | preprint arXiv, enviado 2026-02-11; codigo declarado en https://github.com/vigleik0/collatz | Media-alta como propuesta reproducible; aun no revisado por pares | Propone algoritmo mas eficiente y no lineal, con CPU Rust y GPU CUDA/OpenCL; estima 50-100x contra literatura para ciertos rangos |
| Knight, "Collatz high cycles do not exist" | https://doi.org/10.1016/j.disc.2025.114812 y pagina editorial https://www.sciencedirect.com/science/article/pii/S0012365X25004200 | articulo revisado por pares, Discrete Mathematics, vol. 349(3), marzo 2026 | Alta para el resultado especifico de high cycles | Descarta una familia extremal de ciclos racionales como ciclos enteros positivos; no resuelve ciclos arbitrarios ni divergencia |
| Knight, "A Small Collatz Rule without the Plus One" | https://doi.org/10.25088/ComplexSystems.35.1.1 | articulo 2026 en Complex Systems | Media-alta para el modelo; impacto teorico limitado | Reduce una simulacion multiplicativa de Collatz a 30 condiciones, frente a la regla enorme de Monks; no prueba terminacion |
| Yolcu, Aaronson, Heule, "An Automated Approach to the Collatz Conjecture" | https://doi.org/10.1007/s10817-022-09658-8 y arXiv https://arxiv.org/abs/2105.14697 | articulo revisado por pares, Journal of Automated Reasoning, 2023 | Alta para la equivalencia reescritura-terminacion y resultados negativos/parciales | Establece una ruta automatizada seria: Collatz equivale a terminacion de un sistema de reescritura mixto binario-ternario; no encuentra prueba de Collatz |
| Termination Competition 2025 | https://termination-portal.org/wiki/Termination_Competition_2025 y resultados https://termcomp.github.io/Y2025/ | infraestructura/benchmark de comunidad | Alta como evidencia de estado de herramientas; no es fuente de un teorema Collatz | Las herramientas de terminacion compiten sobre problemas TPDB; no aparece una resolucion publica de Collatz |
| Collatz Conjecture Challenge | https://ccchallenge.org/ | iniciativa publica de formalizacion | Media como tracker vivo; revisar periodicamente | Lista 366 entradas; objetivo de formalizar literatura. Al consultar: `0/358` papers formalizados |
| Tao, "Almost all orbits of the Collatz map attain almost bounded values" | DOI https://doi.org/10.1017/fmp.2022.8 y arXiv https://arxiv.org/abs/1909.03562 | articulo revisado por pares, Forum of Mathematics Pi, 2022 | Muy alta para avance analitico parcial | Sigue siendo el avance teorico moderno mas fuerte: casi todas las orbitas alcanzan valores casi acotados en densidad logaritmica |
| Lagarias, bibliografias/overview | 1963-1999: https://arxiv.org/abs/math/0309224 ; 2000-2009: https://arxiv.org/abs/math/0608208 ; overview: https://arxiv.org/abs/2111.02635 | bibliografia/survey por experto | Muy alta como mapa historico | Confirma que el terreno esta muy recorrido y que Collatz permanece abierto |

## Que hay realmente nuevo en 2026

### 1. Angeltveit 2026: algoritmo de verificacion mas fuerte

Fuente primaria: https://arxiv.org/abs/2602.10466

El paper declara un algoritmo para verificar convergencia de todos los `n < 2^N` que escala mejor que los metodos previos: tarda menos de 2x al pasar de `2^N` a `2^(N+1)`. La idea operativa combina busqueda recursiva por bits menos significativos, bitvectors precomputados, descent sieve, mod 9 preimage sieve, path-merging sieve y odd-even-even sieve. Declara codigo en https://github.com/vigleik0/collatz.

Importante: es un avance de ingenieria/algoritmica de verificacion. No prueba Collatz. El propio texto toma Barina `2^71` como estado del arte y estima que con recursos similares podria empujar mucho mas, pero eso no equivale a una cota nueva hasta que se ejecute y audite.

Impacto para estrategia: si nuestra linea busca "bloques", "prefijos", "bits", "sieves" o "descenso por clases", debemos comparar contra Angeltveit. Cualquier algoritmo local de poda debe medir novedad frente a sus cuatro sieves y su esquema de bitvectors.

### 2. Knight 2026: high cycles

Fuente primaria: https://doi.org/10.1016/j.disc.2025.114812

El articulo distingue ciclos racionales por `k` longitud y `x` terminos impares, y estudia dos extremos: circuitos y high cycles. Ya se sabia que no existen circuitos enteros positivos no triviales; Knight prueba que tampoco hay high cycles enteros positivos. Usa palabras de Christoffel/parity vectors.

Importante: esto no elimina todos los ciclos posibles. El propio resumen editorial deja claro que el problema general sigue abierto. Es un avance real, revisado por pares, pero local dentro de la teoria de ciclos.

Impacto para estrategia: si nuestra busqueda ataca ciclos, debe mapear si nuestros candidatos son circuitos, high cycles u otra familia. Si solo redescubrimos restricciones extremales, probablemente no alcance.

### 3. Knight 2026: regla multiplicativa de 30 condiciones

Fuente primaria: https://doi.org/10.25088/ComplexSystems.35.1.1

El paper construye una regla `K(n)` que simula Collatz sin el `+1`, usando solo multiplicacion y 30 condiciones. Mejora la compacidad frente a Monks, que tenia una regla de 1.021.020 condiciones.

Importante: es una codificacion/simulacion, no una reduccion que haga el problema mas facil automaticamente. El paper deriva condiciones de ciclos conocidas, como relaciones sobre sumas de terminos pares/impares, pero no resuelve terminacion.

Impacto para estrategia: util si queremos una maquina/representacion alternativa para experimentos de terminacion o invariantes. No debe venderse como "se elimino la parte dificil".

### 4. Barina-Maat 2026: `3n + 3^k`

Fuente primaria: https://arxiv.org/abs/2602.05732 y DOI relacionado https://doi.org/10.12921/cmst.2025.0000007

Generaliza por escala: la secuencia `3n + 3^k` para `3^k n` replica la secuencia Collatz de `n` multiplicada por `3^k`, bajo la condicion de convergencia original. Esto es matematicamente correcto como relacion de escala, pero no parece abrir una ruta independiente hacia la prueba.

Impacto para estrategia: bajo. Sirve como control contra falsas generalizaciones: si el resultado depende de asumir convergencia Collatz, no es progreso sobre Collatz.

## Que NO cambio

- No hay prueba aceptada de la conjetura de Collatz al 2026-04-29.
- No hay refutacion publica ni contraejemplo.
- No encontre cota computacional primaria posterior a Barina `2^71`.
- Tao 2022 sigue siendo el avance teorico parcial mas fuerte de alto prestigio.
- Yolcu-Aaronson-Heule sigue siendo la ruta automatizada/terminacion mas seria; no fue superada por una prueba automatica completa.
- Termination Competition y TPDB no muestran que una herramienta haya resuelto el benchmark equivalente a Collatz.

## Claims no auditados o de bajo peso

Estos materiales existen y algunos son recientes, pero no deberian cambiar la estrategia sin auditoria independiente:

- "Collatz Conjecture Is True for All Positive Integers as Verified with Isabelle", Kirk O. Hahn, Preprints.org v2, 2026-01-12: https://www.preprints.org/manuscript/202508.0891 . La propia pagina lo marca como preprint no revisado por pares. Requiere repositorio Isabelle verificable, revision de expertos y localizacion exacta del teorema formalizado.
- "New Algebraic Proofs..." de Yassine Larbaoui, IJMTT 2026, DOI mencionado publicamente: https://doi.org/10.14445/22315373/IJMTT-V72I1P105 . Aunque tiene DOI/revista, el tipo de venue y el patron de "proof of Collatz" requieren extrema cautela. No encontre evidencia de adopcion por especialistas.
- Preprints.org/Sciety con "proofs" de Collatz, por ejemplo actividad en https://sciety.org/articles/activity/10.20944/preprints202503.0499.v1 . Son claims, no consenso.
- Reddit/Scribd/ResearchGate/viXra/rXiv contienen multiples "proofs" 2026. Pueden servir como lista de errores comunes, no como base cientifica.

Criterio recomendado: ningun claim de "proof" cuenta si no entrega uno de estos artefactos: articulo revisado por pares en venue matematico serio; formalizacion verificable en Lean/Isabelle/Coq con repositorio reproducible; o revision tecnica de especialistas reconocidos que identifique exactamente que obstaculo historico supera.

## Estamos en terreno virgen?

No, en sentido global. Hay trabajo previo sobre casi todas las formas naturales de atacar Collatz:

- Computacional: Oliveira e Silva, Roosendaal, yoyo@home, Barina, Angeltveit.
- Paridad/residuos/sieves: desde resultados clasicos hasta Barina/Angeltveit.
- Ciclos: Bohm-Sontacchi, Steiner, Eliahou, Simons-de Weger, Hercher, Knight.
- Densidad/casi todos: Terras, Everett, Korec, Krasikov-Lagarias, Tao.
- Reescritura/terminacion/SAT: de Mol, Yolcu-Aaronson-Heule, Termination Competition/TPDB.
- Codificaciones alternativas: Conway/Fractran, Monks, Knight, tag systems, Wang tiles.
- Formalizacion: Collatz Conjecture Challenge, Isabelle/Lean claims aislados.

Podria haber terreno localmente virgen si nuestra estrategia produce una definicion nueva que no sea simplemente un vector de paridad, una clase residual, una progresion suficiente, una simulacion de maquina o una condicion equivalente escondida. Pero la carga de prueba de originalidad es alta.

## Ya alguien busco esto?

Si "esto" significa busqueda por bloques/prefijos/paridad/residuos, si. Angeltveit 2026 es especialmente cercano a cualquier idea basada en agregar bits, podar ramas y verificar descenso. Yolcu-Aaronson-Heule cubre la ruta de convertir Collatz en terminacion. Knight cubre una parte moderna de ciclos con palabras de Christoffel. Monks/Knight/Conway cubren codificaciones multiplicativas. Tao cubre la direccion probabilistica de casi-todos.

Si nuestra estrategia apunta a "un criterio finito que garantice descenso para todos los enteros", entonces tambien hay precedentes: suficiencia de progresiones aritmeticas, sieves, arboles inversos, y teoria de stopping times. El riesgo principal es probar una condicion que, para verificarse globalmente, ya requiere Collatz.

## Fuente primaria vs claim

Clasificacion operativa:

- Primaria fuerte: articulo revisado por pares con DOI/editorial reconocida, arXiv del autor, codigo oficial del autor, pagina oficial del proyecto o competicion.
- Primaria pero pendiente: arXiv sin revision por pares pero con autores identificables, codigo y reproducibilidad.
- Secundaria util: Wikipedia, blogs, Quanta/MIT Tech Review, paginas divulgativas; sirven para orientacion, no para claims tecnicos.
- Claim no auditado: Preprints.org, ResearchGate, viXra/rXiv, Scribd, Reddit, PDFs sueltos, revistas de baja senal con "proof" total y sin recepcion experta.

Aplicacion:

- Barina `2^71`: fuente primaria fuerte.
- Angeltveit 2026: primaria pendiente; reproducible por codigo.
- Knight high cycles: primaria fuerte.
- Knight regla 30: primaria razonable, pero impacto limitado.
- Yolcu-Aaronson-Heule: primaria fuerte.
- Termination Competition: primaria para estado de herramientas, no para una prueba Collatz.
- "Collatz solved 2026": claim no auditado salvo prueba formal/revision seria.

## Camino con mayor posibilidad cientifica fuerte

La mejor apuesta no es intentar una "prueba completa" desde cero. La ruta con mayor posibilidad cientifica fuerte es un programa de resultados parciales auditables:

1. Formalizacion y certificados: alinear con Collatz Conjecture Challenge. Formalizar un lema local real en Lean/Isabelle o producir certificados verificables para cualquier claim computacional. Esto baja el riesgo de circularidad.
2. Comparacion contra Angeltveit/Barina: si hacemos computo, que sea reproducible, con checksum, doble implementacion y benchmark contra `vigleik0/collatz` y Barina. Un avance serio seria empujar cota o reducir casos con una poda demostrablemente nueva.
3. Teoria de ciclos delimitada: si hay una estructura de bloques nueva, intentar convertirla en una exclusion de una familia concreta de ciclos, al estilo Knight/Hercher/Eliahou, no en una prueba global inmediata.
4. Terminacion automatizada incremental: usar Yolcu-Aaronson-Heule como base y buscar pruebas de subfamilias/variantes con ranking functions certificables. Evitar claims tipo "el terminador resuelve Collatz" si solo resuelve instancias finitas.
5. Puente con Tao: cualquier argumento probabilistico debe distinguir nitidamente "casi todos" de "todos". Un resultado fuerte seria convertir una familia excepcional en algo estructuralmente imposible, no solo improbable.

## Recomendaciones para el orquestador

- Tratar el proyecto como investigacion en zona saturada, no como exploracion virgen.
- Exigir una matriz de originalidad para cada lema: "equivalente a que resultado conocido?", "donde supera a Barina/Angeltveit/Knight/Yolcu?", "que caso historico no cubierto ataca?".
- Crear una regla de cuarentena: ningun documento interno debe afirmar "prueba de Collatz" sin pasar por verificacion formal o revision externa.
- Priorizar outputs publicables modestos: un nuevo sieve certificado, una familia de ciclos excluida, una formalizacion de un paper existente, una reproduccion independiente de `2^71`, o una comparacion robusta con Angeltveit.
- Si hay recursos computacionales, primero reproducir Angeltveit en una muestra y auditar checksums; solo despues intentar extender cotas.
- Si hay recursos matematicos, concentrarse en ciclos/familias excepcionales o formalizacion, no en claims globales basados en intuicion de descenso.
- Mantener una lista viva de "claims 2026 no auditados" para evitar redescubrir errores y para usarla como banco de pruebas de detectores de circularidad.

## Links primarios usados

- Barina 2025, Journal of Supercomputing: https://doi.org/10.1007/s11227-025-07337-0
- Angeltveit 2026, arXiv: https://arxiv.org/abs/2602.10466
- Codigo Angeltveit declarado en paper: https://github.com/vigleik0/collatz
- Knight 2026 high cycles, DOI: https://doi.org/10.1016/j.disc.2025.114812
- Knight 2026 high cycles, ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0012365X25004200
- Knight 2026 regla sin `+1`: https://doi.org/10.25088/ComplexSystems.35.1.1
- Yolcu-Aaronson-Heule 2023, DOI: https://doi.org/10.1007/s10817-022-09658-8
- Yolcu-Aaronson-Heule, arXiv: https://arxiv.org/abs/2105.14697
- Rewriting Collatz code mencionado en WST/paper: https://github.com/emreyolcu/rewriting-collatz
- Termination Competition 2025: https://termination-portal.org/wiki/Termination_Competition_2025
- TermComp 2025 results: https://termcomp.github.io/Y2025/
- Collatz Conjecture Challenge: https://ccchallenge.org/
- Tao 2022, DOI: https://doi.org/10.1017/fmp.2022.8
- Tao arXiv: https://arxiv.org/abs/1909.03562
- Lagarias bibliography 1963-1999: https://arxiv.org/abs/math/0309224
- Lagarias bibliography 2000-2009: https://arxiv.org/abs/math/0608208
- Lagarias overview: https://arxiv.org/abs/2111.02635
- Barina-Maat `3n + 3^k`: https://arxiv.org/abs/2602.05732
- Barina-Maat related DOI: https://doi.org/10.12921/cmst.2025.0000007
- Preprints.org claim Isabelle, bajo peso: https://www.preprints.org/manuscript/202508.0891
- Sciety/preprint claim, bajo peso: https://sciety.org/articles/activity/10.20944/preprints202503.0499.v1
