"""
M16 - Algebra y simulacion: random walk libre vs condicionado por primer cruce.

Pregunta: el modelo geometrico i.i.d. del proyecto simula cadenas hasta que la
suma logaritmica se vuelve negativa. La dinamica real produce cadenas que terminan
en 1 (un valor especifico). La diferencia entre "primer cruce por 0" y
"llegar a un target especifico" explica la sobreproduccion de extremos?

Este script NO usa holdout fresco. Trabaja con el rango quemado n <= 5_000_000
y con simulacion pura de random walks.

Metricas:
- Distribucion de blocks_to_descend (tiempo de primer cruce) para RW libre.
- Distribucion de blocks_to_descend para datos reales.
- Comparacion de colas P(blocks >= k) para k = 5, 10, 15, 20, 25, 30.
- Calculo del drift y varianza del paso logaritmico.
- Prediccion teorica via distribucion de Wald (inverse Gaussian).

No afirma prueba de Collatz.
"""
import argparse
import csv
import math
import os
import sys
import random
from collections import Counter

# Intentar importar el motor del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
try:
    from src.collatz.core import alternating_block
    HAS_CORE = True
except ImportError:
    HAS_CORE = False

def odd_chain_blocks(n, max_blocks=256):
    """Genera la cadena odd-to-odd y devuelve blocks_to_descend y log_factors."""
    if n % 2 == 0 or n < 3:
        return None, None
    current = n
    log_n0 = math.log(n)
    cum_log = 0.0
    log_factors = []
    for b in range(max_blocks):
        # tail = v2(current + 1)
        temp = current + 1
        tail = 0
        while temp % 2 == 0:
            tail += 1
            temp //= 2
        q = temp  # odd part of (current + 1)
        # apply: a = 3^tail * q
        a = q * (3 ** tail)
        # exit_v2 = v2(a - 1)
        temp2 = a - 1
        exit_v2 = 0
        while temp2 % 2 == 0:
            exit_v2 += 1
            temp2 //= 2
        next_odd = temp2
        log_factor = tail * math.log(3.0/2.0) - exit_v2 * math.log(2.0)
        cum_log += log_factor
        log_factors.append(log_factor)
        if next_odd < n:
            return b + 1, log_factors
        current = next_odd
    return max_blocks, log_factors

def simulate_rw_blocks(drift, var, max_blocks=256, seed=None):
    """Simula un random walk con pasos log(3/2)*tail - log(2)*exit_v2
    donde tail, exit_v2 ~ Geom(1/2). Devuelve blocks hasta primer cruce por 0."""
    rng = random.Random(seed)
    cum = 0.0
    for b in range(max_blocks):
        # tail ~ Geom(1/2): P(tail=k) = 2^{-k} para k >= 1
        tail = 1
        while rng.random() < 0.5:
            tail += 1
        # exit_v2 ~ Geom(1/2)
        exit_v2 = 1
        while rng.random() < 0.5:
            exit_v2 += 1
        step = tail * math.log(3.0/2.0) - exit_v2 * math.log(2.0)
        cum += step
        if cum < 0:
            return b + 1
    return max_blocks

