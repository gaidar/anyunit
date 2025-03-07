from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.converter import converter_bp
    from app.routes.api import api_bp
    from app.routes.markdown_converter import markdown_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(converter_bp, url_prefix='/convert')
    app.register_blueprint(api_bp)
    app.register_blueprint(markdown_bp, url_prefix='/markdown')
    
    return app