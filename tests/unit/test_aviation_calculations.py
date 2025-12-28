"""Unit tests for aviation_calculations.py module."""

import pytest
import math
from app.utils.aviation_calculations import (
    calculate_fuel_requirements,
    calculate_ground_speed,
    calculate_density_altitude,
    calculate_crosswind
)


class TestCalculateFuelRequirements:
    """Tests for calculate_fuel_requirements function."""

    def test_basic_calculation_no_wind(self):
        """Test basic fuel calculation without wind."""
        result = calculate_fuel_requirements(
            distance=100,
            indicated_airspeed=100,
            fuel_consumption=10,
            wind_speed=0,
            wind_direction=0,
            heading=0,
            reserve_time=45
        )

        # Flight time = 100nm / 100kts = 1 hour = 60 minutes
        assert result['flight_time'] == pytest.approx(60.0, rel=1e-2)
        # Fuel = 1hr * 10gph + (45/60) * 10 = 10 + 7.5 = 17.5 gallons
        assert result['fuel_required'] == pytest.approx(17.5, rel=1e-2)
        assert result['reserve_fuel'] == pytest.approx(7.5, rel=1e-2)
        assert result['ground_speed'] == pytest.approx(100.0, rel=1e-2)

    def test_headwind_reduces_ground_speed(self):
        """Test that headwind reduces ground speed."""
        result = calculate_fuel_requirements(
            distance=100,
            indicated_airspeed=100,
            fuel_consumption=10,
            wind_speed=20,
            wind_direction=0,  # Wind from north
            heading=0,         # Flying north (into the wind)
            reserve_time=45
        )

        # Ground speed should be reduced by headwind
        assert result['ground_speed'] == pytest.approx(80.0, rel=1e-2)
        # Flight time should be longer
        assert result['flight_time'] > 60.0

    def test_tailwind_increases_ground_speed(self):
        """Test that tailwind increases ground speed."""
        result = calculate_fuel_requirements(
            distance=100,
            indicated_airspeed=100,
            fuel_consumption=10,
            wind_speed=20,
            wind_direction=180,  # Wind from south
            heading=0,           # Flying north (wind from behind)
            reserve_time=45
        )

        # Ground speed should be increased by tailwind
        assert result['ground_speed'] == pytest.approx(120.0, rel=1e-2)
        # Flight time should be shorter
        assert result['flight_time'] < 60.0

    def test_crosswind_minimal_effect(self):
        """Test that pure crosswind has minimal effect on ground speed."""
        result = calculate_fuel_requirements(
            distance=100,
            indicated_airspeed=100,
            fuel_consumption=10,
            wind_speed=20,
            wind_direction=90,  # Wind from east
            heading=0,          # Flying north (crosswind)
            reserve_time=45
        )

        # Ground speed should be close to IAS (crosswind doesn't reduce ground speed much)
        assert result['ground_speed'] == pytest.approx(100.0, rel=1e-1)

    def test_zero_reserve_time(self):
        """Test calculation with zero reserve time."""
        result = calculate_fuel_requirements(
            distance=100,
            indicated_airspeed=100,
            fuel_consumption=10,
            reserve_time=0
        )

        assert result['reserve_fuel'] == 0.0
        assert result['fuel_required'] == pytest.approx(10.0, rel=1e-2)

    def test_invalid_distance_raises_error(self):
        """Test that invalid distance raises ValueError."""
        with pytest.raises(ValueError, match="Distance must be greater than zero"):
            calculate_fuel_requirements(
                distance=0,
                indicated_airspeed=100,
                fuel_consumption=10,
                reserve_time=45
            )

    def test_invalid_airspeed_raises_error(self):
        """Test that invalid airspeed raises ValueError."""
        with pytest.raises(ValueError, match="Indicated airspeed must be greater than zero"):
            calculate_fuel_requirements(
                distance=100,
                indicated_airspeed=0,
                fuel_consumption=10,
                reserve_time=45
            )

    def test_invalid_fuel_consumption_raises_error(self):
        """Test that invalid fuel consumption raises ValueError."""
        with pytest.raises(ValueError, match="Fuel consumption must be greater than zero"):
            calculate_fuel_requirements(
                distance=100,
                indicated_airspeed=100,
                fuel_consumption=0,
                reserve_time=45
            )

    def test_negative_wind_speed_raises_error(self):
        """Test that negative wind speed raises ValueError."""
        with pytest.raises(ValueError, match="Wind speed cannot be negative"):
            calculate_fuel_requirements(
                distance=100,
                indicated_airspeed=100,
                fuel_consumption=10,
                wind_speed=-10,
                reserve_time=45
            )

    def test_invalid_wind_direction_raises_error(self):
        """Test that invalid wind direction raises ValueError."""
        with pytest.raises(ValueError, match="Wind direction must be between 0 and 360"):
            calculate_fuel_requirements(
                distance=100,
                indicated_airspeed=100,
                fuel_consumption=10,
                wind_direction=400,
                reserve_time=45
            )


