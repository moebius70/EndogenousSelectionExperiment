import numpy as np

# PHYSICAL INVARIANTS (The Joule Standard)
K_BIO = 75.0        # Biological metabolic baseline (Watts)
RE_CRIT = 4000      # Social Reynolds Number transition threshold
THERMAL_LIMIT = 20000  # Increased limit to allow for deep-time scaling

def run_selection_experiment(num_agents=10000):
    """
    Revised Numerical Wind Tunnel:
    Uses MULTIPLICATIVE REFINEMENT to show 1/kappa (~2.5) as 
    the stable compromise between frequent cheap reorgs and rare costly ones.
    """
    ratios = np.random.uniform(1.0, 5.0, num_agents)
    survivors = []

    for ratio in ratios:
        energy_cost_E = 1000.0  # Initial Energy Cost
        viscosity = 1.0         # Initial friction
        systemic_heat = 0.0     
        
        for t in range(1, 1001):
            energy_cost_E *= 0.985 # Modeled energy flux acceleration
            
            # Re_soc = momentum / (friction * current_granularity)
            re_soc = (K_BIO / (energy_cost_E + 1e-9)) / viscosity
            
            # TRIGGER: If flow becomes too turbulent, refine substrate
            if re_soc > RE_CRIT:
                # 1. Apply adaptation cost (log-proportional to ratio)
                adaptation_cost = np.log(ratio)
                
                # 2. Apply quadratic turbulence penalty ONLY at transition
                # This simulates the 'heat' of a substrate collapse (e.g., 1971)
                systemic_heat += (re_soc / RE_CRIT)**2 + adaptation_cost
                
                # 3. FIXED: Multiplicative viscosity reduction (Progressive Refinement)
                # This allows the system to stay 'cool' by increasing resolution
                viscosity /= ratio 
            
            # SYSTEMIC MELTING: Filter agents exceeding thermal capacity
            if systemic_heat > THERMAL_LIMIT:
                break
        else:
            survivors.append(ratio)
            
    return survivors

# Execution: Quantifying the Attractor
surviving_population = run_selection_experiment()
if surviving_population:
    print(f"Mean Surviving Ratio (C_acc): {np.mean(surviving_population):.4f}")
