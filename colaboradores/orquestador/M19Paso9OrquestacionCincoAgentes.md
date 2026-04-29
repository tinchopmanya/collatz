# M19 paso 9 - orquestacion con cinco agentes y CI

Fecha: 2026-04-29
Responsable: Codex orquestador
Estado: ejecucion paralela iniciada

## Preguntas antes

- Estamos en terreno virgen?
  - No en Collatz general, ni en rewriting, ni en verificacion computacional.
  - Si queda terreno parcialmente virgen, esta en combinaciones concretas: S1/S2 con herramientas 2026, certificados reproducibles, o traducciones nuevas desde codificaciones 2026.
- Podemos descubrir algo relevante?
  - Si, pero solo con evidencia fuerte: un `YES` top-level certificado para S1/S2, una extension reproducible no reportada, o una reduccion nueva que cambie la dificultad.
- Ya alguien busco esto?
  - Si. Yolcu-Aaronson-Heule reportan busqueda automatica; AProVE/Matchbox/TermComp trabajan terminacion; Knight y Barina tienen resultados 2026 relacionados.
- Que tan lejos estamos?
  - Lejos de una prueba de Collatz. Mas cerca de un resultado tecnico serio sobre fronteras de terminacion automatica.

## Agentes lanzados

| Agente | Rol | Write scope | Pregunta central |
| --- | --- | --- | --- |
| CodexHijo-Web2026 | investigacion web | `colaboradores/codex-web/M19Web2026EstadoActual.md` | que cambio realmente al 2026-04-29 |
| CodexHijo-AProVEEnv | entorno AProVE | `scripts/m19_probe_aprove_environment.py`, workflow probe, reporte | si el bloqueo es ambiente o matematica |
| CodexHijo-Matchbox | segunda herramienta | runner/workflow Matchbox, reporte | si Matchbox es via realista para S1/S2 |
| CodexHijo-KnightM20 | codificacion Knight | reporte M20 y notas opcionales | si la regla de 30 condiciones sirve como reduccion |
| CodexHijo-Certificacion | auditoria/certificados | auditor de artefactos, workflow, reporte | que evidencia permitiria publicar algo |

Regla de integracion:

```text
Nadie decide solo. Los hijos producen evidencia; el orquestador integra, baja tono si hace falta, y commitea solo lo verificable.
```

## GitHub Actions disparados

Se dispararon tres workflows manuales desde `main`:

| Workflow | Run | Objetivo |
| --- | --- | --- |
| M19 rewriting reproduction | https://github.com/tinchopmanya/collatz/actions/runs/25104952224 | reproducir prueba base Zantema |
| M19 rewriting challenge search | https://github.com/tinchopmanya/collatz/actions/runs/25104952228 | buscar S1/S2 con grilla acotada |
| M19 AProVE challenge search | https://github.com/tinchopmanya/collatz/actions/runs/25104952325 | probar S1/S2 con AProVE 2026 |

## Decision operativa

No conviene esperar pasivamente cinco horas. La mejor forma de usar el tiempo es:

1. correr CI remoto;
2. preparar rutas alternativas en paralelo;
3. auditar cualquier salida `YES` como sospechosa hasta confirmar que sea top-level/certificada;
4. registrar tambien resultados negativos, porque reducen el espacio de busqueda.

## Criterio de avance

Avance real si ocurre al menos uno:

- reproducimos una prueba base en CI;
- encontramos un bloqueo ambiental exacto y corregible para AProVE;
- Matchbox queda listo como workflow;
- obtenemos una ruta concreta Knight -> terminacion;
- definimos formato de certificado aceptable para publicar.

## Criterio de abandono

Enfriar M19 si:

- AProVE, Matchbox y el prover original fallan sin certificados;
- no aparece ninguna reduccion nueva;
- los workflows solo producen timeouts sin diagnostico;
- toda mejora depende de computo grande no interpretable.

## Preguntas despues

- Avanzamos?
  - Si: pasamos de diseno a ejecucion paralela y CI remoto.
- Estamos mas cerca de algo publicable?
  - Un poco: la publicabilidad depende de certificados, reproducibilidad y novedad, no de volumen de computo.
- Posibilidad cientifica fuerte alta?
  - Condicional. Alta solo si S1/S2 ceden o si Knight produce una reduccion mas facil. En probabilidad base sigue siendo baja, pero es la mejor zona que encontramos.
- Que toca?
  - Monitorear CI, integrar reportes de hijos, y commitear solo artefactos con verificacion.
