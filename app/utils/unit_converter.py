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

    def get_volume_conversion_tables(self):
        return [
        {
            "title": "Fluid Ounces to Other Units",
            "description": "Common conversions from fluid ounces to other volume units",
            "conversions": [
                {"from": "fluid ounce", "to": "cup", "ratio": "1 fluid ounce = 0.125 cups", "note": "8 fluid ounces = 1 cup"},
                {"from": "fluid ounce", "to": "pint", "ratio": "1 fluid ounce = 0.0625 pints", "note": "16 fluid ounces = 1 pint"},
                {"from": "fluid ounce", "to": "quart", "ratio": "1 fluid ounce = 0.03125 quarts", "note": "32 fluid ounces = 1 quart"},
                {"from": "fluid ounce", "to": "gallon", "ratio": "1 fluid ounce = 0.0078125 gallons", "note": "128 fluid ounces = 1 gallon"},
                {"from": "fluid ounce", "to": "milliliter", "ratio": "1 fluid ounce = 29.5735 milliliters", "note": "Standard metric conversion"}
            ]
        },
        {
            "title": "Cups to Other Units",
            "description": "Common conversions from cups to other volume units",
            "conversions": [
                {"from": "cup", "to": "fluid ounce", "ratio": "1 cup = 8 fluid ounces", "note": "Common in cooking"},
                {"from": "cup", "to": "pint", "ratio": "1 cup = 0.5 pints", "note": "2 cups = 1 pint"},
                {"from": "cup", "to": "milliliter", "ratio": "1 cup = 236.588 milliliters", "note": "Standard metric conversion"},
                {"from": "cup", "to": "liter", "ratio": "1 cup = 0.236588 liters", "note": "For larger recipes"}
            ]
        },
        {
            "title": "Liters to Other Units",
            "description": "Common conversions from liters to other volume units",
            "conversions": [
                {"from": "liter", "to": "milliliter", "ratio": "1 liter = 1,000 milliliters", "note": "Basic metric conversion"},
                {"from": "liter", "to": "gallon", "ratio": "1 liter = 0.264172 gallons", "note": "Important for fuel calculations"},
                {"from": "liter", "to": "quart", "ratio": "1 liter = 1.05669 quarts", "note": "Common for comparing products"},
                {"from": "liter", "to": "cubic meter", "ratio": "1 liter = 0.001 cubic meters", "note": "1,000 liters = 1 cubic meter"}
            ]
        },
        {
            "title": "Gallons to Other Units",
            "description": "Common conversions from gallons to other volume units",
            "conversions": [
                {"from": "gallon", "to": "quart", "ratio": "1 gallon = 4 quarts", "note": "Basic imperial conversion"},
                {"from": "gallon", "to": "pint", "ratio": "1 gallon = 8 pints", "note": "Common for liquids"},
                {"from": "gallon", "to": "cup", "ratio": "1 gallon = 16 cups", "note": "Used in cooking conversions"},
                {"from": "gallon", "to": "fluid ounce", "ratio": "1 gallon = 128 fluid ounces", "note": "Precise measurements"},
                {"from": "gallon", "to": "liter", "ratio": "1 gallon = 3.78541 liters", "note": "Standard metric conversion"}
            ]
        }
    ]

    def get_speed_conversion_tables(self):
        return [
            {
                "title": "Miles per Hour to Other Units",
                "description": "Common conversions from miles per hour to other speed units",
                "conversions": [
                    {"from": "mph", "to": "kph", "ratio": "1 mph = 1.60934 km/h", "note": "Standard conversion used internationally"},
                    {"from": "mph", "to": "mps", "ratio": "1 mph = 0.44704 m/s", "note": "Used in physics calculations"},
                    {"from": "mph", "to": "fps", "ratio": "1 mph = 1.46667 ft/s", "note": "Common in engineering"},
                    {"from": "mph", "to": "knot", "ratio": "1 mph = 0.868976 knots", "note": "Used in maritime and aviation"}
                ]
            },
            {
                "title": "Kilometers per Hour to Other Units",
                "description": "Common conversions from kilometers per hour to other speed units",
                "conversions": [
                    {"from": "kph", "to": "mph", "ratio": "1 km/h = 0.621371 mph", "note": "Standard international conversion"},
                    {"from": "kph", "to": "mps", "ratio": "1 km/h = 0.277778 m/s", "note": "Divide by 3.6 for quick calculation"},
                    {"from": "kph", "to": "fps", "ratio": "1 km/h = 0.911344 ft/s", "note": "Used in engineering"},
                    {"from": "kph", "to": "knot", "ratio": "1 km/h = 0.539957 knots", "note": "Used in maritime and aviation"}
                ]
            },
            {
                "title": "Meters per Second to Other Units",
                "description": "Common conversions from meters per second to other speed units",
                "conversions": [
                    {"from": "mps", "to": "kph", "ratio": "1 m/s = 3.6 km/h", "note": "Standard metric conversion"},
                    {"from": "mps", "to": "mph", "ratio": "1 m/s = 2.23694 mph", "note": "Used in international comparisons"},
                    {"from": "mps", "to": "fps", "ratio": "1 m/s = 3.28084 ft/s", "note": "Used in engineering calculations"},
                    {"from": "mps", "to": "knot", "ratio": "1 m/s = 1.94384 knots", "note": "Used in meteorology and navigation"}
                ]
            },
            {
                "title": "Knots to Other Units",
                "description": "Common conversions from knots to other speed units",
                "conversions": [
                    {"from": "knot", "to": "mph", "ratio": "1 knot = 1.15078 mph", "note": "Used in aviation and maritime"},
                    {"from": "knot", "to": "kph", "ratio": "1 knot = 1.852 km/h", "note": "International standard"},
                    {"from": "knot", "to": "mps", "ratio": "1 knot = 0.514444 m/s", "note": "Used in scientific calculations"},
                    {"from": "knot", "to": "fps", "ratio": "1 knot = 1.68781 ft/s", "note": "Used in engineering"}
                ]
            }
        ]

    def get_pressure_conversion_tables(self):
        return [
            {
                "title": "Pascal to Other Units",
                "description": "Common conversions from pascal to other pressure units",
                "conversions": [
                    {"from": "pa", "to": "kpa", "ratio": "1 Pa = 0.001 kPa", "note": "Basic metric conversion"},
                    {"from": "pa", "to": "bar", "ratio": "1 Pa = 0.00001 bar", "note": "Common engineering conversion"},
                    {"from": "pa", "to": "psi", "ratio": "1 Pa = 0.000145038 psi", "note": "Conversion to imperial unit"},
                    {"from": "pa", "to": "atm", "ratio": "1 Pa = 0.00000986923 atm", "note": "Used in scientific calculations"}
                ]
            },
            {
                "title": "Bar to Other Units",
                "description": "Common conversions from bar to other pressure units",
                "conversions": [
                    {"from": "bar", "to": "kpa", "ratio": "1 bar = 100 kPa", "note": "Common metric conversion"},
                    {"from": "bar", "to": "psi", "ratio": "1 bar = 14.5038 psi", "note": "Important for international specifications"},
                    {"from": "bar", "to": "atm", "ratio": "1 bar = 0.986923 atm", "note": "Approximately 1 atmosphere"},
                    {"from": "bar", "to": "mmhg", "ratio": "1 bar = 750.062 mmHg", "note": "Used in weather and medical applications"}
                ]
            },
            {
                "title": "PSI to Other Units",
                "description": "Common conversions from pounds per square inch to other pressure units",
                "conversions": [
                    {"from": "psi", "to": "kpa", "ratio": "1 psi = 6.89476 kPa", "note": "Standard metric conversion"},
                    {"from": "psi", "to": "bar", "ratio": "1 psi = 0.0689476 bar", "note": "Used in industrial applications"},
                    {"from": "psi", "to": "atm", "ratio": "1 psi = 0.068046 atm", "note": "Used in scientific calculations"},
                    {"from": "psi", "to": "mmhg", "ratio": "1 psi = 51.7149 mmHg", "note": "Used in medical and meteorological contexts"}
                ]
            },
            {
                "title": "Atmosphere to Other Units",
                "description": "Common conversions from atmosphere to other pressure units",
                "conversions": [
                    {"from": "atm", "to": "kpa", "ratio": "1 atm = 101.325 kPa", "note": "Standard atmospheric pressure at sea level"},
                    {"from": "atm", "to": "bar", "ratio": "1 atm = 1.01325 bar", "note": "Slightly more than 1 bar"},
                    {"from": "atm", "to": "psi", "ratio": "1 atm = 14.6959 psi", "note": "Used in engineering and science"},
                    {"from": "atm", "to": "mmhg", "ratio": "1 atm = 760 mmHg", "note": "Traditional definition of atmosphere"}
                ]
            }
        ]

    def get_energy_conversion_tables(self):
        return [
            {
                "title": "Joule to Other Units",
                "description": "Common conversions from joules to other energy units",
                "conversions": [
                    {"from": "j", "to": "kj", "ratio": "1 J = 0.001 kJ", "note": "Basic metric conversion"},
                    {"from": "j", "to": "cal", "ratio": "1 J = 0.239006 cal", "note": "Used in thermal calculations"},
                    {"from": "j", "to": "wh", "ratio": "1 J = 0.000277778 Wh", "note": "Energy to electrical conversion"},
                    {"from": "j", "to": "btu", "ratio": "1 J = 0.000947817 BTU", "note": "Conversion to imperial unit"}
                ]
            },
            {
                "title": "Kilocalorie to Other Units",
                "description": "Common conversions from kilocalories to other energy units",
                "conversions": [
                    {"from": "kcal", "to": "kj", "ratio": "1 kcal = 4.184 kJ", "note": "Used in nutrition"},
                    {"from": "kcal", "to": "j", "ratio": "1 kcal = 4184 J", "note": "Standard scientific conversion"},
                    {"from": "kcal", "to": "wh", "ratio": "1 kcal = 1.16222 Wh", "note": "Used in energy consumption calculations"},
                    {"from": "kcal", "to": "btu", "ratio": "1 kcal = 3.96567 BTU", "note": "Used in heating and cooling"}
                ]
            },
            {
                "title": "Kilowatt-hour to Other Units",
                "description": "Common conversions from kilowatt-hours to other energy units",
                "conversions": [
                    {"from": "kwh", "to": "kj", "ratio": "1 kWh = 3,600 kJ", "note": "Basic electrical energy conversion"},
                    {"from": "kwh", "to": "j", "ratio": "1 kWh = 3,600,000 J", "note": "Full conversion to base SI unit"},
                    {"from": "kwh", "to": "kcal", "ratio": "1 kWh = 860.421 kcal", "note": "Used in heating calculations"},
                    {"from": "kwh", "to": "btu", "ratio": "1 kWh = 3,412.14 BTU", "note": "Used in HVAC applications"}
                ]
            },
            {
                "title": "BTU to Other Units",
                "description": "Common conversions from British Thermal Units to other energy units",
                "conversions": [
                    {"from": "btu", "to": "j", "ratio": "1 BTU = 1,055.06 J", "note": "Standard scientific conversion"},
                    {"from": "btu", "to": "kj", "ratio": "1 BTU = 1.05506 kJ", "note": "Used in engineering"},
                    {"from": "btu", "to": "kcal", "ratio": "1 BTU = 0.252164 kcal", "note": "Used in heating applications"},
                    {"from": "btu", "to": "kwh", "ratio": "1 BTU = 0.000293071 kWh", "note": "Used in energy efficiency calculations"}
                ]
            }
        ]

    def get_power_conversion_tables(self):
        return [
            {
                "title": "Watt to Other Units",
                "description": "Common conversions from watts to other power units",
                "conversions": [
                    {"from": "w", "to": "kw", "ratio": "1 W = 0.001 kW", "note": "Basic metric conversion"},
                    {"from": "w", "to": "hp", "ratio": "1 W = 0.00134102 hp", "note": "Conversion to mechanical power"},
                    {"from": "w", "to": "btuh", "ratio": "1 W = 3.41214 BTU/h", "note": "Used in HVAC applications"}
                ]
            },
            {
                "title": "Kilowatt to Other Units",
                "description": "Common conversions from kilowatts to other power units",
                "conversions": [
                    {"from": "kw", "to": "w", "ratio": "1 kW = 1,000 W", "note": "Basic metric conversion"},
                    {"from": "kw", "to": "hp", "ratio": "1 kW = 1.34102 hp", "note": "Common conversion for engines and motors"},
                    {"from": "kw", "to": "btuh", "ratio": "1 kW = 3,412.14 BTU/h", "note": "Used in heating and cooling"}
                ]
            },
            {
                "title": "Horsepower to Other Units",
                "description": "Common conversions from horsepower to other power units",
                "conversions": [
                    {"from": "hp", "to": "w", "ratio": "1 hp = 745.7 W", "note": "Standard conversion"},
                    {"from": "hp", "to": "kw", "ratio": "1 hp = 0.7457 kW", "note": "Used in automotive and industrial applications"},
                    {"from": "hp", "to": "btuh", "ratio": "1 hp = 2,544.43 BTU/h", "note": "Used in engine specifications"}
                ]
            },
            {
                "title": "BTU/hour to Other Units",
                "description": "Common conversions from BTU per hour to other power units",
                "conversions": [
                    {"from": "btuh", "to": "w", "ratio": "1 BTU/h = 0.293071 W", "note": "Used in heating and cooling"},
                    {"from": "btuh", "to": "kw", "ratio": "1 BTU/h = 0.000293071 kW", "note": "Common HVAC conversion"},
                    {"from": "btuh", "to": "hp", "ratio": "1 BTU/h = 0.000393015 hp", "note": "Used in power comparisons"}
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
        elif category_id == 'volume':
            return self.get_volume_conversion_tables()
        elif category_id == 'speed':
            return self.get_speed_conversion_tables()
        elif category_id == 'pressure':
            return self.get_pressure_conversion_tables()
        elif category_id == 'energy':
            return self.get_energy_conversion_tables()
        elif category_id == 'power':
            return self.get_power_conversion_tables()
        else:
            return []