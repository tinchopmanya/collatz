# Investigacion sobre Collatz - Tercera Ola: Mapa de competencia y propuesta de investigacion original

Fecha de cierre de esta ola: 2026-04-23 06:45:00 -03:00
Estado: tercera ola cerrada
Resumen asociado: [ResumenInvestigacionSobreCollatzTerceraOla.md](ResumenInvestigacionSobreCollatzTerceraOla.md)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)
Olas anteriores: [Primera](InvestigacionSobreElProblemaDeCollatz.md) | [Segunda](InvestigacionSobreCollatzSegundaOla.md)

---

## 1. Objetivo de esta ola

Determinar que se esta haciendo AHORA MISMO (abril 2026), quien lo hace, con que recursos, que huecos quedan, y proponer una linea de investigacion original y alcanzable.

---

## 2. Mapa completo de actividad en abril 2026

### 2.1. Frentes con recursos grandes

**Axiom Math** (Carina Hong, San Francisco)
- Financiamiento: $264M totales ($64M seed octubre 2025 + $200M Serie A marzo 2026).
- Valuacion: $1.6B+.
- Equipo: 30+ personas, incluyendo Francois Charton (resolvio un problema abierto de 100 anos), Aram Markosyan (ex Meta FAIR), Ken Ono (matematico de clase mundial).
- Que hacen: transformer que aprende la logica de control de Collatz al 99.8% de precision para numeros del orden de trillones. Usan Lean para verificacion formal. AxiomProver saco puntaje perfecto en Putnam.
- Paper relacionado: "Transformers know more than they can tell — Learning the Collatz sequence" (arXiv 2511.10811, noviembre 2025). Entrenan en base 2, logran 99.7% de precision. Los errores son estructurados: en mas del 90% de los fallos, el modelo calcula correctamente pero estima mal la longitud de los loops. Tratan al modelo como caja negra (analisis conductual, no interpretabilidad mecanica).
- Fuente: <https://arxiv.org/abs/2511.10811>

**DeepMind / AlphaProof**
- No atacan Collatz directamente.
- Pero: AlphaProof (RL + Lean) saco plata en IMO 2024, y Gemini Deep Think saco oro en IMO 2025 (35/42 puntos, 5 de 6 problemas).
- Metodologia publicada en Nature noviembre 2025.
- Si apuntaran a Collatz, tendrian recursos practicamente ilimitados.
- Fuente: <https://www.nature.com/articles/s41586-025-09833-y>

**OpenAI**
- GPT-5.2 resolvio el Problema #397 de Erdos con prueba verificada en Lean (aceptada por Terence Tao).
- No estan en Collatz publicamente.
- Fuente: <https://scitechdaily.com/for-the-first-time-chatgpt-has-solved-an-unproven-math-problem-in-geometry/>

**Anthropic / Claude**
- Claude Opus 4.6 resolvio un problema abierto de Donald Knuth en teoria de grafos en 1 hora.
- Opus 4.6 resolvio 10 de 12 problemas Putnam 2025 de forma autonoma con Rocq.
- John Janik uso Opus 4.6 para construir una formalizacion de 12,947 lineas en Lean 4 que reduce Collatz a confinamiento Diofantino en un toro bidimensional, en dos semanas.
- Fuentes: <https://github.com/johnjanik/syracuse-confinement>, <https://arxiv.org/html/2603.20405v1>

### 2.2. Investigadores academicos activos

**Edward Y. Chang** (Stanford)
- Dos papers en marzo 2026, ambos con colaboracion humano-LLM:
  1. "Exploring Collatz Dynamics with Human-LLM Collaboration" (arXiv 2603.11066): descomposicion burst-gap, scrambling modular, distribuciones geometricas de gaps y bursts. E[B]=2 para longitud de bursts.
  2. "A Structural Reduction of the Collatz Conjecture to One-Bit Orbit Mixing" (arXiv 2603.25753): reduce la conjetura a si cada orbita visita dos clases de residuos mod 32 con balance suficiente. Prueba el Map Balance Theorem: los conteos de gap starts ≡3 vs ≡7 (mod 8) difieren en exactamente 1 para todo K>=5.
