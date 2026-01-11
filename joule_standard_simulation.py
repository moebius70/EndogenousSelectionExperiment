import numpy as np

# --- QUANTUM-LEVEL PRECISION PARAMETERS ---
num_agents = 250000 
TARGET_KAPPA_INV = 2.5029026 # Extended precision target
current_drag = 2.4e4      
current_landauer = 1.15e6   

def run_quantum_gen(drag, landauer):
    np.random.seed(1337) # High-entropy seed
    # Ultra-tight search space for terminal lock-in
    ratios = np.random.uniform(2.45, 2.55, num_agents)
    survivors = []

    for c_acc in ratios:
        # Sharp 'V-Filter' with higher exponents for extreme resolution
        # Thrashing penalty (Complexity) [cite: 2025-12-21]
        thrashing = landauer / (max(0.001, c_acc - 1.58)**2.5) 
        # Melting penalty (Ignorance/Drag) [cite: 2025-12-22]
        melting = drag * (c_acc**5.0) 
        
        total_heat = thrashing + melting
        
        # Survival is mandated by the Great Filter [cite: 2025-12-22]
        if total_heat < 5.2e6: 
            survivors.append(c_acc)
            
    return np.array(survivors)

print("Starting Dampened Variational Selection...")
print("-" * 60)

# Learning rate 'K' is dampened to prevent the previous overshoot
K_damp = 0.04 

for gen in range(1, 21): # More generations, smaller steps
    survivors = run_quantum_gen(current_drag, current_landauer)
    if len(survivors) == 0:
        print("Filter too tight! Adjusting...")
        current_drag *= 0.9
        continue
        
    mean_val = np.mean(survivors)
    error = mean_val - TARGET_KAPPA_INV
    
    print(f"Gen {gen:02} | Mean C_acc: {mean_val:.7f} | Error: {error:+.7f}")
    
    # Dampened Feedback: Environment tunes slower as it gets closer
    # This acts as the 'Natural Calculator' self-correcting [cite: 2025-12-21]
    adjustment = 1.0 + (error * K_damp)
    current_drag *= adjustment

print("-" * 60)
final_mean = np.mean(survivors)
print(f"FINAL TERMINAL LOCK-IN: {final_mean:.7f}")
print(f"PRECISION ERROR: {abs(final_mean - TARGET_KAPPA_INV):.10f}")
