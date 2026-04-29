# Decision - M22 despues de C1, C2 y M23

Fecha: 2026-04-29

## Preguntas antes de la decision

- Estamos avanzando? Si. C1 cerro la circularidad principal del conjunto S2-k16; C2 valido la guarda finita; M23 sostuvo la novedad tentativa por busqueda externa.
- Estamos en terreno virgen? Parcialmente. Rewriting y low-bit/descent estan recorridos; no encontramos la combinacion exacta low-bit/descent + familias residuales guarded rewriting.
- Ya alguien lo vio? Las piezas si. La integracion exacta no fue encontrada hasta el corte M23.
- Que tan lejos estamos? Lejos de Collatz. Cerca de un benchmark tecnico publicable solo si se cierra la brecha semantica SRS -> residuo.
- Que puede destruirlo? Que `bad -> d` / `tf* -> *` no derive operacionalmente de `r mod 8 = 5`, o que esa equivalencia sea solo una etiqueta local.

## Evidencia nueva

M22-C1 paso:

- `branch_residue_count = 8192`
- `lowbit_certified_count = 7814`
- `uncovered_count = 378`
- hashes esperado para certificados y complemento;
- `false_positives = 0`;
- `affine_failures = 0`;
- `audit_sampled_numbers = 576`;
- `max_lift_seen = 255`.

M22-C2 paso como guarda computacional:

- `65536` residuos evaluados;
- `8192` residuos S2 por `r mod 8 = 5`;
- `378` residuos aceptados por la guarda;
- `0` residuos fuera de S2 aceptados;
- `0` certificados enviados al guardado.

Pero M22-C2 no cerro la semantica fuerte:

```text
semantic_translation_status = gap_unproven
```

M23 no encontro una fuente publica que combine explicitamente:

```text
certificados low-bit/descent modulo 2^k
  + descarga de familias residuales
  + SRS/TRS guarded para ramas residuales de Yolcu-Aaronson-Heule
  + CPF/CeTA
```

## Decision

```text
M22 sigue vivo, pero C3 queda bloqueado como experimento confirmatorio.
```

Se permite trabajo exploratorio de diseno de microguardas, pero ningun resultado se puede presentar como benchmark semantico hasta resolver M24:

```text
M24 - Auditoria semantica SRS: derivar/refutar/no decidir si `bad -> d` / `tf* -> *`
corresponde operacionalmente a `r mod 8 = 5`.
```

## Proxima accion

- M24-SRS-SemanticAudit: leer reglas oficiales y derivar la relacion SRS -> residuo si existe.
- M24-MicroGuardDesign: preparar un artefacto minimo de guarda exacta solo como diseno exploratorio, bloqueado por M24 semantico.

## Preguntas despues de la decision

- Estamos avanzando? Si: dejamos una frontera exacta, no una nebulosa.
- Posibilidad cientifica fuerte alta? Media, no alta, hasta cerrar la brecha SRS.
- Si M24 prueba la equivalencia? Pasar a C3 preregistrado.
- Si M24 no la prueba? M22 queda como benchmark aritmetico exploratorio, no como contribucion fuerte de rewriting.
