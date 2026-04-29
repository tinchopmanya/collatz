# Decision - M24 desbloquea C3 minimo

Fecha: 2026-04-29

## Preguntas antes de decidir

- Estamos avanzando? Si. La brecha semantica estrecha de M22-C2 fue auditada contra el paper y el repo oficial.
- Estamos en terreno virgen? Parcialmente. La equivalencia `tf* -> *` con `n = 8x + 5` viene del paper; lo novedoso tentativo sigue siendo usarla para un benchmark guarded residual con certificados low-bit.
- Ya alguien lo vio? El caso dinamico de `S` si: Yolcu-Aaronson-Heule. No encontramos aun la combinacion con complemento low-bit `U_16`.
- Que tan lejos estamos? Lejos de Collatz; mas cerca de un benchmark tecnico publicable, pero todavia falta construir y comparar C3.
- Que puede destruirlo ahora? Que el SRS guardado cambie el problema, infle CNF o no mejore frente a S2 base.

## Evidencia M24

M24-SRS-SemanticAudit prueba localmente:

```text
f(x) = 2x
t(x) = 2x + 1
*(x) = 2x + 1
tf* = *(f(t(x))) = 8x + 5
```

Con el mapa ASCII local:

```text
a=f, b=t, d=*
bad -> d = tf* -> *
```

Por tanto, activar `bad -> d` en la rama dinamica operacional de `S` corresponde al caso `n % 8 == 5`.

M24-MicroGuardDesign prepara una microguarda finita:

```text
r mod 2^13 = 8189
accepted_count = 8
certified_overlap_count = 0
accepted residues subset U_16
```

## Decision

```text
C3 minimo queda permitido como experimento confirmatorio acotado,
pero no como claim de terminacion global.
```

El primer C3 no debe intentar todo `U_16` de 378 residuos. Debe empezar por la microfamilia `r mod 2^13 = 8189`, porque:

- es exacta dentro del complemento congelado;
- acepta solo 8 residuos;
- no intersecta certificados;
- minimiza el riesgo de inflar CNF antes de aprender.

## Condiciones para C3 minimo

- Generar un artefacto guardado o benchmark textual con checker de implicacion.
- Comparar contra S2 base con parametros preregistrados.
- Medir al menos reglas/estados/variables/clausulas/tiempo si hay frontend SAT.
- Si aparece `YES`, exigir CPF/CeTA antes de claim fuerte.
- Si se infla el problema sin mejora objetiva, cerrar la via guarded en microfamilia.

## Preguntas despues de decidir

- Posibilidad cientifica fuerte alta? Sube a media-alta para benchmark tecnico; sigue baja para prueba de Collatz.
- Terreno virgen? La microfamilia guarded con low-bit certificates parece no encontrada en M23, pero debe presentarse como novedad tentativa.
- Siguiente paso concreto: M25-C3-minimo sobre microguard `8189`, sin Matchbox/AProVE hasta tener artefacto y checker.
