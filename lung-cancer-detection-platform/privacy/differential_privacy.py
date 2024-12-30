import numpy as np
from typing import Union

class AdaptiveDifferentialPrivacy:
    def __init__(
        self, 
        sensitivity_threshold: float = 0.5,
        max_privacy_budget: float = 1.0
    ):
        self.sensitivity_threshold = sensitivity_threshold
        self.max_privacy_budget = max_privacy_budget
        
        # Different noise mechanisms
        self.noise_mechanisms = {
            'laplace': self._laplace_noise,
            'gaussian': self._gaussian_noise
        }
    
    def _laplace_noise(
        self, 
        data: np.ndarray, 
        epsilon: float
    ) -> np.ndarray:
        """
        Apply Laplace noise for differential privacy
        
        :param data: Input data array
        :param epsilon: Privacy budget
        :return: Noise-infused data
        """
        scale = 1 / epsilon
        noise = np.random.laplace(loc=0, scale=scale, size=data.shape)
        return data + noise
    
    def _gaussian_noise(
        self, 
        data: np.ndarray, 
        epsilon: float
    ) -> np.ndarray:
        """
        Apply Gaussian noise for differential privacy
        
        :param data: Input data array
        :param epsilon: Privacy budget
        :return: Noise-infused data
        """
        sigma = np.sqrt(2 * np.log(1.25 / epsilon))
        noise = np.random.normal(loc=0, scale=sigma, size=data.shape)
        return data + noise
    
    def calibrate_noise(
        self, 
        data: Union[np.ndarray, List[float]], 
        current_budget: float
    ) -> np.ndarray:
        """
        Dynamically select and apply noise based on data sensitivity
        
        :param data: Input data vector
        :param current_budget: Available privacy budget
        :return: Noise-infused data
        """
        data_array = np.array(data)
        sensitivity = np.std(data_array)
        
        # Choose noise mechanism based on sensitivity
        noise_type = ('gaussian' if sensitivity > self.sensitivity_threshold 
                      else 'laplace')
        
        # Apply selected noise mechanism
        noisy_data = self.noise_mechanisms[noise_type](
            data_array, 
            epsilon=min(current_budget, self.max_privacy_budget)
        )
        
        return noisy_data