import numpy as np
import tensorflow as tf
from typing import List, Dict, Union
from privacy.differential_privacy import AdaptiveDifferentialPrivacy
from utils.logging import SystemLogger

class LungCancerRiskPredictor:
    """
    Advanced machine learning model for lung cancer risk prediction
    with privacy-preserving capabilities
    """
    def __init__(
        self, 
        input_features: List[str],
        privacy_mechanism: AdaptiveDifferentialPrivacy,
        logger: SystemLogger
    ):
        self.input_features = input_features
        self.privacy_mechanism = privacy_mechanism
        self.logger = logger
        
        # Model architecture
        self.model = self._build_model()
    
    def _build_model(self) -> tf.keras.Model:
        """
        Construct neural network for lung cancer risk prediction
        
        :return: Compiled Keras model
        """
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(len(self.input_features),)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray, 
        privacy_budget: float = 0.5
    ):
        """
        Train model with privacy-preserving techniques
        
        :param X_train: Training features
        :param y_train: Training labels
        :param privacy_budget: Differential privacy budget
        """
        # Apply differential privacy during training
        noisy_X = self.privacy_mechanism.calibrate_noise(X_train, privacy_budget)
        noisy_y = self.privacy_mechanism.calibrate_noise(y_train, privacy_budget)
        
        # Train with privacy-preserved data
        history = self.model.fit(
            noisy_X, noisy_y,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
        
        self.logger.log_system_event(
            event_type='model_training',
            details={
                'privacy_budget': privacy_budget,
                'final_accuracy': history.history['accuracy'][-1]
            }
        )
    
    def predict_with_privacy(
        self, 
        patient_features: Union[List[float], np.ndarray], 
        privacy_budget: float = 0.1
    ) -> float:
        """
        Predict lung cancer risk with privacy preservation
        
        :param patient_features: Patient's medical features
        :param privacy_budget: Privacy budget for prediction
        :return: Privacy-preserved risk score
        """
        # Convert input to numpy array
        features_array = np.array(patient_features).reshape(1, -1)
        
        # Apply noise to prediction
        noisy_features = self.privacy_mechanism.calibrate_noise(
            features_array, 
            privacy_budget
        )
        
        # Generate prediction
        risk_score = self.model.predict(noisy_features)[0][0]
        
        self.logger.log_system_event(
            event_type='risk_prediction',
            details={'privacy_budget': privacy_budget}
        )
        
        return risk_score
