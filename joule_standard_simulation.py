"""
SOVEREIGN ENGINE: VECTORIZED QUENCH (GA Edition)

import numpy as np
import matplotlib.pyplot as plt

def emergent_optimal_rate(num_decades=25, kappa_proxy=0.4, landauer_weight=0.005):
    """
    Emergent refinement rate minimizing buffer mismatch + regulation cost.
    - kappa_proxy: physical turbulence constant (~0.4, no magic target)
    - Optimum emerges as balance for ~1 effective buffer per decade + cost.
    """
    rates = np.linspace(1.0, 4.0, 1000)  # Fine grid
    # Achieved per-decade buffering = rate * kappa_proxy (self-similarity scaling)
    achieved_per_decade = rates * kappa_proxy
    mismatch = (achieved_per_decade - 1.0)**2 * num_decades  # Ideal ~1 per decade for smooth log-law
    regulation = landauer_weight * rates * np.log(rates + 1.1)  # Strong enough pull
    costs = mismatch + regulation
    min_idx = np.argmin(costs)
    return rates[min_idx], costs[min_idx]

# Single run (default)
min_rate, min_cost = emergent_optimal_rate()
print(f"Emergent optimal rate (default) ≈ {min_rate:.4f}")
print(f"Minimum cost: {min_cost:.6f}\n")

# Sweep robustness: vary decades spanned
decades_range = np.arange(15, 36, 5)
emergent_rates = [emergent_optimal_rate(d)[0] for d in decades_range]

# Plot
plt.figure(figsize=(8, 5))
plt.plot(decades_range, emergent_rates, marker='o', linestyle='-', color='b', label='Emergent Rate')
plt.axhline(y=2.5, color='r', linestyle='--', label='Analytic 1/κ ≈ 2.5')
plt.xlabel('Decades Spanned (Inner to Outer Scales)')
plt.ylabel('Emergent Optimal Refinement Rate')
plt.title('Robustness: Emergent Rate Stable Near ~2.5 Across Ranges')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()  # Or plt.savefig('robustness_plot.png')
