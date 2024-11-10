
from matplotlib import pyplot as plt
import numpy as np
import scipy as sp

import time
import pickle

plt.rcParams["font.family"]="serif"
plt.rcParams["mathtext.fontset"]="dejavuserif"

with open("op_p.dat", "rb") as f:
    s_op_p = pickle.load(f)

with open("op_n.dat", "rb") as f:
    s_op_n = pickle.load(f)

with open("op_h.dat", "rb") as f:
    s_op_h = pickle.load(f)

with open("palm.dat", "rb") as f:
    s_palm = pickle.load(f)

with open("har2.dat", "rb") as f:
    s_har2 = pickle.load(f)

with open("har3.dat", "rb") as f:
    s_har3 = pickle.load(f)

f, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=6, figsize=(8, 12), layout="constrained")

ax1.plot(s_op_p["t"], s_op_p["y"][400,:])
ax2.plot(s_op_n["t"], s_op_n["y"][400,:])
ax3.plot(s_op_h["t"], s_op_h["y"][400,:])
ax4.plot(s_palm["t"], s_palm["y"][400,:])
ax5.plot(s_har2["t"], s_har2["y"][400,:])
ax6.plot(s_har3["t"], s_har3["y"][400,:])

for a in (ax1, ax2, ax3, ax4, ax5, ax6):
    a.grid(True)
    #a.set_xlim(0.5, 0.53)
    a.set_xlabel("Time, s")

plt.savefig("analysis_images/waveform_long.png", dpi=100)

f, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=6, figsize=(8, 12), layout="constrained")

ax1.plot(s_op_p["t"], s_op_p["y"][400,:])
ax2.plot(s_op_n["t"], s_op_n["y"][400,:])
ax3.plot(s_op_h["t"], s_op_h["y"][400,:])
ax4.plot(s_palm["t"], s_palm["y"][400,:])
ax5.plot(s_har2["t"], s_har2["y"][400,:])
ax6.plot(s_har3["t"], s_har3["y"][400,:])

for a in (ax1, ax2, ax3, ax4, ax5, ax6):
    a.grid(True)
    a.set_xlim(0.5, 0.53)
    a.set_xlabel("Time, s")

plt.savefig("analysis_images/waveform_small.png", dpi=100)

f, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=6, layout="constrained", figsize=(8, 12))

ft_op_p=sp.fft.fft(s_op_p["y"][400,:])
ft_op_n=sp.fft.fft(s_op_n["y"][400,:])
ft_op_h=sp.fft.fft(s_op_h["y"][400,:])
ft_palm=sp.fft.fft(s_palm["y"][400,:])
ft_har2=sp.fft.fft(s_har2["y"][400,:])
ft_har3=sp.fft.fft(s_har3["y"][400,:])


ax1.plot(np.arange(500), np.absolute(ft_op_p)[0:500])
ax2.plot(np.arange(500), np.absolute(ft_op_n)[0:500])
ax3.plot(np.arange(500), np.absolute(ft_op_h)[0:500])
ax4.plot(np.arange(500), np.absolute(ft_palm)[0:500])
ax5.plot(np.arange(500), np.absolute(ft_har2)[0:500])
ax6.plot(np.arange(500), np.absolute(ft_har3)[0:500])

for a in (ax1, ax2, ax3, ax4, ax5, ax6):
    a.set_xlim(left=0, right=500)
    #a.set_yscale("log")
    #a.set_ylim(bottom=10**-4.1)
    a.grid(True)
    #because the simulation duration is 1 second, frequencies are in units of Hz
    a.set_xlabel("f, Hz")
    a.set_ylabel("Amplitude")

plt.savefig("analysis_images/fft_lin.png", dpi=500)
