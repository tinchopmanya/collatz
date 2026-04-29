# Decision - M19 queda instrumental, M22 pasa a linea principal

Fecha: 2026-04-29

## Preguntas antes de decidir

- Estamos avanzando? Si: M19 produjo gates, evidencia CI y una frontera clara de tooling; M22 produjo un complemento residual concreto.
- Estamos en terreno virgen? No en rewriting ni en low-bit/descent por separado. Parcialmente si en el puente reproducible entre ambos.
- Ya alguien lo hizo? Las piezas si: Yolcu-Aaronson-Heule, Barina, Angeltveit, TermComp/AProVE/Matchbox/CeTA. No encontramos aun una campana publica que combine certificados low-bit con familias residuales guarded rewriting S1/S2.
- Que tan lejos estamos? Lejos de Collatz; moderadamente cerca de un benchmark/reduccion publicable si M22-C1/C2 pasan.
- Que puede destruir la via? Un falso positivo low-bit, una brecha semantica en el puente S2, o que los residuos restantes no sean mas faciles para provers.

## Evidencia que fuerza la decision

M19 reconstruyo mucha infraestructura, pero no entrego todavia un binario Matchbox real:

- `m19_matchbox_artifact_gate.py` exige `sha256`, `ldd` y `--help`.
- `m19_certificate_gate.py` exige `YES` top-level, CPF separado y CeTA `CERTIFIED`.
- Los runs GitHub `success` no bastan: varios fallaron internamente por dependencias.
- La frontera actual de build fuente es `satchmo-2.9.9.3`, `Satchmo/Polynomial.hs:143`, por `MonadFail`.
- La matriz de decision recomienda como maximo un parche mas; dos o mas ya serian arqueologia de ecosistema.

M22, en cambio, tiene un objeto cientifico concreto:

- S2-k16: `8192` clases de rama.
- Low-bit/descent descarga `7814`.
- Complemento congelado: `378`.
- SHA del complemento: `bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210`.

## Decision

```text
M19 queda como linea instrumental.
M22 pasa a ser linea principal.
```

M19 solo continua si ocurre una de estas dos cosas:

- aparece un binario/container Matchbox reproducible que pase el gate;
- se autoriza un ultimo parche acotado de `satchmo`, con muerte inmediata si aparece otro bloqueo legacy.

M22 continua solo con los criterios de `M22KillCriteria.md`:

- M22-C1: rechecker independiente S2-k16;
- M22-C2: validador semantico del puente S2;
- M22-C3: benchmark guarded S2-k16 contra S2 base, solo si C1 y C2 pasan.

## Preguntas despues de decidir

- Estamos avanzando? Si, porque dejamos de empujar una via de bajo ceiling y concentramos energia en una hipotesis falsable.
- Terreno virgen? Parcialmente. La combinacion exacta sigue sin aparecer en la busqueda web, pero hay que tratarla como novedad tentativa hasta que CodexInvestigador cierre M23.
- Posibilidad cientifica fuerte alta? Media-alta si C1/C2 pasan y C3 consigue `YES` o reduccion robusta; baja si C1/C2 no pasan.
- Siguiente accion: esperar C1/C2 y no correr C3 antes de cerrar la brecha semantica.
