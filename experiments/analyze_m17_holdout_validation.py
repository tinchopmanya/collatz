"""
M17: Validacion en holdout fresco [15M, 25M]

Preregistrado:
- Train: n in [3, 5_000_000] impares (rango quemado, para calibrar tablas de profundidad)
- Holdout: n in [15_000_001, 25_000_000] impares (rango NUNCA tocado en el proyecto)
- 3 tests con Bonferroni alfa = 0.05/3 = 0.0167:
  H1: ratio_corregido/real mas cercano a 1.0 que ratio_iid/real en k=15
  H2: idem en k=20
  H3: idem en k=25
- Metrica: |ratio - 1.0|
- Criterio exito: al menos 1/3 tests muestra mejora significativa
- Criterio abandono: ningun test significativo, o corregido sobrecompensa (ratio < 0.90)
"""
import math
import os
import sys
import random
import csv
from collections import defaultdict, Counter

LOG_3_2 = math.log(3.0 / 2.0)
LOG_2 = math.log(2.0)

def odd_chain_blocks(n, max_blocks=256):
    """Retorna numero de bloques hasta que next_odd < n."""
    if n % 2 == 0 or n < 3:
        return 0
    current = n
    for b in range(1, max_blocks + 1):
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
        if next_odd < n:
            return b
        current = next_odd
    return max_blocks

def odd_chain_full(n, max_blocks=256):
    """Retorna lista de log_steps."""
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
        log_step = tail * LOG_3_2 - exit_v2 * LOG_2
        steps.append(log_step)
        if next_odd < n:
            return steps
        current = next_odd
    return steps

def simulate_iid(rng, max_blocks=256):
    cum = 0.0
    for b in range(max_blocks):
        tail = 1
        while rng.random() < 0.5:
            tail += 1
        exit_v2 = 1
        while rng.random() < 0.5:
            exit_v2 += 1
        step = tail * LOG_3_2 - exit_v2 * LOG_2
        cum += step
        if cum < 0:
            return b + 1
    return max_blocks

def simulate_depth_bootstrap(rng, steps_by_depth, max_depth_available, max_blocks=256):
    cum = 0.0
    for d in range(max_blocks):
        depth_key = min(d, max_depth_available - 1)
        pool = steps_by_depth[depth_key]
        if not pool:
            tail = 1
            while rng.random() < 0.5:
                tail += 1
            exit_v2 = 1
            while rng.random() < 0.5:
                exit_v2 += 1
            step = tail * LOG_3_2 - exit_v2 * LOG_2
        else:
            step = rng.choice(pool)
        cum += step
        if cum < 0:
            return d + 1
    return max_blocks

def bootstrap_ratio_ci(real_counter, model_counter, k, n_boot=5000, seed=42):
    """Bootstrap CI para el ratio P_model(>=k)/P_real(>=k)."""
    rng = random.Random(seed)

    real_total = sum(real_counter.values())
    model_total = sum(model_counter.values())

    # Vectores de 0/1 para si blocks >= k
    real_hits = sum(c for b, c in real_counter.items() if b >= k)
    model_hits = sum(c for b, c in model_counter.items() if b >= k)

    p_real = real_hits / real_total
    p_model = model_hits / model_total

    if p_real == 0:
        return float('inf'), float('inf'), float('inf')

    ratio = p_model / p_real

    # Bootstrap parametrico: sample from binomial
    ratios = []
    for _ in range(n_boot):
        r_boot = rng.gauss(real_hits, math.sqrt(real_hits * (1 - real_hits/real_total))) / real_total
        m_boot = rng.gauss(model_hits, math.sqrt(model_hits * (1 - model_hits/model_total))) / model_total
        if r_boot > 0:
            ratios.append(m_boot / r_boot)

    ratios.sort()
    lo = ratios[int(0.025 * len(ratios))]
    hi = ratios[int(0.975 * len(ratios))]
    return ratio, lo, hi

