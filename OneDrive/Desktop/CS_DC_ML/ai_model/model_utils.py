"""
Model utilities for loading and using the trained intrusion detection model
"""

import joblib
import pandas as pd
import numpy as np
import os

class ModelLoader:
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        self.model = None
        self.scaler = None
        self.label_encoders = {}
        self.target_encoder = None
        self.category_encoder = None
        self.feature_columns = []
        
    def load_model(self):
        """Load all model artifacts"""
        try:
            self.model = joblib.load(f'{self.model_dir}/intrusion_detection_model.pkl')
            self.scaler = joblib.load(f'{self.model_dir}/scaler.pkl')
            self.label_encoders = joblib.load(f'{self.model_dir}/label_encoders.pkl')
            self.target_encoder = joblib.load(f'{self.model_dir}/target_encoder.pkl')
            self.category_encoder = joblib.load(f'{self.model_dir}/category_encoder.pkl')
            self.feature_columns = joblib.load(f'{self.model_dir}/feature_columns.pkl')
            
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def predict_traffic(self, traffic_features):
        """Predict if traffic is malicious or normal"""
        if self.model is None:
            if not self.load_model():
                return None
        
        try:
            # Convert to DataFrame if needed
            if isinstance(traffic_features, dict):
                features_df = pd.DataFrame([traffic_features])
            else:
                features_df = pd.DataFrame([traffic_features], columns=self.feature_columns)
            
            # Encode categorical features
            categorical_columns = ['protocol_type', 'service', 'flag']
            for col in categorical_columns:
                if col in features_df.columns:
                    if col in self.label_encoders:
                        # Handle unseen labels
                        unique_values = features_df[col].unique()
                        for val in unique_values:
                            if val not in self.label_encoders[col].classes_:
                                # Assign the most common label for unknown values
                                features_df[col] = features_df[col].replace(val, self.label_encoders[col].classes_[0])
                        
                        features_df[col] = self.label_encoders[col].transform(features_df[col].astype(str))
            
            # Ensure all features are present
            for col in self.feature_columns:
                if col not in features_df.columns:
                    features_df[col] = 0
            
            # Reorder columns to match training data
            features_df = features_df[self.feature_columns]
            
            # Scale features
            features_scaled = self.scaler.transform(features_df)
            
            # Make prediction
            prediction = self.model.predict(features_scaled)
            prediction_proba = self.model.predict_proba(features_scaled)
            
            # Decode prediction
            predicted_label = self.target_encoder.inverse_transform(prediction)[0]
            predicted_category = self.category_encoder.inverse_transform(prediction)[0]
            confidence = float(np.max(prediction_proba[0]))
            
            return {
                'is_malicious': predicted_label != 'normal',
                'prediction': predicted_label,
                'category': predicted_category,
                'confidence': confidence,
                'probabilities': prediction_proba[0].tolist()
            }
            
        except Exception as e:
            print(f"Error making prediction: {e}")
            return None
    
    def get_model_info(self):
        """Get model information"""
        if self.model is None:
            return None
        
        return {
            'model_type': 'RandomForestClassifier',
            'n_features': len(self.feature_columns),
            'feature_columns': self.feature_columns,
            'target_classes': self.target_encoder.classes_.tolist() if self.target_encoder else [],
            'category_classes': self.category_encoder.classes_.tolist() if self.category_encoder else []
        }

# Global model loader instance
model_loader = ModelLoader()

def predict_traffic_features(traffic_features):
    """Convenience function to predict traffic features"""
    return model_loader.predict_traffic(traffic_features)

def get_model_info():
    """Convenience function to get model info"""
    return model_loader.get_model_info()

def initialize_model():
    """Initialize the model (call this at application startup)"""
    return model_loader.load_model()
