"""
M16 paso 2b: descomponer la sobreproduccion de extremos.

Hipotesis competidoras para el gap modelo/real en colas:
  H1: el drift empirico es mas negativo que el teorico (sesgo de muestreo finito)
  H2: la varianza empirica difiere de la teorica
  H3: hay correlaciones entre pasos consecutivos que el modelo i.i.d. ignora
  H4: la distribucion de pasos no es la geometrica pura (colas mas pesadas o livianas)

Este script mide:
  1. Drift y varianza teoricos vs empiricos
  2. Autocorrelacion lag-1 de los pasos logaritmicos
  3. Distribucion empirica de tail y exit_v2 vs geometrica
  4. Skewness y kurtosis de los pasos
"""
import math
import os
import sys
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def odd_chain_steps(n, max_blocks=256):
    """Devuelve lista de (tail, exit_v2, log_step) para la cadena odd-to-odd."""
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
    limit = 1_000_000
    print(f"Analizando pasos logaritmicos para impares <= {limit}...")

    all_tails = []
    all_exits = []
    all_logsteps = []
    # Para autocorrelacion: pares consecutivos dentro de cada cadena
    consec_pairs = []

    for n in range(3, limit + 1, 2):
        steps = odd_chain_steps(n)
        for tail, ev2, ls in steps:
            all_tails.append(tail)
            all_exits.append(ev2)
            all_logsteps.append(ls)
        for i in range(len(steps) - 1):
            consec_pairs.append((steps[i][2], steps[i+1][2]))

    N = len(all_logsteps)

    # --- Momentos empiricos ---
    mu = sum(all_logsteps) / N
    var = sum((s - mu)**2 for s in all_logsteps) / N
    m3 = sum((s - mu)**3 for s in all_logsteps) / N
    m4 = sum((s - mu)**4 for s in all_logsteps) / N
    skew = m3 / var**1.5
    kurt = m4 / var**2 - 3  # excess kurtosis

    # --- Momentos teoricos ---
    # tail ~ Geom(1/2): E[tail] = 2, Var[tail] = 2
    # exit_v2 ~ Geom(1/2): E[ev2] = 2, Var[ev2] = 2
    # log_step = tail * log(3/2) - ev2 * log(2)
    log32 = math.log(3.0/2.0)
    log2 = math.log(2.0)
    mu_theo = 2*log32 - 2*log2
    var_theo = 2*log32**2 + 2*log2**2  # Var[a*X - b*Y] = a^2 Var[X] + b^2 Var[Y]

    print(f"\n=== MOMENTOS ===")
    print(f"{'':>20} {'Empirico':>14} {'Teorico':>14} {'Diff':>14}")
    print(f"{'Drift (mu)':>20} {mu:>14.8f} {mu_theo:>14.8f} {mu-mu_theo:>14.8f}")
    print(f"{'Varianza':>20} {var:>14.8f} {var_theo:>14.8f} {var-var_theo:>14.8f}")
    print(f"{'Skewness':>20} {skew:>14.8f} {'--':>14}")
    print(f"{'Excess kurtosis':>20} {kurt:>14.8f} {'--':>14}")

    # --- Medias de tail y exit_v2 ---
    mu_tail = sum(all_tails) / N
    mu_exit = sum(all_exits) / N
    var_tail = sum((t - mu_tail)**2 for t in all_tails) / N
    var_exit = sum((e - mu_exit)**2 for e in all_exits) / N

    print(f"\n=== COMPONENTES ===")
    print(f"{'':>20} {'Empirico':>14} {'Teorico':>14} {'Diff':>14}")
    print(f"{'E[tail]':>20} {mu_tail:>14.8f} {'2.00000000':>14} {mu_tail-2:>14.8f}")
    print(f"{'E[exit_v2]':>20} {mu_exit:>14.8f} {'2.00000000':>14} {mu_exit-2:>14.8f}")
    print(f"{'Var[tail]':>20} {var_tail:>14.8f} {'2.00000000':>14} {var_tail-2:>14.8f}")
    print(f"{'Var[exit_v2]':>20} {var_exit:>14.8f} {'2.00000000':>14} {var_exit-2:>14.8f}")

    # --- Autocorrelacion lag-1 ---
    if consec_pairs:
        n_pairs = len(consec_pairs)
        mean_x = sum(p[0] for p in consec_pairs) / n_pairs
        mean_y = sum(p[1] for p in consec_pairs) / n_pairs
        cov_xy = sum((p[0]-mean_x)*(p[1]-mean_y) for p in consec_pairs) / n_pairs
        std_x = math.sqrt(sum((p[0]-mean_x)**2 for p in consec_pairs) / n_pairs)
        std_y = math.sqrt(sum((p[1]-mean_y)**2 for p in consec_pairs) / n_pairs)
        autocorr = cov_xy / (std_x * std_y) if std_x > 0 and std_y > 0 else 0
        print(f"\n=== AUTOCORRELACION ===")
        print(f"Pares consecutivos: {n_pairs}")
        print(f"Autocorrelacion lag-1: {autocorr:.8f}")
        print(f"  (0 = independiente, negativo = anti-persistencia)")
        if abs(autocorr) < 0.01:
            print(f"  -> Correlacion despreciable. H3 pierde fuerza.")
        elif autocorr < -0.01:
            print(f"  -> Anti-correlacion detectada. H3 tiene soporte.")
        else:
            print(f"  -> Correlacion positiva. Inesperado si hay anti-persistencia.")

    # --- Distribucion de tail: comparar con geometrica ---
    from collections import Counter
    tail_counts = Counter(all_tails)
    exit_counts = Counter(all_exits)

    print(f"\n=== DISTRIBUCION DE TAIL vs GEOMETRICA ===")
    print(f"{'k':>5} {'P_emp(tail=k)':>16} {'P_geom(k)':>12} {'Ratio':>10}")
    for k in range(1, 11):
        p_emp = tail_counts.get(k, 0) / N
        p_geom = 2**(-k)
        ratio = p_emp / p_geom if p_geom > 0 else 0
        print(f"{k:>5} {p_emp:>16.8f} {p_geom:>12.8f} {ratio:>10.6f}")

    print(f"\n=== DISTRIBUCION DE EXIT_V2 vs GEOMETRICA ===")
    print(f"{'k':>5} {'P_emp(ev2=k)':>16} {'P_geom(k)':>12} {'Ratio':>10}")
    for k in range(1, 11):
        p_emp = exit_counts.get(k, 0) / N
        p_geom = 2**(-k)
        ratio = p_emp / p_geom if p_geom > 0 else 0
        print(f"{k:>5} {p_emp:>16.8f} {p_geom:>12.8f} {ratio:>10.6f}")

    # --- Diagnostico final ---
    print(f"\n=== DIAGNOSTICO CLAVE M16 ===")
    drift_gap = mu - mu_theo
    print(f"1. Gap de drift: {drift_gap:.8f}")
    if abs(drift_gap) > 0.001:
        print(f"   El drift empirico es MAS NEGATIVO que el teorico.")
        print(f"   Esto por si solo produce menos cadenas largas reales vs modelo.")
        print(f"   Causa probable: sesgo de supervivencia o seleccion por n finito.")
    else:
        print(f"   Gap de drift despreciable.")

    print(f"\n2. Autocorrelacion: {autocorr:.8f}")
    if autocorr < -0.005:
        print(f"   HAY anti-correlacion entre pasos consecutivos.")
        print(f"   Esto es una restriccion que el modelo i.i.d. no captura.")
    else:
        print(f"   Sin anti-correlacion significativa.")

if __name__ == '__main__':
    main()
