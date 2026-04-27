# M19 paso 3 - mapa de frontera rewriting/SAT

Fecha: 2026-04-27
Responsable: Codex orquestador
Estado: investigacion web ampliada

## Preguntas antes

- Estamos en terreno virgen?
  - No en la idea general: Collatz como terminacion de rewriting/SAT ya existe.
- Podemos descubrir algo con esto?
  - Si, pero solo si atacamos un borde no cerrado: un desafio explicito del paper, certificacion, reproduccion moderna o extension nueva.
- Ya alguien estuvo buscando esto?
  - Si. Yolcu-Aaronson-Heule, autores de herramientas de terminacion, AProVE/Matchbox, y la comunidad de Termination Competition.
- Que tan lejos estamos de algo importante?
  - Lejos de probar Collatz. Mas cerca de una contribucion tecnica si reproducimos y luego atacamos un subproblema abierto.

## Fuentes verificadas

### Paper principal

- Journal of Automated Reasoning: https://link.springer.com/article/10.1007/s10817-022-09658-8
- arXiv: https://arxiv.org/abs/2105.14697
- Version CADE 2021: https://link.springer.com/chapter/10.1007/978-3-030-79876-5_27
- PDF de autores: https://www.cs.cmu.edu/~mheule/publications/collatz.pdf

Hechos relevantes:

- publicado en Journal of Automated Reasoning el 2023-04-25;
- arXiv v1 del 2021-05-31, v3 del 2022-12-31;
- prueba que la terminacion de cierto sistema de rewriting equivale a Collatz;
- encuentra pruebas automaticas de debilitamientos no triviales;
- no prueba Collatz.

### Codigo oficial

- Repo: https://github.com/emreyolcu/rewriting-collatz
- Commit auditado localmente: `8a4dfda60f97a6d33ff0a24fdfa7a172d4bec340`

El README declara:

- prover minimo con interpretaciones natural/arctic/tropical;
- sistemas de rewriting que simulan funciones tipo Collatz;
- scripts para reproducir las pruebas del paper;
- dependencias: Python, NumPy, CaDiCaL.

Auditoria local:

- `proofs.sh` declara 24 corridas;
- `proofs/` contiene 24 logs;
- todos los logs contienen `SAT` y `QED`;
- el repo no trae una bateria completa de archivos `S1/S2` como tareas separadas listas para correr.

### Ecosistema de terminacion 2025-2026

- Termination Competition: https://termination-portal.org/wiki/Termination_Competition
- Resultados 2025: https://termcomp.github.io/Y2025/
- WST 2025 accepted papers: https://www.imn.htwk-leipzig.de/~waldmann/WST2025/accepted/

Hechos relevantes:

- la categoria SRS Relative existe en Termination Competition;
- desde 2007 hay categorias certificadas;
- en 2025 hay actividad fuerte en AProVE, relative termination, CeTA/Cetera y matrix interpretations;
- AProVE anuncio apertura como open source hacia fines de 2025;
- Cetera trabaja en certificados de terminacion de string rewriting con Agda;
- core matrix interpretations se integran con CeTA.

Conclusion:

```text
La linea no esta muerta. El aporte posible no es inventarla, sino conectar Collatz-rewriting con herramientas/certificacion modernas.
```

## Fronteras detectadas

### Frontera A - Reproducibilidad fuerte

Pregunta:

```text
Podemos regenerar desde cero los logs del paper en Linux/CI, con commits pinneados y artifact auditable?
```

Estado:

- no es matematicamente nuevo;
- si falla, descubre deuda de reproducibilidad;
- si funciona, habilita experimentos serios.

Valor:

- novedad cientifica: baja;
- valor de infraestructura: medio;
- riesgo: bajo.

### Frontera B - Subproblemas S1/S2

El paper define una funcion acelerada `S` equivalente a Collatz en convergencia. Para dos subsistemas de `S`, los autores reportan que no encontraron interpretaciones pese a miles de CPU-horas.

Desafios:

```text
S1 = S \ {ff* -> 0*}
S2 = S \ {tf* -> *}
```

En ASCII del repo local, las reglas dinamicas de `S` aparecen como:

```text
aad -> ed
bad -> d
bd  -> gd
```

Donde las dos reglas abiertas corresponden plausiblemente a remover:

```text
aad -> ed
bad -> d
```

Esto debe verificarse contra la notacion exacta del paper antes de correr busquedas.

Valor:

- terreno virgen parcial: si, si no hay prueba posterior;
- posibilidad fuerte: media-baja;
- dificultad: alta, porque los autores ya gastaron miles de CPU-horas;
- aporte publicable: posible si aparece una prueba certificable o una razon estructural de dificultad.

