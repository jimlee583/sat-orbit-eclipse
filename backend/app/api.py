"""API endpoints for eclipse calculations."""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException

from app.models import (
    CircularEclipseRequest,
    CircularEclipseResponse,
    EclipseSample,
    EclipseSummary,
    YearlyEclipseRequest,
    YearlyEclipseResponse,
)
from app.orbit.eclipse import (
    compute_beta_critical_deg,
    compute_eclipse_duration_sec,
    compute_mean_motion,
    compute_orbital_period_sec,
    compute_orbit_radius_km,
)
from app.orbit.sun import compute_beta_angle_deg, compute_orbit_normal_eci

router = APIRouter(prefix="/api/eclipse", tags=["eclipse"])


@router.post("/circular", response_model=CircularEclipseResponse)
async def compute_circular_eclipse(request: CircularEclipseRequest) -> CircularEclipseResponse:
    """
    Compute eclipse duration for a circular orbit given altitude and beta angle.
    
    - **altitude_km**: Orbital altitude above Earth's surface in kilometers
    - **beta_deg**: Beta angle (angle between orbital plane and Sun vector) in degrees
    """
    if request.altitude_km <= 0:
        raise HTTPException(status_code=400, detail="Altitude must be positive")
    
    if not -90 <= request.beta_deg <= 90:
        raise HTTPException(status_code=400, detail="Beta angle must be between -90 and 90 degrees")
    
    r_km = compute_orbit_radius_km(request.altitude_km)
    n_rad_s = compute_mean_motion(r_km)
    period_sec = compute_orbital_period_sec(n_rad_s)
    beta_crit_deg = compute_beta_critical_deg(r_km)
    
    eclipse_sec = compute_eclipse_duration_sec(r_km, request.beta_deg)
    
    return CircularEclipseResponse(
        altitude_km=request.altitude_km,
        beta_deg=request.beta_deg,
        orbit_radius_km=r_km,
        period_sec=period_sec,
        period_min=period_sec / 60.0,
        beta_crit_deg=beta_crit_deg,
        eclipse_sec=eclipse_sec,
        eclipse_min=eclipse_sec / 60.0,
    )


@router.post("/yearly", response_model=YearlyEclipseResponse)
async def compute_yearly_eclipse(request: YearlyEclipseRequest) -> YearlyEclipseResponse:
    """
    Compute eclipse duration over a year based on orbital parameters.
    
    - **altitude_km**: Orbital altitude above Earth's surface in kilometers
    - **inclination_deg**: Orbital inclination in degrees (0-180)
    - **raan_deg**: Right Ascension of Ascending Node in degrees (0-360)
    - **start_utc**: Start date/time in ISO8601 format
    - **days**: Number of days to simulate (default: 365)
    - **step_hours**: Time step between samples in hours (default: 24)
    """
    if request.altitude_km <= 0:
        raise HTTPException(status_code=400, detail="Altitude must be positive")
    
    if not 0 <= request.inclination_deg <= 180:
        raise HTTPException(
            status_code=400, detail="Inclination must be between 0 and 180 degrees"
        )
    
    if not 0 <= request.raan_deg <= 360:
        raise HTTPException(status_code=400, detail="RAAN must be between 0 and 360 degrees")
    
    if request.days <= 0:
        raise HTTPException(status_code=400, detail="Days must be positive")
    
    if request.step_hours <= 0:
        raise HTTPException(status_code=400, detail="Step hours must be positive")
    
    # Parse start time
    try:
        start_dt = datetime.fromisoformat(request.start_utc.replace("Z", "+00:00"))
        if start_dt.tzinfo is None:
            start_dt = start_dt.replace(tzinfo=timezone.utc)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid start_utc format: {e}")
    
    # Compute orbital parameters
    r_km = compute_orbit_radius_km(request.altitude_km)
    n_rad_s = compute_mean_motion(r_km)
    period_sec = compute_orbital_period_sec(n_rad_s)
    beta_crit_deg = compute_beta_critical_deg(r_km)
    
    # Compute orbit normal vector (fixed for this simulation - no RAAN precession)
    h_hat = compute_orbit_normal_eci(request.inclination_deg, request.raan_deg)
    
    # Generate samples
    samples: list[EclipseSample] = []
    step_delta = timedelta(hours=request.step_hours)
    total_steps = int(request.days * 24 / request.step_hours)
    
    max_eclipse_min = 0.0
    min_eclipse_min = float("inf")
    days_with_eclipse = 0
    current_day = -1
    day_has_eclipse = False
    
    current_time = start_dt
    for _ in range(total_steps + 1):
        beta_deg = compute_beta_angle_deg(current_time, h_hat)
        eclipse_sec = compute_eclipse_duration_sec(r_km, beta_deg)
        eclipse_min = eclipse_sec / 60.0
        
        samples.append(
            EclipseSample(
                t_utc=current_time.isoformat().replace("+00:00", "Z"),
                beta_deg=round(beta_deg, 4),
                eclipse_min=round(eclipse_min, 4),
            )
        )
        
        # Track statistics
        if eclipse_min > max_eclipse_min:
            max_eclipse_min = eclipse_min
        if eclipse_min > 0 and eclipse_min < min_eclipse_min:
            min_eclipse_min = eclipse_min
        
        # Track days with eclipse
        day_of_sim = (current_time - start_dt).days
        if day_of_sim != current_day:
            if day_has_eclipse:
                days_with_eclipse += 1
            current_day = day_of_sim
            day_has_eclipse = False
        if eclipse_min > 0:
            day_has_eclipse = True
        
        current_time += step_delta
    
    # Handle last day
    if day_has_eclipse:
        days_with_eclipse += 1
    
    # Handle case where there's no eclipse at all
    if min_eclipse_min == float("inf"):
        min_eclipse_min = 0.0
    
    summary = EclipseSummary(
        max_eclipse_min=round(max_eclipse_min, 4),
        min_eclipse_min=round(min_eclipse_min, 4),
        days_with_eclipse=days_with_eclipse,
    )
    
    return YearlyEclipseResponse(
        altitude_km=request.altitude_km,
        inclination_deg=request.inclination_deg,
        raan_deg=request.raan_deg,
        orbit_radius_km=r_km,
        period_sec=period_sec,
        period_min=round(period_sec / 60.0, 4),
        beta_crit_deg=round(beta_crit_deg, 4),
        samples=samples,
        summary=summary,
    )
