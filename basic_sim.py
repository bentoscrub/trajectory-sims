"""
This is a basic trajectory simulation for low-mid powered rockets. It serves as a template for trajectory sims with the aim of being expandable to more complicated scenarios.

This simulation follows the example in the following website:
https://pages.vassar.edu/magnes/2019/05/12/computational-simulation-of-rocket-trajectories/

See the Latex doc for more details
"""

import numpy as np
from matplotlib import pyplot as plt

# Initial values

z = 0.001
m = 20.529
v = 0
t = 0.0

# Constants

g = 9.81        # g at sea level
dt = 0.01
burnout_time = 6.9

## Drag stuff
Cd = 0.1        # According to some website, this is a reasonable guess
A = 0.8         # This is cross-sectional area. I'm too dumb to work it out
R = 8.314       # Gas Constant
M = 0.029       # Molar mass of air
T0 = 290        # Baseline Temperature
P0 = 101325     # Baseline Pressure
L = -6          # Temperature Gradient up to 12km

# Gravity. Shouldn't change for 99% of the time, but just in case
def grav(mass, height):
    return(9.8*mass)

# Thrust w.r.t. time

def thrust(time):
    if t >= burnout_time:
        return(0)
    else:
        return(838)

# Drag calculations

## Temperature 

def T(height):
    return(T0 - L*height)

## Pressure

def P(height):
    return(P0*(T0/T(height))**(g*M/R*L))

## rho

def rho(height):
    return((M*T(height))/(R*P(height)))

## Drag

def drag(v, z):
    return(0.5*np.sign(v)*rho(z)*v**2)

def update_mass(time):
    return(m)

# Record the altitude

altitude_table = [[],[],[]]

# Integrate!

while z > 0:
    
    # Calculation
    t += dt                         # Increment by time-step
    Fg = grav(m, z)                 # Calculate force of gravity
    mass = update_mass(t)           # Update mass
    Ft = thrust(t)                  # Find the thrust at the time
    Fd = drag(v, z)                 # Find the drag coefficient
    v = v + ((Ft - Fd - Fg)/m)*dt   # Find the velocity at the time
    z = z + v*dt                    # Find the height change
    
    # Graphing
    altitude_table[0].append(t)
    altitude_table[1].append(z)
    altitude_table[2].append(v)

# Give us the juice!
print("The apogee reached is " + str(int(max(altitude_table[1]))) + " metres")
plt.plot(altitude_table[0], altitude_table[1])
plt.plot(altitude_table[0], altitude_table[2], color="red")
plt.show()
