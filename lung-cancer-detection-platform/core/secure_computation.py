import numpy as np
from typing import List, Any
from privacy.differential_privacy import DifferentialPrivacyMechanism

class SecureMultiPartyComputation:
    def __init__(self, privacy_mechanism: DifferentialPrivacyMechanism):
        self.privacy_mechanism = privacy_mechanism
    
    def aggregate_local_models(self, local_models: List[Any], privacy_budget: float) -> Any:
        """
        Securely aggregate local model updates with differential privacy
        
        :param local_models: List of local model updates
        :param privacy_budget: Privacy budget for noise addition
        :return: Aggregated global model update
        """
        # Basic secure aggregation
        aggregated_update = np.mean(local_models, axis=0)
        
        # Add differential privacy noise
        private_update = self.privacy_mechanism.add_noise(
            aggregated_update, 
            privacy_budget
        )
        
        return private_update
