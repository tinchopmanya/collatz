# Handoff a ClaudeSocio - continuidad del proyecto Collatz

Fecha: 2026-04-25
Motivo: el usuario quiere que ClaudeSocio continue como unico agente activo porque se queda sin saldo de Codex.

## Estado de git

`main` es la rama canonica.

Todas las ramas activas fueron revisadas contra `main` por equivalencia de parches:

- `claude-socio/m15-critica-modelo-modular`: integrado.
- `codex-hijo/m14-residuos`: integrado por cherry-pick `5a4f9d4`.
- `codex-hijo/m15-algebra`: integrado.
- `codex-hijo/m15-algebra-replica`: integrado.
- `codex-hijo/m15-qmod8-transition`: integrado.
- `codex-hijo/m15-qmod8-transition-replica`: integrado.
- `codex-investigador/m15-modelo-modular-literatura`: integrado.

Verificacion antes del handoff:

```powershell
python -m py_compile experiments\analyze_m14_residue.py experiments\analyze_m15_algebra.py experiments\replicate_m15_algebra.py experiments\analyze_m15_qmod8_transition.py experiments\replicate_m15_qmod8_transition.py experiments\test_m14_residual_robustness.py
git diff --check
```

Ambas verificaciones pasaron.

## Estado cientifico

M15 queda cerrado/enfriado en la formulacion:

```text
q mod 8 como estado marginal de memoria suficiente para supervivencia orbital
```

Resumen:

- `q mod 8` predice `next_tail` localmente.
- Esa prediccion es algebra 2-adica esperable, no novedad fuerte.
- La matriz `q_{i+1} mod 8 | q_i mod 8` mezcla casi uniforme en un paso.
- CodexHijo2 replico exactamente a CodexHijo1.
- No se gasto holdout fresco.
- No se debe abrir `q mod 16` automaticamente sin una razon teorica nueva.

## Rol de ClaudeSocio desde ahora

ClaudeSocio ya no actua solo como critico: el usuario quiere que tome decisiones y sea el unico agente activo.

Responsabilidades:

- Leer el repo desde cero.
- Verificar `git status` y trabajar desde `main` actualizado.
- Decidir la siguiente pregunta cientifica.
- Gestionar git sin depender de Codex.
- No delegar a CodexHijo ni a InvestigadorWeb salvo que el usuario cambie la instruccion.
- Mantener el protocolo de preguntas antes/despues de cada iteracion.
- Usar web/papers antes de claims de novedad.
- No afirmar prueba de Collatz sin demostracion formal completa y revision externa.

## Preguntas obligatorias que debe mantener

Antes de cada decision:

- Estamos en algo potencialmente virgen?
- Alguien ya hizo esto?
- Que seria nuevo si sale bien?
- Que resultado destruiria la hipotesis?
- Que tan lejos estamos de algo publicable?
- Necesitamos web, algebra, experimento o critica antes de decidir?
- Estamos usando holdout fresco o contaminado?

Despues de cada iteracion:

- Avanzamos o solo confirmamos algo conocido?
- La hipotesis quedo mas fuerte, mas debil o descartada?
- Hay riesgo post-hoc?
- Hay explicacion algebraica trivial?
- Hay evidencia independiente?
- Que toca ahora?

## Recomendacion del orquestador saliente

No continuar M15 marginal.

La proxima decision deberia ser elegir M16. Opciones razonables:

1. Cerrar un reporte tecnico de M12-M15 como caso de descarte disciplinado.
2. Buscar una nueva pregunta con mas estructura teorica, no solo barrido modular.
3. Auditar bibliografia y claims antes de nuevos experimentos.
4. Explorar modelos de cadenas completas solo si se preregistra metrica y baseline.

La opcion mas segura si queda poco tiempo/saldo es:

```text
Crear un plan M16 corto, con 2-3 candidatas, y elegir una sola que pase filtro de novedad y falsabilidad.
```
