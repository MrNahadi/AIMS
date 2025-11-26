"""
Unit tests for Pydantic models (request and response schemas).
Tests validation logic for SensorInput and serialization for PredictionResponse.
"""

import pytest
from pydantic import ValidationError
from backend.models.request import SensorInput
from backend.models.response import PredictionResponse


class TestSensorInput:
    """Test suite for SensorInput validation."""
    
    def test_valid_sensor_input(self):
        """Test SensorInput validation with valid data (should pass)."""
        valid_data = {
            "Shaft_RPM": 950.0,
            "Engine_Load": 70.0,
            "Fuel_Flow": 120.0,
            "Air_Pressure": 2.5,
            "Ambient_Temp": 25.0,
            "Oil_Temp": 75.0,
            "Oil_Pressure": 3.5,
            "Vibration_X": 0.05,
            "Vibration_Y": 0.05,
            "Vibration_Z": 0.05,
            "Cylinder1_Pressure": 145.0,
            "Cylinder1_Exhaust_Temp": 420.0,
            "Cylinder2_Pressure": 145.0,
            "Cylinder2_Exhaust_Temp": 420.0,
            "Cylinder3_Pressure": 145.0,
            "Cylinder3_Exhaust_Temp": 420.0,
            "Cylinder4_Pressure": 145.0,
            "Cylinder4_Exhaust_Temp": 420.0
        }
        
        # Should not raise any exception
        sensor_input = SensorInput(**valid_data)
        
        # Verify all fields are set correctly
        assert sensor_input.Shaft_RPM == 950.0
        assert sensor_input.Engine_Load == 70.0
        assert sensor_input.Oil_Temp == 75.0
        assert sensor_input.Vibration_X == 0.05
    
    def test_missing_fields(self):
        """Test SensorInput validation with missing fields (should raise ValidationError)."""
        incomplete_data = {
            "Shaft_RPM": 950.0,
            "Engine_Load": 70.0,
            # Missing all other required fields
        }
        
        with pytest.raises(ValidationError) as exc_info:
            SensorInput(**incomplete_data)
        
        # Verify that ValidationError was raised
        errors = exc_info.value.errors()
        assert len(errors) > 0
        # Check that missing fields are reported
        missing_fields = [error['loc'][0] for error in errors]
        assert 'Fuel_Flow' in missing_fields
        assert 'Oil_Temp' in missing_fields
    
    def test_invalid_types(self):
        """Test SensorInput validation with invalid types (should raise ValidationError)."""
        invalid_data = {
            "Shaft_RPM": "not_a_number",  # Should be float
            "Engine_Load": 70.0,
            "Fuel_Flow": 120.0,
            "Air_Pressure": 2.5,
            "Ambient_Temp": 25.0,
            "Oil_Temp": 75.0,
            "Oil_Pressure": 3.5,
            "Vibration_X": 0.05,
            "Vibration_Y": 0.05,
            "Vibration_Z": 0.05,
            "Cylinder1_Pressure": 145.0,
            "Cylinder1_Exhaust_Temp": 420.0,
            "Cylinder2_Pressure": 145.0,
            "Cylinder2_Exhaust_Temp": 420.0,
            "Cylinder3_Pressure": 145.0,
            "Cylinder3_Exhaust_Temp": 420.0,
            "Cylinder4_Pressure": 145.0,
            "Cylinder4_Exhaust_Temp": 420.0
        }
        
        with pytest.raises(ValidationError) as exc_info:
            SensorInput(**invalid_data)
        
        # Verify that ValidationError was raised for type mismatch
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any('Shaft_RPM' in str(error['loc']) for error in errors)


class TestPredictionResponse:
    """Test suite for PredictionResponse serialization."""
    
    def test_prediction_response_serialization(self):
        """Test PredictionResponse serialization with valid data."""
        response_data = {
            "prediction_label": "Normal",
            "probabilities": {
                "Normal": 0.95,
                "Fuel Injection Fault": 0.02,
                "Cooling System Fault": 0.01,
                "Turbocharger Fault": 0.01,
                "Bearing Wear": 0.005,
                "Lubrication Oil Degradation": 0.005,
                "Air Intake Restriction": 0.005,
                "Vibration Anomaly": 0.005
            },
            "shap_values": {
                "Shaft_RPM": 0.05,
                "Engine_Load": -0.02,
                "Fuel_Flow": 0.01,
                "Air_Pressure": -0.01,
                "Ambient_Temp": 0.0,
                "Oil_Temp": -0.03,
                "Oil_Pressure": 0.02,
                "Vibration_X": -0.01,
                "Vibration_Y": -0.01,
                "Vibration_Z": -0.01,
                "Cylinder1_Pressure": 0.0,
                "Cylinder1_Exhaust_Temp": 0.01,
                "Cylinder2_Pressure": 0.0,
                "Cylinder2_Exhaust_Temp": 0.01,
                "Cylinder3_Pressure": 0.0,
                "Cylinder3_Exhaust_Temp": 0.01,
                "Cylinder4_Pressure": 0.0,
                "Cylinder4_Exhaust_Temp": 0.01
            }
        }
        
        # Should not raise any exception
        response = PredictionResponse(**response_data)
        
        # Verify fields are set correctly
        assert response.prediction_label == "Normal"
        assert response.probabilities["Normal"] == 0.95
        assert len(response.shap_values) == 18
        assert response.shap_values["Oil_Temp"] == -0.03
        
        # Test serialization to dict
        response_dict = response.model_dump()
        assert response_dict["prediction_label"] == "Normal"
        assert "probabilities" in response_dict
        assert "shap_values" in response_dict
