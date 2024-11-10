import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import time

epsilon_0 = 8.854187817620389e-12
mu_0 = 4 * np.pi * 1e-7


class Medium:
    """docstring for Medium"""
    def __init__(self, epsilon_r, mu_r, sigma):
        self._epsilon_r = epsilon_r
        self._mu_r = mu_r
        self._sigma = sigma

    def epsilon_eq(self, wave):
        """
        dielectric constant [F/m]
        """
        return epsilon_0 * self._epsilon_r * (1 + self._sigma / (1j * wave._omega * epsilon_0 * self._epsilon_r))

    def mu_eq(self):
        """
        magnetic constant [H/m]
        """
        return mu_0 * self._mu_r

    def zeta_eq(self, wave):
        """
        characteristic impedance [Ω]
        """
        return (self.mu_eq() / self.epsilon_eq(wave)) ** 0.5

    def type(self, wave):
        U = self._sigma / (wave._omega * epsilon_0 * self._epsilon_r)
        _type = 'Good conductor' if (U >= 1e2) else 'Dielectric' if (U < 1e2 and U >= 1e-2) else 'Insulator'
        return (U, _type)
    
    def __repr__(self):
        return f"<epsilon_r={self._epsilon_r}, mu_r={self._mu_r}, sigma={self._sigma}>"

