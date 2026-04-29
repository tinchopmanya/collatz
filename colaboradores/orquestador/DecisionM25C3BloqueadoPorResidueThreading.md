# Decision - C3 minimo queda bloqueado por residue-state threading

Fecha: 2026-04-29

## Preguntas antes de decidir

- Estamos avanzando? Si. M25 produjo preregistro, checker de implicacion y un bloqueo preciso.
- Estamos en terreno virgen? Parcialmente. El bloqueo aparece al intentar convertir certificados low-bit en un SRS guardado semanticamente honesto.
- Ya alguien lo hizo? M23 no encontro una combinacion publica equivalente, pero esto sigue siendo novedad tentativa.
- Que tan lejos estamos? Lejos de una prueba de Collatz; cerca de un subproblema tecnico claro.
- Que destruye la via? No poder propagar estado de residuo por reglas auxiliares sin cambiar el problema o inflar el SRS.

## Resultado M25

M25-C3-Preregistration quedo integrado antes de cualquier prover. Define:

- hipotesis exacta `M25-C3-minimo-r8189-v1`;
- inputs y hashes congelados;
- metricas permitidas;
- criterios de exito/abandono;
- reglas anti p-hacking.

M25-C3-MinimalGuardedBenchmark produjo un checker que pasa:

```text
G_8189 = U_16 intersection {r | r mod 2^13 = 8189}
G_8189 intersection C_16 = empty
forall r in G_8189: r mod 8 = 5
bad -> d = tf* -> *
tf* -> * = n mod 8 = 5
```

Pero el artefacto marca:

```text
c3_build_status = blocked
c3_blocked_reason = guarded_srs_semantics_missing
```

## Decision

No se corre Matchbox, AProVE ni ningun prover sobre C3 todavia.

El siguiente milestone no es "correr C3", sino:

```text
M26 - residue-state threading through auxiliary rules
```

Objetivo de M26:

- especificar como se transporta un residuo modulo `2^13` o `2^16` a traves de las reglas auxiliares `X`;
- fijar orientacion de bits;
- probar que la guarda insertada en `bad -> d` conserva exactamente un subproblema de S2;
- medir si el producto de estados/reglas no explota antes de cualquier prover.

## Preguntas despues de decidir

- Estamos avanzando? Si, porque ahora sabemos la pieza faltante exacta.
- Posibilidad cientifica fuerte alta? Media: sube si M26 logra un checker de threading pequeno; baja si el producto de estados explota.
- Terreno virgen? M26 parece el punto mas original hasta ahora, pero tambien el mas riesgoso.
- Siguiente paso: disenar M26 con un prototipo de transductor/automata de residuos para las reglas auxiliares, sin prover.
