import numpy as np
import harmonica as hm
from scipy.fft import fft, ifft, fftfreq
from .data_processing import apply_filter, create_lowpass_filter
from . import constants


def run_inversion(
    bouguer_data, topo_data, distance_m, compensation_depth_d, num_iterations=4
):
    """
    Runs the iterative inversion to find the Moho depth.
    """
    num_points = len(distance_m)
    dx_m = distance_m[1] - distance_m[0]

    lowpass_filter = create_lowpass_filter(num_points, dx_m)
    bouguer_filtered = apply_filter(bouguer_data, lowpass_filter)
    topo_filtered = apply_filter(topo_data, lowpass_filter)

    current_moho_root = (
        topo_filtered * constants.DENSITY_CRUST / constants.DENSITY_DIFFERENCE
    )
    history = {"moho_root": [current_moho_root]}

    for i in range(num_iterations):
        print(f"--- Running Iteration {i + 1} ---")

        if np.any(current_moho_root < 0):
            min_val = np.min(current_moho_root)
            print(
                f"-> Iteration {i + 1}: Found negative root values (min: {min_val:.2f} m). Applying fix."
            )

        coords = (np.zeros_like(distance_m), distance_m, np.zeros_like(distance_m))
        prisms = []
        for j in range(num_points - 1):
            root_val = max(0, current_moho_root[j])
            prisms.append(
                [
                    -500e3,
                    500e3,
                    distance_m[j],
                    distance_m[j + 1],
                    -compensation_depth_d - root_val,
                    -compensation_depth_d,
                ]
            )
        densities = np.full(len(prisms), -constants.DENSITY_DIFFERENCE)

        gravity_effect_mgal = hm.prism_gravity(coords, prisms, densities, field="g_z")
        gravity_effect_ms2 = gravity_effect_mgal * 1e-5

        gravity_residual = bouguer_filtered - gravity_effect_ms2

        residual_fft = fft(gravity_residual)
        k = 2 * np.pi * fftfreq(num_points, d=dx_m)
        downward_cont_factor = np.exp(np.abs(k) * compensation_depth_d)

        # Multiply by the low-pass filter to prevent amplification of high-frequency noise.
        correction_fft = residual_fft * downward_cont_factor * lowpass_filter

        moho_correction = np.real(ifft(correction_fft)) / (
            2 * np.pi * constants.G * constants.DENSITY_DIFFERENCE
        )

        new_moho_root = current_moho_root + moho_correction
        current_moho_root = apply_filter(new_moho_root, lowpass_filter)
        history["moho_root"].append(current_moho_root)

    final_moho_depth = compensation_depth_d + current_moho_root
    return final_moho_depth, history
