import numpy as np
import matplotlib.pyplot as plt

# Define parameters
m = 1.0       # mass
k = 1.0       # spring constant
omega_res = np.sqrt(k / m)  # natural frequency
omega_range = np.linspace(0.5 * omega_res, 1.5 * omega_res, 500)  # range of driving frequencies

# Define multiple values of F0 and gamma
F0_values = [0.5, 1.0, 1.5]   # Different amplitudes of driving force
gamma_values = [0.1, 0.2, 0.3]  # Different damping coefficients

# Plot resonance curves
plt.figure(figsize=(10, 6))
for F0 in F0_values:
    for gamma in gamma_values:
        # Compute amplitude A(omega) for each driving frequency in omega_range
        amplitude = F0 / np.sqrt((k - m * omega_range**2)**2 + (gamma * omega_range)**2)
        
        # Plot the resonance curve
        label = f'F0 = {F0}, gamma = {gamma}'
        plt.plot(omega_range, amplitude, label=label)

# Customize the plot
plt.title("Resonance Curves for Forced Damped Oscillators")
plt.xlabel("Driving Frequency (ω)")
plt.ylabel("Amplitude (A)")
plt.legend(loc="upper right")
plt.grid(True)
plt.savefig("resonance_curve.png")
plt.show()


