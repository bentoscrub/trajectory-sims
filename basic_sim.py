import numpy as np
from matplotlib import pyplot as plt

z = 0.001
m = 20.529
Cd = 8
v = 0
t = 0.0
dt = 0.01
burnout_time = 10
p_coeff = 10

def grav(mass, height):
    return(9.8*mass)

def thrust(time):
    if t >= burnout_time:
        return(0)
    else:
        return(838)

def coeff(height):
    return(0.01)

def drag(v, z):
    if (np.sign(v) < 0) and (z < 100):
        return(np.sign(v)*p_coeff*v**2)
    return(np.sign(v)*coeff(z)*v**2)

def update_mass(time):
    return(m)

altitude_table = [[],[],[]]

while z > 0:
    t += dt
    Fg = grav(m, z)
    mass = update_mass(t)
    Ft = thrust(t)
    Fd = drag(v, z)
    v = v + ((Ft - Fd - Fg)/m)*dt
    z = z + v*dt
    altitude_table[0].append(t)
    altitude_table[1].append(z)
    altitude_table[2].append(v)

plt.plot(altitude_table[0], altitude_table[1])
plt.show()
