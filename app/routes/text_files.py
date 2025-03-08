from flask import Blueprint, render_template

text_files_bp = Blueprint('text_files', __name__)

@text_files_bp.route('/')
def index():
    """Render the text files converter page"""
    
    # Define the supported conversion formats
    conversion_formats = [
        {"id": "json-to-xml", "name": "JSON to XML"},
        {"id": "json-to-csv", "name": "JSON to CSV"},
        {"id": "csv-to-json", "name": "CSV to JSON"},
        {"id": "csv-to-xml", "name": "CSV to XML"},
        {"id": "xml-to-json", "name": "XML to JSON"},
        {"id": "xml-to-csv", "name": "XML to CSV"}
    ]
    
    return render_template('pages/text_files.html', conversion_formats=conversion_formats)