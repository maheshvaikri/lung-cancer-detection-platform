import requests
from typing import Dict, Any, List
from core.compliance import ComplianceEngine
from privacy.anonymizer import Anonymizer

class FHIRServerAdapter:
    def __init__(
        self, 
        fhir_server_url: str, 
        compliance_engine: ComplianceEngine,
        anonymizer: Anonymizer
    ):
        self.fhir_server_url = fhir_server_url
        self.compliance_engine = compliance_engine
        self.anonymizer = anonymizer
    
    def fetch_patient_records(
        self, 
        patient_criteria: Dict[str, Any], 
        consent_token: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve and sanitize patient records from FHIR server
        
        :param patient_criteria: Search parameters for record retrieval
        :param consent_token: Patient consent authorization
        :return: List of privacy-preserved patient records
        """
        # Validate consent before data retrieval
        if not self.compliance_engine.validate_consent(consent_token):
            raise PermissionError("Insufficient patient consent")
        
        # Construct FHIR search request
        response = requests.get(
            f"{self.fhir_server_url}/Patient", 
            params=patient_criteria,
            headers={
                'Authorization': f'Bearer {consent_token}',
                'Accept': 'application/fhir+json'
            }
        )
        
        # Process and anonymize retrieved records
        raw_records = response.json().get('entry', [])
        sanitized_records = [
            self.anonymizer.remove_pii(record['resource']) 
            for record in raw_records
        ]
        
        return sanitized_records