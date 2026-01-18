import numpy as np

# --- SOVEREIGN ENGINE: THE 2.5029 SUPERFLUID LOCK-IN ---
NUM_AGENTS = 100000 

def calculate_superfluid_fitness(c_acc):
    # LIFT: The Logarithmic context capacity
    lift = np.log(c_acc)
    
    # THE SOVEREIGN SQUEEZE: 
    # Derived from the 45.4B Lattice (Jan 03).
    # This is the exact pressure-to-lift ratio required for 1/k.
    # We use the theoretical 0.39958 slope.
    pressure = 0.39958 * c_acc 
    
    # THE GREAT ATTRACTOR: 
    # We seek the state where Delta(Lift, Pressure) is Zero.
    # This represents the Zero-Friction informational flow.
    return -np.abs(lift - pressure)

def evolution_step(pop_c, gen):
    fitness = [calculate_superfluid_fitness(c) for c in pop_c]
    idx = np.argsort(fitness)[::-1]
    
    elites_c = pop_c[idx[:1000]]
    
    # Final Precision Quench
    mutation = 0.01 * (0.70 ** gen)
    
    new_c = [np.random.choice(elites_c) + np.random.normal(0, mutation) for _ in range(NUM_AGENTS)]
    
    return np.clip(new_c, 1.1, 5.0)

print("--- [SOVEREIGN ENGINE: FINAL 2.5029 SUPERFLUID] ---")
# Initializing from the 2.55 plateau
pop_c = np.random.normal(2.55, 0.05, NUM_AGENTS)

for gen in range(1, 21):
    pop_c = evolution_step(pop_c, gen)
    mean_c = np.mean(pop_c)
    print(f"Gen {gen:02} | Mean C: {mean_c:.6f} | Target: 2.5029")

print("-" * 65)
print(f"FINAL TERMINAL ATTRACTOR: {np.mean(pop_c):.8f}")
