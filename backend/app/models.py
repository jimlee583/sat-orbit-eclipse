"""Pydantic models for API request/response validation."""

from pydantic import BaseModel, Field


class CircularEclipseRequest(BaseModel):
    """Request model for computing eclipse duration from altitude and beta angle."""

    altitude_km: float = Field(
        ...,
        gt=0,
        description="Orbital altitude above Earth's surface in kilometers",
        examples=[400.0],
    )
    beta_deg: float = Field(
        ...,
        ge=-90,
        le=90,
        description="Beta angle (angle between orbital plane and Sun vector) in degrees",
        examples=[23.5],
    )


class CircularEclipseResponse(BaseModel):
    """Response model for circular eclipse calculation."""

    altitude_km: float = Field(..., description="Input altitude in kilometers")
    beta_deg: float = Field(..., description="Input beta angle in degrees")
    orbit_radius_km: float = Field(..., description="Orbit radius (Re + altitude) in kilometers")
    period_sec: float = Field(..., description="Orbital period in seconds")
    period_min: float = Field(..., description="Orbital period in minutes")
    beta_crit_deg: float = Field(
        ..., description="Critical beta angle for eclipse occurrence in degrees"
    )
    eclipse_sec: float = Field(..., description="Eclipse duration in seconds")
    eclipse_min: float = Field(..., description="Eclipse duration in minutes")


class YearlyEclipseRequest(BaseModel):
    """Request model for computing yearly eclipse curve."""

    altitude_km: float = Field(
        ...,
        gt=0,
        description="Orbital altitude above Earth's surface in kilometers",
        examples=[400.0],
    )
    inclination_deg: float = Field(
        ...,
        ge=0,
        le=180,
        description="Orbital inclination in degrees",
        examples=[51.6],
    )
    raan_deg: float = Field(
        ...,
        ge=0,
        le=360,
        description="Right Ascension of Ascending Node in degrees",
        examples=[0.0],
    )
    start_utc: str = Field(
        default="2026-01-01T00:00:00Z",
        description="Start date/time in ISO8601 format",
        examples=["2026-01-01T00:00:00Z"],
    )
    days: int = Field(
        default=365,
        gt=0,
        le=730,
        description="Number of days to simulate",
    )
    step_hours: float = Field(
        default=24.0,
        gt=0,
        le=168,
        description="Time step between samples in hours",
    )


class EclipseSample(BaseModel):
    """A single sample point in the yearly eclipse curve."""

    t_utc: str = Field(..., description="UTC timestamp in ISO8601 format")
    beta_deg: float = Field(..., description="Beta angle at this time in degrees")
    eclipse_min: float = Field(..., description="Eclipse duration per orbit in minutes")


class EclipseSummary(BaseModel):
    """Summary statistics for the yearly eclipse curve."""

    max_eclipse_min: float = Field(..., description="Maximum eclipse duration in minutes")
    min_eclipse_min: float = Field(
        ..., description="Minimum non-zero eclipse duration in minutes"
    )
    days_with_eclipse: int = Field(..., description="Number of days with any eclipse")


class YearlyEclipseResponse(BaseModel):
    """Response model for yearly eclipse calculation."""

    altitude_km: float = Field(..., description="Input altitude in kilometers")
    inclination_deg: float = Field(..., description="Input inclination in degrees")
    raan_deg: float = Field(..., description="Input RAAN in degrees")
    orbit_radius_km: float = Field(..., description="Orbit radius in kilometers")
    period_sec: float = Field(..., description="Orbital period in seconds")
    period_min: float = Field(..., description="Orbital period in minutes")
    beta_crit_deg: float = Field(..., description="Critical beta angle in degrees")
    samples: list[EclipseSample] = Field(..., description="Time series of eclipse data")
    summary: EclipseSummary = Field(..., description="Summary statistics")
