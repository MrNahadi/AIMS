"""
Predictor service for marine engine fault diagnosis.
Handles inference logic, SHAP computation, and response formatting.
"""

from typing import Any

import numpy as np
import pandas as pd

from backend.models.request import SensorInput
from backend.models.response import PredictionResponse


# Fault label mapping (0-7 to human-readable strings)
FAULT_LABELS = {
    0: "Normal",
    1: "Fuel Injection Fault",
    2: "Cooling System Fault",
    3: "Turbocharger Fault",
    4: "Bearing Wear",
    5: "Lubrication Oil Degradation",
    6: "Air Intake Restriction",
    7: "Vibration Anomaly"
}

# Feature names in the correct order (matching training data)
FEATURE_NAMES = [
    "Shaft_RPM",
    "Engine_Load",
    "Fuel_Flow",
    "Air_Pressure",
    "Ambient_Temp",
    "Oil_Temp",
    "Oil_Pressure",
    "Vibration_X",
    "Vibration_Y",
    "Vibration_Z",
    "Cylinder1_Pressure",
    "Cylinder1_Exhaust_Temp",
    "Cylinder2_Pressure",
    "Cylinder2_Exhaust_Temp",
    "Cylinder3_Pressure",
    "Cylinder3_Exhaust_Temp",
    "Cylinder4_Pressure",
    "Cylinder4_Exhaust_Temp"
]


def predict_fault(
    sensor_input: SensorInput,
    model: Any,
    preprocessor: Any,
    shap_explainer: Any
) -> PredictionResponse:
    """
    Perform fault prediction with SHAP explanations.
    
    Args:
        sensor_input: Validated sensor readings from the request
        model: Trained LightGBM classifier
        preprocessor: Fitted StandardScaler for feature transformation
        shap_explainer: Fitted SHAP TreeExplainer for computing explanations
    
    Returns:
        PredictionResponse containing prediction label, probabilities, and SHAP values
    """
    # Convert SensorInput to pandas DataFrame with feature names
    input_df = pd.DataFrame([[
        sensor_input.Shaft_RPM,
        sensor_input.Engine_Load,
        sensor_input.Fuel_Flow,
        sensor_input.Air_Pressure,
        sensor_input.Ambient_Temp,
        sensor_input.Oil_Temp,
        sensor_input.Oil_Pressure,
        sensor_input.Vibration_X,
        sensor_input.Vibration_Y,
        sensor_input.Vibration_Z,
        sensor_input.Cylinder1_Pressure,
        sensor_input.Cylinder1_Exhaust_Temp,
        sensor_input.Cylinder2_Pressure,
        sensor_input.Cylinder2_Exhaust_Temp,
        sensor_input.Cylinder3_Pressure,
        sensor_input.Cylinder3_Exhaust_Temp,
        sensor_input.Cylinder4_Pressure,
        sensor_input.Cylinder4_Exhaust_Temp
    ]], columns=FEATURE_NAMES)
    
    # Transform input using preprocessor (StandardScaler)
    input_scaled_array = preprocessor.transform(input_df)
    
    # Convert back to DataFrame to preserve feature names for model and SHAP
    input_scaled = pd.DataFrame(input_scaled_array, columns=FEATURE_NAMES)
    
    # Generate prediction and probabilities
    prediction = model.predict(input_scaled)[0]  # Single prediction (0-7)
    probabilities = model.predict_proba(input_scaled)[0]  # Array of 8 probabilities
    
    # Compute SHAP values for the input
    shap_values = shap_explainer.shap_values(input_scaled)
    
    # For multi-class classification, SHAP returns values for each class
    # We use the SHAP values for the predicted class
    if isinstance(shap_values, list):
        # shap_values is a list of arrays (one per class)
        # Shape: [num_classes][num_samples, num_features]
        shap_values_for_prediction = shap_values[int(prediction)][0, :]
    else:
        # shap_values is a 3D array: [num_samples, num_features, num_classes]
        # Extract SHAP values for the predicted class
        shap_values_for_prediction = shap_values[0, :, int(prediction)]
    
    # Map numeric prediction to label string
    prediction_label = FAULT_LABELS[int(prediction)]
    
    # Format probabilities as dict with label strings as keys
    probabilities_dict = {
        FAULT_LABELS[i]: float(prob) 
        for i, prob in enumerate(probabilities)
    }
    
    # Format SHAP values as dict with feature names as keys
    shap_values_dict = {
        feature_name: float(shap_value)
        for feature_name, shap_value in zip(FEATURE_NAMES, shap_values_for_prediction)
    }
    
    # Return PredictionResponse object
    return PredictionResponse(
        prediction_label=prediction_label,
        probabilities=probabilities_dict,
        shap_values=shap_values_dict
    )