- Significado: separa balance a nivel del mapa (probado, perfecto) de balance a nivel de orbita (conjeturado, es lo que falta).
- Fuentes: <https://arxiv.org/abs/2603.11066>, <https://arxiv.org/abs/2603.25753>

**Bonacorsi y Bordoni** (Columbia University)
- "Bayesian Modeling of Collatz Stopping Times" (arXiv 2603.04479, marzo 2026).
- Modelo bayesiano jerarquico NB2-GLM que predice tiempos de parada usando solo log(n) y residuo mod 8.
- Hallazgo clave: features simples (log n + mod 8) funcionan mejor que modelos mecanisticos mas elaborados basados en odd-block decomposition.
- Confirman que la heterogeneidad en stopping times tiene estratificacion aritmetica fuerte por clase de residuo.
- Fuente: <https://arxiv.org/abs/2603.04479>

**Paper IOPscience 2024** (J. Phys. Complexity)
- "Stochastic-like characteristics of arithmetic dynamical systems: the Collatz hailstone sequences".
- Confirman que las orbitas individuales de Collatz muestran propiedades de movimiento browniano geometrico.
- Usaron: tests de criptografia, power spectrum, DFA, autocorrelacion, entropia.
- Pero: analizaron orbitas individuales, no la serie de stopping times tau(n) como funcion de n.
- Fuente: <https://doi.org/10.1088/2632-072X/ad271f>

**Paper AIJFR 2025** (Anomalous Behavior)
- "Investigating Anomalous Behavior in the Collatz Conjecture: Prime Factor Influence and Power Laws".
- Identificaron que potencias de 3, 7, 19, 53 muestran distribucion de ley de potencias en vez de gaussiana.
- Mezclar estos primos amplifica stopping times de forma no aditiva.
- Analizaron residuos mod 8.
- Pero: NO EXPLICARON POR QUE esos primos especificos. Solo identificaron el fenomeno.
- Fuente: <https://www.aijfr.com/papers/2025/6/1880.pdf>

**Ralf Becker** (Medium, analisis visual)
- Conjeturo que el rolling average de stopping times exhibe autoafinidad estadistica tipo Weierstrass.
- Es solo una conjetura visual, no un analisis formal con exponentes de Hurst o MF-DFA.
- Fuente: <https://medium.com/@ratwolf/collatz-conjecture-patterns-in-a-simple-rule-38688455f640>

**Kazuo Nakanishi** (jxiv preprint)
- "A Structural Study of Parity Vectors in the Collatz Conjecture".
- Clasifico parity vectors por d (numero de ocurrencias de 1).
- Estudio estructural, no estadistico.
- Fuente: <https://jxiv.jst.go.jp/index.php/jxiv/preprint/download/3096/7302/6705>

### 2.3. Esfuerzos comunitarios

**Collatz Conjecture Challenge** (ccchallenge.org)
- Formalizacion de la literatura, un paper a la vez.
- Tiene un "Wishlist 2026" de papers por formalizar.
- Fuente: <https://ccchallenge.org/>

**Decenas de preprints** en arXiv, Preprints.org, Academia.edu, figshare, Zenodo.
- La gran mayoria son intentos de prueba no validados.
- Algunos son genuinamente interesantes (Petri nets, topologia, Galois fields).
- Regla: si no paso peer review en una revista fuerte, tratar con escepticismo.

### 2.4. Proyectos estudiantiles

- Al menos dos proyectos en ISEF 2025/2026 sobre Collatz (bounds, binary distributions).
- Tesis de grado en Georgia Southern sobre Collatz mod m.

---

## 3. Los 5 huecos genuinos que identifique

Despues de mapear todo lo anterior, estos son los huecos reales donde nadie esta trabajando o donde el trabajo existente es insuficiente:

### HUECO 1: Por que 3, 7, 19, 53 y no otros primos

**Estado:** el paper AIJFR 2025 IDENTIFICA que estos primos son anomalos pero NO EXPLICA por que. Nadie conecto esto con una propiedad algebraica de estos primos (orden multiplicativo de 2 mod p, relacion con la secuencia de Collatz a nivel modular, etc.).