class Wave:
    def __init__(self, f=1.8e9, A=10):
        self._f = f             # [Hz]
        self._omega = 2 * np.pi * f     # [rad/s]
        self._A = A             # [V/m]
        self._medium1 = Medium(epsilon_r=1, mu_r=1, sigma=0) # vacuum is the default
        self._medium2 = self._medium1

    def add_mediums(self, medium1, medium2):
        self._medium1 = medium1
        self._medium2 = medium2
        
    def k(self, medium):
        """
        wavenumber [1/m]
        """
        return self._omega * np.sqrt(medium.mu_eq() * medium.epsilon_eq(self))

    def gamma(self, medium1, medium2):
        """
        reflection coefficient
        """
        return (medium2.zeta_eq(self) - medium1.zeta_eq(self)) / (medium2.zeta_eq(self) + medium1.zeta_eq(self))

    def tau(self, medium1, medium2):
        """
        transmission coefficient
        """
        return 2 * medium2.zeta_eq(self) / (medium2.zeta_eq(self) + medium1.zeta_eq(self))

    def delta(self, medium2):
        """
        skin depth
        """
        alpha = self.k(medium2).imag
        return -1 / alpha if alpha != 0 else np.inf

    def v(self, medium):
        """
        signal velocity [m/s]
        """
        return (1 / np.sqrt(medium.epsilon_eq(self) * medium.mu_eq())).real

    def lambda_(self, medium):
        """
        wavelength [m]
        """
        return self.v(medium) / self._f

    def power_density_inc(self, medium):
        return 0.5 * 1 / abs(medium.zeta_eq(self)) * abs(self._A) ** 2

    def power_density_trans(self, medium1, medium2):
        return self.power_density_inc(medium1) * (1 - (abs(self.gamma(medium1, medium2))) ** 2)

    def __repr__(self):
        return f"Wave: f = {self._f} Hz; A = {self._A}"

    def print_data(self):
        print(f"U_1 := sigma_1/(omega*epsilon_0*epsilon_r_1) = {self._medium1.type(self)[0]:.4g}  ==> medium 1 is a(n) \033[92m{self._medium1.type(self)[1]}\x1b[0m")
        print(f"U_2 := sigma_2/(omega*epsilon_0*epsilon_r_2) = {self._medium2.type(self)[0]:.4g}  ==> medium 2 is a(n) \033[92m{self._medium2.type(self)[1]}\x1b[0m")
        print(f"mu_eq_1 = {self._medium1.mu_eq():.4g}")
        print(f"mu_eq_2 = {self._medium2.mu_eq():.4g}")
        print(f"epsilon_eq_1 = {self._medium1.epsilon_eq(self):.4g}")
        print(f"epsilon_eq_2 = {self._medium2.epsilon_eq(self):.4g}")
        print(f"zeta_eq_1 = {self._medium1.zeta_eq(self):.4g}")
        print(f"zeta_eq_2 = {self._medium2.zeta_eq(self):.4g}")
        print(f"k_1 = {self.k(self._medium1):.4g}")
        print(f"k_2 = {self.k(self._medium2):.4g}")
        print(f"gamma_e = {self.gamma(self._medium1, self._medium2):.4g} = {abs(self.gamma(self._medium1, self._medium2)):.4g} ∠ {np.angle(self.gamma(self._medium1, self._medium2)):.4g}")
        print(f"tau_e = {self.tau(self._medium1, self._medium2):.4g} = {abs(self.tau(self._medium1, self._medium2)):.4g} ∠ {np.angle(self.tau(self._medium1, self._medium2)):.4g}")
        print(f"delta = {self.delta(self._medium2):.4g}")        
        print(f"S_i = {self.power_density_inc(self._medium1):.4g}")
        print(f"S_t = {self.power_density_trans(self._medium1, self._medium2):.4g} = {100 * self.power_density_trans(self._medium1, self._medium2) / self.power_density_inc(self._medium1):.4g}% S_i")

    def show(self, t, E1_i, ylim):
        fig, ax = plt.subplots(figsize=(10,8))
        fig.set_dpi(100)

        d_neg = -3 * self.lambda_(self._medium1)
        d_pos = -d_neg

        z_medium1 = np.linspace(d_neg, 0, 300)
        z_medium2 = np.linspace(0, d_pos, 300)
        z = z_medium1 + z_medium2

        k_1 = self.k(self._medium1)
        k_2 = self.k(self._medium2)

        gamma_e = self.gamma(self._medium1, self._medium2)
        tau_e = self.tau(self._medium1, self._medium2)

        e1_i = lambda z, t: (E1_i(k_1, -z, t)).real
        e1_r = lambda z, t: (gamma_e * E1_i(k_1, +z, t)).real
        e2_t = lambda z, t: (tau_e * E1_i(k_2, -z, t)).real
        e1_tot = lambda z, t: e1_i(z,t) + e1_r(z, t)

        lines = []
        line1, = ax.plot(z_medium1, e1_i(z_medium1, t[0]), "--", color='blue', label='$e_1^i(z=z_0,t)$', linewidth=1)
        line2, = ax.plot(z_medium1, e1_r(z_medium1, t[0]), "-.", color='red', label='$e_1^r(z=z_0,t)$', linewidth=1)
        line3, = ax.plot(z_medium1, e1_tot(z_medium1, t[0]), "-", color='green', label='$e_1^{tot}(z=z_0,t)$', linewidth=1.5)
        line4, = ax.plot(z_medium2, e2_t(z_medium2, t[0]), "-", color='purple', label='$e_2^t(z=z_0,t)$', linewidth=1.5)

        ax.axvline(x=0, color='k', linestyle='--', label="Boundary at z=0")  # Add boundary line at z=0
        plt.title("Traveling wave" + \
                "\nmedium 1: z<0, epsilon_r=" + str(self._medium1._epsilon_r) + ", mu_r=" + str(self._medium1._mu_r) + ", sigma =" + str(self._medium1._sigma) +\
                "\nmedium 2: z>0, epsilon_r=" + str(self._medium2._epsilon_r) + ", mu_r=" + str(self._medium2._mu_r) + ", sigma =" + str(self._medium2._sigma) 
                )
        plt.xlabel("Distance z [m]")
        plt.ylabel("Electric Field [V/m]")
        plt.ylim(ylim)

        def init():
            line1.set_ydata(np.ma.array(z_medium1, mask=True))
            line2.set_ydata(np.ma.array(z_medium1, mask=True))
            line3.set_ydata(np.ma.array(z_medium1, mask=True))
            line4.set_ydata(np.ma.array(z_medium2, mask=True))
            return line1, line2, line3, line4

        def animate(i):
            line1.set_ydata(e1_i(z_medium1, t[i]))
            line2.set_ydata(e1_r(z_medium1, t[i]))
            line3.set_ydata(e1_tot(z_medium1, t[i]))
            line4.set_ydata(e2_t(z_medium2, t[i]))
            return line1, line2, line3, line4

        plt.legend(loc='upper right')
        ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(t), interval=50, blit=True)
        plt.show()
        

# Define medium properties
medium1 = Medium(epsilon_r=4, mu_r=1, sigma=0.01)  # Medium 1 with dielectric properties
medium2 = Medium(epsilon_r=1, mu_r=1, sigma=0)     # Medium 2 as vacuum

# Define wave parameters
wave_frequency = 1.8e9  # Frequency in Hz
wave_amplitude = 10     # Amplitude in V/m
wave = Wave(f=wave_frequency, A=wave_amplitude)

# Add media to the wave (e.g., wave moving from medium1 to medium2)
wave.add_mediums(medium1, medium2)

# Display wave and medium properties
wave.print_data()

# Define time and initial electric field function
t = np.linspace(0, 2 * np.pi / wave._omega * 10, 300)  # Time array
E1_i = lambda k, z, t: wave._A * np.exp(1j * (k * z - wave._omega * t))  # Initial electric field

# Define y-axis limits for plot
ylim = (-15, 15)

# Run the animation
wave.show(t, E1_i, ylim)

