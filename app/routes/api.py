# app/routes/api.py
from flask import Blueprint, jsonify, request
from app.utils.unit_converter import UnitManager

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        required_fields = ['category', 'fromUnit', 'toUnit', 'value']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Get the value and ensure it's a number
        try:
            value = float(data['value'])
        except (TypeError, ValueError):
            return jsonify({'success': False, 'error': 'Invalid value provided'}), 400
        
        # Perform conversion
        unit_manager = UnitManager()
        result = unit_manager.convert_value(
            data['category'],
            data['fromUnit'],
            data['toUnit'],
            value
        )
        
        if result is None:
            return jsonify({'success': False, 'error': 'Invalid conversion'}), 400
        
        # Format the result
        formatted_result = format_number(result)
        
        return jsonify({
            'success': True,
            'result': result,
            'formatted': formatted_result
        })
    
    except Exception as e:
        print(f"Conversion error: {str(e)}")  # For debugging
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

def format_number(value):
    """Format number for display"""
    try:
        if abs(value) >= 1e6 or (abs(value) < 1e-6 and value != 0):
            return f"{value:.6e}"
        else:
            # Remove trailing zeros and decimal point if not needed
            return f"{value:.6f}".rstrip('0').rstrip('.')
    except (TypeError, ValueError):
        return str(value)