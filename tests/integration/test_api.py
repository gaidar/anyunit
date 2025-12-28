"""Integration tests for API endpoints."""

import pytest
import json


class TestConvertApi:
    """Tests for /api/convert endpoint."""

    def test_successful_conversion(self, client):
        """Test successful unit conversion."""
        response = client.post('/api/convert',
            data=json.dumps({
                'category': 'length',
                'fromUnit': 'm',
                'toUnit': 'ft',
                'value': 1
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'result' in data
        assert 'formatted' in data
        assert data['result'] == pytest.approx(3.28084, rel=1e-4)

    def test_temperature_conversion(self, client):
        """Test temperature conversion."""
        response = client.post('/api/convert',
            data=json.dumps({
                'category': 'temperature',
                'fromUnit': 'c',
                'toUnit': 'f',
                'value': 100
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['result'] == pytest.approx(212.0)

    def test_missing_fields(self, client):
        """Test conversion with missing required fields."""
        response = client.post('/api/convert',
            data=json.dumps({
                'category': 'length',
                'fromUnit': 'm'
                # Missing toUnit and value
            }),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'error' in data

    def test_invalid_category(self, client):
        """Test conversion with invalid category."""
        response = client.post('/api/convert',
            data=json.dumps({
                'category': 'invalid',
                'fromUnit': 'm',
                'toUnit': 'ft',
                'value': 1
            }),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False

    def test_invalid_units(self, client):
        """Test conversion with invalid units."""
        response = client.post('/api/convert',
            data=json.dumps({
                'category': 'length',
                'fromUnit': 'invalid',
                'toUnit': 'ft',
                'value': 1
            }),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False

    def test_invalid_value(self, client):
        """Test conversion with invalid value."""
        response = client.post('/api/convert',
            data=json.dumps({
                'category': 'length',
                'fromUnit': 'm',
                'toUnit': 'ft',
                'value': 'not-a-number'
            }),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False

    def test_no_data(self, client):
        """Test conversion with no data."""
        response = client.post('/api/convert',
            content_type='application/json'
        )

        # Server returns 400 or 500 for malformed/empty requests
        assert response.status_code in (400, 500)

    def test_zero_value(self, client):
        """Test conversion with zero value."""
        response = client.post('/api/convert',
            data=json.dumps({
                'category': 'length',
                'fromUnit': 'm',
                'toUnit': 'ft',
                'value': 0
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['result'] == 0

    def test_large_value(self, client):
        """Test conversion with large value."""
        response = client.post('/api/convert',
            data=json.dumps({
                'category': 'length',
                'fromUnit': 'm',
                'toUnit': 'km',
                'value': 1000000
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['result'] == pytest.approx(1000.0)


class TestAviationFuelCalcApi:
    """Tests for /aviation/api/aviation/fuel-calc endpoint."""

    def test_successful_calculation(self, client):
        """Test successful fuel calculation."""
        response = client.post('/aviation/api/aviation/fuel-calc',
            data=json.dumps({
                'distance': 100,
                'indicatedAirspeed': 100,
                'fuelConsumption': 10,
                'windSpeed': 0,
                'windDirection': 0,
                'heading': 0,
                'reserveTime': 45
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'ground_speed' in data
        assert 'flight_time' in data
        assert 'fuel_required' in data
        assert 'reserve_fuel' in data

    def test_with_headwind(self, client):
        """Test fuel calculation with headwind."""
        response = client.post('/aviation/api/aviation/fuel-calc',
            data=json.dumps({
                'distance': 100,
                'indicatedAirspeed': 100,
                'fuelConsumption': 10,
                'windSpeed': 20,
                'windDirection': 0,
                'heading': 0,
                'reserveTime': 45
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['ground_speed'] < 100  # Reduced by headwind

    def test_invalid_data(self, client):
        """Test fuel calculation with invalid data."""
        response = client.post('/aviation/api/aviation/fuel-calc',
            data=json.dumps({
                'distance': 0,  # Invalid
                'indicatedAirspeed': 100,
                'fuelConsumption': 10,
                'reserveTime': 45
            }),
            content_type='application/json'
        )

        assert response.status_code == 400


class TestAviationGroundSpeedApi:
    """Tests for /aviation/api/aviation/ground-speed endpoint."""

    def test_successful_calculation(self, client):
        """Test successful ground speed calculation."""
        response = client.post('/aviation/api/aviation/ground-speed',
            data=json.dumps({
                'indicatedAirspeed': 120,
                'windSpeed': 10,
                'windDirection': 180,
                'heading': 0,
                'temperature': 15,
                'pressureAltitude': 0
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'ground_speed' in data
        assert 'density_altitude' in data
        assert 'headwind_component' in data
        assert 'crosswind_component' in data

    def test_at_altitude(self, client):
        """Test ground speed calculation at altitude."""
        response = client.post('/aviation/api/aviation/ground-speed',
            data=json.dumps({
                'indicatedAirspeed': 100,
                'windSpeed': 0,
                'windDirection': 0,
                'heading': 0,
                'temperature': 5,
                'pressureAltitude': 5000
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        # TAS should be higher than IAS at altitude
        assert data['ground_speed'] > 100


class TestAviationDensityAltitudeApi:
    """Tests for /aviation/api/aviation/density-altitude endpoint."""

    def test_successful_calculation(self, client):
        """Test successful density altitude calculation."""
        response = client.post('/aviation/api/aviation/density-altitude',
            data=json.dumps({
                'pressureAltitude': 5000,
                'temperature': 25
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'density_altitude' in data
        # Hot day at 5000ft should have high DA
        assert data['density_altitude'] > 5000

    def test_standard_conditions(self, client):
        """Test density altitude at standard conditions."""
        response = client.post('/aviation/api/aviation/density-altitude',
            data=json.dumps({
                'pressureAltitude': 0,
                'temperature': 15
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['density_altitude'] == pytest.approx(0.0, abs=10)

    def test_empty_strings_default(self, client):
        """Test density altitude with empty strings (uses defaults)."""
        response = client.post('/aviation/api/aviation/density-altitude',
            data=json.dumps({
                'pressureAltitude': '',
                'temperature': ''
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'density_altitude' in data


class TestMarkdownApi:
    """Tests for markdown conversion endpoint."""

    def test_convert_markdown_to_html(self, client):
        """Test markdown to HTML conversion."""
        response = client.post('/markdown/convert',
            data=json.dumps({
                'markdown': '# Hello World\n\nThis is **bold** text.'
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert '<h1>' in data['html']
        assert '<strong>' in data['html']

    def test_convert_markdown_tables(self, client):
        """Test markdown table conversion."""
        response = client.post('/markdown/convert',
            data=json.dumps({
                'markdown': '| Col1 | Col2 |\n|------|------|\n| A | B |'
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert '<table>' in data['html']

    def test_convert_no_markdown(self, client):
        """Test conversion with no markdown provided."""
        response = client.post('/markdown/convert',
            data=json.dumps({}),
            content_type='application/json'
        )

        assert response.status_code == 400