**Que falta:** computar stopping times para potencias de TODOS los primos hasta algun limite alto. Determinar cuales primos son anomalos y cuales no. Buscar que propiedad algebraica separa los dos grupos. Buscar en OEIS si la secuencia de primos anomalos ya aparece en otro contexto.

**Por que es alcanzable:** es computacion pura + analisis estadistico + busqueda algebraica. No requiere ideas teoricas profundas, solo sistematicidad.

**Por que es importante:** si encontras la propiedad que caracteriza a los primos anomalos, eso revela estructura oculta en Collatz que contradice los modelos estocasticos. Seria publicable.

### HUECO 2: Analisis multifractal formal de la serie tau(n)

**Estado:** Ralf Becker conjeturo autoafinidad visual. El paper IOPscience hizo DFA pero sobre orbitas individuales, no sobre la funcion tau(n) vs n. Nadie hizo MF-DFA (Multifractal Detrended Fluctuation Analysis) sobre la serie de stopping times.

**Que falta:** computar tau(n) para n hasta 10^7 o 10^8. Aplicar DFA clasico para obtener el exponente de Hurst. Aplicar MF-DFA para obtener el espectro multifractal. Comparar con movimiento browniano fraccional y con la funcion de Weierstrass. Determinar si la serie es monofractal o genuinamente multifractal.

**Por que es alcanzable:** DFA y MF-DFA son tecnicas estandar con implementaciones en Python (MFDFA, nolds). La computacion de tau(n) es trivial hasta 10^7 y manejable hasta 10^8.

**Por que es importante:** si tau(n) es genuinamente multifractal, eso tiene implicaciones profundas sobre la naturaleza de las correlaciones en Collatz. Si es monofractal con H != 0.5, confirma correlaciones de largo alcance que contradicen el modelo de moneda justa.

### HUECO 3: Interpretabilidad mecanica del transformer de Collatz

**Estado:** el paper "Transformers know more than they can tell" (Axiom/arXiv 2025) trato al modelo como caja negra. Analizaron errores conductualmente pero NO abrieron las capas de atencion. No usaron tecnicas de interpretabilidad mecanica (circuit tracing, attention pattern analysis, probing). Anthropic publico en 2025 un framework de circuit tracing para Claude 3.5 Haiku que podria aplicarse aqui.

**Que falta:** entrenar un transformer pequeno en la tarea de Collatz (prediccion de long steps o stopping time). Aplicar herramientas de interpretabilidad mecanica: visualizar attention heads, hacer probing de representaciones intermedias, identificar circuitos. Determinar que "algoritmo" aprendio el modelo internamente.

