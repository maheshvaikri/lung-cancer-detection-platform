import requests
from typing import Dict, Any, List
from core.compliance import ComplianceEngine
from privacy.anonymizer import Anonymizer
from utils.logging import SystemLogger

class HospitalDataConnector:
    """
    Comprehensive connector for integrating with multiple hospital information systems
    """
    def __init__(
        self, 
        compliance_engine: ComplianceEngine,
        anonymizer: Anonymizer,
        logger: SystemLogger,
        base_endpoints: Dict[str, str] = None
    ):
        self.compliance_engine = compliance_engine
        self.anonymizer = anonymizer
        self.logger = logger
        
        # Default hospital system endpoints (configurable)
        self.endpoints = base_endpoints or {
            'patient_records': '/fhir/Patient',
            'clinical_data': '/fhir/Observation',
            'diagnostic_reports': '/fhir/DiagnosticReport'
        }
    
    def fetch_patient_records(
        self, 
        hospital_id: str, 
        patient_criteria: Dict[str, Any],
        consent_token: str
    ) -> List[Dict[str, Any]]:
        """
        Fetch and anonymize patient records from a specific hospital system
        
        :param hospital_id: Unique hospital identifier
        :param patient_criteria: Search parameters
        :param consent_token: Patient consent authorization
        :return: List of anonymized patient records
        """
        try:
            # Validate consent and access permissions
            if not self.compliance_engine.validate_consent(consent_token):
                self.logger.log_security_event(
                    event_type='consent_violation',
                    details={'hospital_id': hospital_id}
                )
                raise PermissionError("Insufficient patient consent")
            
            # Construct hospital-specific API request
            response = requests.get(
                f"{hospital_id}{self.endpoints['patient_records']}",
                params=patient_criteria,
                headers={
                    'Authorization': f'Bearer {consent_token}',
                    'Accept': 'application/fhir+json'
                }
            )
            
            response.raise_for_status()
            
            # Process and anonymize records
            raw_records = response.json().get('entry', [])
            anonymized_records = [
                self.anonymizer.remove_pii(record['resource']) 
                for record in raw_records
            ]
            
            self.logger.log_system_event(
                event_type='data_retrieval',
                details={
                    'hospital_id': hospital_id,
                    'records_retrieved': len(anonymized_records)
                }
            )
            
            return anonymized_records
        
        except requests.RequestException as e:
            self.logger.log_error_event(
                event_type='hospital_data_retrieval_error',
                details={
                    'hospital_id': hospital_id,
                    'error': str(e)
                }
            )
            raise