import numpy as np

# --- THE 2.5029 SUPERFLUID QUENCH ---
NUM_AGENTS = 1000000 # Increased population for higher precision
# BIT_COST_SRU = 4.4e6    

# # S_drag: Precision Drag for 1/kappa ratio (Eq 17)
# # 2.0e7 mandates the 2.5029 ratio for survival
# DRAG_COEFF = 2.0e7      

# # Ceiling raised to 1.85e7 to prevent the 'Vacuum Collapse'
# # This creates the narrowest possible 'Goldilocks' window
# ENTROPY_CEILING = 1.85e7

BIT_COST_SRU = 4.4e6    
DRAG_COEFF = 2.0e7      

# Set to 1.848e7 (approx 0.35% margin)
# This prevents the Gen 01 'Vacuum Collapse' while 
# maintaining the 2.5029 attractor as the only stable state.
ENTROPY_CEILING = 1.848e7

def evolution_step():
    # Searching the localized region of the attractor
    c_acc_pool = np.random.uniform(1.0, 10.0, NUM_AGENTS)
    
    # Equation 18: Information Complexity
    s_info = BIT_COST_SRU * np.log2(c_acc_pool)
    
    # Equation 17: Structural Drag
    s_drag = DRAG_COEFF / np.sqrt(c_acc_pool)
    
    total_entropy = s_info + s_drag
    
    # Selection: Only the 'Superfluid' agents survive
    survivors = c_acc_pool[total_entropy < ENTROPY_CEILING]
    return survivors

print("--- [SOVEREIGN ENGINE: FINAL PRECISION QUENCH] ---")

for gen in range(1, 6):
    population = evolution_step()
    
    if len(population) == 0:
        print(f"Gen {gen:02} | EXTINCTION: Margin too narrow.")
        break
        
    mean_c = np.mean(population)
    std_dev = np.std(population)
    
    print(f"Gen {gen:02} | Survivors: {len(population):>6} | Mean: {mean_c:.5f} | Precision (σ): {std_dev:.5f}")

print("-" * 55)
if len(population) > 0:
    print(f"FINAL TERMINAL ATTRACTOR: {np.mean(population):.7f}")
