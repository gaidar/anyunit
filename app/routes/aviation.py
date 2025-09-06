from flask import Blueprint, render_template, jsonify, request
from app.utils.aviation_calculations import (
    calculate_fuel_requirements,
    calculate_ground_speed,
    calculate_density_altitude,
    calculate_crosswind
)
from app.utils.seo import generate_meta_tags

aviation = Blueprint('aviation', __name__)

@aviation.route('/')
def aviation_calculators():
    meta_tags = generate_meta_tags(base_url=request.url_root)
    return render_template('aviation/index.html', meta_tags=meta_tags)

@aviation.route('/api/aviation/fuel-calc', methods=['POST'])
def fuel_calculator():
    data = request.get_json()
    try:
        result = calculate_fuel_requirements(
            distance=float(data['distance']),
            indicated_airspeed=float(data['indicatedAirspeed']),
            fuel_consumption=float(data['fuelConsumption']),
            wind_speed=float(data.get('windSpeed', 0)),
            wind_direction=float(data.get('windDirection', 0)),
            heading=float(data.get('heading', 0)),
            reserve_time=float(data['reserveTime'])
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@aviation.route('/api/aviation/ground-speed', methods=['POST'])
def ground_speed_calculator():
    data = request.get_json()
    try:
        result = calculate_ground_speed(
            indicated_airspeed=float(data['indicatedAirspeed']),
            wind_speed=float(data['windSpeed']),
            wind_direction=float(data['windDirection']),
            heading=float(data['heading']),
            temperature=float(data['temperature']),
            pressure_altitude=float(data.get('pressureAltitude', 0))
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@aviation.route('/api/aviation/density-altitude', methods=['POST'])
def density_altitude_calculator():
    data = request.get_json()
    try:
        # Handle empty strings by using get() with default values
        pressure_altitude = data.get('pressureAltitude', '')
        temperature = data.get('temperature', '')
        
        # Convert empty strings to default values
        if pressure_altitude == '':
            pressure_altitude = '0'
        if temperature == '':
            temperature = '15'
            
        result = calculate_density_altitude(
            pressure_altitude=float(pressure_altitude),
            temperature=float(temperature)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
