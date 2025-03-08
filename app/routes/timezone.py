from flask import Blueprint, render_template, current_app
import json
import os

timezone_bp = Blueprint('timezone', __name__)

def load_timezone_data():
    json_path = os.path.join(current_app.static_folder, 'data', 'timezones.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception as e:
        current_app.logger.error(f"Error loading timezone data: {str(e)}")
        # Return empty data as fallback
        return {"timezones": [], "cities_data": {}}

@timezone_bp.route('/')
def index():
    
    timezone_data = load_timezone_data()
    
    return render_template('pages/timezone.html', 
                          timezone_data=timezone_data['timezones'],
                          cities_data=timezone_data['cities_data'])