"""Response models for AIMS API."""
from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    """
    Prediction response model for marine engine fault prediction.
    Contains the predicted fault label, class probabilities, and SHAP feature importance values.
    """
    prediction_label: str = Field(
        ..., 
        description="Human-readable fault classification label"
    )
    probabilities: dict[str, float] = Field(
        ..., 
        description="Confidence scores for all 8 fault types"
    )
    shap_values: dict[str, float] = Field(
        ..., 
        description="Feature importance values for all 18 sensor features"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction_label": "Normal Operation",
                "probabilities": {
                    "Normal Operation": 0.85,
                    "Overheating": 0.05,
                    "Low Oil Pressure": 0.03,
                    "High Vibration": 0.02,
                    "Fuel System Issue": 0.02,
                    "Cooling System Fault": 0.01,
                    "Exhaust System Issue": 0.01,
                    "Electrical Fault": 0.01
                },
                "shap_values": {
                    "Shaft_RPM": 0.12,
                    "Engine_Load": 0.08,
                    "Fuel_Flow": 0.05,
                    "Air_Pressure": 0.03,
                    "Ambient_Temp": 0.02,
                    "Oil_Temp": 0.15,
                    "Oil_Pressure": 0.10,
                    "Vibration_X": 0.07,
                    "Vibration_Y": 0.06,
                    "Vibration_Z": 0.05,
                    "Cylinder1_Pressure": 0.04,
                    "Cylinder1_Exhaust_Temp": 0.03,
                    "Cylinder2_Pressure": 0.04,
                    "Cylinder2_Exhaust_Temp": 0.03,
                    "Cylinder3_Pressure": 0.04,
                    "Cylinder3_Exhaust_Temp": 0.03,
                    "Cylinder4_Pressure": 0.04,
                    "Cylinder4_Exhaust_Temp": 0.03
                }
            }
        }
