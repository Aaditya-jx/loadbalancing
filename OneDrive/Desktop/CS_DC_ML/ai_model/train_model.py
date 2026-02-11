"""
AI Intrusion Detection Model Training
Trains Random Forest classifier on NSL-KDD style dataset
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import pickle
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from generate_nsl_kdd_data import NSLKDDDataGenerator

class IntrusionDetectionModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        self.target_encoder = LabelEncoder()
        self.category_encoder = LabelEncoder()
        
    def load_data(self, filepath='data/nsl_kdd_dataset.csv'):
        """Load dataset from CSV file"""
        if not os.path.exists(filepath):
            print(f"Dataset not found at {filepath}. Generating new dataset...")
            generator = NSLKDDDataGenerator(num_samples=10000)
            df = generator.generate_dataset(normal_ratio=0.7)
            generator.save_dataset(df, filepath)
        
        df = pd.read_csv(filepath)
        print(f"Dataset loaded: {df.shape}")
        return df
    
    def preprocess_data(self, df):
        """Preprocess the dataset"""
        # Separate features and target
        X = df.drop(['label', 'category'], axis=1)
        y = df['label']
        y_category = df['category']
        
        # Store feature columns
        self.feature_columns = X.columns.tolist()
        
        # Encode categorical features
        categorical_columns = ['protocol_type', 'service', 'flag']
        
        for col in categorical_columns:
            if col in X.columns:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                self.label_encoders[col] = le
        
        # Encode target variables
        y_encoded = self.target_encoder.fit_transform(y)
        y_category_encoded = self.category_encoder.fit_transform(y_category)
        
        # Scale numerical features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y_encoded, y_category_encoded
    
    def train_model(self, X_train, y_train):
        """Train Random Forest classifier"""
        print("Training Random Forest model...")
        
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        print("Model training completed!")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop 10 Important Features:")
        print(feature_importance.head(10))
        
        return feature_importance
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate model performance"""
        print("\nEvaluating model...")
        
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"\nModel Performance Metrics:")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")
        
        # Classification report
        print("\nClassification Report:")
        label_names = self.target_encoder.classes_
        print(classification_report(y_test, y_pred, target_names=label_names))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        # Plot confusion matrix
        plt.figure(figsize=(12, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=label_names, yticklabels=label_names)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.tight_layout()
        plt.savefig('models/confusion_matrix.png')
        plt.close()
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': cm,
            'classification_report': classification_report(y_test, y_pred, target_names=label_names)
        }
    
    def save_model(self, model_dir='models'):
        """Save trained model and preprocessing objects"""
        os.makedirs(model_dir, exist_ok=True)
        
        # Save model
        joblib.dump(self.model, f'{model_dir}/intrusion_detection_model.pkl')
        
        # Save scaler
        joblib.dump(self.scaler, f'{model_dir}/scaler.pkl')
        
        # Save label encoders
        joblib.dump(self.label_encoders, f'{model_dir}/label_encoders.pkl')
        
        # Save target encoders
        joblib.dump(self.target_encoder, f'{model_dir}/target_encoder.pkl')
        joblib.dump(self.category_encoder, f'{model_dir}/category_encoder.pkl')
        
        # Save feature columns
        joblib.dump(self.feature_columns, f'{model_dir}/feature_columns.pkl')
        
        print(f"Model and artifacts saved to {model_dir}/")
    
    def load_model(self, model_dir='models'):
        """Load trained model and preprocessing objects"""
        self.model = joblib.load(f'{model_dir}/intrusion_detection_model.pkl')
        self.scaler = joblib.load(f'{model_dir}/scaler.pkl')
        self.label_encoders = joblib.load(f'{model_dir}/label_encoders.pkl')
        self.target_encoder = joblib.load(f'{model_dir}/target_encoder.pkl')
        self.category_encoder = joblib.load(f'{model_dir}/category_encoder.pkl')
        self.feature_columns = joblib.load(f'{model_dir}/feature_columns.pkl')
        
        print(f"Model and artifacts loaded from {model_dir}/")
    
    def predict(self, features):
        """Make predictions on new data"""
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        # Convert to DataFrame if needed
        if isinstance(features, dict):
            features = pd.DataFrame([features])
        elif isinstance(features, list):
            features = pd.DataFrame([features], columns=self.feature_columns)
        
        # Encode categorical features
        categorical_columns = ['protocol_type', 'service', 'flag']
        for col in categorical_columns:
            if col in features.columns:
                if col in self.label_encoders:
                    # Handle unseen labels
                    unique_values = features[col].unique()
                    for val in unique_values:
                        if val not in self.label_encoders[col].classes_:
                            # Assign unknown label
                            features[col] = features[col].replace(val, self.label_encoders[col].classes_[0])
                    
                    features[col] = self.label_encoders[col].transform(features[col].astype(str))
        
        # Ensure all features are present
        for col in self.feature_columns:
            if col not in features.columns:
                features[col] = 0
        
        # Reorder columns
        features = features[self.feature_columns]
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        prediction = self.model.predict(features_scaled)
        prediction_proba = self.model.predict_proba(features_scaled)
        
        # Decode prediction
        predicted_label = self.target_encoder.inverse_transform(prediction)
        
        # Get category
        predicted_category = self.category_encoder.inverse_transform(prediction)
        
        return {
            'prediction': predicted_label[0],
            'category': predicted_category[0],
            'confidence': float(np.max(prediction_proba[0])),
            'probabilities': prediction_proba[0].tolist()
        }
    
    def train_and_evaluate(self, dataset_path='data/nsl_kdd_dataset.csv'):
        """Complete training and evaluation pipeline"""
        print("Starting AI Intrusion Detection Model Training...")
        
        # Load data
        df = self.load_data(dataset_path)
        
        # Preprocess data
        X, y, y_category = self.preprocess_data(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Training set size: {X_train.shape[0]}")
        print(f"Test set size: {X_test.shape[0]}")
        
        # Train model
        feature_importance = self.train_model(X_train, y_train)
        
        # Evaluate model
        metrics = self.evaluate_model(X_test, y_test)
        
        # Save model
        self.save_model()
        
        # Save feature importance plot
        plt.figure(figsize=(12, 6))
        top_features = feature_importance.head(15)
        sns.barplot(data=top_features, x='importance', y='feature')
        plt.title('Top 15 Feature Importance')
        plt.xlabel('Importance')
        plt.tight_layout()
        plt.savefig('models/feature_importance.png')
        plt.close()
        
        print("\nTraining completed successfully!")
        print(f"Model saved with accuracy: {metrics['accuracy']:.4f}")
        
        return metrics, feature_importance

if __name__ == "__main__":
    # Initialize and train model
    model = IntrusionDetectionModel()
    metrics, feature_importance = model.train_and_evaluate()
    
    print("\nTraining Summary:")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1-Score: {metrics['f1_score']:.4f}")
