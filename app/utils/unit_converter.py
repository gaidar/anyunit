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
        return self._units_data['categories'].get(category_id)

    def get_unit_info(self, category_id, unit_id):
        category = self.get_category(category_id)
        if category and 'units' in category:
            return category['units'].get(unit_id)
        return None

    def get_conversion_factor(self, category_id, from_unit, to_unit):
        category = self.get_category(category_id)
        if not category or 'units' not in category:
            return None
            
        units = category['units']
        if from_unit not in units or to_unit not in units:
            return None

        if category_id == 'temperature':
            return None  # Temperature requires special conversion formulas
            
        from_factor = units[from_unit]['factor']
        to_factor = units[to_unit]['factor']
        
        return from_factor / to_factor

    def convert_value(self, category_id, from_unit, to_unit, value):
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

    def get_detailed_conversion_tables(self, category_id):
        json_path = os.path.join(current_app.static_folder, 'data', category_id + '.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)