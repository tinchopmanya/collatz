# Decision de orquestacion M14 tras Claude y Codex hijo

Fecha: 2026-04-25
Estado: decision registrada

## Insumos revisados

- [Respuesta de Claude](../revisor-claude/RespuestaFormaDeTrabajoMultiagente.md)
- Rama del Codex hijo: `codex-hijo/m14-residuos`
- Commit del Codex hijo: `e961b45 Explore M14 residue decomposition`
- Reporte del Codex hijo en su rama: `colaboradores/codex-hijo/ResultadosM14.md`
- Script del Codex hijo en su rama: `experiments/analyze_m14_residue.py`

## Veredicto de Codex orquestador

Claude tiene razon en el punto metodologico central:

```text
El residuo `prev_exit_v2 = 5` + `interior_block` no debe tratarse como confirmado porque fue encontrado en un proceso exploratorio con muchas comparaciones.
```

El Codex hijo tambien aporta algo util:

```text
Dentro de la subpoblacion exploratoria, `q_current mod 4` separa fuertemente el exceso de `next_tail = 1`.
```

Estas dos cosas no se contradicen.

La decision es:

```text
No mergear todavia la rama `codex-hijo/m14-residuos` a `main`.
Registrar esa rama como evidencia exploratoria.
Cambiar M14 para que primero sea una prueba de destruccion/confirmacion.
```

## Clasificacion del aporte de Claude

Tipo:

```text
revision metodologica + cambio de protocolo
```

Se aceptan estos cambios:

- separar olas exploratorias y confirmatorias;
- contar comparaciones multiples;
- aplicar correccion conservadora;
- exigir prueba de destruccion antes de escalar;
- considerar correlacion intra-cadena;
- tratar a Claude como revisor adversarial y no como ejecutor principal.

## Clasificacion del aporte del Codex hijo

Tipo:

```text
experimento exploratorio
```

Hallazgo exploratorio:

```text
En `prev_exit_v2 = 5` + `interior_block`, `q_current mod 4` separa la senal:
q = 1 mod 4 concentra exceso de `next_tail = 1`;
q = 3 mod 4 va en sentido contrario.
```

Riesgos:

- el corte aparece despues de mirar los datos;
- los cortes modulares son anidados;
- el modelo sintetiza residuos de `q`, no reproduce una orbita modular completa;
- puede ser algebra trivial o mezcla de supervivencia;
- no se aplico correccion por comparaciones multiples.

Decision:

```text
Conservar en rama. No integrar a `main` como conclusion.
```

## Nueva forma oficial de M14

M14 queda redefinido como:

```text
Confirmar o destruir el residuo antes de descomponerlo mas.
```

Orden recomendado:

1. Conteo de tests realizados en M13 y en el experimento del Codex hijo.
2. Correccion Bonferroni conservadora para la celda `prev_exit_v2 = 5` + `interior_block`.
3. Permutation test o bootstrap robusto para la diferencia `P(next_tail = 1)`.
4. Revision algebraica directa: dado `prev_exit_v2 = 5`, calcular si `next_tail = 1` queda determinado o sesgado por congruencias modulo potencias de 2.
5. Solo si sobrevive, volver a la rama exploratoria del Codex hijo y decidir si `q_current mod 4` merece formalizacion.

## Criterios de exito

M14 avanza si:

- la senal sobrevive correccion por comparaciones multiples con umbral fuerte;
- el test robusto no destruye la diferencia;
- o aparece una explicacion algebraica exacta que predice el exceso observado.

## Criterios de abandono

M14 se cierra como descarte si:

- el p-valor ajustado no supera el umbral definido;
- el efecto desaparece bajo bootstrap/permutacion por cadena;
- la congruencia algebraica predice una fraccion compatible con el modelo nulo;
- o el efecto se reparte como mezcla sin una causa interpretable.

## Proxima tarea recomendada

Crear un experimento confirmatorio nuevo, separado de la rama exploratoria:

```text
experiments/test_m14_residual_robustness.py
```

Salida esperada:

- `reports/m14_residual_robustness_summary.csv`
- `reports/m14_residual_robustness_permutation.csv`
- `reports/m14_residual_robustness.md`

Este experimento debe tratar el hallazgo del Codex hijo como hipotesis exploratoria, no como conclusion.
