"""
3D Rectangular
"""
import numpy as np
from lunarsats.three_dee import setup
import lunarsats.utils.calc3D as calc3D
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

def main():
    """
    3D Rectangular Main
    """
    t_i = setup.time_0
    t_f = setup.time_final
    iterations = setup.iterations
    t = np.linspace(t_i,t_f,iterations)
    t[0] = t_i
    h = int((t_f - t_i)/iterations)

    r_sat = np.zeros([iterations, 3])
    r_moon = np.zeros([iterations, 3])
    v_sat = np.zeros([iterations, 3])
    v_moon = np.zeros([iterations, 3])

    r_sat[0,:] = setup.r_sat
    r_moon[0,:] = setup.r_moon
    v_sat[0,:] = setup.v_sat
    v_moon[0,:] = setup.v_moon

    for t in range(0, iterations-1):
        [r_sat[t+1,:], v_sat[t+1,:]] = calc3D.rk4_sat(h, v_sat[t,:], r_moon[t,:], r_sat[t,:])
        [r_moon[t+1,:], v_moon[t+1,:]] = calc3D.rk4_moon(h, v_moon[t,:], r_moon[t,:], r_sat[t,:])
        #print(r_sat[t+1,:])

    r_sat_x = r_sat[:,0]
    r_sat_y = r_sat[:,1]
    r_sat_z = r_sat[:,2]

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(r_sat_x, r_sat_y, r_sat_z, 'gray')
    # Data for three-dimensional scattered points
    ax.scatter3D(r_sat_x, r_sat_y, r_sat_z, cmap='Greens')
    plt.show()
              