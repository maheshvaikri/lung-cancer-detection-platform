import os
import sys
import argparse
from typing import Optional

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Core platform components
from web.app import create_app
from models.lung_cancer_predictor import LungCancerRiskPredictor
from integrations.hospital_data_connector import HospitalDataConnector
from core.compliance import ComplianceEngine
from core.data_storage import SecureDataStore
from privacy.differential_privacy import AdaptiveDifferentialPrivacy
from privacy.anonymizer import Anonymizer
from utils.config import load_configuration
from utils.logging import SystemLogger

def initialize_platform(
    config_path: Optional[str] = None,
    log_level: Optional[str] = None
) -> dict:
    """
    Initialize the healthcare platform components
    
    :param config_path: Path to configuration file
    :param log_level: Logging level override
    :return: Dictionary of initialized platform components
    """
    # Load configuration
    config = load_configuration(config_path or 'config.yaml')
    
    # Override log level if provided
    if log_level:
        config['log_level'] = log_level
    
    # Initialize logging
    logger = SystemLogger(
        log_level=config.get('log_level', 'INFO')
    )
    
    try:
        # Initialize core privacy components
        anonymizer = Anonymizer()
        privacy_mechanism = AdaptiveDifferentialPrivacy(
            sensitivity_threshold=config['privacy_settings'].get('sensitivity_threshold', 0.5),
            max_privacy_budget=config['privacy_settings'].get('max_budget', 1.0)
        )
        
        # Initialize compliance and data management
        compliance_engine = ComplianceEngine()
        data_store = SecureDataStore(
            db_path=config['database'].get('path', 'secure_medical_store.db')
        )
        
        # Initialize hospital data connector
        hospital_connector = HospitalDataConnector(
            compliance_engine=compliance_engine,
            anonymizer=anonymizer,
            logger=logger
        )
        
        # Initialize ML model
        risk_predictor = LungCancerRiskPredictor(
            input_features=[
                'age', 'smoking_history', 'family_history', 
                'exposure_factors', 'previous_conditions'
            ],
            privacy_mechanism=privacy_mechanism,
            logger=logger
        )
        
        # Log successful initialization
        logger.log_system_event(
            event_type='platform_initialization',
            details={'status': 'success'}
        )
        
        return {
            'app': create_app(config_path),
            'logger': logger,
            'compliance_engine': compliance_engine,
            'data_store': data_store,
            'hospital_connector': hospital_connector,
            'risk_predictor': risk_predictor,
            'config': config
        }
    
    except Exception as e:
        # Log initialization error
        logger.log_error_event(
            event_type='platform_initialization_error',
            details={
                'error_message': str(e),
                'error_type': type(e).__name__
            }
        )
        raise

def run_web_server(
    host: str = '0.0.0.0', 
    port: int = 5000, 
    debug: bool = False
):
    """
    Run the web application server
    
    :param host: Server host
    :param port: Server port
    :param debug: Debug mode flag
    """
    # Initialize platform components
    platform = initialize_platform()
    
    # Extract Flask app
    app = platform['app']
    logger = platform['logger']
    
    try:
        # Log server startup
        logger.log_system_event(
            event_type='server_startup',
            details={
                'host': host,
                'port': port,
                'debug_mode': debug
            }
        )
        
        # Run the application
        app.run(
            host=host, 
            port=port, 
            debug=debug
        )
    
    except Exception as e:
        # Log server startup failure
        logger.log_error_event(
            event_type='server_startup_error',
            details={
                'error_message': str(e),
                'host': host,
                'port': port
            }
        )
        raise

def train_model(
    training_data_path: str, 
    privacy_budget: float = 0.5
):
    """
    Train lung cancer risk prediction model
    
    :param training_data_path: Path to training dataset
    :param privacy_budget: Differential privacy budget
    """
    # Initialize platform components
    platform = initialize_platform()
    
    risk_predictor = platform['risk_predictor']
    logger = platform['logger']
    
    try:
        # Load training data (implementation depends on data format)
        # This is a placeholder - actual implementation would depend on your data
        import numpy as np
        
        # Simulated training data loading
        X_train = np.random.rand(1000, 5)  # 1000 samples, 5 features
        y_train = np.random.randint(2, size=(1000, 1))  # Binary labels
        
        # Train model with privacy preservation
        risk_predictor.train(
            X_train, 
            y_train, 
            privacy_budget=privacy_budget
        )
        
        # Log successful model training
        logger.log_system_event(
            event_type='model_training_complete',
            details={
                'privacy_budget': privacy_budget,
                'training_samples': len(X_train)
            }
        )
    
    except Exception as e:
        # Log model training error
        logger.log_error_event(
            event_type='model_training_error',
            details={
                'error_message': str(e),
                'privacy_budget': privacy_budget
            }
        )
        raise

def main():
    """
    Main entry point for the healthcare platform
    """
    parser = argparse.ArgumentParser(
        description="Privacy-Preserving Healthcare Platform"
    )
    
    # Add command-line arguments
    parser.add_argument(
        'mode', 
        choices=['server', 'train', 'init'], 
        help='Platform operation mode'
    )
    parser.add_argument(
        '--host', 
        default='0.0.0.0', 
        help='Server host (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--port', 
        type=int, 
        default=5000, 
        help='Server port (default: 5000)'
    )
    parser.add_argument(
        '--config', 
        help='Path to configuration file'
    )
    parser.add_argument(
        '--log-level', 
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level'
    )
    parser.add_argument(
        '--data', 
        help='Path to training data (for train mode)'
    )
    parser.add_argument(
        '--privacy-budget', 
        type=float, 
        default=0.5, 
        help='Privacy budget for training (default: 0.5)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Execute based on selected mode
        if args.mode == 'server':
            run_web_server(
                host=args.host, 
                port=args.port, 
                debug=(args.log_level == 'DEBUG')
            )
        elif args.mode == 'train':
            train_model(
                training_data_path=args.data or 'training_data.csv',
                privacy_budget=args.privacy_budget
            )
        elif args.mode == 'init':
            # Just initialize and validate platform components
            initialize_platform(
                config_path=args.config,
                log_level=args.log_level
            )
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()