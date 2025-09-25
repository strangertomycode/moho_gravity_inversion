import numpy as np
import pandas as pd
import harmonica as hm
import os


def generate_data():
    """Creates and saves the synthetic dataset using a physically correct model."""
    print("Generating synthetic data with Harmonica library...")

    # 1. Define the Profile and Observation Points
    distance_km = np.arange(501)
    distance_m = distance_km * 1000
    coords = (np.zeros_like(distance_m), distance_m, np.zeros_like(distance_m))

    # 2. Create Synthetic Topography
    topography_m = np.zeros_like(distance_km, dtype=float)
    topo_mask = (distance_km >= 200) & (distance_km <= 300)
    topography_m[topo_mask] = 2000

    # 3. Define the "True" Moho Root as a Prism
    root_density_contrast = (2.67 - 3.20) * 1000  # in kg/m^3

    # Define the 3D boundaries of the root with correct negative depths
    # [west, east, south, north, bottom, top]
    prism_bounds = [
        -500e3,
        500e3,  # west, east (+/- 500 km)
        200e3,
        300e3,  # south, north (under the mountain)
        -50e3,
        -30e3,  # CORRECTED: bottom is -50km, top is -30km deep
    ]

    # 4. Calculate the Bouguer Anomaly using Harmonica
    bouguer_mgal = hm.prism_gravity(
        coordinates=coords,
        prisms=[prism_bounds],
        density=[root_density_contrast],
        field="g_z",
    )

    # 5. Save to CSV
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

    print(f"✅ Physically correct synthetic data saved to '{output_path}'")


if __name__ == "__main__":
    generate_data()
