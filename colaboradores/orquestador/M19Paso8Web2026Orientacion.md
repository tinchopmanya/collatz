# M19 paso 8 - orientacion web 2026 ampliada

Fecha: 2026-04-27
Responsable: Codex orquestador
Estado: investigacion web ampliada; decision de foco actualizada

## Preguntas antes

- Estamos en terreno virgen?
  - No en Collatz general, verificacion computacional, sistemas de reescritura, ni codificaciones equivalentes.
- Podemos descubrir algo relevante?
  - Si, pero solo si encontramos una prueba/certificado nuevo para un desafio concreto como S1/S2, o si conectamos dos codificaciones publicadas de una forma no explotada.
- Ya alguien estuvo buscando esto?
  - Si. Barina, Angeltveit, Yolcu-Aaronson-Heule, AProVE/TermComp y trabajos recientes de codificacion tipo Knight.
- Que tan lejos estamos?
  - Lejos de una prueba de Collatz; cerca de producir resultados negativos/positivos reproducibles sobre herramientas modernas aplicadas a desafios especificos.

## Fuentes nuevas revisadas

### Estado computacional 2026

- Barina mantiene pagina viva de verificacion; el sitio fue generado el 2026-04-27 y reporta la marca publicada `2^71` de 2025.
- Angeltveit 2026 propone un algoritmo mejorado para verificar Collatz para todo `n < 2^N`, no una prueba general.

Lectura:

```text
La frontera publica fuerte en 2026 sigue siendo verificacion y aceleracion,
no demostracion teorica completa.
```

### Rewriting/terminacion

- Yolcu-Aaronson-Heule sigue siendo la via mas directamente conectada con nuestro repo.
- AProVE tiene release publico `master_2026_02_15`.
- Termination Competition 2025 confirma que la comunidad de herramientas de terminacion sigue activa.
- Matchbox es publico y relevante, pero su instalacion local es mas pesada que AProVE.

Lectura:

```text
La mejor apuesta de alto techo sigue siendo atacar S1/S2 con herramientas
modernas y dejar trazas reproducibles.
```

### Kevin Knight 2026

Paper:

- `A Small Collatz Rule without the Plus One`, Complex Systems 35(1), 2026.

Resumen:

- Construye una regla multiplicativa de 30 condiciones que simula Collatz sin el `+1`.
- Reduce dramaticamente una codificacion previa de Monks con 1,021,020 condiciones.
- No prueba Collatz; transforma el problema a otra dinamica/codificacion.

Lectura:

```text
No es una solucion, pero puede ser util como codificacion alternativa para
generar instancias de terminacion o comparar con reescritura.
```

## Decision

No conviene abandonar M19 por claims generales 2026. La decision fuerte es:

```text
seguir con S1/S2 como frontera principal, y abrir una sublinea M20 solo si
la codificacion de Knight puede traducirse a un problema de terminacion
mas pequeno o mas amigable para AProVE/Matchbox que el sistema S.
```

## Tareas siguientes

1. Ejecutar AProVE en GitHub Actions con `S1` y `S2`.
2. Si AProVE no da `YES`, preparar Matchbox como segunda herramienta.
3. Leer Knight con lupa y decidir si su regla de 30 condiciones genera un TRS/SRS comparable.
4. No perseguir claims no auditados salvo que tengan codigo, formalizacion o revision externa fuerte.

## Preguntas despues

- Avanzamos?
  - Si. Ya tenemos una orientacion 2026 mas amplia y una razon clara para no dispersarnos.
- Estamos en algo virgen?
  - No en la idea general. La posible zona virgen es la combinacion concreta: S1/S2 + herramientas 2026 + certificados reproducibles; o traduccion Knight -> terminacion automatica.
- Hay posibilidad cientifica fuerte alta?
  - Alta solo condicionalmente: si aparece un `YES` certificado para S1/S2 o una traduccion nueva mas facil de certificar. Sin eso, la probabilidad de breakthrough sigue baja.
- Que destruye la via?
  - Que AProVE/Matchbox/CeTA no produzcan certificados y que Knight no reduzca la dificultad de terminacion.
- Que toca ahora?
  - Correr CI y preparar Matchbox/Yices1-compatible si AProVE queda bloqueado.

## Fuentes

- https://pcbarina.fit.vutbr.cz/
- https://arxiv.org/abs/2602.10466
- https://link.springer.com/article/10.1007/s10817-022-09658-8
- https://arxiv.org/abs/2105.14697
- https://github.com/aprove-developers/aprove-releases
- https://termcomp.github.io/Y2025/
- https://github.com/jwaldmann/matchbox
- https://doi.org/10.25088/ComplexSystems.35.1.1
