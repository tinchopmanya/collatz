"""
M16 paso 3b: test de circularidad via split interno.

Calibrar modelo corregido con primera mitad (n <= 2.5M).
Evaluar contra segunda mitad (2.5M < n <= 5M).
Si el modelo corregido cierra el gap en la segunda mitad,
no es circularidad.
"""
import math, random, csv, os
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
    cum = 0.0
    for b in range(max_blocks):
        tail = 1
        while rng.random() < 0.5: tail += 1
        exit_v2 = 1
        while rng.random() < 0.5: exit_v2 += 1
        cum += tail * math.log(3.0/2.0) - exit_v2 * math.log(2.0)
        if cum < 0: return b + 1
    return max_blocks

def simulate_depth_bootstrap(rng, steps_by_depth, max_d, max_blocks=256):
    cum = 0.0
    for d in range(max_blocks):
        dk = min(d, max_d - 1)
        pool = steps_by_depth[dk]
        if not pool:
            tail = 1
            while rng.random() < 0.5: tail += 1
            exit_v2 = 1
            while rng.random() < 0.5: exit_v2 += 1
            step = tail * math.log(3.0/2.0) - exit_v2 * math.log(2.0)
        else:
            step = rng.choice(pool)
        cum += step
        if cum < 0: return d + 1
    return max_blocks

def collect_data(lo, hi):
    steps_by_depth = defaultdict(list)
    blocks_counter = Counter()
    n_chains = 0
    for n in range(lo if lo % 2 == 1 else lo + 1, hi + 1, 2):
        steps = odd_chain_full(n)
        if not steps: continue
        n_chains += 1
        blocks_counter[len(steps)] += 1
        for d, s in enumerate(steps):
            if d < 50:
                steps_by_depth[d].append(s)
    return steps_by_depth, blocks_counter, n_chains

def main():
    seed = 20260425
    n_sim = 1_250_000

    # --- Calibrar con primera mitad ---
    print("Recolectando primera mitad (3 <= n <= 2500000) para calibracion...")
    cal_steps, cal_blocks, cal_n = collect_data(3, 2_500_000)
    max_d = max(d for d in cal_steps if len(cal_steps[d]) >= 50) + 1
    print(f"  Cadenas calibracion: {cal_n}, profundidad max: {max_d}")

    # --- Evaluar contra segunda mitad ---
    print("Recolectando segunda mitad (2500001 <= n <= 5000000) para evaluacion...")
    _, eval_blocks, eval_n = collect_data(2_500_001, 5_000_000)
    print(f"  Cadenas evaluacion: {eval_n}")

    # --- Simular modelos ---
    print(f"Simulando {n_sim} cadenas i.i.d....")
    rng1 = random.Random(seed)
    iid_counter = Counter()
    for _ in range(n_sim):
        iid_counter[simulate_iid(rng1)] += 1

    print(f"Simulando {n_sim} cadenas corregidas (calibradas en primera mitad)...")
    rng2 = random.Random(seed + 1)
    corr_counter = Counter()
    for _ in range(n_sim):
        corr_counter[simulate_depth_bootstrap(rng2, cal_steps, max_d)] += 1

    # --- Comparar en segunda mitad ---
    eval_total = sum(eval_blocks.values())
    iid_total = sum(iid_counter.values())
    corr_total = sum(corr_counter.values())

    print(f"\n=== VALIDACION EN SEGUNDA MITAD (out-of-sample) ===")
    print(f"{'k':>5} {'P_eval':>12} {'P_iid':>12} {'R_iid':>8} {'P_corr':>12} {'R_corr':>8}")

    for k in [5, 10, 15, 20, 25, 30]:
        p_e = sum(c for b, c in eval_blocks.items() if b >= k) / eval_total
        p_i = sum(c for b, c in iid_counter.items() if b >= k) / iid_total
        p_c = sum(c for b, c in corr_counter.items() if b >= k) / corr_total
        r_i = p_i / p_e if p_e > 0 else 0
        r_c = p_c / p_e if p_e > 0 else 0
        print(f"{k:>5} {p_e:>12.8f} {p_i:>12.8f} {r_i:>8.4f} {p_c:>12.8f} {r_c:>8.4f}")

    print(f"\n=== DIAGNOSTICO ===")
    for k in [20, 30]:
        p_e = sum(c for b, c in eval_blocks.items() if b >= k) / eval_total
        p_i = sum(c for b, c in iid_counter.items() if b >= k) / iid_total
        p_c = sum(c for b, c in corr_counter.items() if b >= k) / corr_total
        if p_e > 0:
            gap_i = abs(p_i/p_e - 1)
            gap_c = abs(p_c/p_e - 1)
            red = 1 - gap_c/gap_i if gap_i > 0 else 0
            print(f"k={k}: gap i.i.d.={gap_i:.4f}, gap corregido={gap_c:.4f}, reduccion={red:.1%}")

if __name__ == '__main__':
    main()
