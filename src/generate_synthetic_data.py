import numpy as np
import pandas as pd
import harmonica as hm
from scipy.ndimage import gaussian_filter
import os


def generate_data():
    """Creates and saves a synthetic dataset with a smoothed 'true' root."""
    print("Generating synthetic data with a SMOOTHED 'true' model...")

    # 1. Define the Profile and Observation Points
    distance_km = np.arange(501)
    distance_m = distance_km * 1000
    coords = (np.zeros_like(distance_m), distance_m, np.zeros_like(distance_m))

    # 2. Create Synthetic Topography
    topography_m = np.zeros_like(distance_km, dtype=float)
    topo_mask = (distance_km >= 200) & (distance_km <= 300)
    topography_m[topo_mask] = 2000

    # 3. Define the "True" Moho Root as a block, then smooth it
    true_compensation_depth = 30e3
    true_root_depth = 20e3

    # Create the initial blocky root
    true_moho_root_m = np.zeros_like(distance_m, dtype=float)
    root_mask = (distance_m >= 200e3) & (distance_m <= 300e3)
    true_moho_root_m[root_mask] = true_root_depth

    # Smooth the true root to create a more realistic target
    true_moho_root_m = gaussian_filter(true_moho_root_m, sigma=15)

    # 4. Calculate the Bouguer Anomaly from the new SMOOTHED root
    root_density_contrast = (2.67 - 3.20) * 1000  # in kg/m^3

    # Model the smooth root as a series of adjacent prisms
    prisms = []
    for i in range(len(distance_m) - 1):
        if true_moho_root_m[i] > 1e-3:
            prisms.append(
                [
                    -500e3,
                    500e3,
                    distance_m[i],
                    distance_m[i + 1],
                    -true_compensation_depth - true_moho_root_m[i],
                    -true_compensation_depth,
                ]
            )

    densities = np.full(len(prisms), root_density_contrast)

    bouguer_mgal = hm.prism_gravity(
        coordinates=coords, prisms=prisms, density=densities, field="g_z"
    )

    df = pd.DataFrame(
        {
            "distance_km": distance_km,
            "topography_m": topography_m,
            "bouguer_mgal": bouguer_mgal,
        }
    )

    if not os.path.exists("data"):
        os.makedirs("data")

    output_path = "data/synthetic_profile_data.csv"
    df.to_csv(output_path, index=False)

    print(f"✅ Smoothed synthetic data saved to '{output_path}'")


if __name__ == "__main__":
    generate_data()
