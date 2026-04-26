"""
M18: Ratio modelo_iid/real por rango de n.

Resuelve el hilo suelto de M17: hay cambio de signo del gap entre rangos?

Resultado: NO. El unico efecto significativo es sobreproduccion en n < 2.5M.
Para n > 2.5M, el modelo i.i.d. es estadisticamente indistinguible de la realidad.
"""
import math, random, csv, os
from collections import Counter

LOG32 = math.log(3.0 / 2.0)
LOG2 = math.log(2.0)

def odd_chain_blocks(n, max_blocks=256):
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
        if temp2 < n:
            return b
        current = temp2
    return max_blocks

def main():
    os.makedirs('reports', exist_ok=True)

    # i.i.d. simulation
    print("Simulating 5M i.i.d. chains...")
    rng = random.Random(999)
    iid = Counter()
    for _ in range(5_000_000):
        cum = 0.0
        for b in range(1, 257):
            t = 1
            while rng.random() < 0.5: t += 1
            e = 1
            while rng.random() < 0.5: e += 1
            cum += t * LOG32 - e * LOG2
            if cum < 0:
                iid[b] += 1
                break
        else:
            iid[256] += 1
    iid_tot = sum(iid.values())

    # Real data in 10 bins of 2.5M
    print("Computing real data in 10 bins...")
    bins = []
    boundaries = list(range(0, 25_000_001, 2_500_000))
    for i in range(len(boundaries) - 1):
        lo = max(3, boundaries[i] + 1)
        hi = boundaries[i + 1]
        c = Counter()
        nc = 0
        start = lo if lo % 2 == 1 else lo + 1
        for n in range(start, hi + 1, 2):
            b = odd_chain_blocks(n)
            if b > 0:
                c[b] += 1
                nc += 1
        bins.append((lo, hi, c, nc))
        print(f"  {lo/1e6:.1f}M-{hi/1e6:.1f}M: {nc} chains")

    # Tabulate
    rows = []
    for k in [10, 15, 20, 25]:
        p_i = sum(c for b, c in iid.items() if b >= k) / iid_tot
        for lo, hi, counter, nc in bins:
            hits = sum(c for b, c in counter.items() if b >= k)
            p_r = hits / nc if nc > 0 else 0
            ratio = p_i / p_r if p_r > 0 else 0
            se_r = math.sqrt(p_r * (1 - p_r) / nc) if p_r > 0 else 0
            se_i = math.sqrt(p_i * (1 - p_i) / iid_tot)
            if p_r > 0:
                se_ratio = ratio * math.sqrt((se_r / p_r)**2 + (se_i / p_i)**2)
                cl = ratio - 1.96 * se_ratio
                ch = ratio + 1.96 * se_ratio
            else:
                cl = ch = 0
            rows.append({
                'k': k,
                'range': f'{lo/1e6:.1f}M-{hi/1e6:.1f}M',
                'ln_n_mid': f'{math.log((lo + hi) / 2):.3f}',
                'n_chains': nc,
                'hits': hits,
                'P_real': f'{p_r:.10f}',
                'ratio': f'{ratio:.4f}',
                'ci_lo': f'{cl:.4f}',
                'ci_hi': f'{ch:.4f}',
                'contains_1': 'Y' if cl <= 1.0 <= ch else 'N',
            })

    path = 'reports/m18_ratio_by_range.csv'
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    print(f"\nWritten {len(rows)} rows to {path}")

    # Summary
    print("\n=== SUMMARY ===")
    for k in [10, 15, 20, 25]:
        sig = [r for r in rows if int(r['k']) == k and r['contains_1'] == 'N']
        print(f"k={k}: {len(sig)}/10 bins with ratio significantly != 1.0")
        for r in sig:
            print(f"  {r['range']}: ratio={r['ratio']}, CI=[{r['ci_lo']}, {r['ci_hi']}]")

if __name__ == '__main__':
    main()
