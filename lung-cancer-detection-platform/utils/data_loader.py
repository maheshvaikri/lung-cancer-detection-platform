# utils/data_loader.py
import pandas as pd
import numpy as np
from typing import Tuple, Dict
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class MedicalDataLoader:
    @staticmethod
    def load_training_data(
        file_path: str, 
        config: Dict[str, Any]
    ) -> Dict[str, np.ndarray]:
        """
        Load and preprocess medical training data
        
        :param file_path: Path to training data file
        :param config: Model configuration
        :return: Processed training data dictionary
        """
        # Support multiple file formats
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
        
        # Validate required features
        required_features = config['ml_model']['lung_cancer_predictor']['input_features']
        missing_features = set(required_features) - set(df.columns)
        
        if missing_features:
            raise ValueError(f"Missing features: {missing_features}")
        
        # Select and preprocess features
        X = df[required_features]
        y = df['cancer_risk']  # Assuming binary label
        
        # Handle missing values
        X = X.fillna(X.median())
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=0.2, 
            random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        return {
            'X_train': X_train_scaled,
            'X_test': X_test_scaled,
            'y_train': y_train.values,
            'y_test': y_test.values,
            'scaler': scaler
        }