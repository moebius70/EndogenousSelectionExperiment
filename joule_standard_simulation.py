import numpy as np
import matplotlib.pyplot as plt

def cost_for_rate(rate, num_decades=25, kappa_proxy=0.4, landauer_weight=0.005):
    achieved_per_decade = rate * kappa_proxy
    mismatch = (achieved_per_decade - 1.0)**2 * num_decades
    regulation = landauer_weight * rate * np.log(rate + 1.1)
    return mismatch + regulation

def ga_quench(num_agents=10000, generations=30, num_decades=25):
    # Population: initial noisy rates
    rates = np.random.normal(2.5, 1.0, num_agents)  # Broad start
    rates = np.clip(rates, 1.0, 4.0)
    
    for gen in range(generations):
        costs = np.array([cost_for_rate(r, num_decades) for r in rates])
        # Selection: keep low-cost half
        survivors_idx = np.argsort(costs)[:num_agents // 2]
        survivors = rates[survivors_idx]
        # Reproduction + mutation
        rates = np.repeat(survivors, 2)
        rates += np.random.normal(0, 0.05, num_agents)
        rates = np.clip(rates, 1.0, 4.0)
    
    return np.mean(rates), np.var(rates)

# Run GA
mean, var = ga_quench()
print(f"GA converged mean ≈ {mean:.4f}, variance: {var:.2e}")

# (Add sweep/plot as before if needed)
