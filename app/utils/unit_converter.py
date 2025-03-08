# app/utils/unit_converter.py
import json
import os
from flask import current_app

class UnitManager:
    _instance = None
    _units_data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UnitManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._units_data is None:
            self.load_units_data()

    def load_units_data(self):
        """Load units data from JSON file"""
        json_path = os.path.join(current_app.static_folder, 'data', 'units.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            self._units_data = json.load(f)

    def get_categories(self):
        """Return all categories with their basic info"""
        return {
            cat_id: {
                'title': data['title'],
                'description': data['description'],
                'icon': data['icon']
            }
            for cat_id, data in self._units_data['categories'].items()
        }

    def get_category(self, category_id):
        """Get detailed information about a specific category"""
        return self._units_data['categories'].get(category_id)

    def get_unit_info(self, category_id, unit_id):
        """Get information about a specific unit"""
        category = self.get_category(category_id)
        if category and 'units' in category:
            return category['units'].get(unit_id)
        return None

    def get_conversion_factor(self, category_id, from_unit, to_unit):
        """Get conversion factor between two units"""
        category = self.get_category(category_id)
        if not category or 'units' not in category:
            return None
            
        units = category['units']
        if from_unit not in units or to_unit not in units:
            return None

        if category_id == 'temperature':
            return None  # Temperature requires special conversion formulas
            
        # Calculate conversion factor
        from_factor = units[from_unit]['factor']
        to_factor = units[to_unit]['factor']
        
        return from_factor / to_factor

    def convert_value(self, category_id, from_unit, to_unit, value):
        """Convert a value between units"""
        try:
            value = float(value)
        except (TypeError, ValueError):
            return None

        if category_id == 'temperature':
            return self._convert_temperature(from_unit, to_unit, value)

        factor = self.get_conversion_factor(category_id, from_unit, to_unit)
        if factor is None:
            return None

        return value * factor

    def _convert_temperature(self, from_unit, to_unit, value):
        """Handle temperature conversions"""
        conversions = {
            'c_to_f': lambda c: (c * 9/5) + 32,
            'f_to_c': lambda f: (f - 32) * 5/9,
            'c_to_k': lambda c: c + 273.15,
            'k_to_c': lambda k: k - 273.15,
            'f_to_k': lambda f: (f - 32) * 5/9 + 273.15,
            'k_to_f': lambda k: (k - 273.15) * 9/5 + 32
        }
        
        conversion_key = f"{from_unit}_to_{to_unit}"
        if conversion_key in conversions:
            return conversions[conversion_key](value)
        
        return None

    def get_length_conversion_tables(self):
        return [
            {
                "title": "Inches to Other Units",
                "description": "Common conversions from inches to other length units",
                "conversions": [
                    {"from": "inch", "to": "foot", "ratio": "1 inch = 0.0833 feet", "note": "12 inches = 1 foot"},
                    {"from": "inch", "to": "yard", "ratio": "1 inch = 0.0278 yards", "note": "36 inches = 1 yard"},
                    {"from": "inch", "to": "meter", "ratio": "1 inch = 0.0254 meters", "note": "Standard metric conversion"},
                    {"from": "inch", "to": "centimeter", "ratio": "1 inch = 2.54 centimeters", "note": "Common conversion in crafts"},
                    {"from": "inch", "to": "millimeter", "ratio": "1 inch = 25.4 millimeters", "note": "Used in precision measurements"}
                ]
            },
            {
                "title": "Feet to Other Units",
                "description": "Common conversions from feet to other length units",
                "conversions": [
                    {"from": "foot", "to": "inch", "ratio": "1 foot = 12 inches", "note": "Basic imperial conversion"},
                    {"from": "foot", "to": "yard", "ratio": "1 foot = 0.333 yards", "note": "3 feet = 1 yard"},
                    {"from": "foot", "to": "meter", "ratio": "1 foot = 0.3048 meters", "note": "Standard metric conversion"},
                    {"from": "foot", "to": "mile", "ratio": "1 foot = 0.000189 miles", "note": "5,280 feet = 1 mile"}
                ]
            },
            {
                "title": "Meters to Other Units",
                "description": "Common conversions from meters to other length units",
                "conversions": [
                    {"from": "meter", "to": "centimeter", "ratio": "1 meter = 100 centimeters", "note": "Basic metric conversion"},
                    {"from": "meter", "to": "kilometer", "ratio": "1 meter = 0.001 kilometers", "note": "1,000 meters = 1 kilometer"},
                    {"from": "meter", "to": "foot", "ratio": "1 meter = 3.28084 feet", "note": "Common imperial conversion"},
                    {"from": "meter", "to": "yard", "ratio": "1 meter = 1.09361 yards", "note": "Used in international sports"}
                ]
            },
            {
                "title": "Miles to Other Units",
                "description": "Common conversions from miles to other length units",
                "conversions": [
                    {"from": "mile", "to": "kilometer", "ratio": "1 mile = 1.60934 kilometers", "note": "International standard conversion"},
                    {"from": "mile", "to": "foot", "ratio": "1 mile = 5,280 feet", "note": "Basic imperial definition"},
                    {"from": "mile", "to": "yard", "ratio": "1 mile = 1,760 yards", "note": "Common in land measurement"},
                    {"from": "mile", "to": "meter", "ratio": "1 mile = 1,609.34 meters", "note": "Used in international comparisons"}
                ]
            }
        ]

    def get_temperature_conversion_tables(self):
    
        return [
            {
                "title": "Celsius to Other Units",
                "description": "Common conversions from Celsius to other temperature units",
                "conversions": [
                    {"from": "celsius", "to": "fahrenheit", "formula": "°F = (°C × 9/5) + 32", "note": "Standard conversion formula"},
                    {"from": "celsius", "to": "kelvin", "formula": "K = °C + 273.15", "note": "Scientific standard conversion"}
                ]
            },
            {
                "title": "Fahrenheit to Other Units",
                "description": "Common conversions from Fahrenheit to other temperature units",
                "conversions": [
                    {"from": "fahrenheit", "to": "celsius", "formula": "°C = (°F - 32) × 5/9", "note": "Standard conversion formula"},
                    {"from": "fahrenheit", "to": "kelvin", "formula": "K = (°F - 32) × 5/9 + 273.15", "note": "Less common but useful"}
                ]
            },
            {
                "title": "Important Temperature Points",
                "description": "Reference points in different temperature scales",
                "points": [
                    {"description": "Water Freezing Point", "celsius": "0°C", "fahrenheit": "32°F", "kelvin": "273.15K"},
                    {"description": "Water Boiling Point", "celsius": "100°C", "fahrenheit": "212°F", "kelvin": "373.15K"},
                    {"description": "Room Temperature", "celsius": "20-22°C", "fahrenheit": "68-72°F", "kelvin": "293-295K"},
                    {"description": "Body Temperature", "celsius": "37°C", "fahrenheit": "98.6°F", "kelvin": "310.15K"},
                    {"description": "Absolute Zero", "celsius": "-273.15°C", "fahrenheit": "-459.67°F", "kelvin": "0K"}
                ]
            }
        ]

    def get_weight_conversion_tables(self):
        return [
            {
                "title": "Pounds to Other Units",
                "description": "Common conversions from pounds to other weight/mass units",
                "conversions": [
                    {"from": "pound", "to": "ounce", "ratio": "1 pound = 16 ounces", "note": "Basic imperial conversion"},
                    {"from": "pound", "to": "kilogram", "ratio": "1 pound = 0.453592 kilograms", "note": "Standard metric conversion"},
                    {"from": "pound", "to": "gram", "ratio": "1 pound = 453.592 grams", "note": "Common in international recipes"},
                    {"from": "pound", "to": "stone", "ratio": "1 pound = 0.0714286 stone", "note": "14 pounds = 1 stone (UK measurement)"}
                ]
            },
            {
                "title": "Kilograms to Other Units",
                "description": "Common conversions from kilograms to other weight/mass units",
                "conversions": [
                    {"from": "kilogram", "to": "gram", "ratio": "1 kilogram = 1,000 grams", "note": "Basic metric conversion"},
                    {"from": "kilogram", "to": "pound", "ratio": "1 kilogram = 2.20462 pounds", "note": "Standard imperial conversion"},
                    {"from": "kilogram", "to": "ounce", "ratio": "1 kilogram = 35.274 ounces", "note": "Used in international trade"},
                    {"from": "kilogram", "to": "metric ton", "ratio": "1 kilogram = 0.001 metric tons", "note": "1,000 kilograms = 1 metric ton"}
                ]
            },
            {
                "title": "Ounces to Other Units",
                "description": "Common conversions from ounces to other weight/mass units",
                "conversions": [
                    {"from": "ounce", "to": "pound", "ratio": "1 ounce = 0.0625 pounds", "note": "16 ounces = 1 pound"},
                    {"from": "ounce", "to": "gram", "ratio": "1 ounce = 28.3495 grams", "note": "Common in cooking conversions"},
                    {"from": "ounce", "to": "kilogram", "ratio": "1 ounce = 0.0283495 kilograms", "note": "Used in international shipping"}
                ]
            },
            {
                "title": "Tons to Other Units",
                "description": "Common conversions from tons to other weight/mass units",
                "conversions": [
                    {"from": "ton", "to": "pound", "ratio": "1 ton = 2,000 pounds", "note": "US short ton definition"},
                    {"from": "ton", "to": "kilogram", "ratio": "1 ton = 907.185 kilograms", "note": "US short ton to metric"},
                    {"from": "metric ton", "to": "ton", "ratio": "1 metric ton = 1.10231 tons", "note": "Metric to US ton conversion"},
                    {"from": "metric ton", "to": "kilogram", "ratio": "1 metric ton = 1,000 kilograms", "note": "Basic metric definition"}
                ]
            }
        ]

    def get_detailed_conversion_tables(self, category_id):
        """Get detailed conversion tables for a specific category"""
        if category_id == 'length':
            return self.get_length_conversion_tables()
        elif category_id == 'temperature':
            return self.get_temperature_conversion_tables()
        elif category_id == 'weight':
            return self.get_weight_conversion_tables()
        else:
            return []