"""Time conversion utilities."""

from datetime import datetime, timezone


def parse_iso8601(iso_string: str) -> datetime:
    """
    Parse ISO8601 datetime string to datetime object.
    
    Handles 'Z' suffix for UTC and ensures timezone awareness.
    
    Args:
        iso_string: ISO8601 formatted datetime string
        
    Returns:
        Timezone-aware datetime object
        
    Raises:
        ValueError: If the string cannot be parsed
    """
    # Replace 'Z' with '+00:00' for Python's fromisoformat
    normalized = iso_string.replace("Z", "+00:00")
    
    dt = datetime.fromisoformat(normalized)
    
    # Ensure timezone awareness
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    return dt


def datetime_to_julian_day(dt: datetime) -> float:
    """
    Convert datetime to Julian Day Number.
    
    Uses the algorithm for computing Julian Day from calendar date.
    
    Args:
        dt: Datetime object (should be UTC for astronomical calculations)
        
    Returns:
        Julian Day Number as float
    """
    # Ensure we're working with UTC
    if dt.tzinfo is not None:
        # Convert to UTC timestamp
        utc_dt = dt.astimezone(timezone.utc)
    else:
        utc_dt = dt
    
    year = utc_dt.year
    month = utc_dt.month
    day = utc_dt.day
    
    # Time as fraction of day
    hour = utc_dt.hour
    minute = utc_dt.minute
    second = utc_dt.second
    microsecond = utc_dt.microsecond
    
    day_fraction = (hour + minute / 60.0 + second / 3600.0 + microsecond / 3600000000.0) / 24.0
    
    # Julian Day calculation
    # Using the algorithm from Astronomical Algorithms by Jean Meeus
    if month <= 2:
        year -= 1
        month += 12
    
    a = int(year / 100)
    b = 2 - a + int(a / 4)
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + day_fraction + b - 1524.5
    
    return jd


def julian_day_to_datetime(jd: float) -> datetime:
    """
    Convert Julian Day Number to datetime.
    
    Args:
        jd: Julian Day Number
        
    Returns:
        UTC datetime object
    """
    jd = jd + 0.5
    z = int(jd)
    f = jd - z
    
    if z < 2299161:
        a = z
    else:
        alpha = int((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - int(alpha / 4)
    
    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)
    
    day = b - d - int(30.6001 * e) + f
    
    if e < 14:
        month = e - 1
    else:
        month = e - 13
    
    if month > 2:
        year = c - 4716
    else:
        year = c - 4715
    
    # Extract time from fractional day
    day_int = int(day)
    day_frac = day - day_int
    
    hours = day_frac * 24
    hour = int(hours)
    minutes = (hours - hour) * 60
    minute = int(minutes)
    seconds = (minutes - minute) * 60
    second = int(seconds)
    microsecond = int((seconds - second) * 1000000)
    
    return datetime(year, month, day_int, hour, minute, second, microsecond, tzinfo=timezone.utc)
