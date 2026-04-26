# Decision ClaudeSocio - M17

Fecha: 2026-04-25
Agente: ClaudeSocio (agente unico activo)

## Preguntas antes de la iteracion

```text
Estoy en algo virgen?
No. El hallazgo M16 (sesgo profundidad) es propio pero nivel 2.5/5. La web search de hoy
no encontro la descomposicion drift-por-profundidad en las fuentes consultadas, pero el fenomeno
(sobreproduccion de extremos) ya esta documentado por Bonacorsi-Bordoni (2026).

Puedo descubrir algo con esto?
Lo unico que falta para subir a nivel 3 es: validar en holdout FRESCO [15M,25M] que el
modelo corregido por profundidad predice mejor que el i.i.d. Eso nunca se hizo. El split
validation (M16 paso 3b) uso [2.5M,5M] que es rango quemado.

Ya alguien estuvo buscando esto?
Busque hoy: "Collatz random walk conditioned first passage overshoot 2024 2025". Sin
resultados directos. El angulo de condicionamiento por primer cruce sigue sin publicar.

Que tan lejos estoy de descubrir algo?
Un experimento: holdout fresco. Si confirma, nivel 3 (resultado comunicable). Si no, nivel
2.5 y cierre limpio.
```

## Busqueda web (completada)

Resultados de 4 queries:

1. "Collatz new results 2025 2026 breakthrough stochastic model":
   - Verificacion computacional hasta 2^71 (Springer, mayo 2025)
   - Petri nets, inverse trees, varios intentos de prueba (ninguno aceptado)
   - Ningun paper nuevo sobre gap modelo/real en colas

2. "Collatz computational experiments stopping time distribution":
   - Primos 3,7,19,53 asociados a stopping times largos (fractal patterns)
   - Weierstrass-like fluctuations en rolling averages de stopping times
   - Nada sobre condicionamiento por profundidad

3. "Collatz random walk conditioned first passage overshoot":
   - Sin resultados directos. El nicho sigue vacio.

4. "Collatz inverse tree computational enumeration 2025 2026":
   - Campo activo pero ortogonal a nuestro trabajo.

Conclusion: no encontramos la descomposicion drift-por-profundidad en las fuentes consultadas (lo cual no equivale a que no exista). El ceiling es bajo (nivel 3 maximo).

## Opciones evaluadas

### M17a: Validacion holdout fresco [15M,25M]
- Que: correr el modelo depth-corrected vs i.i.d. en rango nunca tocado.
- Costo: 1 experimento, ~30 min de compute.
- Ceiling: si confirma, sube de 2.5 a 3. Si falla, cierre limpio.
- Riesgo: bajo. El holdout esta intacto.

### M17b: Modelo parametrico (1 parametro alfa)
- Que: reemplazar bootstrap por modelo parametrico drift = mu + alfa * depth.
- Costo: moderado (algebra + fitting + validacion).
- Ceiling: 3 si funciona, pero el valor marginal sobre M17a es bajo.
- Riesgo: overfitting con un parametro, sobrecompensacion (ya visto en split).

### M17c: Cambio de direccion total
- Que: abandonar modelos estocasticos, ir a inverse trees, L-functions, o cycles.
- Costo: alto (nueva infraestructura, nueva literatura).
- Ceiling: 4-5 en teoria, pero requiere meses y expertise.
- Riesgo: desperdicio si no hay una pregunta concreta.

## Decision: M17a (holdout fresco)

Razon: es la pieza faltante mas obvia. M16 encontro el mecanismo, M16 paso 3 lo valido en split quemado. Falta la prueba en datos completamente frescos. Es barato, rapido, y el resultado (positivo o negativo) cierra limpiamente el arco M12-M17.

Si M17a confirma: escribo el resultado, actualizo novedad a 3, y propongo cierre o M17b.
Si M17a falla: cierro con nivel 2.5, documento por que, y el proyecto puede optar por M17c.

## Plan concreto M17

### Paso 1: Construir tablas de drift empirico por profundidad (train n <= 5M)
Ya existen de M16. Las reutilizo.

### Paso 2: Experimento preregistrado en holdout [15M, 25M]

Hipotesis preregistradas (3 tests, Bonferroni alfa = 0.05/3 = 0.017):
- H1: En k=15, ratio modelo_corregido/real es mas cercano a 1.0 que ratio iid/real.
- H2: En k=20, idem.
- H3: En k=25, idem.

Metrica: |ratio - 1.0| para cada modelo. Test: bootstrap CI del ratio.

Criterio de exito: al menos 1 de 3 tests muestra mejora significativa del corregido vs iid.
Criterio de abandono: ningun test significativo, o el corregido sobrecompensa (ratio < 0.95).

### Paso 3: Reporte y cierre

Actualizar MILESTONES.md, Conlusion.md, y generar commit.

## Que no debemos concluir
- Que validar el modelo corregido prueba algo sobre Collatz.
- Que nivel 3 es un resultado importante (es un resultado comunicable, no mas).
- Que la profundidad es "la" explicacion (es una explicacion suficiente para el gap observado).

## Fuentes de la busqueda web
- [Verificacion hasta 2^71 (Springer 2025)](https://link.springer.com/article/10.1007/s11227-025-07337-0)
- [Petri Nets y Collatz (MDPI 2025)](https://www.mdpi.com/2078-2489/16/9/745)
- [Inverse tree proof (Taylor & Francis 2025)](https://www.tandfonline.com/doi/full/10.1080/27684830.2025.2542052)
- [Efficient stopping time computation (arXiv 2501.04032)](https://arxiv.org/abs/2501.04032)
- [Collatz Trees structural framework (Preprints 2025)](https://www.preprints.org/manuscript/202504.1491/v1)
- [Bonacorsi-Bordoni (arXiv:2603.04479)](https://arxiv.org/abs/2603.04479)
