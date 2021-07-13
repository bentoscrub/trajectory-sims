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
v = 0
t = 0.0

# Constants

g   = 9.81          # g at sea level
dt  = 0.01          # _please_ keep this as a power of ten
p   = 101325        # you know what this is ;)

## Drag stuff
r   = 0.324
A   = 3.1416*(0.5*r)**2
Cd  = 0.6       # fetch from RAS or CFD

lattitude = -34.35527400945747
longitude = 146.8997219810873
date = datetime.date(2021, 7, 12)

# Thrust constants, shamelessly pulled from Luan Dinh's thesis, link in the readme

## Engine Specs

average_thrust  = 9000      # (N)
exp_ratio       = 6         # this is exit area over throat area A_e/A_t
tank_pressure   = 3000000   # (Pa)
chamber_pressure= 2100000   # (Pa)
gamma           = 1.12      # important const
M_e             = 2.75797809954708  # exit mach
characteristic_v= 1650      # fuel characteristic velocity
efficiency      = 0.85      # engine efficiency
prop_mass       = 283.65
dry_mass        = 140

## Calculations

mass0           = dry_mass + prop_mass
exit_pressure   = chamber_pressure/(1 + ((gamma - 1)/2)*M_e**2)**(gamma/(gamma - 1))
C_f             = (((2*(gamma**2))/(gamma - 1))*((2/(gamma + 1))**((gamma + 1)/(gamma - 1)))*(1 - (exit_pressure/chamber_pressure)**((gamma - 1)/gamma)))**0.5 + exp_ratio*((exit_pressure - p)/chamber_pressure)
throat_area     = average_thrust/(C_f*chamber_pressure)
dm              = (chamber_pressure*throat_area)/(characteristic_v*efficiency)
spec_impulse    = average_thrust/(dm*g)
exhaust_v       = spec_impulse*g
motor_burnout   = (mass0 - dry_mass)/dm

## Thrust w.r.t. time

def thrust(time, atmosphere):
    if time < motor_burnout:
        
        return(dm*exhaust_v + (exit_pressure - atmosphere.P)*exp_ratio*throat_area)
    elif time >= motor_burnout:
        return(0)

# Gravity. Shouldn't change for 99% of the time, but just in case
def grav(mass, height):
    return(g*mass)

# Drag calculations

## Cd

def Coeffd(velocity):
    return(Cd)

## Drag

def drag(v, z, atmosphere):
    if np.sign(v) > 0:
        return(Coeffd(v)*A*0.5*atmosphere.rho*v**2)
    else:
        return(0)

def update_mass(time):
    return(max(mass0 - dm*time, dry_mass))

if __name__ == "__main__":

    altitude_table = [[],[],[],[]]
    mass = mass0
    c = 0                               # don't mind me, just counting the iterations
    while z > 0:
        
        atmos = fluids.atmosphere.ATMOSPHERE_NRLMSISE00(z, lattitude, longitude, date.timetuple()[7])
        
        c += 1
        # Calculation
        t += dt                             # Increment by time-step
        mass = max(mass - dm*dt, dry_mass)  # Update mass
        Fg = grav(mass, z)                  # Calculate force of gravity
        Ft = thrust(t, atmos)               # Find the thrust at the time
        Fd = drag(v, z, atmos)              # Find the drag force
        dv = ((Ft - Fd - Fg)/mass)*dt
        v = v + dv                          # Find the velocity at the time
        z = z + v*dt                        # Find the height change
        
        if c % int(1/dt) == 0:
            print(Ft)
        
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
