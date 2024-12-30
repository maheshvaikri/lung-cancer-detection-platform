from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from web.routes import create_routes
from core.compliance import ComplianceEngine
from utils.config import load_configuration
from utils.logging import SystemLogger

def create_app(config_path: str = 'config.yaml'):
    """
    Create and configure Flask application
    
    :param config_path: Path to configuration file
    :return: Configured Flask application
    """
    # Load configuration
    config = load_configuration(config_path)
    
    # Initialize Flask app
    app = Flask(__name__)
    
    # CORS configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": config.get('allowed_origins', ['*']),
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type"]
        }
    })
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = config['jwt_secret_key']
    jwt = JWTManager(app)
    
    # Initialize core components
    logger = SystemLogger(log_level=config.get('log_level', 'INFO'))
    compliance_engine = ComplianceEngine()
    
    # Create routes with dependency injection
    create_routes(
        app, 
        compliance_engine=compliance_engine,
        logger=logger,
        config=config
    )
    
    return app