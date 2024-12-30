from typing import Dict, Any
from datetime import datetime, timedelta

class ComplianceEngine:
    def __init__(self):
        self.consent_records = {}
    
    def validate_data_access(self, 
                              patient_id: str, 
                              purpose: str, 
                              user_role: str) -> bool:
        """
        Validate data access based on consent and role
        
        :param patient_id: Patient identifier
        :param purpose: Purpose of data access
        :param user_role: Role of the user requesting access
        :return: Whether access is permitted
        """
        # Check if consent exists and is valid
        if patient_id not in self.consent_records:
            return False
        
        consent = self.consent_records[patient_id]
        
        # Check consent expiration and purpose
        if (consent['expiration'] < datetime.now() or 
            purpose not in consent['permitted_purposes']):
            return False
        
        # Role-based access control
        permitted_roles = {
            'researcher': ['aggregate_analysis', 'model_training'],
            'clinician': ['individual_prediction', 'treatment_planning']
        }
        
        return purpose in permitted_roles.get(user_role, [])
    
    def record_consent(self, 
                       patient_id: str, 
                       purposes: List[str], 
                       duration_days: int = 365):
        """
        Record patient consent
        
        :param patient_id: Patient identifier
        :param purposes: Permitted data usage purposes
        :param duration_days: Consent validity period
        """
        self.consent_records[patient_id] = {
            'permitted_purposes': purposes,
            'expiration': datetime.now() + timedelta(days=duration_days)
        }