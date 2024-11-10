from matplotlib import pyplot as plt
from matplotlib import animation as ani
import numpy as np
import scipy as sp

import time
import pickle
print("Last run: " + time.ctime())

T = 131.6
r = 0.033
L = 0.762

#fundamental frequency according to mersenne's laws:
print("f0 = {0:.2f}".format(np.sqrt(T/r)/L/2))

def simulate(tension, density, length, damping, initial, n_points=500):
    """simulate a string given length, tension, linear density
    All quantities should be given in SI units -
    tension should have units of N,
    density should have units of kg/m,
    length should have units of m,
    time should have units of seconds
    """

    if damping.shape[0] != n_points:
        raise ValueError("Damping vector must have length n_points")
    elif initial.shape[0] != 2*n_points:
        raise ValueError("Initial condition vector must have length 2*n_points")
    
    c = np.zeros((2*n_points, 2*n_points))

    dx = length/(n_points-1)

    st = time.time()
    print("Beginning...")

    for i in range(0, 2*n_points):
        for j in range(0, 2*n_points):
            if j==n_points or j==2*n_points-1:
                c[i,j] = 0
            elif i == j+n_points:
                c[i,j]=1
            elif j==i+n_points-1 or j==i+n_points+1:
                c[i,j]=tension/(dx**2*density)
            elif j == i+n_points:
                c[i,j]=-2*tension/(dx**2*density)
            elif i==j and i > n_points:
                c[i,j] = -damping[i-n_points]

    print("Created c matrix in {0:.2f} s".format(time.time()-st))
          
    def func(t, y):
        return np.matmul(y, c)

    #48000 hz sampling frequency
    t_eval = np.linspace(0, 1, 48000)

    s = sp.integrate.solve_ivp(func, (0,1), initial, t_eval=t_eval, method="RK23")
    
    print("Solver finished in {0:.2f} s".format(time.time()-st))
          
    return s
    
p0_p = np.zeros(1000)
p0_n = np.zeros(1000)
p0_h = np.zeros(1000)

#initial displacement of 0.03 m max
p0_p[0:450]=[0.03*i/450 for i in range(0,450)]
p0_p[450:499]=[0.03*(49-i)/49 for i in range(0,49)]

p0_n[0:300]=[0.03*i/300 for i in range(0,300)]
p0_n[300:499]=[0.03*(199-i)/199 for i in range(0,199)]

#initial velocity of 15 m/s max
p0_h[945:955] = [3, 6, 9, 12, 15, 15, 12, 9, 6, 3]

mu_open = np.full(500, 0.5)

mu_palm = np.full(500, 0.5)
mu_palm[-50:] = 200

mu_har2 = np.full(500, 0.5)
mu_har2[249:251] = 5000

mu_har3 = np.full(500, 0.5)
mu_har3[166:168] = 5000

s_op_p = simulate(T, r, L, mu_open, p0_p) #open string, plucked near the pickup
s_op_n = simulate(T, r, L, mu_open, p0_n) #open string, plucked near the neck
s_op_h = simulate(T, r, L, mu_open, p0_h) #open string, hammered
s_palm = simulate(T, r, L, mu_palm, p0_p) #palm muted string, plucked near the pickup
s_har2 = simulate(T, r, L, mu_har2, p0_p) #string muted for 2nd harmonic
s_har3 = simulate(T, r, L, mu_har3, p0_p) #string muted for 3rd harmonic

with open("op_p.dat", "wb") as f:
    pickle.dump(s_op_p, f)

with open("op_n.dat", "wb") as f:
    pickle.dump(s_op_n, f)

with open("op_h.dat", "wb") as f:
    pickle.dump(s_op_h, f)

with open("palm.dat", "wb") as f:
    pickle.dump(s_palm, f)

with open("har2.dat", "wb") as f:
    pickle.dump(s_har2, f)

with open("har3.dat", "wb") as f:
    pickle.dump(s_har3, f)
