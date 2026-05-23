import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"
from scipy.signal import detrend
import os

# ========== SETTINGS ==========
original_dir = "/Users/niraj/Downloads/Projects/Project_Geo_Lab/GM/Near Field Set II"
damping = 0.05
periods = np.arange(0.01, 4.01, 0.01)

# ========== READ AT2 ==========
def read_at2(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    dt_line = next(line for line in lines if "DT=" in line)
    dt = float(dt_line.split('=')[2].split()[0])
    data_lines = lines[4:]
    data = ' '.join(data_lines).split()
    accel = np.array([float(val) for val in data])
    pga = np.max(np.abs(accel))
    print(f"  {os.path.basename(file_path):<40}  PGA = {pga:.4f} g")
    return accel, dt

def compute_response_spectrum(accel, dt, periods, damping=0.05):
    """
    Computes the response spectrum of a ground motion using the Newmark-Beta method.
    This implementation uses the unconditionally stable average acceleration scheme.

    Args:
        accel (np.ndarray): Array of ground acceleration values (in g).
        dt (float): Time step of the acceleration record.
        periods (np.ndarray): Array of periods for which to compute the spectral acceleration.
        damping (float): Damping ratio (e.g., 0.05 for 5%).

    Returns:
        np.ndarray: Array of spectral acceleration values (Sa) in g.
    """
    # Newmark-Beta method parameters for the unconditionally stable
    # constant average acceleration method.
    gamma = 0.5
    beta = 0.25

    # Detrend the acceleration time series to remove baseline drift
    accel = detrend(accel)
    
    Sa = []
    for T in periods:
        if T == 0:
            Sa.append(np.max(np.abs(accel)))
            continue

        omega = 2 * np.pi / T
        m = 1.0
        k = omega**2 * m
        c = 2 * damping * omega * m

        # Initialize displacement, velocity, and acceleration
        u, v, a = 0.0, 0.0, 0.0
        # Set initial acceleration: a_0 = (-m*ag_0 - c*v_0 - k*u_0) / m
        a = -accel[0] 
        
        u_hist = []

        # Pre-calculate constants for the integration loop to improve efficiency
        a1 = (m / (beta * dt**2)) + (c * gamma / (beta * dt))
        a2 = (m / (beta * dt)) + c * (gamma / beta - 1)
        a3 = m * (1 / (2 * beta) - 1) + c * dt * (gamma / (2 * beta) - 1)
        
        k_eff = k + a1 # Effective stiffness

        for ag in accel:
            # Calculate effective force at the current step
            p_eff = -m * ag + a1 * u + a2 * v + a3 * a
            
            # Solve for displacement at the current step
            u_new = p_eff / k_eff
            
            # Update acceleration and velocity for the current step based on u_new
            a_new = (u_new - u) / (beta * dt**2) - v / (beta * dt) - (1 / (2 * beta) - 1) * a
            v_new = v + a * (1 - gamma) * dt + a_new * gamma * dt
            
            # Update state for the next iteration
            u, v, a = u_new, v_new, a_new
            
            u_hist.append(u)

        umax = max(abs(np.array(u_hist)))
        # Append Pseudo-Spectral Acceleration (PSA), which is standard practice
        Sa.append(omega**2 * umax)
        
    return np.array(Sa)

# ========== LOAD ALL FILES ==========
original_files = sorted([f for f in os.listdir(original_dir) if f.endswith(".AT2")])

Sa_original_all = []

print("--------------------------------------------------------------------------")

print("Computing response spectra for original ground motions...")
for file in original_files:
    accel, dt = read_at2(os.path.join(original_dir, file))
    Sa = compute_response_spectrum(accel, dt, periods, damping)
    Sa_original_all.append(Sa)

Sa_original_all = np.array(Sa_original_all)
mean_orig = np.mean(Sa_original_all, axis=0)

# ========== PLOTTING ==========
fig, ax = plt.subplots(figsize=(8, 6))

# Plot Original
for Sa in Sa_original_all:
    ax.plot(periods, Sa, color='gray', alpha=0.5, linewidth=0.9)
ax.plot(periods, mean_orig, color='black', lw=1.2, label='Mean spectrum original')
ax.set_xlabel('Period (sec)')
ax.set_ylabel('Spectral Acceleration (g)')
ax.legend()


plt.tight_layout()
plt.show()

print("--------------------------------------------------------------------------")