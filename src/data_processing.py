import numpy as np
import pandas as pd
from scipy.fft import fft, ifft, fftfreq
from . import constants


def load_profile_data(filepath):
    """Loads profile data and converts units to SI."""
    df = pd.read_csv(filepath)
    distance_m = df["distance_km"].values * 1000
    topography_m = df["topography_m"].values
    bouguer_ms2 = df["bouguer_mgal"].values * 1e-5
    return distance_m, topography_m, bouguer_ms2


def create_lowpass_filter(num_points, dx_m):
    """Creates the modified Hanning window filter described in the paper."""
    freq = fftfreq(num_points, d=dx_m)
    wavelength = (
        np.divide(1.0, np.abs(freq), out=np.full_like(freq, np.inf), where=freq != 0)
        / 1000
    )

    filter_window = np.zeros(num_points)
    filter_window[wavelength > constants.FILTER_WL_START] = 1.0

    mask = (wavelength <= constants.FILTER_WL_START) & (
        wavelength >= constants.FILTER_WL_END
    )
    wl_range = constants.FILTER_WL_START - constants.FILTER_WL_END
    filter_window[mask] = 0.5 * (
        1 + np.cos(np.pi * (constants.FILTER_WL_START - wavelength[mask]) / wl_range)
    )

    return filter_window


def apply_filter(data, filter_window):
    """Applies a filter in the frequency domain."""
    return np.real(ifft(fft(data) * filter_window))
