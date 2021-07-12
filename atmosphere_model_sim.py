"""
based on the basic_sim.py themplate, this simulation accounts for a more accurate thrust curve. Thrust curves are stored as lists. Might make a curve-maker as well idk

See the doc for more details (yet to be written up lol)
"""

import numpy as np
from matplotlib import pyplot as plt
import csv
import fluids
import datetime

# Initial values

z = 0.001
m = 19.651
v = 0
t = 0.0

# Constants

g = 9.81        # g at sea level
dt = 0.01       # _please_ keep this as a power of ten

## Drag stuff
Cd = 0.01       # fetch from RAS or CFD

lattitude = -34.35527400945747
longitude = 146.8997219810873
date = datetime.date(2021, 7, 12)

## Thrust stuff
thrust_data = [[0, 0], [0.059, 1210.59], [0.059, 2024.22], [0.163, 2235.37], [0.214, 2302.94], [0.492, 2153.73], [0.767, 2091.79], [1.015, 2103.05], [1.335, 2083.05], [1.571, 2029.85], [2.366, 1779.29], [3.488, 1534.35], [3.755, 1030.41], [3.895, 960.027], [4.12, 650.341], [4.207, 591.219], [4.44, 340.655], [4.665, 199.888], [4.778, 90.091], [4.8, 0]]

# Thrust w.r.t. time

def thrust(time):
    if time > thrust_data[-1][0]:
        return(0)
    else:
        for i in range(len(thrust_data) - 1):                                   # go through the thrust data stuff
            if (time > thrust_data[i][0]) and (time < thrust_data[i + 1][0]):   # go through the list until "time" is less than the _next_ value in time series
                return(((thrust_data[i + 1][1] - thrust_data[i][1])/(thrust_data[i + 1][0] - thrust_data[i][0]))*(time - thrust_data[i][0]) + thrust_data[i][1])

# Gravity. Shouldn't change for 99% of the time, but just in case
def grav(mass, height):
    return(g*mass)

# Drag calculations

## Prelims

### rho

def rho(height):
    atmosphere = fluids.atmosphere.ATMOSPHERE_NRLMSISE00(height, lattitude, longitude, date.timetuple()[7])
    return(atmosphere.rho)

### Cd

def Coeffd(velocity):
    return(Cd)

## Drag

def drag(v, z):
    return(Coeffd(v)*0.5*np.sign(v)*rho(z)*v**2)

def update_mass(time):
    return(m)

if __name__ == "__main__":

    altitude_table = [[],[],[],[]]

    c = 0                               # don't mind me, just counting the iterations
    while z > 0:
        c += 1
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
        altitude_table[3].append(Fd)
   
    print("launched at (" + str(lattitude) + " " + str(longitude) + ") on " + str(date.timetuple()[2]) + "/" + str(date.timetuple()[1]) + "/" + str(date.timetuple()[0]))
    print("The apogee reached is " + str(int(max(altitude_table[1]))) + " metres")
    print("The max velocity is " + str(int(max(altitude_table[2]))) + " metres per second")
    plt.plot(altitude_table[0], altitude_table[1], color="blue")
    plt.plot(altitude_table[0], altitude_table[2], color="red")
    plt.plot(altitude_table[0], altitude_table[3], color="green")
    plt.show()
