# Universal Gravitational Constant in SI units (m^3 kg^-1 s^-2)
G = 6.67430e-11

# Standard densities in kg/m^3 [cite: 299]
RHO_CRUST = 2.67 * 1000
RHO_MANTLE = 3.20 * 1000
DELTA_RHO = RHO_MANTLE - RHO_CRUST

# Filter parameters in km, as described in the paper [cite: 112, 330]
FILTER_WL_START = 50.0  # Wavelengths > 50 km have unity gain
FILTER_WL_END = 33.0  # Wavelengths < 33 km are zeroed
