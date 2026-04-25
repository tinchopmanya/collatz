# Auditoria de fuentes Collatz

Fecha: 2026-04-25
Milestone: M0 - Higiene y auditoria
Estado: primera pasada

## Criterios

- `Alta`: paper revisado por pares, libro/encuesta reconocida, fuente oficial o proyecto tecnico verificable.
- `Media`: arXiv serio, preprint con afirmaciones acotadas, pagina tecnica con datos reproducibles.
- `Baja`: nota periodistica, blog, ResearchGate sin version primaria clara, claims de empresa sin verificacion externa.
- `Pendiente`: claim registrado pero todavia no auditado.

## Claims de base matematica

| Claim | Fuente | Confianza | Nota |
| --- | --- | --- | --- |
| La conjetura de Collatz sigue abierta. | Lagarias, Tao, Barina, Wikipedia como referencia secundaria | Alta | No hay prueba general aceptada ni contraejemplo conocido. |
| La verificacion computacional publicada llega hasta `2^71`. | David Barina, Journal of Supercomputing 2025 | Alta | Fuente revisada por pares: <https://link.springer.com/article/10.1007/s11227-025-07337-0>. |
| Tao probo que casi todas las orbitas alcanzan valores casi acotados en densidad logaritmica. | Terence Tao, Forum of Mathematics Pi 2022 | Alta | Fuente revisada por pares: <https://doi.org/10.1017/fmp.2022.8>. |
| Lagarias es una encuesta base para el problema `3x+1`. | Lagarias, arXiv 2111.02635 y obra AMS | Alta | Fuente: <https://arxiv.org/abs/2111.02635>. |
| No hay Collatz `m-cycles` con `m <= 91`. | Christian Hercher, JIS / arXiv | Alta | Fuente arXiv: <https://arxiv.org/abs/2201.00406>. |
| "Collatz high cycles do not exist" existe como resultado publicado en Discrete Mathematics 2026. | Kevin Knight, Discrete Mathematics | Media | Confirmado como publicacion, pendiente de lectura tecnica antes de usarlo fuerte. |
| El Collatz Conjecture Challenge formaliza o mapea literatura relevante. | ccchallenge.org | Media | Util como indice; cada entrada debe verificarse contra fuente primaria. |

## Claims computacionales y de IA

| Claim | Fuente | Confianza | Nota |
| --- | --- | --- | --- |
| Existe el preprint `Transformers know more than they can tell -- Learning the Collatz sequence` con resultados de 99.7% en algunas bases. | arXiv / ResearchGate indexado | Media | El resultado parece real, pero hay que leer la version primaria antes de incorporarlo. |
| Axiom Math levanto USD 64M seed en 2025 y trabaja en IA matematica. | Forbes 2025 y fuentes secundarias | Media | No es central para Collatz; sirve como contexto de ecosistema, no como base matematica. |
| Axiom Math levanto USD 264M totales y tiene valuacion de USD 1.6B. | Fuentes secundarias 2026 | Baja | Falta fuente primaria fuerte. No usar como claim central. |
| AxiomProver logro 12/12 en Putnam 2025. | TAMradar, Reddit, notas secundarias | Baja | Claim llamativo; requiere fuente oficial o verificacion independiente. |
| GPT-5.2 resolvio problemas de Erdos con validacion de Tao/Lean. | Notas de prensa, blogs, wiki de Tao mencionada en resultados | Baja | Relevante para IA matematica, no para Collatz. No usar sin fuente primaria. |
| Claude Opus 4.6 resolvio un problema de Knuth. | Blogs y notas secundarias | Baja | No usar como base para decisiones Collatz. |

## Claims de tercera ola que requieren cuidado

| Claim | Estado | Decision |
| --- | --- | --- |
| "En abril 2026, Collatz esta mas activo que nunca." | Retorico, no medido | Reescribir o respaldar con conteo bibliografico. |
| "Axiom Math invirtio USD 264M." | Fuente secundaria debil | Mantener fuera de conclusiones fuertes. |
| "Chang redujo la conjetura a orbit mixing mod 32." | Preprint arXiv encontrado | Tratar como media: interesante, no establecido. |
| "Janik formalizo 12,947 lineas en Lean 4." | Pendiente | Verificar repo y paper antes de usar. |
| "Cinco huecos genuinos donde nadie trabaja." | Demasiado fuerte | Cambiar a "cinco huecos candidatos detectados". |
| "No competimos con Axiom ni DeepMind." | Correcto como estrategia, no como evidencia | Puede mantenerse como criterio tactico. |

## Decisiones de auditoria

- Las olas 1 y 2 pueden servir como base inicial, con verificacion puntual.
- La ola 3 debe tratarse como mapa exploratorio, no como evidencia fuerte.
- El roadmap debe priorizar datos propios y fuentes matematicas primarias.
- Antes de citar cualquier claim de IA/startups, exigir fuente primaria o rebajarlo a contexto.

## Proxima accion M0

Revisar archivo por archivo:

- [InvestigacionSobreElProblemaDeCollatz.md](InvestigacionSobreElProblemaDeCollatz.md)
- [InvestigacionSobreCollatzSegundaOla.md](InvestigacionSobreCollatzSegundaOla.md)
- [InvestigacionSobreCollatzTerceraOla.md](InvestigacionSobreCollatzTerceraOla.md)

Objetivo de la siguiente pasada:

- marcar lineas concretas a corregir;
- actualizar `Conlusion.md` si alguna conclusion dependia de claims debiles;
- abrir M1 cuando la base este suficientemente limpia.
