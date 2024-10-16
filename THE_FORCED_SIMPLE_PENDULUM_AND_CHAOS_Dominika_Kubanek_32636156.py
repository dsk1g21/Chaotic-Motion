# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:01:25 2024

@author: dominika

All functions are defined at the start of the code.
When functions are called there is a break in the code via hash
"""

import numpy as np
from scipy.integrate import solve_ivp as ivp
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def motion(tau , theta):
    '''

    Parameters
    ----------
    tau : Scalar
        Dimensionless time function.
    theta : Vector
        The angle of the pendulums motion, to be solved for.

    Returns
    -------
    dgammadtau : Vector
        The system of first order differential equations for the oscillation 
        amplitude and the angular velocity.

    '''
    theta1 , gamma = theta
    dgammadtau = [gamma , -K * gamma - np.sin(theta1) + F * np.cos((1 - eta) * tau)]
    return dgammadtau

#-----------------------------------------------------------------------------#

def flips(tau , theta):
    '''
    
    Parameters
    ----------
    tau : Scalar
        Dimensionless time function.
    theta : Vector
        The angle of the pendulum's motion.
    
    Returns
    -------
    event : Scalar
        Product of two consecutive angles. It is being checked to see if it is
        negative. If False the function tests the next angles.        
    condition : Scalar
        If both event and condition are not True then the function ignores those
        consecutive angles and tests the next provided the new angle is not negative.
    
    '''
    event = theta[0] * theta[1]
    condition = theta[1] > 0 
    return event and condition

#-----------------------------------------------------------------------------#
def lorenz_attractor(t , three_D):
    '''
    
    Parameters
    ----------
    t : Scalar
        Time function.
    three_D : Vector
        Holds x, y, z.

    Returns
    -------
    array : Vector
        The system of differential equations we wish to solve for.
        
    '''
    x , y , z = three_D
    dotx = sigma * (y - x)
    doty = x * (rho - z) - y
    dotz = x * y - beta * z
    array = np.array([dotx , doty , dotz])
    return array

#-----------------------------------------------------------------------------#

#-----------------------SIMPLE PENDULUM MOTION SOLUTION-----------------------#
tau = np.linspace(0 , 200 , 1000)

theta0 = [np.radians(np.pi/6) , np.radians(0)] # initial values of the problem

K = 0.5  # k/mL(Lg)**0.5 for simplicity reduced to K
F =  1.37  # driving force of the pendulum
eta = 1/3

sol = ivp(motion , [0 , 200] , theta0 , t_eval=tau , dense_output=True)
solution = sol.sol(tau)

sol_om_position , sol_om_velocity  = solution[0] , solution[1]

phases = np.arctan2(np.sin(sol_om_position) , np.cos(sol_om_position)) # containing the angles within pi and -pi for plot readability

fig , axs = plt.subplots(2, 1) #plotting both phase plot and positon against time plot as subplots

axs[0].set_title('Single Pendulum with F=%f, and initial ' r'$\theta = \frac{\pi}{6}$' %F)
axs[0].plot(phases , sol_om_velocity , color='hotpink' , lw=0.8)
axs[0].set_xlabel(r'Oscillation Amplitude')
axs[0].set_ylabel(r'Angular Velocity')

axs[1].plot(tau , phases , color='hotpink' , lw=0.8)
axs[1].set_xlabel('Time')
axs[1].set_ylabel('Angular Displacement')

plt.tight_layout()
plt.show()

plt.title('Single Pendulum with F=%f, and initial ' r'$\theta = \frac{\pi}{6}$' %F)
plt.xlabel(r'Oscillation Amplitude')
plt.ylabel(r'Angular Velocity')
plt.plot(phases , sol_om_velocity , color='hotpink' , lw=0.8)

plt.show()

plt.title('Single Pendulum with F=%f, and initial ' r'$\theta = \frac{\pi}{6}$' %F)
plt.plot(tau , phases , color='hotpink' , lw=0.8)
plt.xlabel('Time')
plt.ylabel('Angular Displacement')

plt.show()

#----------------------------------HISTOGRAMS--------------------------------#

hist_sol = ivp(motion , [0 , 200] , theta0 , events=flips)

timeflips = hist_sol.t_events[0]
time_between = []

for h in range(len(timeflips) - 1):
    times = timeflips[h + 1] - timeflips[h]
    time_between.append(times)

TimeBetweenFlips = pd.DataFrame(data=time_between)

y = sns.histplot(TimeBetweenFlips , legend=False)
y.set(xlabel='Time')
y.set(ylabel='Number of successive full circuits')
y.set(title='Histogram of time between each successive flip of the pendulum with m=1, L=1')

plt.show()
    
#-----------------------------EXTENSION OF CHAOS-----------------------------#
t = np.linspace(0 , 50 , 1000)

sigma = 10
rho = 28
beta = 8 / 3

initial = [0 , 1 , 1]

sol_lorenz = ivp(lorenz_attractor , [0 , 50] , initial , t_eval=t , dense_output=True)
lorenz = sol_lorenz.sol(t)

x , y , z = lorenz[0] , lorenz[1] , lorenz[2]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.plot3D(x , y , z , color='purple' , lw=0.5)
ax.set_xlabel('X' + r'$(\sigma = %f)$'%sigma , labelpad=1)
ax.set_ylabel('Y' + r'($\rho = %f)$' %rho , labelpad=3)
ax.set_zlabel('Z' + r'$(\beta = %f)$'%beta , labelpad=-25)
ax.set_title('Lorenz Attractor')

plt.tight_layout()

plt.show()

plt.title('Each coordinates propagation in time')
plt.plot(t , x , color='orange' , lw=0.8 , label='x')
plt.plot(t , y , color='purple' , lw=0.8 , label='y')
plt.plot(t , z , color='blue' , lw=0.8 , label='z')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Coordinates x , y , z')

plt.show()