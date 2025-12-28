"""Unit tests for unit_converter.py module."""

import pytest
from app.utils.unit_converter import UnitManager


class TestUnitManagerSingleton:
    """Tests for UnitManager singleton pattern."""

    def test_singleton_instance(self, app_context):
        """Test that UnitManager returns the same instance."""
        manager1 = UnitManager()
        manager2 = UnitManager()
        assert manager1 is manager2

    def test_units_data_loaded(self, unit_manager):
        """Test that units data is loaded."""
        assert unit_manager._units_data is not None
        assert 'categories' in unit_manager._units_data


class TestGetCategories:
    """Tests for get_categories method."""

    def test_returns_all_categories(self, unit_manager):
        """Test that all categories are returned."""
        categories = unit_manager.get_categories()
        expected_categories = ['length', 'weight', 'temperature', 'volume',
                               'speed', 'pressure', 'energy', 'power']
        for cat in expected_categories:
            assert cat in categories

    def test_category_has_required_fields(self, unit_manager):
        """Test that each category has title, description, and icon."""
        categories = unit_manager.get_categories()
        for cat_id, cat_data in categories.items():
            assert 'title' in cat_data
            assert 'description' in cat_data
            assert 'icon' in cat_data


class TestGetCategory:
    """Tests for get_category method."""

    def test_get_existing_category(self, unit_manager):
        """Test getting an existing category."""
        category = unit_manager.get_category('length')
        assert category is not None
        assert category['title'] == 'Length'
        assert 'units' in category

    def test_get_nonexistent_category(self, unit_manager):
        """Test getting a non-existent category."""
        category = unit_manager.get_category('nonexistent')
        assert category is None


class TestGetUnitInfo:
    """Tests for get_unit_info method."""

    def test_get_existing_unit(self, unit_manager):
        """Test getting info for an existing unit."""
        unit_info = unit_manager.get_unit_info('length', 'm')
        assert unit_info is not None
        assert unit_info['name'] == 'Meter'
        assert unit_info['symbol'] == 'm'
        assert unit_info['factor'] == 1

    def test_get_nonexistent_unit(self, unit_manager):
        """Test getting info for a non-existent unit."""
        unit_info = unit_manager.get_unit_info('length', 'nonexistent')
        assert unit_info is None

    def test_get_unit_from_nonexistent_category(self, unit_manager):
        """Test getting unit from non-existent category."""
        unit_info = unit_manager.get_unit_info('nonexistent', 'm')
        assert unit_info is None


class TestGetConversionFactor:
    """Tests for get_conversion_factor method."""

    def test_same_unit_factor(self, unit_manager):
        """Test conversion factor for same unit is 1."""
        factor = unit_manager.get_conversion_factor('length', 'm', 'm')
        assert factor == 1.0

    def test_meter_to_kilometer(self, unit_manager):
        """Test conversion factor from meter to kilometer."""
        factor = unit_manager.get_conversion_factor('length', 'm', 'km')
        assert factor == pytest.approx(0.001)

    def test_kilometer_to_meter(self, unit_manager):
        """Test conversion factor from kilometer to meter."""
        factor = unit_manager.get_conversion_factor('length', 'km', 'm')
        assert factor == pytest.approx(1000)

    def test_temperature_returns_none(self, unit_manager):
        """Test that temperature conversion factor returns None."""
        factor = unit_manager.get_conversion_factor('temperature', 'c', 'f')
        assert factor is None

    def test_invalid_category(self, unit_manager):
        """Test conversion factor for invalid category."""
        factor = unit_manager.get_conversion_factor('nonexistent', 'm', 'km')
        assert factor is None

    def test_invalid_units(self, unit_manager):
        """Test conversion factor for invalid units."""
        factor = unit_manager.get_conversion_factor('length', 'invalid', 'km')
        assert factor is None


class TestConvertValue:
    """Tests for convert_value method."""

    def test_length_conversion_meter_to_foot(self, unit_manager):
        """Test length conversion from meter to foot."""
        result = unit_manager.convert_value('length', 'm', 'ft', 1)
        # 1 meter = 3.28084 feet
        assert result == pytest.approx(3.28084, rel=1e-4)

    def test_length_conversion_kilometer_to_mile(self, unit_manager):
        """Test length conversion from kilometer to mile."""
        result = unit_manager.convert_value('length', 'km', 'mi', 1)
        # 1 kilometer = 0.621371 miles
        assert result == pytest.approx(0.621371, rel=1e-4)

    def test_weight_conversion_kg_to_lb(self, unit_manager):
        """Test weight conversion from kilogram to pound."""
        result = unit_manager.convert_value('weight', 'kg', 'lb', 1)
        # 1 kg = 2.20462 pounds
        assert result == pytest.approx(2.20462, rel=1e-4)

    def test_conversion_with_string_value(self, unit_manager):
        """Test conversion with string value."""
        result = unit_manager.convert_value('length', 'm', 'km', '1000')
        assert result == pytest.approx(1.0)

    def test_conversion_with_invalid_value(self, unit_manager):
        """Test conversion with invalid value."""
        result = unit_manager.convert_value('length', 'm', 'km', 'invalid')
        assert result is None

    def test_conversion_with_none_value(self, unit_manager):
        """Test conversion with None value."""
        result = unit_manager.convert_value('length', 'm', 'km', None)
        assert result is None

    def test_conversion_zero_value(self, unit_manager):
        """Test conversion with zero value."""
        result = unit_manager.convert_value('length', 'm', 'km', 0)
        assert result == 0.0

    def test_conversion_negative_value(self, unit_manager):
        """Test conversion with negative value."""
        result = unit_manager.convert_value('length', 'm', 'km', -1000)
        assert result == pytest.approx(-1.0)


