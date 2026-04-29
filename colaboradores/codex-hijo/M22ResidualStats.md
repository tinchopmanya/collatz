# M22 residual stats

Fecha: 2026-04-29
Agente: CodexHijo-M22-ResidualStats
Rama: `codex-hijo/m22-residual-stats`
Commit: ver entrega final
Milestone: M22
Tarea: perfilar el complemento congelado S2-k16 sin depender de Matchbox

## Antes

1. Estoy en algo virgen? No para low-bit descent ni rewriting por separado; parcialmente si en el uso del complemento S2-k16 como cola de trabajo guardada.
2. Alguien ya busco esto? M19/M22 ya fijaron S1/S2 y la cobertura low-bit; `M22KillCriteria.md` fijo que C1 y C2 son las compuertas reales.
3. Que parte exacta podria ser nueva? Una caracterizacion reproducible del complemento `U_16` que diga si hay subfamilias pequenas, exactas y utiles para rewriting.
4. Puedo descubrir algo con esto? Si: si el complemento tiene bloques, simetrias o buckets exactos que reduzcan el proximo experimento confirmatorio.
5. Que tan lejos estoy de algo relevante? Cerca de priorizar microbenchmarks; lejos de una prueba, porque C1 independiente y C2 semantico siguen abiertos.
6. Que evidencia haria que siga? Buckets exactos con `0` overinclude certificado, hashes estables, y una lista corta de familias para un validador S2.
7. Que evidencia haria que abandone? Drift de hash, ausencia total de estructura pequena, o que las familias solo funcionen como clustering no semantico.

## Comando reproducible

```powershell
python scripts\m22_residual_stats.py
python -m py_compile scripts\m22_bridge_lowbit_rewriting.py scripts\m22_freeze_s2_k16.py scripts\m22_residual_stats.py tests\test_m22_bridge_lowbit_rewriting.py tests\test_m22_freeze_s2_k16.py tests\test_m22_residual_stats.py
python -m unittest discover -s tests -p "test_m22_*.py"
```

## Archivos creados

- `scripts/m22_residual_stats.py`
- `tests/test_m22_residual_stats.py`
- `reports/m22_residual_stats_summary.csv`
- `reports/m22_residual_stats_mod_distribution.csv`
- `reports/m22_residual_stats_branch_blocks.csv`
- `reports/m22_residual_stats_symmetries.csv`
- `reports/m22_residual_stats_candidate_subfamilies.csv`
- `reports/m22_residual_stats_c1_c2_gate.csv`
- `colaboradores/codex-hijo/M22ResidualStats.md`

## Resultado central

El script toma `reports/m22_s2_k16_uncovered_residues.csv` si existe, o regenera `freeze_s2(16)` si falta, y en ambos casos exige:

```text
uncovered_count = 378
uncovered_sha256 = bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210
residue mod 8 = 5 para todos los residuos
```

Lectura estructural:

- Distribucion modular: `1470` filas para `j = 3..16`.
- Bloques contiguos en indice S2 `(r - 5) / 8`: `360` bloques; `342` son singletons; maximo bloque `2`.
- Simetrias simples: ninguna cierra `U_16`; la mejor senal es `xor_residue_bit_13/14/15` con `158/378` hits dirigidos.
- Subfamilias candidatas: `72` filas priorizadas; ahora se rankean primero las que son `C2-exact microbenchmark after C1 recheck`.
- Buckets low-bit exactos pequenos: `92` buckets con `2..24` residuos y `0` overinclude certificado.

## Conexion con M22-C1/C2

`reports/m22_residual_stats_c1_c2_gate.csv` separa las conclusiones para no inflar el resultado:

- M22-C1 no queda satisfecho por este script. La razon esta explicitada: el script verifica SHA y forma, pero no es un rechecker independiente porque lee el CSV congelado y su fallback importa `m22_freeze_s2_k16.freeze_s2`.
- M22-C1 recibe soporte parcial: el hash/count quedan anclados y pueden ser usados como salida esperada por un rechecker independiente.
- M22-C2 recibe soporte parcial: un guard exacto finito parece factible, pero la compresion por rangos es mala (`360` bloques, `342` singletons), asi que un validador semantico sigue siendo obligatorio.
- M22-C2 mata atajos: `255` buckets low-bit pequenos son no exactos; aunque el mejor tiene densidad `0.9375`, usarlo solo cambiaria el problema.
- M22-C2 no permite quotient por simetrias simples: la mejor simetria solo cubre `158/378`, no cierra el complemento.

## Despues

1. La originalidad cambio? Subio un poco como ingenieria reproducible: ahora hay una cola exacta de subfamilias, no solo muestras.
2. La probabilidad de relevancia subio, bajo o quedo igual? Subio moderadamente para microbenchmarks; quedo igual para publicabilidad hasta cerrar C1/C2.
3. Se encontro senal robusta, ruido o descarte? Senal mixta: hay `92` microfamilias exactas, pero casi no hay bloques contiguos y no hay simetria de cierre.
4. Que aprendimos que no sabiamos antes? El complemento es atomizado en rangos, pero contiene buckets low-bit exactos que sirven como primeras pruebas C2-safe.
5. Conviene seguir, escalar, formalizar o abandonar? Seguir sin escalar: primero C1 independiente y C2 validador, luego microbenchmarks exactos.
6. Cual es la siguiente pregunta minima? Puede un validador C2 aceptar exactamente un bucket exacto `r mod 2^13 = 8189` y rechazar todo lo demas sin cambiar la semantica S2?

## Recomendacion

Continuar M22, pero no vender estas stats como resultado confirmatorio. El siguiente paso minimo debe ser C2 sobre una microfamilia exacta, preferentemente `r mod 2^13 = 8189` con `8/8` residuos y `0` overinclude, en paralelo con C1 independiente para reproducir hashes y auditorias. No invertir todavia en un SRS guardado completo de `378` residuos: los `360` bloques y `1473` nodos trie sugieren que podria inflar CNF antes de aportar una prueba.

## Que no se debe concluir

- No hay prueba de Collatz.
- No hay C1 cerrado.
- No hay C2 cerrado.
- No hay evidencia de que Matchbox/AProVE vayan a cerrar S2-k16.
- Las familias no exactas son colas de busqueda, no guardas semanticas.
