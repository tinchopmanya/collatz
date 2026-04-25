# Decision final M15 - cierre de `q mod 8` marginal

Fecha: 2026-04-25
Milestone: M15
Entradas principales:

- `colaboradores/codex-hijo/ResultadosM15QMod8Transition.md`
- `colaboradores/codex-hijo/ReplicaM15QMod8Transition.md`

Commits integrados:

- `d8de743` - CodexHijo1, transicion `q mod 8`
- `5b8cb4f` - CodexHijo2, replica independiente

## Preguntas antes de decidir

- Estamos en algo potencialmente virgen?
  - No en la algebra local. La pregunta de memoria marginal `q mod 8` era una ablation interna, no un claim teorico nuevo.
- Alguien ya hizo esto?
  - La literatura cubre el marco 2-adico general. No encontramos esta ablation exacta, pero el resultado final es coherente con la expectativa de mezcla 2-adica.
- Que seria realmente nuevo si salia bien?
  - Que `q mod 8` conservara memoria suficiente entre bloques para afectar supervivencia orbital.
- Que resultado destruye la hipotesis?
  - Una matriz de transicion casi uniforme y replica exacta. Eso ocurrio.
- Que tan lejos estamos de algo publicable?
  - Esta linea no esta cerca de publicacion. Si se usa, es como ejemplo interno de descarte disciplinado.
- Hay evidencia independiente?
  - Si. CodexHijo2 replico exactamente con implementacion directa de la formula, sin importar `collatz.alternating_block`.

## Resultado replicado

Matriz `q_{i+1} mod 8 | q_i mod 8`, filas `q_i`, columnas `q_{i+1}`:

| desde \ hacia | 1 | 3 | 5 | 7 |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0.250005999914 | 0.249999600006 | 0.249986800190 | 0.250007599891 |
| 3 | 0.250027999910 | 0.250032799895 | 0.249996000013 | 0.249943200182 |
| 5 | 0.249996799980 | 0.249998399990 | 0.250001600010 | 0.250003200020 |
| 7 | 0.250000000000 | 0.249998399980 | 0.249993599918 | 0.250008000102 |

Medidas replicadas:

- max TV contra uniforme en 1 paso: `0.000060799805`;
- max TV contra uniforme en 2 pasos: `0.000015002180`;
- max TV contra uniforme en 3 pasos: `0.000015000447`;
- diferencia maxima de conteos entre CodexHijo1 y CodexHijo2: `0`;
- diferencia maxima de probabilidad: `0.000000000000`.

## Decision

Cerrar/enfriar M15 en la forma:

```text
q mod 8 como estado marginal de memoria suficiente para supervivencia orbital
```

No se usa holdout fresco para esta H1.
No se sube automaticamente a `q mod 16`.
No se presenta como resultado teorico.

La razon:

```text
q mod 8 predice next_tail localmente, pero el estado q mod 8 se remezcla casi uniformemente entre bloques consecutivos.
```

Por lo tanto, la ventaja local no muestra una via clara para propagarse a `blocks_to_descend`, stopping time o supervivencia orbital en esta formulacion marginal.

## Que aprendimos

- La compuerta multiagente funciono: web, critica, ejecucion y replica evitaron un holdout innecesario.
- La senal local era algebra real, pero dinamicamente irrelevante como memoria marginal.
- El criterio "antes de gastar holdout, medir memoria del estado" queda validado como practica.

## Que no concluimos

- No probamos ni refutamos Collatz.
- No demostramos que todos los modelos modulares sean inutiles.
- No descartamos `q mod 16`, `q mod 32` o estados mas ricos; simplemente no hay permiso epistemico para abrirlos sin una razon teorica nueva.
- No miramos el holdout fresco `15000001..25000000`.
- No negamos que `q mod 8` prediga `next_tail`; lo predice, pero eso ya era algebra local.

## Preguntas despues

- Avanzamos o solo confirmamos algo conocido?
  - Avanzamos metodologicamente y descartamos una H1 antes de gastar holdout. Cientificamente, la pista quedo cerrada como marginal.
- La hipotesis quedo mas fuerte, mas debil o descartada?
  - Descartada/enfriada en su formulacion actual.
- Hay riesgo post-hoc?
  - Bajo para esta conclusion, porque la compuerta y criterio fueron definidos antes de la replica.
- Hay explicacion algebraica trivial?
  - Si para `next_tail`; la mezcla observada tambien parece coherente con mezcla 2-adica esperada.
- Hay replica independiente?
  - Si, exacta.
- Que toca ahora?
  - No lanzar mas hijos sobre M15 marginal. El orquestador debe elegir una nueva pregunta M16 con filtro web/critico antes de ejecucion.
