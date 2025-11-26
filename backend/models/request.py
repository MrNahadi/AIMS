"""Request models for AIMS API."""
from pydantic import BaseModel, Field


class SensorInput(BaseModel):
    """
    Sensor input model for marine engine fault prediction.
    Contains 18 sensor readings from the marine engine.
    Field names match the ML model's expected feature order.
    """
    Shaft_RPM: float = Field(..., description="Shaft rotational speed in revolutions per minute")
    Engine_Load: float = Field(..., description="Engine load percentage (0-100)")
    Fuel_Flow: float = Field(..., description="Fuel flow rate in liters per hour")
    Air_Pressure: float = Field(..., description="Air intake pressure in bar")
    Ambient_Temp: float = Field(..., description="Ambient temperature in degrees Celsius")
    Oil_Temp: float = Field(..., description="Lubrication oil temperature in degrees Celsius")
    Oil_Pressure: float = Field(..., description="Lubrication oil pressure in bar")
    Vibration_X: float = Field(..., description="Vibration measurement on X-axis in mm/s")
    Vibration_Y: float = Field(..., description="Vibration measurement on Y-axis in mm/s")
    Vibration_Z: float = Field(..., description="Vibration measurement on Z-axis in mm/s")
    Cylinder1_Pressure: float = Field(..., description="Cylinder 1 combustion pressure in bar")
    Cylinder1_Exhaust_Temp: float = Field(..., description="Cylinder 1 exhaust gas temperature in degrees Celsius")
    Cylinder2_Pressure: float = Field(..., description="Cylinder 2 combustion pressure in bar")
    Cylinder2_Exhaust_Temp: float = Field(..., description="Cylinder 2 exhaust gas temperature in degrees Celsius")
    Cylinder3_Pressure: float = Field(..., description="Cylinder 3 combustion pressure in bar")
    Cylinder3_Exhaust_Temp: float = Field(..., description="Cylinder 3 exhaust gas temperature in degrees Celsius")
    Cylinder4_Pressure: float = Field(..., description="Cylinder 4 combustion pressure in bar")
    Cylinder4_Exhaust_Temp: float = Field(..., description="Cylinder 4 exhaust gas temperature in degrees Celsius")
    
    class Config:
        json_schema_extra = {
            "example": {
                "Shaft_RPM": 1800.0,
                "Engine_Load": 65.0,
                "Fuel_Flow": 15.2,
                "Air_Pressure": 1.5,
                "Ambient_Temp": 25.0,
                "Oil_Temp": 90.0,
                "Oil_Pressure": 4.5,
                "Vibration_X": 2.1,
                "Vibration_Y": 1.8,
                "Vibration_Z": 2.3,
                "Cylinder1_Pressure": 120.0,
                "Cylinder1_Exhaust_Temp": 350.0,
                "Cylinder2_Pressure": 118.0,
                "Cylinder2_Exhaust_Temp": 348.0,
                "Cylinder3_Pressure": 122.0,
                "Cylinder3_Exhaust_Temp": 352.0,
                "Cylinder4_Pressure": 119.0,
                "Cylinder4_Exhaust_Temp": 349.0
            }
        }
