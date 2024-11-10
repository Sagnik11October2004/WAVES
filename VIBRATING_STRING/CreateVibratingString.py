import matplotlib.pyplot as plt
import numpy as np
import vstr
# Number oscillators and properties
Nosc = 50
Ms = np.array( [10.0] * Nosc)
Ks = np.array( [1.0] * (Nosc+1))

# Creating the string
s = vstr.string(Nosc, masses=Ms, springs=Ks)
# Initial conditions
Xs  = s.Xs
Y0s = Y0s = 0.5* np.sin(2*np.pi/2 * Xs)
V0s = np.array([0.0] * Nosc)
Ts = np.linspace(0, 5000, 500)
Ys, Vs = s.solved_motion(Ts, Y0s, V0s)
#Plotting initial condition
vstr.plot_string(Xs, Ys[0])

# Plotting string animation
vstr.animate_string(s.Xs, Ys, saveName='VibratingString')
