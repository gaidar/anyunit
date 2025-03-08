# app/routes/main.py
from flask import Blueprint, render_template
from app.utils.unit_converter import UnitManager
from app.utils.seo import generate_meta_tags

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get the complete unit data from UnitManager
    unit_manager = UnitManager()
    categories_data = unit_manager._units_data['categories']
    meta_tags = generate_meta_tags()
    
    return render_template('pages/index.html',
                         categories=categories_data,
                         meta_tags=meta_tags)

@main_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('pages/privacy_policy.html')