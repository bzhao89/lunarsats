"""
Utility Calcs for 3D rectangular sim
"""
import numpy as np
from lunarsats.three_dee import setup

mass_earth = setup.mass_earth
mass_moon = setup.mass_moon
mass_sat = setup.mass_sat
G = setup.G

def force(r_moon, r_sat=None) -> list:
    """
    Calculate forces on bodies
    """
    if r_sat:
        delta_r = []
        for i in range(3):
            delta_r[i] = r_sat[i] - r_moon[i]
        delta_r_hat = delta_r / np.linalg.norm(delta_r)
        mag_delta_r = np.linalg.norm(delta_r)
        force_mag_moon = G * mass_sat * mass_moon / (mag_delta_r)**2
        f_from_moon = -force_mag_moon * delta_r_hat

        r_hat_earth = r_sat / np.linalg.norm(r_sat)
        force_mag_earth = G * mass_sat * mass_earth / (np.linalg.norm(r_sat))**2
        f_from_earth = -force_mag_earth * r_hat_earth

        return f_from_moon + f_from_earth    
    else:
        # Calculate force on moon (from Earth only, force from sat ~0)
        r_hat = r_moon / np.linalg.norm(r_moon)
        force_mag = G * mass_earth * mass_moon / (np.linalg.norm(r_moon)**2)
        return -force_mag * r_hat
    
def rk4(h, v, r_moon, r_sat = None):
    """
    Fourth-Order Runge-Kutta solver for body position and velocity
    """
    k11 = v
    if r_sat:
        k21 = force(r_moon, r_sat) / mass_sat

        k12 = v + 0.5*h*k21
        k22 = force(r_moon,r_sat+0.5*h*k11) / mass_sat

        k13 = v + 0.5*h*k22
        k23 = force(r_moon, r_sat+0.5*h*k12) / mass_sat

        k14 = v + h*k23
        k24 = force(r_moon, r_sat+h*k13) / mass_sat

        position = r_sat + float(h * (k11 + 2.0*k12 + 2.0*k13 + k14) / 6.0)
        velocity = v + float(h * (k21 + 2.0*k22 + 2.0*k23 + k24) / 6.0)
        return [position, velocity]
    else:
        k21 = force(r_moon) / mass_moon

        k12 = v + 0.5*h*k21
        k22 = force(r_moon + 0.5*h*k11) / mass_moon

        k13 = v + 0.5*h*k22
        k23 = force(r_moon + 0.5*h*k12) / mass_moon

        k14 = v + h*k23
        k24 = force(r_moon + h*k13) / mass_moon
    
        position = r_moon + float(h * (k11 + 2.0*k12 + 2.0*k13 + k14) / 6.0)
        velocity = v + float(h * (k21 + 2.0*k22 + 2.0*k23 + k24) / 6.0)
        return [position, velocity]