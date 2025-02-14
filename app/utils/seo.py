# app/utils/seo.py
def generate_meta_tags(category=None, from_unit=None, to_unit=None):
    """Generate meta tags for different pages"""
    if category and from_unit and to_unit:
        return {
            'title': f"Convert {from_unit.upper()} to {to_unit.upper()} | {category.title()} Converter",
            'description': f"Convert {from_unit.upper()} to {to_unit.upper()} easily with our free online converter. Get instant, accurate {category} conversions.",
            'canonical': f"/convert/{category}/{from_unit}-to-{to_unit}"
        }
    elif category:
        return {
            'title': f"{category.title()} Converter | Unit Conversion",
            'description': f"Convert between different {category} units instantly. Free online {category} converter with common conversions and formulas.",
            'canonical': f"/convert/{category}"
        }
    else:
        return {
            'title': "Unit Converter | Convert Any Unit Instantly",
            'description': "Free online unit converter. Convert between different units of measurement including length, weight, temperature, and more.",
            'canonical': "/"
        }