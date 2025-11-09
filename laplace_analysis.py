import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def calculate_laplace_transform(m, c, k, F0, omega, max_freq=100, num_points=1000):
    """
    Calculate Laplace transform and frequency response of the damped oscillator.
    
    Parameters:
    -----------
    m, c, k : float
        System parameters
    F0, omega : float
        Forcing parameters
    max_freq : float
        Maximum frequency for Bode plot
    num_points : int
        Number of frequency points
        
    Returns:
    --------
    frequencies : array
        Frequency array
    magnitude : array
        Magnitude response in dB
    phase : array
        Phase response in degrees
    poles : array
        System poles
    zeros : array
        System zeros
    """
    # Define transfer function: H(s) = 1 / (ms^2 + cs + k)
    numerator = [1]
    denominator = [m, c, k]
    
    # Create transfer function
    sys = signal.TransferFunction(numerator, denominator)
    
    # Calculate poles and zeros
    poles = np.roots(denominator)
    zeros = np.roots(numerator)
    
    # Frequency response
    frequencies = np.logspace(-2, np.log10(max_freq), num_points)
    w, mag, phase = signal.bode(sys, w=frequencies)
    
    # Adjust magnitude for the forced response
    # The forced response has an additional factor of F0*ω/(s^2 + ω^2)
    forced_magnitude = mag + 20 * np.log10(F0 * omega)
    
    return w, forced_magnitude, phase, poles, zeros

def analytical_solution_laplace(t, m, c, k, F0, omega, x0, v0):
    """
    Calculate analytical solution using inverse Laplace transform.
    
    Parameters:
    -----------
    t : array
        Time array
    m, c, k : float
        System parameters
    F0, omega : float
        Forcing parameters
    x0, v0 : float
        Initial conditions
        
    Returns:
    --------
    x : array
        Analytical solution for position
    """
    # Calculate system characteristics
    omega_n = np.sqrt(k / m)
    zeta = c / (2 * np.sqrt(m * k))
    
    # Homogeneous solution
    if zeta < 1:  # Underdamped
        omega_d = omega_n * np.sqrt(1 - zeta**2)
        A = np.sqrt((x0**2) + ((v0 + zeta*omega_n*x0)/omega_d)**2)
        phi = np.arctan2(omega_d * x0, v0 + zeta * omega_n * x0)
        x_hom = A * np.exp(-zeta * omega_n * t) * np.cos(omega_d * t - phi)
    elif zeta == 1:  # Critically damped
        A1 = x0
        A2 = v0 + omega_n * x0
        x_hom = (A1 + A2 * t) * np.exp(-omega_n * t)
    else:  # Overdamped
        r1 = -zeta*omega_n + omega_n*np.sqrt(zeta**2 - 1)
        r2 = -zeta*omega_n - omega_n*np.sqrt(zeta**2 - 1)
        A1 = (v0 - r2*x0) / (r1 - r2)
        A2 = (r1*x0 - v0) / (r1 - r2)
        x_hom = A1 * np.exp(r1 * t) + A2 * np.exp(r2 * t)
    
    # Particular solution (steady-state)
    denom = (k - m*omega**2)**2 + (c*omega)**2
    A_forced = F0 * np.sqrt((k - m*omega**2)**2) / denom
    B_forced = F0 * c * omega / denom
    
    x_part = (F0 / np.sqrt(denom)) * np.sin(omega * t - np.arctan2(c*omega, k - m*omega**2))
    
    return x_hom + x_part