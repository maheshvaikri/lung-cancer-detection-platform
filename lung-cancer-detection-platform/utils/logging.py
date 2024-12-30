import logging
import json
from datetime import datetime
from typing import Dict, Any

class SystemLogger:
    """
    Comprehensive logging system for healthcare platform
    """
    def __init__(
        self, 
        log_level: str = 'INFO',
        log_file: str = 'healthcare_platform.log'
    ):
        # Configure main logger
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=log_file,
            filemode='a'
        )
        
        self.logger = logging.getLogger('HealthcarePlatform')
        
        # Additional log file for security and system events
        self.security_logger = logging.getLogger('SecurityEvents')
        security_handler = logging.FileHandler('security_events.log')
        security_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.security_logger.addHandler(security_handler)
    
    def log_system_event(
        self, 
        event_type: str, 
        details: Dict[str, Any]
    ):
        """
        Log general system events
        
        :param event_type: Type of system event
        :param details: Additional event details
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': event_type,
            'details': details
        }
        
        self.logger.info(json.dumps(log_entry))
    
    def log_security_event(
        self, 
        event_type: str, 
        details: Dict[str, Any]
    ):
        """
        Log security-related events
        
        :param event_type: Type of security event
        :param details: Security event details
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': event_type,
            'details': details
        }
        
        self.security_logger.warning(json.dumps(log_entry))
    
    def log_error_event(
        self, 
        event_type: str, 
        details: Dict[str, Any]
    ):
        """
        Log error events
        
        :param event_type: Type of error
        :param details: Error details
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': event_type,
            'details': details
        }
        
        self.logger.error(json.dumps(log_entry))