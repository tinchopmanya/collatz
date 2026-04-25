# Resumen de investigacion sobre Collatz - Tercera Ola

Fecha de cierre: 2026-04-23 06:45:00 -03:00
Investigacion completa: [InvestigacionSobreCollatzTerceraOla.md](InvestigacionSobreCollatzTerceraOla.md)
Conclusion dinamica: [Conlusion.md](Conlusion.md)

## Resumen fuerte corto (~300 palabras)

La tercera ola mapeo quien esta atacando Collatz en abril 2026 y con que recursos. Axiom Math ($264M, 30+ personas, valuacion $1.6B) lidera el frente AI+Lean con transformers que predicen Collatz al 99.8%. DeepMind (AlphaProof, oro en IMO 2025), OpenAI (GPT-5.2 resolvio un Erdos) y Anthropic (Opus 4.6 resolvio un Knuth y 10/12 Putnam) tienen capacidad pero no atacan Collatz directamente. Edward Chang (Stanford) publico en marzo 2026 dos papers con colaboracion humano-LLM que reducen la conjetura a un problema de orbit mixing mod 32. Columbia publico un modelo bayesiano de stopping times. La formalizacion de Janik en Lean 4 (12,947 lineas, hecha con Opus 4.6) reduce Collatz a confinamiento Diofantino.

Se identificaron 5 huecos genuinos donde nadie esta trabajando: (1) explicar POR QUE los primos 3, 7, 19, 53 son anomalos — el paper de 2025 solo identifica el fenomeno sin explicarlo; (2) analisis multifractal formal de la serie de stopping times tau(n) — solo hay una conjetura visual, nadie aplico MF-DFA; (3) interpretabilidad mecanica del transformer de Collatz — Axiom trato su modelo como caja negra; (4) conectar la anomalia de primos con el framework burst-gap de Chang (marzo 2026) — nadie lo hizo; (5) correlaciones de largo alcance en vectores de paridad a escala masiva.

La propuesta es un laboratorio computacional en 5 fases (6 semanas): construir herramientas, atacar los primos anomalos, hacer analisis multifractal, conectar con burst-gap, y documentar/publicar. No compite con los equipos grandes (que buscan la prueba), sino que explora patrones en huecos que nadie cubre. Cada hallazgo es publicable independientemente.

## Resumen fuerte ampliado (~1000 palabras)

La tercera ola de investigacion tuvo un objetivo distinto a las anteriores: no estudiar el problema en si, sino mapear el ecosistema de quienes lo atacan en abril 2026 para determinar donde hay espacio para contribuir de forma original.

El panorama es drasticamente distinto al de un ano atras. Los modelos de AI alcanzan ahora capacidades matematicas de elite: Claude Opus 4.6 resolvio un problema abierto de Donald Knuth en una hora y 10 de 12 problemas Putnam; GPT-5.2 resolvio el Problema #397 de Erdos con prueba verificada en Lean; AlphaProof de DeepMind alcanzo nivel de oro en la IMO 2025. En total, mas de una docena de problemas abiertos fueron marcados como "resueltos" con AI en los creditos desde fines de 2025.

En Collatz especificamente, el jugador mas grande es Axiom Math, fundada por Carina Hong (24 anos, ex Stanford), con $264M de financiamiento total y una valuacion de $1.6B+. Su equipo de 30+ personas incluye investigadores de Meta FAIR, Google Brain, y al matematico Ken Ono. Demostraron que un transformer pequeno puede aprender la logica de control del algoritmo de Collatz con 99.8% de precision para numeros del orden de trillones. Su paper de noviembre 2025 ("Transformers know more than they can tell") mostro que los errores del modelo son estructurados y predecibles, y que la longitud de los loops se puede deducir de la representacion binaria. Sin embargo, trataron al modelo como caja negra conductual, sin aplicar interpretabilidad mecanica.

