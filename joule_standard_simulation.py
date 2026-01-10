import numpy as np

# PHYSICAL INVARIANTS: THE JOULE STANDARD LABORATORY
K_BIO = 75.0        # Biological metabolic baseline (Watts)
RE_CRIT = 4000      # Social Reynolds Number threshold
THERMAL_LIMIT = 50000  # Filters out non-optimal ratios

def run_selection_experiment(num_agents=10000):
    """
    Final Refinement: Demonstrates the von Karman Attractor 
    by balancing Adaptation Frequency vs. Turbulent Drag.
    """
    ratios = np.random.uniform(1.0, 5.0, num_agents)
    survivors = []

    for ratio in ratios:
        energy_cost_E = 1000.0  
        viscosity = 1.0         
        systemic_heat = 0.0     
        previous_re_soc = 0.0   
        
        for t in range(1, 1001):
            energy_cost_E *= 0.985 # Energy flux drive
            re_soc = (K_BIO / (energy_cost_E + 1e-9)) / viscosity
            
            # 1. NEW: Ongoing Turbulent Drag (lingering penalty)
            # This penalizes high-ratio agents for staying 'coarse' too long.
            if re_soc > RE_CRIT:
                systemic_heat += 8.0 * ((re_soc / RE_CRIT) - 1)**2 # Optimized drag factor
            
            # 2. TRIGGER: Crossing-from-below guard
            if previous_re_soc <= RE_CRIT < re_soc:
                adaptation_cost = 4500 + 500 * np.log(ratio)
                systemic_heat += (re_soc / RE_CRIT)**2 + adaptation_cost
                viscosity /= ratio # Multiplicative refinement (ZFP Shift)
            
            previous_re_soc = re_soc
            
            if systemic_heat > THERMAL_LIMIT: # Great Filter
                break
        else:
            survivors.append(ratio)
            
    return survivors

# Execution: Quantifying the Attractor
survivors = run_selection_experiment()
if survivors:
    print(f"Mean Surviving Ratio (C_acc): {np.mean(survivors):.4f}")
    print(f"Theoretical Attractor (1/kappa): 2.5029")