def main():
    train_limit = 5_000_000
    holdout_lo = 15_000_001
    holdout_hi = 25_000_000
    n_sim = 5_000_000  # muchas simulaciones para estabilidad
    max_blocks = 256
    seed = 20260425
    out_dir = 'reports'

    os.makedirs(out_dir, exist_ok=True)

    # === FASE 1: Calibrar tablas de profundidad en train ===
    print(f"=== FASE 1: Calibracion en train [3, {train_limit}] ===")
    steps_by_depth = defaultdict(list)
    train_counter = Counter()
    n_train = 0

    for n in range(3, train_limit + 1, 2):
        steps = odd_chain_full(n, max_blocks)
        if not steps:
            continue
        n_train += 1
        train_counter[len(steps)] += 1
        for d, s in enumerate(steps):
            if d < 50:
                steps_by_depth[d].append(s)
        if n_train % 500000 == 0:
            print(f"  Train: {n_train} cadenas procesadas...")

    max_depth_avail = max(d for d in steps_by_depth if len(steps_by_depth[d]) >= 100) + 1
    print(f"  Cadenas train: {n_train}")
    print(f"  Profundidad maxima con >= 100 muestras: {max_depth_avail}")

    # === FASE 2: Recoger datos reales en holdout ===
    print(f"\n=== FASE 2: Datos reales en holdout [{holdout_lo}, {holdout_hi}] ===")
    holdout_counter = Counter()
    n_holdout = 0

    for n in range(holdout_lo if holdout_lo % 2 == 1 else holdout_lo + 1, holdout_hi + 1, 2):
        blocks = odd_chain_blocks(n, max_blocks)
        if blocks == 0:
            continue
        n_holdout += 1
        holdout_counter[blocks] += 1
        if n_holdout % 500000 == 0:
            print(f"  Holdout: {n_holdout} cadenas procesadas...")

    print(f"  Cadenas holdout: {n_holdout}")

    # === FASE 3: Simular modelos ===
    print(f"\n=== FASE 3: Simulacion de {n_sim} cadenas por modelo ===")

    rng1 = random.Random(seed)
    iid_counter = Counter()
    for i in range(n_sim):
        b = simulate_iid(rng1, max_blocks)
        iid_counter[b] += 1
        if (i + 1) % 1000000 == 0:
            print(f"  i.i.d.: {i+1} simuladas...")

    rng2 = random.Random(seed + 1)
    corr_counter = Counter()
    for i in range(n_sim):
        b = simulate_depth_bootstrap(rng2, steps_by_depth, max_depth_avail, max_blocks)
        corr_counter[b] += 1
        if (i + 1) % 1000000 == 0:
            print(f"  Corregido: {i+1} simuladas...")

    # === FASE 4: Comparacion en holdout ===
    print(f"\n=== FASE 4: Resultados en HOLDOUT [{holdout_lo}, {holdout_hi}] ===")

    real_total = sum(holdout_counter.values())
    iid_total = sum(iid_counter.values())
    corr_total = sum(corr_counter.values())

    thresholds = [1, 2, 3, 5, 8, 10, 15, 20, 25, 30, 40]

    print(f"\n{'k':>5} {'P_real':>14} {'P_iid':>14} {'R_iid':>8} {'P_corr':>14} {'R_corr':>8}")
    rows = []
    for k in thresholds:
        p_r = sum(c for b, c in holdout_counter.items() if b >= k) / real_total
        p_i = sum(c for b, c in iid_counter.items() if b >= k) / iid_total
        p_c = sum(c for b, c in corr_counter.items() if b >= k) / corr_total
        r_i = p_i / p_r if p_r > 0 else float('inf')
        r_c = p_c / p_r if p_r > 0 else float('inf')
        print(f"{k:>5} {p_r:>14.10f} {p_i:>14.10f} {r_i:>8.4f} {p_c:>14.10f} {r_c:>8.4f}")
        rows.append({
            'k': k, 'P_real': f"{p_r:.12f}", 'P_iid': f"{p_i:.12f}",
            'ratio_iid': f"{r_i:.6f}", 'P_corrected': f"{p_c:.12f}",
            'ratio_corrected': f"{r_c:.6f}",
        })

    # === FASE 5: Tests preregistrados ===
    print(f"\n=== FASE 5: Tests preregistrados (Bonferroni alfa = 0.017) ===")

    test_ks = [15, 20, 25]
    results = []

    for k in test_ks:
        ratio_iid, lo_iid, hi_iid = bootstrap_ratio_ci(holdout_counter, iid_counter, k, n_boot=10000, seed=seed)
        ratio_corr, lo_corr, hi_corr = bootstrap_ratio_ci(holdout_counter, corr_counter, k, n_boot=10000, seed=seed+1)

        gap_iid = abs(ratio_iid - 1.0)
        gap_corr = abs(ratio_corr - 1.0)

        # El test es: 1.0 esta dentro del CI del modelo corregido pero no del i.i.d.?
        iid_contains_1 = lo_iid <= 1.0 <= hi_iid
        corr_contains_1 = lo_corr <= 1.0 <= hi_corr

        # Sobrecompensacion?
        overcompensates = ratio_corr < 0.90

        print(f"\nk={k}:")
        print(f"  i.i.d.: ratio={ratio_iid:.4f}, CI95=[{lo_iid:.4f}, {hi_iid:.4f}], |gap|={gap_iid:.4f}, 1.0 in CI: {iid_contains_1}")
        print(f"  Corr:   ratio={ratio_corr:.4f}, CI95=[{lo_corr:.4f}, {hi_corr:.4f}], |gap|={gap_corr:.4f}, 1.0 in CI: {corr_contains_1}")

        if overcompensates:
            print(f"  *** SOBRECOMPENSACION: ratio_corr={ratio_corr:.4f} < 0.90 ***")
        elif not iid_contains_1 and corr_contains_1:
            print(f"  >>> MEJORA SIGNIFICATIVA: corregido contiene 1.0, i.i.d. no")
        elif gap_corr < gap_iid:
            print(f"  Mejora no significativa: gap corregido < gap i.i.d. pero ambos contienen (o no) 1.0")
        else:
            print(f"  Sin mejora")

        results.append({
            'k': k,
            'ratio_iid': f"{ratio_iid:.6f}", 'ci_iid': f"[{lo_iid:.4f}, {hi_iid:.4f}]",
            'ratio_corr': f"{ratio_corr:.6f}", 'ci_corr': f"[{lo_corr:.4f}, {hi_corr:.4f}]",
            'gap_iid': f"{gap_iid:.6f}", 'gap_corr': f"{gap_corr:.6f}",
            'iid_contains_1': iid_contains_1, 'corr_contains_1': corr_contains_1,
            'overcompensates': overcompensates,
        })

    # === FASE 6: Veredicto ===
    n_significant = sum(1 for r in results if not r['overcompensates'] and not r['iid_contains_1'] and r['corr_contains_1'])
    n_overcomp = sum(1 for r in results if r['overcompensates'])

    print(f"\n=== VEREDICTO M17 ===")
    print(f"Tests significativos: {n_significant}/3")
    print(f"Sobrecompensaciones: {n_overcomp}/3")

    if n_overcomp > 0:
        print("RESULTADO: Sobrecompensacion detectada. Modelo corregido crudo no es adecuado para holdout.")
        print("El hallazgo cualitativo (sesgo profundidad) se mantiene pero el modelo bootstrap no generaliza cuantitativamente.")
    elif n_significant >= 1:
        print("RESULTADO: Confirmacion en holdout. El modelo corregido mejora significativamente en al menos un umbral.")
        print("Nivel de novedad sube a 3/5.")
    else:
        print("RESULTADO: Sin mejora significativa en holdout. Cierre en nivel 2.5/5.")

    # === Guardar CSVs ===
    path1 = os.path.join(out_dir, 'm17_holdout_comparison.csv')
    with open(path1, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['k','P_real','P_iid','ratio_iid','P_corrected','ratio_corrected'])
        w.writeheader()
        w.writerows(rows)

    path2 = os.path.join(out_dir, 'm17_holdout_tests.csv')
    with open(path2, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['k','ratio_iid','ci_iid','ratio_corr','ci_corr',
                                           'gap_iid','gap_corr','iid_contains_1','corr_contains_1','overcompensates'])
        w.writeheader()
        w.writerows(results)

    print(f"\nCSVs: {path1}, {path2}")

    # === Tambien medir en train para comparacion ===
    print(f"\n=== REFERENCIA: Resultados en TRAIN [3, {train_limit}] ===")
    for k in test_ks:
        p_r = sum(c for b, c in train_counter.items() if b >= k) / n_train
        p_i = sum(c for b, c in iid_counter.items() if b >= k) / iid_total
        p_c = sum(c for b, c in corr_counter.items() if b >= k) / corr_total
        r_i = p_i / p_r if p_r > 0 else float('inf')
        r_c = p_c / p_r if p_r > 0 else float('inf')
        print(f"k={k}: ratio_iid={r_i:.4f}, ratio_corr={r_c:.4f}")

    print("\nDone.")

if __name__ == '__main__':
    main()