### Frontera C - Conjeturas modulo 8

El paper prueba que una trayectoria no convergente no puede evitar las clases:

```text
2, 3, 4, 6 mod 8
```

Permanece abierto en el texto si debe encontrar:

```text
0, 1, 5, 7 mod 8
```

El caso 0 seguiria del caso 5 segun el paper. Las conjeturas explicitas mas interesantes son:

```text
4.11: toda trayectoria no convergente contiene algun n = 1 mod 8.
4.12: toda trayectoria no convergente contiene algun n = 5 mod 8.
4.13: toda trayectoria no convergente contiene algun n = 7 mod 8.
4.14: toda trayectoria no convergente contiene algun n = 5 mod 8 o n = 7 mod 8.
```

El paper indica una recompensa de USD 500 por resolver una de estas conjeturas.

Valor:

- terreno virgen parcial: si, como subproblema explicito;
- posibilidad fuerte: media-baja;
- ventaja nuestra: ya tenemos infraestructura de residuos y modulo 8 de M15;
- riesgo: alto, porque podria necesitar teoria nueva, no solo computo.

### Frontera D - Certificacion moderna

Pregunta:

```text
Podemos convertir una prueba del repo rewriting-collatz a un formato verificable por CeTA/Cetera/Agda/Isabelle?
```

Razon:

- el paper usa logs/prover, pero una prueba certificada por herramienta moderna tendria mas valor de auditoria;
- WST 2025 muestra actividad nueva en certificacion de matrix interpretations y relative termination.

Valor:

- novedad matematica: baja-media;
- valor cientifico: medio;
- probabilidad realista: mejor que intentar probar Collatz directamente.

### Frontera E - Herramientas modernas

Pregunta:

```text
Puede AProVE/Matchbox/TermComp 2025 resolver algun subproblema que el prover minimo no resolvio?
```

Razon:

- AProVE reporta mejoras en relative termination;
- Matchbox/CeTA/Cetera evolucionaron;
- los desafios S1/S2 son exactamente del tipo donde una herramienta moderna podria aportar.

Valor:

- terreno virgen: parcial;
- posibilidad fuerte: media si se logra reproducir y comparar;
- condicion: necesitamos preparar archivos en formato TPDB y correr herramientas reales.

## Evaluacion comparativa

| Ruta | Novedad | Probabilidad | Valor si sale | Siguiente accion |
| --- | ---: | ---: | ---: | --- |
| Reproducir logs oficiales | 1 | 4 | 2 | Ejecutar CI manual |
| Comparar logs reproducidos vs oficiales | 2 | 4 | 2 | Diff semantico |
| Generar S1/S2 TPDB | 2 | 3 | 3 | Derivar archivos exactos |
| Buscar prueba S1/S2 con herramientas modernas | 3 | 1-2 | 4 | Requiere solver/tooling |
| Atacar Conj. 4.14 modulo 8 | 3 | 1-2 | 4 | Formalizar partial Collatz H |
| Certificar prueba existente | 3 | 2-3 | 3-4 | Investigar CeTA/Cetera |
| Probar Collatz completo | 5 | 0-1 | 5 | No atacar directamente |

## Decision del orquestador

No conviene saltar ya a busqueda abierta S1/S2.

La secuencia correcta es:

1. Ejecutar el workflow M19 de reproduccion `zantema`.
2. Si pasa, extender workflow a las 24 pruebas oficiales.
3. Crear un generador local de archivos `S1/S2` y de conjeturas modulo 8 en formato TPDB.
4. Probar primero herramientas existentes, no inventar solver propio.
5. Solo si una herramienta encuentra algo, pasar a certificacion.

## Preguntas despues

- Estamos en algo virgen?
  - No en la linea general. Si en subproblemas concretos: S1/S2, Conj. 4.14, certificacion moderna.
- Podemos descubrir algo relevante?
  - Si, pero el primer resultado relevante seria tecnico: reproducibilidad + conversion/certificacion. Un resultado matematico seria mucho mas dificil.
- Ya alguien estuvo buscando esto?
  - Si. Los autores y la comunidad de terminacion. De hecho, S1/S2 ya resistieron miles de CPU-horas.
- Que tan lejos estamos?
  - A una ejecucion CI de reproducir baseline. A varias iteraciones de poder atacar una frontera real.
- Que haria ahora?
  - Ejecutar CI manual. Si funciona, automatizar las 24 pruebas y preparar S1/S2 exactos.
