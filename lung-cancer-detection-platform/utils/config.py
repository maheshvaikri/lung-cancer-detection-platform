import yaml
import os
from typing import Dict, Any

def load_configuration(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """
    Load application configuration from YAML file
    
    :param config_path: Path to configuration file
    :return: Parsed configuration dictionary
    """
    # Default configuration
    default_config = {
        'environment': 'development',
        'log_level': 'INFO',
        'jwt_secret_key': os.urandom(24),
        'allowed_origins': ['http://localhost:3000'],
        'database': {
            'host': 'localhost',
            'port': 5432,
            'name': 'healthcare_platform'
        },
        'privacy_settings': {
            'default_budget': 0.1,
            'max_budget': 1.0
        }
    }
    
    # Try to load custom configuration
    try:
        with open(config_path, 'r') as config_file:
            custom_config = yaml.safe_load(config_file)
            
            # Merge default and custom configurations
            default_config.update(custom_config)
    
    except FileNotFoundError:
        print(f"Warning: Configuration file {config_path} not found. Using default configuration.")
    except yaml.YAMLError as e:
        print(f"Error parsing configuration: {e}")
    
    return default_config