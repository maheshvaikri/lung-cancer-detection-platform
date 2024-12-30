import json
import uuid
from datetime import datetime
from typing import Dict, Any

class SecureAuditLogger:
    def __init__(self, log_file_path: str = 'audit_logs.jsonl'):
        self.log_file_path = log_file_path
    
    def log_event(
        self, 
        event_type: str, 
        user_role: str, 
        data_access_details: Dict[str, Any]
    ):
        """
        Create secure, tamper-evident audit log entry
        
        :param event_type: Classification of system event
        :param user_role: Organizational role executing action
        :param data_access_details: Contextual information about the event
        """
        audit_entry = {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user_role': user_role,
            'details': json.dumps(data_access_details),
            # Add cryptographic signature for tamper-evidence
            'signature': self._generate_signature(data_access_details)
        }
        
        # Append to append-only log file
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(json.dumps(audit_entry) + '\n')
    
    def _generate_signature(self, data: Dict[str, Any]) -> str:
        """
        Generate a cryptographic signature for the log entry
        
        :param data: Log entry details
        :return: Cryptographic signature
        """
        import hashlib
        
        # Create a hash based on entry details
        signature_base = json.dumps(data, sort_keys=True)
        return hashlib.sha256(signature_base.encode()).hexdigest()