def wald_survival(k, mu, lam):
    """P(T > k) para la distribucion de Wald (inverse Gaussian) con
    drift mu (negativo) y parametro lambda.
    T = tiempo de primer cruce de un RW con drift mu y varianza sigma^2.
    Parametros: mu_wald = |barrier| / |mu|, lambda_wald = barrier^2 / sigma^2.
    Pero aqui usamos la aproximacion para P(primer cruce > k bloques)
    cuando el barrier es 0 (bajar del punto de partida).

    Para un RW con drift negativo mu y varianza sigma^2 por paso,
    P(no ha cruzado 0 en k pasos | empieza en 0+) es aproximadamente
    la cola de una IG. Pero para primer cruce desde 0, la distribucion
    es mas simple: es la de la primera bajada (first ladder height).

    Usamos simulacion directa, no formula cerrada, porque la formula
    cerrada requiere suposiciones sobre la distribucion de pasos que
    no son gaussianas en nuestro caso."""
    pass  # placeholder - usaremos simulacion

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=1_000_000)
    parser.add_argument('--sim-count', type=int, default=500_000)
    parser.add_argument('--max-blocks', type=int, default=256)
    parser.add_argument('--seed', type=int, default=20260425)
    parser.add_argument('--out-dir', default='reports')
    parser.add_argument('--prefix', default='m16_rw_conditioned')
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    # --- Parte 1: medir drift y varianza reales ---
    print(f"Midiendo drift y varianza de pasos logaritmicos para impares <= {args.limit}...")
    all_steps = []
    real_blocks_counter = Counter()
    count = 0
    for n in range(3, args.limit + 1, 2):
        blocks, log_factors = odd_chain_blocks(n, args.max_blocks)
        if blocks is not None:
            real_blocks_counter[blocks] += 1
            all_steps.extend(log_factors)
            count += 1

    n_steps = len(all_steps)
    mu = sum(all_steps) / n_steps
    var = sum((s - mu)**2 for s in all_steps) / n_steps
    sigma = math.sqrt(var)

    print(f"  Cadenas reales: {count}")
    print(f"  Pasos totales: {n_steps}")
    print(f"  Drift medio (mu): {mu:.8f}")
    print(f"  Varianza (sigma^2): {var:.8f}")
    print(f"  Desviacion (sigma): {sigma:.8f}")
    print(f"  Drift teorico (2*log(3/4)): {2*math.log(3.0/4.0):.8f}")

    # --- Parte 2: simulacion de RW libre ---
    print(f"\nSimulando {args.sim_count} random walks libres (Geom i.i.d.)...")
    rng_base = random.Random(args.seed)
    sim_blocks_counter = Counter()
    for i in range(args.sim_count):
        seed_i = rng_base.randint(0, 2**31)
        b = simulate_rw_blocks(mu, var, args.max_blocks, seed=seed_i)
        sim_blocks_counter[b] += 1

    # --- Parte 3: comparacion de colas ---
    thresholds = [1, 2, 3, 5, 8, 10, 15, 20, 25, 30, 40]

    real_total = sum(real_blocks_counter.values())
    sim_total = sum(sim_blocks_counter.values())

    print(f"\nComparacion de colas P(blocks >= k):")
    print(f"{'k':>5} {'Real':>12} {'Modelo':>12} {'Ratio M/R':>10}")

    rows = []
    for k in thresholds:
        real_surv = sum(c for b, c in real_blocks_counter.items() if b >= k) / real_total
        sim_surv = sum(c for b, c in sim_blocks_counter.items() if b >= k) / sim_total
        ratio = sim_surv / real_surv if real_surv > 0 else float('inf')
        print(f"{k:>5} {real_surv:>12.8f} {sim_surv:>12.8f} {ratio:>10.4f}")
        rows.append({
            'k': k,
            'P_real_blocks_ge_k': f"{real_surv:.10f}",
            'P_model_blocks_ge_k': f"{sim_surv:.10f}",
            'ratio_model_over_real': f"{ratio:.6f}",
        })

    # --- Parte 4: distribucion detallada para blocks 1..40 ---
    detail_rows = []
    for b in range(1, 41):
        r = real_blocks_counter.get(b, 0) / real_total
        s = sim_blocks_counter.get(b, 0) / sim_total
        detail_rows.append({
            'blocks': b,
            'P_real': f"{r:.10f}",
            'P_model': f"{s:.10f}",
            'diff': f"{s - r:.10f}",
        })

    # --- Parte 5: estadisticas resumen ---
    real_mean = sum(b * c for b, c in real_blocks_counter.items()) / real_total
    sim_mean = sum(b * c for b, c in sim_blocks_counter.items()) / sim_total
    real_max = max(real_blocks_counter.keys())
    sim_max = max(sim_blocks_counter.keys())

    # --- Guardar resultados ---
    summary_path = os.path.join(args.out_dir, f"{args.prefix}_summary.csv")
    with open(summary_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['metric', 'value'])
        w.writerow(['limit', args.limit])
        w.writerow(['real_chains', count])
        w.writerow(['sim_chains', args.sim_count])
        w.writerow(['total_steps', n_steps])
        w.writerow(['drift_empirical', f"{mu:.10f}"])
        w.writerow(['drift_theoretical', f"{2*math.log(3.0/4.0):.10f}"])
        w.writerow(['variance', f"{var:.10f}"])
        w.writerow(['sigma', f"{sigma:.10f}"])
        w.writerow(['real_mean_blocks', f"{real_mean:.6f}"])
        w.writerow(['sim_mean_blocks', f"{sim_mean:.6f}"])
        w.writerow(['real_max_blocks', real_max])
        w.writerow(['sim_max_blocks', sim_max])
        w.writerow(['seed', args.seed])
    print(f"\nSummary: {summary_path}")

    tails_path = os.path.join(args.out_dir, f"{args.prefix}_tails.csv")
    with open(tails_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['k', 'P_real_blocks_ge_k', 'P_model_blocks_ge_k', 'ratio_model_over_real'])
        w.writeheader()
        w.writerows(rows)
    print(f"Tails: {tails_path}")

    detail_path = os.path.join(args.out_dir, f"{args.prefix}_detail.csv")
    with open(detail_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['blocks', 'P_real', 'P_model', 'diff'])
        w.writeheader()
        w.writerows(detail_rows)
    print(f"Detail: {detail_path}")

    # --- Parte 6: diagnostico clave ---
    print("\n=== DIAGNOSTICO M16 ===")
    print(f"Drift empirico: {mu:.8f}")
    print(f"Drift teorico:  {2*math.log(3.0/4.0):.8f}")
    print(f"Diferencia:     {mu - 2*math.log(3.0/4.0):.8f}")
    print()

    # El punto clave: el ratio modelo/real en las colas
    # Si el ratio crece con k, el modelo i.i.d. sobreproduce colas
    ratios_at_high_k = []
    for k in [10, 20, 30]:
        real_surv = sum(c for b, c in real_blocks_counter.items() if b >= k) / real_total
        sim_surv = sum(c for b, c in sim_blocks_counter.items() if b >= k) / sim_total
        if real_surv > 0:
            ratios_at_high_k.append((k, sim_surv / real_surv))

    if len(ratios_at_high_k) >= 2:
        ratio_10 = ratios_at_high_k[0][1]
        ratio_last = ratios_at_high_k[-1][1]
        if ratio_last > ratio_10 * 1.5:
            print("SOBREPRODUCCION CRECIENTE: el ratio modelo/real crece con k.")
            print("El modelo i.i.d. sobreestima colas largas de forma sistematica.")
            print("Esto es consistente con la hipotesis M16.")
        elif ratio_last > ratio_10 * 1.1:
            print("SOBREPRODUCCION LEVE: ratio crece pero no dramaticamente.")
        else:
            print("SIN SOBREPRODUCCION CLARA: el ratio es estable o decreciente.")
            print("La hipotesis M16 pierde fuerza.")

    print("\nDone.")

if __name__ == '__main__':
    main()
