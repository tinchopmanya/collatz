# Decision M15 tras CodexHijo1 transicion `q mod 8`

Fecha: 2026-04-25
Milestone: M15
Entrada principal: `colaboradores/codex-hijo/ResultadosM15QMod8Transition.md`
Commit integrado: `d8de743`

## Preguntas antes de decidir

- Estamos en algo potencialmente virgen?
  - No como matematica local. Esta iteracion pregunta si hay memoria modular marginal suficiente para que `q mod 8` afecte cadenas completas.
- Alguien ya hizo esto?
  - La literatura cubre el marco 2-adico general. No teniamos esta ablation interna exacta.
- Que seria nuevo si sale bien?
  - Una evidencia interna de memoria modular de baja dimension que justifique un modelo predictivo de supervivencia.
- Que resultado destruiria la hipotesis?
  - Una matriz `q_{i+1} mod 8 | q_i mod 8` casi uniforme y con mezcla rapida.
- Que tan lejos estamos de algo publicable?
  - Lejos. Este resultado sirve principalmente para decidir si gastar holdout o cerrar la pista.
- Esta decision necesita replica?
  - Si. Como el resultado enfria M15, debe replicarse antes de cierre definitivo.

## Resultado de CodexHijo1

Comando reproducible:

```powershell
python experiments\analyze_m15_qmod8_transition.py --limit 5000000 --out-dir reports --prefix m15_qmod8_transition
```

Poblacion:

- impares `3 <= n <= 5000000`;
- una transicion odd-to-odd por impar inicial;
- rango quemado/exploratorio, no holdout.

Matriz de transicion:

| desde \ hacia | 1 | 3 | 5 | 7 |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0.25000600 | 0.24999960 | 0.24998680 | 0.25000760 |
| 3 | 0.25002800 | 0.25003280 | 0.24999600 | 0.24994320 |
| 5 | 0.24999680 | 0.24999840 | 0.25000160 | 0.25000320 |
| 7 | 0.25000000 | 0.24999840 | 0.24999360 | 0.25000800 |

Medidas:

- max TV contra uniforme en 1 paso: `0.000060799805`;
- max TV contra uniforme en 2 pasos: `0.000015002180`;
- max TV contra uniforme en 3 pasos: `0.000015000447`;
- estacionaria max diff vs uniforme: `0.000009500401`.

## Decision preliminar

M15 queda enfriado en su forma marginal `q mod 8` como memoria de supervivencia.

La razon es que `q mod 8` si predice `next_tail`, pero el siguiente estado `q_{i+1} mod 8` se remezcla casi uniformemente. Eso impide, en esta formulacion marginal, que la ventaja local tenga memoria clara para propagarse a cadenas completas.

No cierro M15 todavia. Antes de cerrar:

- CodexHijo2 debe replicar/falsificar con implementacion independiente;
- si replica, M15 se cierra como descarte limpio o se reformula fuera de `q mod 8` marginal;
- si contradice, se revisan definiciones de `q`, bloque y poblacion.

## Estado de agentes

- CodexInvestigadorWeb: completado.
- ClaudeSocioCritico: completado.
- CodexHijo1: completado e integrado.
- CodexHijo2: desbloqueado para replica/falsacion.

## Preguntas despues

- Avanzamos o solo confirmamos algo conocido?
  - Avanzamos en descarte: evitamos gastar holdout en una H1 que parece remezclarse inmediatamente.
- La hipotesis quedo mas fuerte, mas debil o descartada?
  - Mucho mas debil. Preliminarmente enfriada.
- Hay riesgo post-hoc?
  - Bajo en esta compuerta: la matriz `q mod 8` fue preregistrada como gate.
- Hay explicacion algebraica trivial?
  - Probablemente si en el limite 2-adico, pero CodexHijo1 solo entrego evidencia empirica.
- Hay replica independiente?
  - Todavia no. Esa es la proxima tarea.
- Que toca ahora?
  - Lanzar CodexHijo2 con el Prompt 2 de `PromptsM15Ronda2.md`.
