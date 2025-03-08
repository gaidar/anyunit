# app/routes/converter.py
from flask import Blueprint, render_template, jsonify, request, abort, current_app, redirect, url_for
from app.utils.unit_converter import UnitManager
from app.utils.seo import generate_meta_tags

converter_bp = Blueprint('converter', __name__)

def get_related_conversions(category_info, current_from, current_to):
    """Get related conversions for the current conversion"""
    related = []
    seen = set()
    
    # Add popular conversions first
    if 'popular_conversions' in category_info:
        for conv in category_info['popular_conversions']:
            key = f"{conv['from']}-{conv['to']}"
            if key not in seen and (conv['from'] != current_from or conv['to'] != current_to):
                related.append({
                    'title': f"{category_info['units'][conv['from']]['name']} to {category_info['units'][conv['to']]['name']}",
                    'url': f"/{conv['from']}-to-{conv['to']}"
                })
                seen.add(key)
    
    # Add conversions that share the same units
    units = category_info['units']
    for unit_id, unit_info in units.items():
        if unit_info.get('popular', False):
            # If unit is current 'from' unit, suggest conversions to other popular units
            if unit_id == current_from:
                for other_unit, other_info in units.items():
                    if other_unit != current_to and other_info.get('popular', False):
                        key = f"{unit_id}-{other_unit}"
                        if key not in seen:
                            related.append({
                                'title': f"{unit_info['name']} to {other_info['name']}",
                                'url': f"/{unit_id}-to-{other_unit}"
                            })
                            seen.add(key)
            
            # If unit is current 'to' unit, suggest conversions from other popular units
            elif unit_id == current_to:
                for other_unit, other_info in units.items():
                    if other_unit != current_from and other_info.get('popular', False):
                        key = f"{other_unit}-{unit_id}"
                        if key not in seen:
                            related.append({
                                'title': f"{other_info['name']} to {unit_info['name']}",
                                'url': f"/{other_unit}-to-{unit_id}"
                            })
                            seen.add(key)
    
    # Limit to 6 related conversions
    return related[:6]

def format_number(value):
    """Format number for display"""
    try:
        # Handle None or empty values
        if value is None:
            return "0"
            
        # Convert to float if string
        if isinstance(value, str):
            value = float(value)
            
        # Use scientific notation for very large or small numbers
        if abs(value) >= 1e6 or (abs(value) < 1e-6 and abs(value) > 0):
            return f"{value:.6e}"
            
        # For "normal" numbers, use regular formatting with up to 6 decimal places
        # Remove trailing zeros after decimal point
        return f"{value:.6f}".rstrip('0').rstrip('.')
    except (ValueError, TypeError):
        return "0"

def generate_conversion_table(unit_manager, category, from_unit, to_unit):
    """Generate a table of common conversion values"""
    result = []
    
    # Define common values based on unit type
    if category == 'temperature':
        base_values = [-40, -20, 0, 20, 40, 60, 80, 100]
    else:
        # Generate exponential values for other unit types
        base_values = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
    
    for value in base_values:
        converted = unit_manager.convert_value(category, from_unit, to_unit, value)
        if converted is not None:
            result.append({
                'from': format_number(value),
                'to': format_number(converted)
            })
    
    return result

def normalize_category(category):
    """Normalize category name to match our data structure"""
    return category.lower()

@converter_bp.route('/<category>/')
def category(category):
    # Normalize the category name
    normalized_category = normalize_category(category)
    
    # If the original category was different from normalized, redirect
    if category != normalized_category:
        return redirect(url_for('converter.category', category=normalized_category))
    
    unit_manager = UnitManager()
    category_info = unit_manager.get_category(normalized_category)
    
    if not category_info:
        abort(404)
    
    # Generate conversion tables for common conversions
    conversion_tables = []
    if 'popular_conversions' in category_info:
        for conv in category_info['popular_conversions']:
            table_values = generate_conversion_table(unit_manager, normalized_category, conv['from'], conv['to'])
            table = {
                'title': f"{category_info['units'][conv['from']]['name']} to {category_info['units'][conv['to']]['name']}",
                'from_unit': category_info['units'][conv['from']]['symbol'],
                'to_unit': category_info['units'][conv['to']]['symbol'],
                'table_values': table_values
            }
            conversion_tables.append(table)
    
    # Get detailed conversion tables for special categories
    detailed_tables = []
    if normalized_category in ['length', 'temperature', 'weight', 'volume']:
        detailed_tables = unit_manager.get_detailed_conversion_tables(normalized_category)
    
    meta_tags = generate_meta_tags(category=normalized_category)
    
    return render_template('pages/category.html',
                         category=normalized_category,
                         category_info=category_info,
                         units=category_info['units'],
                         conversion_tables=conversion_tables,
                         detailed_tables=detailed_tables,
                         meta_tags=meta_tags)

@converter_bp.route('/<category>/<from_unit>-to-<to_unit>')
def convert(category, from_unit, to_unit):
    # Normalize the category name
    normalized_category = normalize_category(category)
    
    # If the original category was different from normalized, redirect
    if category != normalized_category:
        return redirect(url_for('converter.convert', 
                              category=normalized_category,
                              from_unit=from_unit,
                              to_unit=to_unit))
    
    unit_manager = UnitManager()
    category_info = unit_manager.get_category(normalized_category)
    
    if not category_info or from_unit not in category_info['units'] or to_unit not in category_info['units']:
        abort(404)
    
    unit_info = {
        'from': category_info['units'][from_unit],
        'to': category_info['units'][to_unit]
    }
    
    # Generate common values table
    common_values = generate_conversion_table(unit_manager, normalized_category, from_unit, to_unit)
    
    # Get conversion formula if applicable
    formula = None
    if 'formulas' in category_info:
        formula_key = f"{from_unit}_to_{to_unit}"
        formula = category_info['formulas'].get(formula_key)
    
    # Get related conversions
    related_conversions = get_related_conversions(category_info, from_unit, to_unit)
    
    meta_tags = generate_meta_tags(
        category=normalized_category, 
        from_unit=from_unit, 
        to_unit=to_unit
    )
    
    return render_template('pages/convert.html',
                         category=normalized_category,
                         from_unit=from_unit,
                         to_unit=to_unit,
                         unit_info=unit_info,
                         common_values=common_values,
                         formula=formula,
                         related_conversions=related_conversions,
                         meta_tags=meta_tags)

@converter_bp.route('/api/convert', methods=['POST'])
def api_convert():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        required_fields = ['category', 'fromUnit', 'toUnit', 'value']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        unit_manager = UnitManager()
        result = unit_manager.convert_value(
            data['category'],
            data['fromUnit'],
            data['toUnit'],
            data['value']
        )
        
        if result is None:
            return jsonify({'success': False, 'error': 'Invalid conversion'}), 400
        
        return jsonify({
            'success': True,
            'result': result,
            'formatted': format_number(result)
        })
    
    except Exception as e:
        current_app.logger.error(f"Conversion error: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

# Error handlers
@converter_bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@converter_bp.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500