class TestCalculateGroundSpeed:
    """Tests for calculate_ground_speed function."""

    def test_basic_calculation_sea_level(self):
        """Test basic ground speed calculation at sea level."""
        result = calculate_ground_speed(
            indicated_airspeed=100,
            wind_speed=0,
            wind_direction=0,
            heading=0,
            temperature=15,  # Standard temperature
            pressure_altitude=0
        )

        # At sea level with no wind, GS should equal IAS
        assert result['ground_speed'] == pytest.approx(100.0, rel=1e-2)
        # Standard temp at sea level is 15°C, so DA should be close to 0
        assert result['density_altitude'] == pytest.approx(0.0, rel=100)

    def test_tas_increases_with_altitude(self):
        """Test that TAS increases with altitude."""
        result_low = calculate_ground_speed(
            indicated_airspeed=100,
            wind_speed=0,
            wind_direction=0,
            heading=0,
            temperature=15,
            pressure_altitude=0
        )

        result_high = calculate_ground_speed(
            indicated_airspeed=100,
            wind_speed=0,
            wind_direction=0,
            heading=0,
            temperature=5,  # Standard temp at 5000ft
            pressure_altitude=5000
        )

        # TAS should be higher at higher altitude
        assert result_high['ground_speed'] > result_low['ground_speed']

    def test_headwind_component_positive(self):
        """Test headwind component is positive when flying into wind."""
        result = calculate_ground_speed(
            indicated_airspeed=100,
            wind_speed=20,
            wind_direction=0,  # Wind from north
            heading=0,         # Flying north
            temperature=15,
            pressure_altitude=0
        )

        assert result['headwind_component'] == pytest.approx(20.0, rel=1e-2)
        assert result['crosswind_component'] == pytest.approx(0.0, abs=0.1)

    def test_tailwind_component_negative(self):
        """Test headwind component is negative (tailwind) when wind from behind."""
        result = calculate_ground_speed(
            indicated_airspeed=100,
            wind_speed=20,
            wind_direction=180,  # Wind from south
            heading=0,           # Flying north
            temperature=15,
            pressure_altitude=0
        )

        assert result['headwind_component'] == pytest.approx(-20.0, rel=1e-2)

    def test_crosswind_component(self):
        """Test crosswind component calculation."""
        result = calculate_ground_speed(
            indicated_airspeed=100,
            wind_speed=20,
            wind_direction=90,  # Wind from east
            heading=0,          # Flying north
            temperature=15,
            pressure_altitude=0
        )

        assert result['crosswind_component'] == pytest.approx(20.0, rel=1e-2)
        assert result['headwind_component'] == pytest.approx(0.0, abs=0.1)

    def test_density_altitude_hot_day(self):
        """Test density altitude on a hot day."""
        result = calculate_ground_speed(
            indicated_airspeed=100,
            wind_speed=0,
            wind_direction=0,
            heading=0,
            temperature=35,  # 20°C above standard
            pressure_altitude=0
        )

        # DA = PA + 120 * (OAT - ISA) = 0 + 120 * (35 - 15) = 2400 ft
        assert result['density_altitude'] == pytest.approx(2400.0, rel=1e-2)

    def test_density_altitude_cold_day(self):
        """Test density altitude on a cold day."""
        result = calculate_ground_speed(
            indicated_airspeed=100,
            wind_speed=0,
            wind_direction=0,
            heading=0,
            temperature=-5,  # 20°C below standard
            pressure_altitude=0
        )

        # DA = PA + 120 * (OAT - ISA) = 0 + 120 * (-5 - 15) = -2400 ft
        assert result['density_altitude'] == pytest.approx(-2400.0, rel=1e-2)

    def test_invalid_airspeed_raises_error(self):
        """Test that invalid airspeed raises ValueError."""
        with pytest.raises(ValueError):
            calculate_ground_speed(
                indicated_airspeed=0,
                wind_speed=0,
                wind_direction=0,
                heading=0,
                temperature=15,
                pressure_altitude=0
            )


