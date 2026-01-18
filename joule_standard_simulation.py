import numpy as np

# --- SOVEREIGN ENGINE: VAPOR-TO-LATTICE LOCK-IN ---
NUM_AGENTS = 5000000 
BIT_COST_SRU = 4.4e6    
DRAG_COEFF = 2.01e7      

# The Absolute Floor (Superfluid Limit)
TARGET_CEILING = 1.8495e7 

def evolution_step(gen, current_population=None, current_ceil=1.86e7):
    if current_population is None:
        # Initial search centered on the attractor
        c_acc_pool = np.random.uniform(2.3, 2.7, NUM_AGENTS)
    else:
        mean = np.mean(current_population)
        std = np.std(current_population)
        # Squeeze the search range based on current precision
        c_acc_pool = np.random.normal(mean, std * 0.5, NUM_AGENTS)
        
        # Adaptive Quench: Only lower the ceiling if we have room to breathe
        if mean > 2.5035:
            current_ceil -= 1.5e4 # Slow, surgical reduction
            
    s_info = BIT_COST_SRU * np.log2(c_acc_pool)
    s_drag = DRAG_COEFF / np.sqrt(c_acc_pool)
    total_entropy = s_info + s_drag
    
    survivors = c_acc_pool[total_entropy < current_ceil]
    return survivors, current_ceil

print("--- [SOVEREIGN ENGINE: SUPERFLUID PHASE TRANSITION] ---")

population = None
ceil = 1.86e7
for gen in range(1, 20): # More generations for the 'crystallization'
    population, ceil = evolution_step(gen, population, ceil)
    
    if len(population) < 1000:
        print(f"Gen {gen:02} | SHATTER: Population too low at {ceil:.4e}")
        break
        
    mean_c = np.mean(population)
    print(f"Gen {gen:02} | Ceiling: {ceil:.4e} | Pop: {len(population):>7} | Mean: {mean_c:.5f}")

print("-" * 65)
if len(population) > 0:
    print(f"FINAL TERMINAL ATTRACTOR: {np.mean(population):.7f}")