**Por que es alcanzable:** transformers pequenos se entrenan en horas con una GPU. Las herramientas de interpretabilidad (TransformerLens, Neel Nanda's tools) estan maduras. No hace falta reinventar nada.

**Por que es importante:** si el transformer aprendio un algoritmo interno que los humanos no conocen, eso seria un descubrimiento genuino. Es exactamente lo que paso con AlphaFold (el modelo aprendio reglas de plegamiento que los biologos no conocian).

### HUECO 4: Conectar la anomalia de primos con el framework burst-gap de Chang

**Estado:** Chang publico su framework burst-gap en marzo 2026. El paper de primos anomalos es de 2025. NADIE conecto los dos. Las preguntas obvias: los primos anomalos generan distribuciones anomalas de longitud de bursts o gaps? El Map Balance Theorem de Chang se rompe para orbitas que empiezan en potencias de primos anomalos?

**Que falta:** implementar la descomposicion burst-gap de Chang computacionalmente. Calcularla para potencias de primos anomalos vs no anomalos. Comparar distribuciones. Testear si la conjetura de equidistribucion orbital de Chang falla para numeros con factores anomalos.

**Por que es alcanzable:** Chang describio el framework en detalle suficiente para reimplementar. Es computacion directa.

**Por que es importante:** conectaria dos hallazgos independientes y podria revelar por que ciertos numeros "resisten" mas la convergencia.

### HUECO 5: Correlaciones de largo alcance en vectores de paridad

**Estado:** el paper IOPscience encontro beta > 1 (persistencia fuerte) en el espectro de potencias de orbitas individuales. Nakanishi estudio parity vectors estructuralmente. Pero nadie hizo un analisis sistematico de correlaciones de largo alcance en la secuencia de paridades (impar/par) a lo largo de MUCHAS orbitas distintas. Tampoco se buscaron patrones prohibidos de forma exhaustiva.

**Que falta:** generar vectores de paridad para millones de numeros. Buscar n-gramas prohibidos o extremadamente raros. Calcular informacion mutua y autocorrelacion a distintos lags. Comparar con modelo de moneda justa.

**Por que es alcanzable:** generacion de datos trivial, analisis estadistico estandar.

**Por que es importante:** si existen correlaciones que violan el modelo IID, eso conecta directamente con por que el argumento probabilistico no puede cerrarse como prueba.

---

## 4. Propuesta de investigacion: plan de ataque

### 4.1. Fase 1 — Laboratorio computacional (semana 1-2)

Construir el repo con:
- Motor de Collatz optimizado (Python + Cython o NumPy vectorizado).
- Generador de datasets: tau(n), max excursion, parity vectors, odd-step counts.
- Descomposicion burst-gap segun Chang.
- Pipeline de analisis: DFA, MF-DFA, autocorrelacion, espectro de potencias, test de aleatoriedad.
- Visualizaciones.

### 4.2. Fase 2 — Ataque al Hueco 1: primos anomalos (semana 2-3)

1. Computar tau(p^k) para todos los primos p < 10,000 y k = 1..20.
2. Para cada primo p, testear si la distribucion de tau(p^k) vs k sigue ley de potencias o gaussiana (test de Kolmogorov-Smirnov, metodo de Clauset-Shalizi-Newman para power law fitting).
3. Clasificar primos en "anomalos" y "normales".
4. Buscar la secuencia de primos anomalos en OEIS.
5. Calcular propiedades algebraicas: orden multiplicativo de 2 mod p, ord_p(3), residuo de 3 mod p, posicion en la secuencia de Wieferich, etc.
6. Formular hipotesis sobre que propiedad algebraica separa los dos grupos.

### 4.3. Fase 3 — Ataque al Hueco 2: analisis multifractal (semana 3-4)

1. Generar tau(n) para n = 1 a 10^7 (manejable en minutos).
2. Aplicar DFA -> exponente de Hurst H.
3. Aplicar MF-DFA -> espectro de singularidades f(alpha).
4. Si H != 0.5: confirma correlaciones de largo alcance.
5. Si el espectro es ancho: confirma multifractalidad genuina.
6. Comparar tau(n) restringido a primos vs compuestos vs potencias de anomalos.
7. Buscar relacion entre H y la clase de residuo mod 8.

### 4.4. Fase 4 — Ataque al Hueco 4: burst-gap y primos anomalos (semana 4-5)

1. Implementar descomposicion burst-gap de Chang.
2. Calcular para orbitas de n = p^k con p anomalo vs p normal.
3. Comparar distribuciones de longitud de burst y gap.
4. Testear equidistribucion orbital de Chang para estos subconjuntos.
5. Buscar si el desequilibrio orbital se concentra en numeros con factores anomalos.

### 4.5. Fase 5 — Documentacion y publicacion (semana 5-6)

1. Documentar hallazgos en el sistema de investigacion.
2. Si hay resultados solidos: preparar draft para arXiv (preprint) y/o Journal of Integer Sequences / Experimental Mathematics.
3. Publicar repo en GitHub como herramienta abierta.

---

## 5. Por que esta propuesta tiene chances

1. **No compite con los grandes.** Axiom, DeepMind y OpenAI buscan LA PRUEBA. Nosotros buscamos PATRONES. Son frentes complementarios, no competitivos.

2. **Los huecos son reales.** Ninguno de los 5 huecos esta siendo atacado por equipos grandes. Son demasiado "exploratorios" para justificar millones de dolares, pero son exactamente donde aparecen descubrimientos.

3. **Las herramientas existen.** No hay que inventar nada: Python, NumPy, MFDFA, nolds, SciPy, matplotlib. Todo open source.

4. **El timing es perfecto.** Chang publico el framework burst-gap hace un mes. El paper de primos anomalos tiene un ano. Nadie los conecto aun. Ser el primero en conectarlos es una ventana temporal real.

5. **Es publicable independientemente del resultado.** Si encontras que propiedad separa los primos anomalos: paper. Si confirmas multifractalidad: paper. Si conectas burst-gap con anomalos: paper. Si NO encontras nada: "negative result" paper, tambien publicable en ciertos journals.

---

## 6. Riesgos y limitaciones

1. **Los primos anomalos podrian no tener una explicacion simple.** La secuencia 3, 7, 19, 53 podria ser accidental o depender de umbrales numericos arbitrarios. En ese caso, el Hueco 1 no da resultado limpio.

2. **La multifractalidad podria ser trivial.** Si tau(n) es monofractal con H ~ 0.5, eso confirma el modelo estocastico y no hay novedad. Pero aun asi, confirmar formalmente lo que se asumia informalmente tiene valor.

3. **Chang podria publicar la conexion con primos antes.** Es un riesgo temporal real. Pero Chang esta enfocado en la reduccion estructural, no en analisis estadistico.

4. **No vamos a probar Collatz.** Esto es exploracion, no resolucion. Hay que tener eso claro desde el principio.

---

## Fuentes usadas en esta ola

- Axiom Math / Carina Hong: <https://techfundingnews.com/axiom-math-ai-mathematician-64m-seed/>, <https://b.capital/why-we-invested/toward-mathematical-superintelligence-why-we-invested-in-axiom/>
- Axiom Serie A: <https://eu.36kr.com/en/p/3611624168731395>
- "Transformers know more than they can tell" (arXiv 2511.10811): <https://arxiv.org/abs/2511.10811>
- Edward Chang, "Exploring Collatz Dynamics with Human-LLM Collaboration" (arXiv 2603.11066): <https://arxiv.org/abs/2603.11066>
- Edward Chang, "A Structural Reduction..." (arXiv 2603.25753): <https://arxiv.org/abs/2603.25753>
- Bonacorsi & Bordoni, "Bayesian Modeling of Collatz Stopping Times" (arXiv 2603.04479): <https://arxiv.org/abs/2603.04479>
- IOPscience, "Stochastic-like characteristics..." (2024): <https://doi.org/10.1088/2632-072X/ad271f>
- AIJFR, "Investigating Anomalous Behavior..." (2025): <https://www.aijfr.com/papers/2025/6/1880.pdf>
- Ralf Becker, fractal patterns: <https://medium.com/@ratwolf/collatz-conjecture-patterns-in-a-simple-rule-38688455f640>
- Nakanishi, parity vectors: <https://jxiv.jst.go.jp/index.php/jxiv/preprint/download/3096/7302/6705>
- John Janik, Lean 4 formalization: <https://github.com/johnjanik/syracuse-confinement>
- Claude solves Knuth problem: <https://www.abhs.in/blog/claude-solves-donald-knuth-open-math-problem-proof-2026>
- Opus 4.6 Putnam: <https://arxiv.org/html/2603.20405v1>
- AlphaProof Nature paper: <https://www.nature.com/articles/s41586-025-09833-y>
- GPT-5.2 Erdos problem: <https://scitechdaily.com/for-the-first-time-chatgpt-has-solved-an-unproven-math-problem-in-geometry/>
- Tao on AI in math: <https://academy.openai.com/en/public/blogs/terence-tao-ai-is-ready-for-primetime-in-math-and-theoretical-physics-2026-03-06>
- Manifold prediction market: <https://manifold.markets/BrincinTime/will-the-collatz-conjecture-3x1-pro>
- Premio 120M JPY: <https://mathprize.net/posts/collatz-conjecture/>
- Collatz Conjecture Challenge: <https://ccchallenge.org/>
- OEIS A058047: <https://oeis.org/A058047>