class TestCalculateDensityAltitude:
    """Tests for calculate_density_altitude function."""

    def test_standard_conditions_sea_level(self):
        """Test density altitude at standard sea level conditions."""
        result = calculate_density_altitude(
            pressure_altitude=0,
            temperature=15  # Standard temp at sea level
        )

        assert result['density_altitude'] == pytest.approx(0.0, abs=10)

    def test_standard_conditions_5000ft(self):
        """Test density altitude at standard 5000ft conditions."""
        result = calculate_density_altitude(
            pressure_altitude=5000,
            temperature=5  # Standard temp at 5000ft (15 - 2*5 = 5°C)
        )

        assert result['density_altitude'] == pytest.approx(5000.0, abs=10)

    def test_hot_day_increases_da(self):
        """Test that hot temperature increases density altitude."""
        result = calculate_density_altitude(
            pressure_altitude=5000,
            temperature=25  # 20°C above standard
        )

        # DA = 5000 + 120 * (25 - 5) = 5000 + 2400 = 7400 ft
        assert result['density_altitude'] == pytest.approx(7400.0, rel=1e-2)

    def test_cold_day_decreases_da(self):
        """Test that cold temperature decreases density altitude."""
        result = calculate_density_altitude(
            pressure_altitude=5000,
            temperature=-15  # 20°C below standard
        )

        # DA = 5000 + 120 * (-15 - 5) = 5000 - 2400 = 2600 ft
        assert result['density_altitude'] == pytest.approx(2600.0, rel=1e-2)


class TestCalculateCrosswind:
    """Tests for calculate_crosswind function."""

    def test_direct_crosswind(self):
        """Test 90-degree crosswind."""
        result = calculate_crosswind(wind_speed=20, wind_angle=90)

        assert result['crosswind'] == pytest.approx(20.0, rel=1e-2)
        assert result['headwind'] == pytest.approx(0.0, abs=0.1)

    def test_direct_headwind(self):
        """Test 0-degree headwind."""
        result = calculate_crosswind(wind_speed=20, wind_angle=0)

        assert result['headwind'] == pytest.approx(20.0, rel=1e-2)
        assert result['crosswind'] == pytest.approx(0.0, abs=0.1)

    def test_45_degree_wind(self):
        """Test 45-degree wind angle."""
        result = calculate_crosswind(wind_speed=20, wind_angle=45)

        expected = 20 * math.sin(math.radians(45))  # ≈ 14.14
        assert result['crosswind'] == pytest.approx(expected, rel=1e-2)
        assert result['headwind'] == pytest.approx(expected, rel=1e-2)

    def test_no_wind(self):
        """Test zero wind speed."""
        result = calculate_crosswind(wind_speed=0, wind_angle=45)

        assert result['crosswind'] == 0.0
        assert result['headwind'] == 0.0
