import numpy as np
import pandas as pd


def load_profile_data(filepath):
    """Loads profile data and converts units to SI."""
    df = pd.read_csv(filepath)
    distance_m = df["distance_km"].values * 1000
    topography_m = df["topography_m"].values
    bouguer_ms2 = df["bouguer_mgal"].values * 1e-5
    return distance_m, topography_m, bouguer_ms2