Edward Chang (Stanford) publico dos papers en marzo 2026 trabajando con colaboracion humano-LLM. El primero introduce una descomposicion burst-gap de las trayectorias y encuentra que gaps y bursts siguen distribuciones geometricas. El segundo reduce la conjetura de Collatz a un problema de one-bit orbit mixing: si cada orbita visita dos clases de residuos mod 32 con balance suficiente, la conjetura es verdadera. Probo el Map Balance Theorem: a nivel del mapa, el balance es perfecto (difieren en exactamente 1); el residuo esta en el nivel orbital. Esto es lo mas reciente y lo mas estructuralmente limpio que existe.

Un equipo de Columbia (Bonacorsi y Bordoni) publico en marzo 2026 un modelo bayesiano jerarquico que predice stopping times usando solo log(n) y residuo mod 8. Sorprendentemente, este modelo simple supera a generadores mecanisticos mas elaborados, confirmando que la estructura modular de bajo orden es el driver principal de la heterogeneidad en tiempos de parada.

John Janik uso Claude Opus 4.6 durante dos semanas en febrero 2026 para construir una formalizacion de 12,947 lineas en Lean 4 que reduce la conjetura a un problema de confinamiento Diofantino en un toro bidimensional. Identifica tres fuerzas que confinan las trayectorias: atriccion de Hensel (2-adica), separacion de Baker (Arquimediana) y cota de Denjoy-Koksma (ergodica).

Despues de mapear todo esto, se identificaron cinco huecos genuinos. Primero, el paper AIJFR de 2025 descubrio que potencias de los primos 3, 7, 19, y 53 muestran distribuciones de stopping time tipo ley de potencias en vez de la gaussiana predicha por modelos estocasticos, y que mezclar estos primos amplifica el efecto de forma no aditiva. Pero nadie explico POR QUE esos primos especificos. No se conecto con ninguna propiedad algebraica (orden multiplicativo, residuos, secuencias conocidas en OEIS). Este hueco es atacable computacionalmente: basta computar stopping times para potencias de todos los primos hasta un limite, clasificarlos, y buscar la propiedad algebraica que separa anomalos de normales.

Segundo, la conjetura de autoafinidad fractal de Ralf Becker sobre el rolling average de stopping times nunca fue testeada formalmente. El paper IOPscience de 2024 hizo DFA sobre orbitas individuales pero no sobre la funcion tau(n). Nadie aplico MF-DFA a la serie de stopping times para determinar si es monofractal o genuinamente multifractal, ni calculo el exponente de Hurst de tau(n).

Tercero, nadie hizo interpretabilidad mecanica del transformer de Collatz. Los modelos existen y funcionan al 99.7%, pero fueron tratados como cajas negras. Abrir las capas de atencion con herramientas como TransformerLens podria revelar que "algoritmo" descubrio el modelo internamente.

Cuarto, los dos hallazgos mas interesantes de los ultimos 12 meses (primos anomalos y framework burst-gap) no fueron conectados. Verificar si los primos anomalos generan distribuciones anomalas de bursts o gaps, o si la conjetura de equidistribucion orbital de Chang falla para estos numeros, es una pregunta obvia que nadie hizo.

Quinto, las correlaciones de largo alcance en vectores de paridad no fueron analizadas sistematicamente a escala masiva. Se sabe que hay persistencia (beta > 1) pero no se buscaron patrones prohibidos ni se cuantifico la informacion mutua entre pasos distantes.

La propuesta concreta es un laboratorio computacional en cinco fases a lo largo de seis semanas: construir herramientas core, atacar los primos anomalos, hacer analisis multifractal formal, conectar con el framework burst-gap de Chang, y documentar hallazgos para posible publicacion. Esta propuesta no compite con los equipos grandes (que buscan la prueba) sino que explora patrones en nichos que nadie esta cubriendo. Cada hallazgo, positivo o negativo, es publicable de forma independiente.
