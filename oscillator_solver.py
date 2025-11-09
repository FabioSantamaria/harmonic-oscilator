import numpy as np
from scipy.integrate import solve_ivp

def damped_oscillator_ode(t, y, m, c, k, F0, omega):
    """
    Defines the ODE system for a damped harmonic oscillator with external forcing.
    
    Parameters:
    -----------
    t : float
        Time
    y : array
        State vector [position, velocity]
    m, c, k : float
        Mass, damping, and spring constant
    F0, omega : float
        External force amplitude and frequency
        
    Returns:
    --------
    dydt : array
        Time derivative of state vector
    """
    x, v = y
    dxdt = v
    dvdt = (F0 * np.sin(omega * t) - c * v - k * x) / m
    return [dxdt, dvdt]

def solve_damped_oscillator(m, c, k, F0, omega, x0, v0, t_max, num_points):
    """
    Solves the damped oscillator ODE.
    
    Parameters:
    -----------
    m, c, k : float
        System parameters
    F0, omega : float
        Forcing parameters
    x0, v0 : float
        Initial conditions
    t_max : float
        Simulation time
    num_points : int
        Number of time points
        
    Returns:
    --------
    t : array
        Time array
    x, v : array
        Position and velocity arrays
    """
    t_eval = np.linspace(0, t_max, num_points)
    
    sol = solve_ivp(
        damped_oscillator_ode,
        [0, t_max],
        [x0, v0],
        args=(m, c, k, F0, omega),
        t_eval=t_eval,
        method='RK45',
        rtol=1e-8,
        atol=1e-10,
        dense_output=True
    )
    
    return sol.t, sol.y[0], sol.y[1]