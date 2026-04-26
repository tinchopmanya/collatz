"""
M16 paso 3: modelo corregido por profundidad vs modelo i.i.d.

El modelo i.i.d. usa:
  tail ~ Geom(1/2), exit_v2 ~ Geom(1/2), independientes por bloque.

El modelo corregido usa:
  Para profundidad d:
    exit_v2 ~ Geom(1/2) con media ajustada por un factor lineal en d
    tail ~ Geom(1/2) con media ajustada complementaria

  Implementacion practica:
    En lugar de parametrizar la geometrica distinta por profundidad,
    usamos un enfoque mas simple y robusto:
    BOOTSTRAP de pasos reales por profundidad.

    Es decir, para cada profundidad d, muestreamos pasos de la
    distribucion empirica de pasos a esa profundidad.

    Esto captura automaticamente el sesgo de supervivencia.

Comparacion:
  1. Modelo i.i.d. (baseline)
  2. Modelo bootstrap por profundidad (corregido)
  3. Datos reales
"""
import math
import os
import sys
import random
import csv
from collections import defaultdict, Counter

def odd_chain_full(n, max_blocks=256):
    if n % 2 == 0 or n < 3:
        return []
    current = n
    steps = []
    for b in range(max_blocks):
        temp = current + 1
        tail = 0
        while temp % 2 == 0:
            tail += 1
            temp //= 2
        q = temp
        a = q * (3 ** tail)
        temp2 = a - 1
        exit_v2 = 0
        while temp2 % 2 == 0:
            exit_v2 += 1
            temp2 //= 2
        next_odd = temp2
        log_step = tail * math.log(3.0/2.0) - exit_v2 * math.log(2.0)
        steps.append(log_step)
        if next_odd < n:
            return steps
        current = next_odd
    return steps

def simulate_iid(rng, max_blocks=256):
    """Modelo i.i.d.: tail, exit_v2 ~ Geom(1/2) independientes."""
    cum = 0.0
    for b in range(max_blocks):
        tail = 1
        while rng.random() < 0.5:
            tail += 1
        exit_v2 = 1
        while rng.random() < 0.5:
            exit_v2 += 1
        step = tail * math.log(3.0/2.0) - exit_v2 * math.log(2.0)
        cum += step
        if cum < 0:
            return b + 1
    return max_blocks

def simulate_depth_bootstrap(rng, steps_by_depth, max_depth_available, max_blocks=256):
    """Modelo corregido: muestrea pasos de la distribucion empirica por profundidad."""
    cum = 0.0
    for d in range(max_blocks):
        # Usar la profundidad d si hay suficientes muestras, sino la maxima disponible
        depth_key = min(d, max_depth_available - 1)
        pool = steps_by_depth[depth_key]
        if not pool:
            # Fallback a i.i.d.
            tail = 1
            while rng.random() < 0.5:
                tail += 1
            exit_v2 = 1
            while rng.random() < 0.5:
                exit_v2 += 1
            step = tail * math.log(3.0/2.0) - exit_v2 * math.log(2.0)
        else:
            step = rng.choice(pool)
        cum += step
        if cum < 0:
            return d + 1
    return max_blocks

def main():
    limit = 5_000_000
    n_sim = 2_500_000
    max_blocks = 256
    seed = 20260425
    out_dir = 'reports'
    prefix = 'm16_corrected_model'

    os.makedirs(out_dir, exist_ok=True)

    # --- Recoger pasos reales por profundidad ---
    print(f"Recolectando pasos reales por profundidad (n <= {limit})...")
    steps_by_depth = defaultdict(list)
    real_blocks_counter = Counter()
    n_chains = 0

    for n in range(3, limit + 1, 2):
        steps = odd_chain_full(n, max_blocks)
        if not steps:
            continue
        n_chains += 1
        real_blocks_counter[len(steps)] += 1
        for d, s in enumerate(steps):
            if d < 50:  # guardar hasta profundidad 50
                steps_by_depth[d].append(s)

    max_depth_avail = max(d for d in steps_by_depth if len(steps_by_depth[d]) >= 100) + 1
    print(f"  Cadenas: {n_chains}")
    print(f"  Profundidad maxima con >= 100 muestras: {max_depth_avail}")

    # --- Simular modelo i.i.d. ---
    print(f"\nSimulando {n_sim} cadenas i.i.d....")
    rng = random.Random(seed)
    iid_counter = Counter()
    for i in range(n_sim):
        b = simulate_iid(rng, max_blocks)
        iid_counter[b] += 1

    # --- Simular modelo corregido por profundidad ---
    print(f"Simulando {n_sim} cadenas con bootstrap por profundidad...")
    rng2 = random.Random(seed + 1)
    corr_counter = Counter()
    for i in range(n_sim):
        b = simulate_depth_bootstrap(rng2, steps_by_depth, max_depth_avail, max_blocks)
        corr_counter[b] += 1

    # --- Comparar colas ---
    real_total = sum(real_blocks_counter.values())
    iid_total = sum(iid_counter.values())
    corr_total = sum(corr_counter.values())

    thresholds = [1, 2, 3, 5, 8, 10, 15, 20, 25, 30, 40]

    print(f"\n{'k':>5} {'P_real':>12} {'P_iid':>12} {'R_iid/real':>11} {'P_corr':>12} {'R_corr/real':>12}")
    rows = []
    for k in thresholds:
        p_r = sum(c for b, c in real_blocks_counter.items() if b >= k) / real_total
        p_i = sum(c for b, c in iid_counter.items() if b >= k) / iid_total
        p_c = sum(c for b, c in corr_counter.items() if b >= k) / corr_total
        r_i = p_i / p_r if p_r > 0 else float('inf')
        r_c = p_c / p_r if p_r > 0 else float('inf')
        print(f"{k:>5} {p_r:>12.8f} {p_i:>12.8f} {r_i:>11.4f} {p_c:>12.8f} {r_c:>12.4f}")
        rows.append({
            'k': k,
            'P_real': f"{p_r:.10f}",
            'P_iid': f"{p_i:.10f}",
            'ratio_iid': f"{r_i:.6f}",
            'P_corrected': f"{p_c:.10f}",
            'ratio_corrected': f"{r_c:.6f}",
        })

    # --- Guardar CSV ---
    path = os.path.join(out_dir, f"{prefix}_comparison.csv")
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['k','P_real','P_iid','ratio_iid','P_corrected','ratio_corrected'])
        w.writeheader()
        w.writerows(rows)
    print(f"\nCSV: {path}")

    # --- Diagnostico ---
    print(f"\n=== DIAGNOSTICO M16 PASO 3 ===")
    # Medir mejora del modelo corregido vs i.i.d. en k=20
    for k in [10, 20, 30]:
        p_r = sum(c for b, c in real_blocks_counter.items() if b >= k) / real_total
        p_i = sum(c for b, c in iid_counter.items() if b >= k) / iid_total
        p_c = sum(c for b, c in corr_counter.items() if b >= k) / corr_total
        if p_r > 0:
            gap_iid = abs(p_i/p_r - 1)
            gap_corr = abs(p_c/p_r - 1)
            if gap_iid > 0:
                reduction = 1 - gap_corr/gap_iid
                print(f"k={k}: gap i.i.d.={gap_iid:.4f}, gap corregido={gap_corr:.4f}, reduccion={reduction:.1%}")

    print("\nDone.")

if __name__ == '__main__':
    main()
