import re
from typing import Dict, Any

class Anonymizer:
    SENSITIVE_FIELDS = [
        'patient_name', 
        'patient_id', 
        'social_security_number', 
        'contact_info'
    ]
    
    def remove_pii(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove personally identifiable information from medical record
        
        :param record: Original medical record
        :return: Record with PII removed
        """
        anonymized_record = record.copy()
        
        for field in self.SENSITIVE_FIELDS:
            if field in anonymized_record:
                anonymized_record[field] = self._anonymize_value(anonymized_record[field])
        
        return anonymized_record
    
    def _anonymize_value(self, value: str) -> str:
        """
        Anonymize a single value
        
        :param value: Original value
        :return: Anonymized value
        """
        if isinstance(value, str):
            # Replace with hash or masked value
            return re.sub(r'\w', '*', value)
        return value