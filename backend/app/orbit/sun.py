"""Sun position and beta angle calculations."""

import math
from datetime import datetime

from app.orbit.time import datetime_to_julian_day


def compute_sun_vector_eci(dt: datetime) -> tuple[float, float, float]:
    """
    Compute approximate Sun unit vector in Earth-Centered Inertial (ECI) frame.
    
    Uses a simplified algorithm based on J2000 epoch.
    Accuracy is sufficient for yearly eclipse predictions.
    
    Args:
        dt: UTC datetime
        
    Returns:
        Tuple of (x, y, z) unit vector components in ECI frame
    """
    # Julian day
    jd = datetime_to_julian_day(dt)
    
    # Julian centuries from J2000.0
    t = (jd - 2451545.0) / 36525.0
    
    # Mean longitude of the Sun (degrees)
    l0 = 280.46646 + 36000.76983 * t + 0.0003032 * t * t
    l0 = l0 % 360.0
    
    # Mean anomaly of the Sun (degrees)
    m = 357.52911 + 35999.05029 * t - 0.0001537 * t * t
    m = m % 360.0
    m_rad = math.radians(m)
    
    # Equation of center (degrees)
    c = (1.914602 - 0.004817 * t - 0.000014 * t * t) * math.sin(m_rad)
    c += (0.019993 - 0.000101 * t) * math.sin(2 * m_rad)
    c += 0.000289 * math.sin(3 * m_rad)
    
    # Sun's true longitude (degrees)
    sun_lon = l0 + c
    sun_lon_rad = math.radians(sun_lon)
    
    # Obliquity of the ecliptic (degrees)
    epsilon = 23.439291 - 0.0130042 * t - 1.64e-7 * t * t + 5.04e-7 * t * t * t
    epsilon_rad = math.radians(epsilon)
    
    # Sun position in ecliptic coordinates (assuming circular orbit, distance = 1)
    # Then convert to equatorial (ECI) coordinates
    
    # Right ascension and declination
    cos_lon = math.cos(sun_lon_rad)
    sin_lon = math.sin(sun_lon_rad)
    cos_eps = math.cos(epsilon_rad)
    sin_eps = math.sin(epsilon_rad)
    
    # ECI unit vector components
    x = cos_lon
    y = sin_lon * cos_eps
    z = sin_lon * sin_eps
    
    # Normalize (should already be close to 1)
    mag = math.sqrt(x * x + y * y + z * z)
    
    return (x / mag, y / mag, z / mag)


def compute_orbit_normal_eci(inclination_deg: float, raan_deg: float) -> tuple[float, float, float]:
    """
    Compute orbit normal (angular momentum) unit vector in ECI frame.
    
    The orbit normal h_hat points in the direction of angular momentum,
    perpendicular to the orbital plane.
    
    For an orbit with inclination i and RAAN Ω:
    h_hat = (sin(i)*sin(Ω), -sin(i)*cos(Ω), cos(i))
    
    Args:
        inclination_deg: Orbital inclination in degrees (0-180)
        raan_deg: Right Ascension of Ascending Node in degrees (0-360)
        
    Returns:
        Tuple of (x, y, z) unit vector components in ECI frame
    """
    i_rad = math.radians(inclination_deg)
    raan_rad = math.radians(raan_deg)
    
    sin_i = math.sin(i_rad)
    cos_i = math.cos(i_rad)
    sin_raan = math.sin(raan_rad)
    cos_raan = math.cos(raan_rad)
    
    # Orbit normal vector
    hx = sin_i * sin_raan
    hy = -sin_i * cos_raan
    hz = cos_i
    
    return (hx, hy, hz)


def compute_beta_angle_deg(
    dt: datetime, h_hat: tuple[float, float, float]
) -> float:
    """
    Compute beta angle (angle between orbital plane and Sun vector).
    
    beta = asin(dot(sun_hat, h_hat))
    
    Beta angle determines eclipse characteristics:
    - beta = 0: Maximum eclipse duration
    - |beta| = 90: Sun is in the orbital plane (no eclipse for high orbits)
    - |beta| > beta_crit: No eclipse
    
    Args:
        dt: UTC datetime
        h_hat: Orbit normal unit vector in ECI frame
        
    Returns:
        Beta angle in degrees (-90 to +90)
    """
    sun_hat = compute_sun_vector_eci(dt)
    
    # Dot product
    dot = sun_hat[0] * h_hat[0] + sun_hat[1] * h_hat[1] + sun_hat[2] * h_hat[2]
    
    # Clamp to valid range for asin
    dot = max(-1.0, min(1.0, dot))
    
    # Beta angle
    beta_rad = math.asin(dot)
    
    return math.degrees(beta_rad)
