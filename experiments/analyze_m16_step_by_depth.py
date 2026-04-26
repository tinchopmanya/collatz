"""
M16 paso 2c: distribucion de pasos logaritmicos por profundidad de bloque.

Pregunta: los pasos logaritmicos cambian de distribucion a medida que
avanzamos dentro de una cadena? Si los bloques tardios tienen drift
mas negativo, eso explicaria por que las cadenas reales producen menos
extremos que el modelo i.i.d.

Mide:
  - E[log_step] por profundidad de bloque (bloque 1, 2, 3, ..., 20)
  - E[tail] y E[exit_v2] por profundidad
  - Autocorrelacion lags 1-5
  - Solo cadenas con blocks_to_descend >= 5 para tener suficientes bloques internos
"""
import math
import os
import sys
from collections import defaultdict

def odd_chain_full(n, max_blocks=256):
    """Devuelve lista de (tail, exit_v2, log_step) completa."""
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
        steps.append((tail, exit_v2, log_step))
        if next_odd < n:
            return steps
        current = next_odd
    return steps

def main():
    limit = 5_000_000
    max_depth = 30

    print(f"Analizando pasos por profundidad para impares <= {limit}...")

    # Acumuladores por profundidad
    sum_log = defaultdict(float)
    sum_tail = defaultdict(float)
    sum_exit = defaultdict(float)
    count_at = defaultdict(int)

    # Para autocorrelacion
    lag_pairs = defaultdict(list)  # lag -> list of (x_i, x_{i+lag})

    total_chains = 0

    for n in range(3, limit + 1, 2):
        steps = odd_chain_full(n)
        if not steps:
            continue
        total_chains += 1

        for depth, (tail, ev2, ls) in enumerate(steps):
            if depth < max_depth:
                sum_log[depth] += ls
                sum_tail[depth] += tail
                sum_exit[depth] += ev2
                count_at[depth] += 1

        # Autocorrelacion: recoger pares para lags 1-5
        for lag in range(1, 6):
            for i in range(len(steps) - lag):
                if len(lag_pairs[lag]) < 2_000_000:  # cap para memoria
                    lag_pairs[lag].append((steps[i][2], steps[i+lag][2]))

    print(f"Cadenas totales: {total_chains}")
    print()

    # --- Tabla de drift por profundidad ---
    print("=== DRIFT POR PROFUNDIDAD DE BLOQUE ===")
    print(f"{'Depth':>6} {'Count':>10} {'E[log_step]':>14} {'E[tail]':>10} {'E[exit_v2]':>12} {'Drift vs theo':>14}")
    mu_theo = 2*math.log(3.0/4.0)

    for d in range(min(max_depth, 25)):
        if count_at[d] == 0:
            break
        ml = sum_log[d] / count_at[d]
        mt = sum_tail[d] / count_at[d]
        me = sum_exit[d] / count_at[d]
        diff = ml - mu_theo
        print(f"{d+1:>6} {count_at[d]:>10} {ml:>14.8f} {mt:>10.6f} {me:>12.6f} {diff:>14.8f}")

    # --- Autocorrelacion por lag ---
    print(f"\n=== AUTOCORRELACION POR LAG ===")
    print(f"{'Lag':>5} {'N pairs':>10} {'Corr':>12}")
    for lag in range(1, 6):
        pairs = lag_pairs[lag]
        if len(pairs) < 100:
            continue
        n_p = len(pairs)
        mx = sum(p[0] for p in pairs) / n_p
        my = sum(p[1] for p in pairs) / n_p
        cov = sum((p[0]-mx)*(p[1]-my) for p in pairs) / n_p
        sx = math.sqrt(sum((p[0]-mx)**2 for p in pairs) / n_p)
        sy = math.sqrt(sum((p[1]-my)**2 for p in pairs) / n_p)
        corr = cov / (sx * sy) if sx > 0 and sy > 0 else 0
        print(f"{lag:>5} {n_p:>10} {corr:>12.8f}")

    # --- Diagnostico ---
    print(f"\n=== DIAGNOSTICO ===")

    # Comparar drift del bloque 1 vs bloques 5-10
    if count_at[0] > 0 and count_at[5] > 0:
        drift_1 = sum_log[0] / count_at[0]
        # Promedio de bloques 5-9 (depth 4-8)
        sum_late = sum(sum_log[d] for d in range(4, min(9, max_depth)) if count_at[d] > 0)
        cnt_late = sum(count_at[d] for d in range(4, min(9, max_depth)) if count_at[d] > 0)
        if cnt_late > 0:
            drift_late = sum_late / cnt_late
            print(f"Drift bloque 1:     {drift_1:.8f}")
            print(f"Drift bloques 5-9:  {drift_late:.8f}")
            print(f"Diferencia:         {drift_late - drift_1:.8f}")
            if drift_late < drift_1 - 0.01:
                print("  -> Bloques tardios tienen drift MAS NEGATIVO.")
                print("  -> Esto explica parcialmente la sobreproduccion de extremos:")
                print("     las cadenas largas acumulan pasos con drift mas contractivo.")
            elif abs(drift_late - drift_1) < 0.01:
                print("  -> Drift similar entre bloques tempranos y tardios.")
                print("  -> La profundidad NO es el factor principal.")
            else:
                print("  -> Bloques tardios tienen drift MENOS negativo (inesperado).")

if __name__ == '__main__':
    main()
