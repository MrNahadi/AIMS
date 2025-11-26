"""
Integration tests for FastAPI endpoints.
Tests the /predict endpoint using FastAPI TestClient.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

from backend.main import app


class TestServerStartup:
    """Test suite for server startup and import validation."""
    
    def test_server_starts_without_import_errors(self):
        """
        Integration test: Server starts without import errors.
        
        Property 1: Server starts without import errors
        Validates: Requirements 1.2, 2.2
        Feature: backend-import-fix, Property 1: Server starts without import errors
        """
        # Create TestClient - this will trigger the lifespan startup
        # If there are any import errors, this will raise an exception
        try:
            client = TestClient(app)
            
            # Verify the app was created successfully
            assert client is not None
            assert app is not None
            
            # Verify endpoints are accessible by checking the health endpoint
            response = client.get("/")
            assert response.status_code == 200
            
            # Verify the response structure
            data = response.json()
            assert "message" in data
            assert "version" in data
            assert "status" in data
            assert data["status"] == "healthy"
            
            # Verify the /predict endpoint exists (even if artifacts aren't loaded)
            # We're not testing functionality here, just that the endpoint is registered
            response = client.post("/predict", json={
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
            })
            
            # The endpoint should be accessible (200 or 500, but not 404)
            # 500 is acceptable if artifacts aren't loaded
            assert response.status_code in [200, 500], \
                f"Expected 200 or 500, got {response.status_code}"
            
        except ModuleNotFoundError as e:
            pytest.fail(f"Server failed to start due to import error: {e}")
        except ImportError as e:
            pytest.fail(f"Server failed to start due to import error: {e}")
        except Exception as e:
            pytest.fail(f"Server failed to start with unexpected error: {e}")


@pytest.fixture
def client():
    """Create a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def valid_sensor_payload():
    """Create a valid sensor input payload."""
    return {
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


@pytest.fixture
def mock_artifacts():
    """Create mock model artifacts."""
    # Mock preprocessor
    preprocessor = Mock()
    preprocessor.transform.return_value = np.array([[
        950.0, 70.0, 120.0, 2.5, 25.0, 75.0, 3.5,
        0.05, 0.05, 0.05, 145.0, 420.0, 145.0, 420.0,
        145.0, 420.0, 145.0, 420.0
    ]])
    
    # Mock model
    model = Mock()
    model.predict.return_value = np.array([0])
    model.predict_proba.return_value = np.array([[
        0.95, 0.02, 0.01, 0.01, 0.005, 0.005, 0.005, 0.005
    ]])
    
    # Mock SHAP explainer
    explainer = Mock()
    shap_values_class_0 = np.array([[0.05, -0.02, 0.01, -0.01, 0.0, -0.03, 0.02,
                                     -0.01, -0.01, -0.01, 0.0, 0.01, 0.0, 0.01,
                                     0.0, 0.01, 0.0, 0.01]])
    explainer.shap_values.return_value = [shap_values_class_0] + [np.zeros((1, 18))] * 7
    
    return {
        "model": model,
        "preprocessor": preprocessor,
        "shap_explainer": explainer
    }


class TestHealthEndpoint:
    """Test suite for health check endpoint."""
    
    def test_root_endpoint(self, client):
        """Test GET / endpoint returns health status."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "AIMS API is running"
        assert data["version"] == "1.0"
        assert data["status"] == "healthy"


class TestPredictEndpoint:
    """Test suite for /predict endpoint."""
    
    def test_predict_with_valid_payload(self, client, valid_sensor_payload, mock_artifacts):
        """Test POST /predict with valid payload (should return 200)."""
        # Set mock artifacts in app state
        app.state.model = mock_artifacts["model"]
        app.state.preprocessor = mock_artifacts["preprocessor"]
        app.state.shap_explainer = mock_artifacts["shap_explainer"]
        
        response = client.post("/predict", json=valid_sensor_payload)
        
        # Verify response status
        assert response.status_code == 200
        
        # Verify response structure
        data = response.json()
        assert "prediction_label" in data
        assert "probabilities" in data
        assert "shap_values" in data
        
        # Verify prediction content
        assert data["prediction_label"] == "Normal"
        assert isinstance(data["probabilities"], dict)
        assert isinstance(data["shap_values"], dict)
        
        # Verify probabilities has all 8 fault types
        assert len(data["probabilities"]) == 8
        assert "Normal" in data["probabilities"]
        assert data["probabilities"]["Normal"] == 0.95
        
        # Verify SHAP values has all 18 features
        assert len(data["shap_values"]) == 18
        assert "Shaft_RPM" in data["shap_values"]
        assert "Oil_Temp" in data["shap_values"]
    
    def test_predict_with_invalid_payload_missing_fields(self, client):
        """Test POST /predict with invalid payload (should return 422)."""
        invalid_payload = {
            "Shaft_RPM": 950.0,
            "Engine_Load": 70.0,
            # Missing all other required fields
        }
        
        response = client.post("/predict", json=invalid_payload)
        
        # Verify response status is 422 (Unprocessable Entity)
        assert response.status_code == 422
        
        # Verify error details are returned
        data = response.json()
        assert "detail" in data
        assert isinstance(data["detail"], list)
        assert len(data["detail"]) > 0
    
    def test_predict_with_invalid_payload_wrong_types(self, client):
        """Test POST /predict with invalid types (should return 422)."""
        invalid_payload = {
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
        
        response = client.post("/predict", json=invalid_payload)
        
        # Verify response status is 422
        assert response.status_code == 422
    

    
    def test_response_schema_matches_prediction_response(self, client, valid_sensor_payload, mock_artifacts):
        """Test response schema matches PredictionResponse."""
        # Set mock artifacts in app state
        app.state.model = mock_artifacts["model"]
        app.state.preprocessor = mock_artifacts["preprocessor"]
        app.state.shap_explainer = mock_artifacts["shap_explainer"]
        
        response = client.post("/predict", json=valid_sensor_payload)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify required fields exist
        assert "prediction_label" in data
        assert "probabilities" in data
        assert "shap_values" in data
        
        # Verify field types
        assert isinstance(data["prediction_label"], str)
        assert isinstance(data["probabilities"], dict)
        assert isinstance(data["shap_values"], dict)
        
        # Verify probabilities are floats
        for label, prob in data["probabilities"].items():
            assert isinstance(label, str)
            assert isinstance(prob, float)
        
        # Verify SHAP values are floats
        for feature, value in data["shap_values"].items():
            assert isinstance(feature, str)
            assert isinstance(value, float)
    
    def test_predict_without_loaded_artifacts(self, client, valid_sensor_payload):
        """Test POST /predict when artifacts are not loaded (should return 500)."""
        # Set artifacts to None to simulate missing artifacts
        app.state.model = None
        app.state.preprocessor = None
        app.state.shap_explainer = None
        
        response = client.post("/predict", json=valid_sensor_payload)
        
        # Verify response status is 500
        assert response.status_code == 500
        
        # Verify error message
        data = response.json()
        assert "detail" in data
        assert "Model artifacts not loaded" in data["detail"]