class TestTemperatureConversion:
    """Tests for temperature conversions."""

    def test_celsius_to_fahrenheit_freezing(self, unit_manager):
        """Test Celsius to Fahrenheit at freezing point."""
        result = unit_manager.convert_value('temperature', 'c', 'f', 0)
        assert result == pytest.approx(32.0)

    def test_celsius_to_fahrenheit_boiling(self, unit_manager):
        """Test Celsius to Fahrenheit at boiling point."""
        result = unit_manager.convert_value('temperature', 'c', 'f', 100)
        assert result == pytest.approx(212.0)

    def test_fahrenheit_to_celsius_freezing(self, unit_manager):
        """Test Fahrenheit to Celsius at freezing point."""
        result = unit_manager.convert_value('temperature', 'f', 'c', 32)
        assert result == pytest.approx(0.0)

    def test_fahrenheit_to_celsius_boiling(self, unit_manager):
        """Test Fahrenheit to Celsius at boiling point."""
        result = unit_manager.convert_value('temperature', 'f', 'c', 212)
        assert result == pytest.approx(100.0)

    def test_celsius_to_kelvin(self, unit_manager):
        """Test Celsius to Kelvin conversion."""
        result = unit_manager.convert_value('temperature', 'c', 'k', 0)
        assert result == pytest.approx(273.15)

    def test_kelvin_to_celsius(self, unit_manager):
        """Test Kelvin to Celsius conversion."""
        result = unit_manager.convert_value('temperature', 'k', 'c', 273.15)
        assert result == pytest.approx(0.0)

    def test_fahrenheit_to_kelvin(self, unit_manager):
        """Test Fahrenheit to Kelvin conversion."""
        result = unit_manager.convert_value('temperature', 'f', 'k', 32)
        assert result == pytest.approx(273.15)

    def test_kelvin_to_fahrenheit(self, unit_manager):
        """Test Kelvin to Fahrenheit conversion."""
        result = unit_manager.convert_value('temperature', 'k', 'f', 273.15)
        assert result == pytest.approx(32.0)

    def test_negative_temperature(self, unit_manager):
        """Test negative temperature conversion."""
        result = unit_manager.convert_value('temperature', 'c', 'f', -40)
        assert result == pytest.approx(-40.0)  # -40°C = -40°F


class TestVolumeConversion:
    """Tests for volume conversions."""

    def test_liter_to_gallon(self, unit_manager):
        """Test liter to gallon conversion."""
        result = unit_manager.convert_value('volume', 'l', 'gal', 1)
        # 1 liter ≈ 0.264172 gallons
        assert result == pytest.approx(0.264172, rel=1e-3)


class TestSpeedConversion:
    """Tests for speed conversions."""

    def test_kph_to_mph(self, unit_manager):
        """Test km/h to mph conversion."""
        result = unit_manager.convert_value('speed', 'kph', 'mph', 100)
        # 100 km/h ≈ 62.137 mph
        assert result == pytest.approx(62.137, rel=1e-3)

    def test_mps_to_knots(self, unit_manager):
        """Test m/s to knots conversion."""
        result = unit_manager.convert_value('speed', 'mps', 'knot', 1)
        # 1 m/s ≈ 1.94384 knots
        assert result == pytest.approx(1.94384, rel=1e-3)


class TestPressureConversion:
    """Tests for pressure conversions."""

    def test_bar_to_psi(self, unit_manager):
        """Test bar to psi conversion."""
        result = unit_manager.convert_value('pressure', 'bar', 'psi', 1)
        # 1 bar ≈ 14.5038 psi
        assert result == pytest.approx(14.5038, rel=1e-3)


class TestEnergyConversion:
    """Tests for energy conversions."""

    def test_joule_to_calorie(self, unit_manager):
        """Test joule to calorie conversion."""
        result = unit_manager.convert_value('energy', 'j', 'cal', 1)
        # 1 joule ≈ 0.239006 calories
        assert result == pytest.approx(0.239006, rel=1e-3)


class TestPowerConversion:
    """Tests for power conversions."""

    def test_watt_to_horsepower(self, unit_manager):
        """Test watt to horsepower conversion."""
        result = unit_manager.convert_value('power', 'w', 'hp', 746)
        # 746 watts ≈ 1 horsepower
        assert result == pytest.approx(1.0, rel=1e-2)
