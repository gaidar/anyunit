import math
from typing import Dict, Union

def calculate_fuel_requirements(
    distance: float,
    indicated_airspeed: float,
    fuel_consumption: float,
    wind_speed: float = 0,
    wind_direction: float = 0,
    heading: float = 0,
    reserve_time: float = 45
) -> Dict[str, Union[float, str]]:
    # Input validation
    if distance <= 0:
        raise ValueError("Distance must be greater than zero")
    if indicated_airspeed <= 0:
        raise ValueError("Indicated airspeed must be greater than zero")
    if fuel_consumption <= 0:
        raise ValueError("Fuel consumption must be greater than zero")
    if wind_speed < 0:
        raise ValueError("Wind speed cannot be negative")
    if not 0 <= wind_direction <= 360:
        raise ValueError("Wind direction must be between 0 and 360 degrees")
    if not 0 <= heading <= 360:
        raise ValueError("Heading must be between 0 and 360 degrees")
    if reserve_time < 0:
        raise ValueError("Reserve time cannot be negative")
    """
    Calculate fuel requirements and flight time for a flight
    
    Args:
        distance: Distance in nautical miles
        indicated_airspeed: Indicated airspeed in knots
        fuel_consumption: Fuel consumption in gallons per hour
        wind_speed: Wind speed in knots (default 0)
        wind_direction: Wind direction in degrees (0-360, default 0)
        heading: Aircraft heading in degrees (0-360, default 0)
        reserve_time: Reserve time in minutes (default 45)
    
    Returns:
        Dictionary containing fuel requirements, ground speed and flight time
    """
    # Calculate relative wind angle (wind direction is the FROM direction)
    angle_rad = math.radians((wind_direction - heading) % 360)

    # Approximate TAS with IAS at low altitude (no altitude input here)
    tas = indicated_airspeed

    # Headwind component (positive = headwind, negative = tailwind)
    headwind = wind_speed * math.cos(angle_rad)

    # Ground speed along track
    ground_speed = max(1.0, tas - headwind)  # ensure not below 1 kt
    
    # Calculate flight time in hours
    flight_time = distance / ground_speed
    
    # Calculate fuel requirements
    reserve_fuel = (reserve_time / 60) * fuel_consumption
    total_fuel = (flight_time * fuel_consumption) + reserve_fuel
    
    return {
        'ground_speed': round(ground_speed, 2),
        'flight_time': round(flight_time * 60, 2),  # Convert to minutes
        'fuel_required': round(total_fuel, 2),
        'reserve_fuel': round(reserve_fuel, 2)
    }

def calculate_ground_speed(
    indicated_airspeed: float,
    wind_speed: float,
    wind_direction: float,
    heading: float,
    temperature: float,
    pressure_altitude: float = 0
) -> Dict[str, float]:
    # Input validation
    if indicated_airspeed <= 0:
        raise ValueError("Indicated airspeed must be greater than zero")
    if wind_speed < 0:
        raise ValueError("Wind speed cannot be negative")
    if not 0 <= wind_direction <= 360:
        raise ValueError("Wind direction must be between 0 and 360 degrees")
    if not 0 <= heading <= 360:
        raise ValueError("Heading must be between 0 and 360 degrees")
    """
    Calculate ground speed considering wind and atmospheric conditions
    
    Args:
        indicated_airspeed: Indicated airspeed in knots
        wind_speed: Wind speed in knots
        wind_direction: Wind direction in degrees (0-360)
        heading: Aircraft heading in degrees (0-360)
        temperature: Temperature in Celsius
        pressure_altitude: Pressure altitude in feet (default 0)
    
    Returns:
        Dictionary containing ground speed and density altitude
    """
    # Calculate density altitude (rule of thumb)
    standard_temp = 15 - (pressure_altitude / 1000) * 2
    temp_difference = temperature - standard_temp
    density_alt = pressure_altitude + (120 * temp_difference)
    
    # Approximate TAS from IAS: ~2% per 1000 ft
    tas = indicated_airspeed * (1 + 0.02 * (pressure_altitude / 1000.0))

    # Relative wind angle (wind is FROM direction)
    angle_rad = math.radians((wind_direction - heading) % 360)

    # Components
    headwind = wind_speed * math.cos(angle_rad)   # +ve headwind, -ve tailwind
    crosswind = wind_speed * math.sin(angle_rad)

    # Ground speed along track
    ground_speed = max(1.0, tas - headwind)
    
    return {
        'ground_speed': round(ground_speed, 2),
        'density_altitude': round(density_alt, 2),
        'headwind_component': round(headwind, 2),
        'crosswind_component': round(crosswind, 2)
    }

def calculate_density_altitude(
    pressure_altitude: float,
    temperature: float
) -> Dict[str, float]:
    # Input validation
    if pressure_altitude < 0:
        raise ValueError("Pressure altitude cannot be negative")
    """
    Calculate density altitude
    
    Args:
        pressure_altitude: Pressure altitude in feet
        temperature: Temperature in Celsius
    
    Returns:
        Dictionary containing density altitude
    """
    standard_temp = 15 - (pressure_altitude / 1000) * 2
    temp_difference = temperature - standard_temp
    density_alt = pressure_altitude + (120 * temp_difference)
    
    return {
        'density_altitude': round(density_alt, 2)
    }

def calculate_crosswind(
    wind_speed: float,
    wind_angle: float
) -> Dict[str, float]:
    """
    Calculate crosswind and headwind components
    
    Args:
        wind_speed: Wind speed in knots
        wind_angle: Wind angle relative to runway in degrees
    
    Returns:
        Dictionary containing crosswind and headwind components
    """
    wind_angle_rad = math.radians(wind_angle)
    crosswind = wind_speed * math.sin(wind_angle_rad)
    headwind = wind_speed * math.cos(wind_angle_rad)
    
    return {
        'crosswind': round(crosswind, 2),
        'headwind': round(headwind, 2)
    }
