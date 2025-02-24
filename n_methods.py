# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:11:29 2025

@author: ddiaz.beca
"""
from scipy.integrate import ode
import numpy as np

def adams_predictor_corrector(f, t, y, h, f_prev):
    # Predictor de Adams-Bashforth de cuarto orden
    yp = y + (h/24) * (55*f_prev[0] - 59*f_prev[1] + 37*f_prev[2] - 9*f_prev[3])
    
    # Corrector de Adams-Moulton de tercer orden
    yc = y + (h/24) * (9*f(t + h, yp) + 19*f_prev[0] - 5*f_prev[1] + f_prev[2])
    
    return yc

def rk4_step( f, t, y, h ):
	'''
	Calculate one RK4 step
	'''
	k1 = f( t, y )
	k2 = f( t + 0.5 * h, y + 0.5 * k1 * h )
	k3 = f( t + 0.5 * h, y + 0.5 * k2 * h )
	k4 = f( t +       h, y +       k3 * h )

	return y + h / 6.0 * ( k1 + 2 * k2 + 2 * k3 + k4 )


def lsoda_solver(f, states, t0, t_end, dt):
    solver = ode(f)
    solver.set_integrator('lsoda')
    solver.set_initial_value(states[0], t0)
    
    t = [t0]
    sol = [states[0]]
    
    while solver.successful() and solver.t < t_end:
        solver.integrate(solver.t + dt)
        t.append(solver.t)
        sol.append(solver.y)
    
    return np.array(sol), np.array(t)
    

def zvode_solver(f, states, t0, t_end, t_eval):
    solver = ode(f)

    solver.set_integrator('zvode') 
    solver.set_initial_value(states[0], t0)
    t = [t0]
    sol = [states[0]]
    
    for t_target in t_eval[1:]: # Iterar a través de t_eval *desde el segundo elemento*
        if solver.successful() and solver.t < t_target: # Verificar si el solver tiene éxito y el tiempo actual es menor que el tiempo objetivo
            solver.integrate(t_target) # Integrar *hasta* el tiempo objetivo actual de t_eval
            t.append(solver.t) # Añadir el tiempo alcanzado por el solver (debería ser muy cercano a t_target)
            sol.append(solver.y) # Añadir el estado en el tiempo alcanzado
        else:
            break # Salir del bucle si el solver falla o alcanza/supera t_end
    
    return np.array(sol), np.array(t)


def dop853_solver(f, states, t0, t_end, dt):
    solver = ode(f)
    solver.set_integrator('dop853')
    solver.set_initial_value(states[0], t0)
    
    t = [t0]
    sol = [states[0]]
    
    while solver.successful() and solver.t < t_end:
        solver.integrate(solver.t + dt)
        t.append(solver.t)
        sol.append(solver.y)
    
    return np.array(sol), np.array(t)