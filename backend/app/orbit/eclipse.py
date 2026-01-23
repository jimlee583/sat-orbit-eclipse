"""Eclipse duration calculations for circular orbits."""

import math

# Earth constants
EARTH_RADIUS_KM = 6371.0  # Mean Earth radius in kilometers
EARTH_MU = 398600.4418  # Earth gravitational parameter in km^3/s^2


def compute_orbit_radius_km(altitude_km: float) -> float:
    """
    Compute orbital radius from altitude.
    
    Args:
        altitude_km: Altitude above Earth's surface in kilometers
        
    Returns:
        Orbital radius in kilometers
    """
    return EARTH_RADIUS_KM + altitude_km


def compute_mean_motion(radius_km: float) -> float:
    """
    Compute mean motion (angular velocity) for a circular orbit.
    
    n = sqrt(mu / r^3)
    
    Args:
        radius_km: Orbital radius in kilometers
        
    Returns:
        Mean motion in radians per second
    """
    return math.sqrt(EARTH_MU / (radius_km ** 3))


def compute_orbital_period_sec(mean_motion: float) -> float:
    """
    Compute orbital period from mean motion.
    
    T = 2*pi / n
    
    Args:
        mean_motion: Mean motion in radians per second
        
    Returns:
        Orbital period in seconds
    """
    return 2.0 * math.pi / mean_motion


def compute_beta_critical_deg(radius_km: float) -> float:
    """
    Compute critical beta angle for eclipse occurrence.
    
    beta_crit = asin(Re / r)
    
    If |beta| > beta_crit, the orbit never enters Earth's shadow.
    
    Args:
        radius_km: Orbital radius in kilometers
        
    Returns:
        Critical beta angle in degrees
    """
    sin_beta_crit = EARTH_RADIUS_KM / radius_km
    # Clamp to valid range for asin
    sin_beta_crit = max(-1.0, min(1.0, sin_beta_crit))
    return math.degrees(math.asin(sin_beta_crit))


def compute_eclipse_duration_sec(radius_km: float, beta_deg: float) -> float:
    """
    Compute eclipse duration per orbit using cylindrical shadow approximation.
    
    Eclipse half-angle: theta_e = acos(sqrt(r^2 - Re^2) / (r * cos(beta)))
    Eclipse duration: T_eclipse = 2 * theta_e / n
    
    Args:
        radius_km: Orbital radius in kilometers
        beta_deg: Beta angle in degrees
        
    Returns:
        Eclipse duration in seconds (0 if no eclipse)
    """
    # Check if eclipse occurs
    beta_crit_deg = compute_beta_critical_deg(radius_km)
    if abs(beta_deg) >= beta_crit_deg:
        return 0.0
    
    # Convert to radians
    beta_rad = math.radians(beta_deg)
    
    # Compute eclipse geometry
    r = radius_km
    re = EARTH_RADIUS_KM
    
    cos_beta = math.cos(beta_rad)
    
    # Avoid division by zero when cos(beta) is very small
    if abs(cos_beta) < 1e-10:
        return 0.0
    
    # Height of orbital plane above Earth center projected along Sun vector
    h = math.sqrt(r * r - re * re)
    
    # Eclipse half-angle
    cos_theta_e = h / (r * cos_beta)
    
    # Clamp to valid range for acos
    if cos_theta_e >= 1.0:
        return 0.0
    if cos_theta_e <= -1.0:
        # Full orbit in shadow (shouldn't happen for reasonable orbits)
        theta_e = math.pi
    else:
        theta_e = math.acos(cos_theta_e)
    
    # Mean motion
    n = compute_mean_motion(radius_km)
    
    # Eclipse duration
    eclipse_duration_sec = 2.0 * theta_e / n
    
    return eclipse_duration_sec
