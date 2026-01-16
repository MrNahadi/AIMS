"""
Unit tests for predictor service.
Tests the predict_fault function with mocked model artifacts.
"""

import pytest
import numpy as np
from unittest.mock import Mock

from backend.models.request import SensorInput
from backend.models.response import PredictionResponse
from backend.services.predictor import predict_fault, FAULT_LABELS, FEATURE_NAMES


class TestFaultLabels:
    """Test suite for FAULT_LABELS mapping."""
    
    def test_fault_labels_mapping(self):
        """Test FAULT_LABELS mapping (verify all 8 labels exist)."""
        # Verify all 8 fault types are defined
        assert len(FAULT_LABELS) == 8
        
        # Verify keys are 0-7
        assert set(FAULT_LABELS.keys()) == {0, 1, 2, 3, 4, 5, 6, 7}
        
        # Verify expected labels exist
        assert FAULT_LABELS[0] == "Normal"
        assert FAULT_LABELS[1] == "Fuel Injection Fault"
        assert FAULT_LABELS[2] == "Cooling System Fault"
        assert FAULT_LABELS[3] == "Turbocharger Fault"
        assert FAULT_LABELS[4] == "Bearing Wear"
        assert FAULT_LABELS[5] == "Lubrication Oil Degradation"
        assert FAULT_LABELS[6] == "Air Intake Restriction"
        assert FAULT_LABELS[7] == "Vibration Anomaly"


class TestFeatureNames:
    """Test suite for FEATURE_NAMES."""
    
    def test_feature_names_count(self):
        """Test that FEATURE_NAMES has correct number of features."""
        assert len(FEATURE_NAMES) == 18
    
    def test_shap_values_dictionary_has_correct_feature_names(self):
        """Test SHAP values dictionary has correct feature names."""
        expected_features = [
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
        
        assert FEATURE_NAMES == expected_features


class TestPredictFault:
    """Test suite for predict_fault function."""
    
    @pytest.fixture
    def sample_sensor_input(self):
        """Create a sample SensorInput for testing."""
        return SensorInput(
            Shaft_RPM=950.0,
            Engine_Load=70.0,
            Fuel_Flow=120.0,
            Air_Pressure=2.5,
            Ambient_Temp=25.0,
            Oil_Temp=75.0,
            Oil_Pressure=3.5,
            Vibration_X=0.05,
            Vibration_Y=0.05,
            Vibration_Z=0.05,
            Cylinder1_Pressure=145.0,
            Cylinder1_Exhaust_Temp=420.0,
            Cylinder2_Pressure=145.0,
            Cylinder2_Exhaust_Temp=420.0,
            Cylinder3_Pressure=145.0,
            Cylinder3_Exhaust_Temp=420.0,
            Cylinder4_Pressure=145.0,
            Cylinder4_Exhaust_Temp=420.0
        )
    
    @pytest.fixture
    def mock_preprocessor(self):
        """Create a mock preprocessor."""
        preprocessor = Mock()
        # Mock transform to return scaled input (identity transformation for simplicity)
        preprocessor.transform.return_value = np.array([[
            950.0, 70.0, 120.0, 2.5, 25.0, 75.0, 3.5,
            0.05, 0.05, 0.05, 145.0, 420.0, 145.0, 420.0,
            145.0, 420.0, 145.0, 420.0
        ]])
        return preprocessor
    
    @pytest.fixture
    def mock_model(self):
        """Create a mock LightGBM model."""
        model = Mock()
        # Mock predict to return class 0 (Normal)
        model.predict.return_value = np.array([0])
        # Mock predict_proba to return probabilities for all 8 classes
        model.predict_proba.return_value = np.array([[
            0.95, 0.02, 0.01, 0.01, 0.005, 0.005, 0.005, 0.005
        ]])
        return model
    
    @pytest.fixture
    def mock_shap_explainer_list_format(self):
        """Create a mock SHAP explainer that returns list format."""
        explainer = Mock()
        # Mock shap_values to return list of arrays (one per class)
        # For class 0, return SHAP values for 18 features
        shap_values_class_0 = np.array([[0.05, -0.02, 0.01, -0.01, 0.0, -0.03, 0.02,
                                         -0.01, -0.01, -0.01, 0.0, 0.01, 0.0, 0.01,
                                         0.0, 0.01, 0.0, 0.01]])
        # Create list with 8 arrays (one per class)
        explainer.shap_values.return_value = [shap_values_class_0] + [np.zeros((1, 18))] * 7
        return explainer
    
    @pytest.fixture
    def mock_shap_explainer_3d_format(self):
        """Create a mock SHAP explainer that returns 3D array format."""
        explainer = Mock()
        # Mock shap_values to return 3D array: [num_samples, num_features, num_classes]
        shap_3d = np.zeros((1, 18, 8))
        # Set SHAP values for class 0
        shap_3d[0, :, 0] = np.array([0.05, -0.02, 0.01, -0.01, 0.0, -0.03, 0.02,
                                     -0.01, -0.01, -0.01, 0.0, 0.01, 0.0, 0.01,
                                     0.0, 0.01, 0.0, 0.01])
        explainer.shap_values.return_value = shap_3d
        return explainer
    
    def test_predict_fault_with_valid_input_list_format(
        self, 
        sample_sensor_input, 
        mock_model, 
        mock_preprocessor, 
        mock_shap_explainer_list_format
    ):
        """Test predict_fault with valid input (should return PredictionResponse) - list format."""
        result = predict_fault(
            sensor_input=sample_sensor_input,
            model=mock_model,
            preprocessor=mock_preprocessor,
            shap_explainer=mock_shap_explainer_list_format
        )
        
        # Verify result is PredictionResponse
        assert isinstance(result, PredictionResponse)
        
        # Verify prediction label
        assert result.prediction_label == "Normal"
        
        # Verify probabilities
        assert len(result.probabilities) == 8
        assert result.probabilities["Normal"] == 0.95
        assert result.probabilities["Fuel Injection Fault"] == 0.02
        
        # Verify SHAP values
        assert len(result.shap_values) == 18
        assert "Shaft_RPM" in result.shap_values
        assert "Oil_Temp" in result.shap_values
        assert result.shap_values["Shaft_RPM"] == 0.05
        assert result.shap_values["Oil_Temp"] == -0.03
        
        # Verify mocks were called
        mock_preprocessor.transform.assert_called_once()
        mock_model.predict.assert_called_once()
        mock_model.predict_proba.assert_called_once()
        mock_shap_explainer_list_format.shap_values.assert_called_once()
    
    def test_predict_fault_with_valid_input_3d_format(
        self, 
        sample_sensor_input, 
        mock_model, 
        mock_preprocessor, 
        mock_shap_explainer_3d_format
    ):
        """Test predict_fault with valid input (should return PredictionResponse) - 3D format."""
        result = predict_fault(
            sensor_input=sample_sensor_input,
            model=mock_model,
            preprocessor=mock_preprocessor,
            shap_explainer=mock_shap_explainer_3d_format
        )
        
        # Verify result is PredictionResponse
        assert isinstance(result, PredictionResponse)
        
        # Verify prediction label
        assert result.prediction_label == "Normal"
        
        # Verify SHAP values
        assert len(result.shap_values) == 18
        assert result.shap_values["Shaft_RPM"] == 0.05
        assert result.shap_values["Oil_Temp"] == -0.03
    
    def test_predict_fault_turbocharger_fault(
        self, 
        sample_sensor_input, 
        mock_preprocessor, 
        mock_shap_explainer_list_format
    ):
        """Test predict_fault with Turbocharger Fault prediction."""
        # Create model that predicts class 3 (Turbocharger Fault)
        model = Mock()
        model.predict.return_value = np.array([3])
        model.predict_proba.return_value = np.array([[
            0.05, 0.05, 0.05, 0.75, 0.03, 0.03, 0.02, 0.02
        ]])
        
        result = predict_fault(
            sensor_input=sample_sensor_input,
            model=model,
            preprocessor=mock_preprocessor,
            shap_explainer=mock_shap_explainer_list_format
        )
        
        # Verify prediction label
        assert result.prediction_label == "Turbocharger Fault"
        assert result.probabilities["Turbocharger Fault"] == 0.75
    
    def test_shap_values_have_all_feature_names(
        self, 
        sample_sensor_input, 
        mock_model, 
        mock_preprocessor, 
        mock_shap_explainer_list_format
    ):
        """Test that SHAP values dictionary contains all expected feature names."""
        result = predict_fault(
            sensor_input=sample_sensor_input,
            model=mock_model,
            preprocessor=mock_preprocessor,
            shap_explainer=mock_shap_explainer_list_format
        )
        
        # Verify all feature names are present in SHAP values
        for feature_name in FEATURE_NAMES:
            assert feature_name in result.shap_values
        
        # Verify no extra keys
        assert set(result.shap_values.keys()) == set(FEATURE_NAMES)
    
    def test_predict_fault_with_real_data(self):
        """
        Test predict_fault with real sensor data from the dataset.
        Verifies predictions remain unchanged after DataFrame fix.
        
        Validates: Requirements 3.1
        """
        import joblib
        from pathlib import Path
        
        # Load actual model artifacts
        artifacts_dir = Path(__file__).parent.parent / "artifacts"
        preprocessor = joblib.load(artifacts_dir / "preprocessor.pkl")
        model = joblib.load(artifacts_dir / "lgbm_model.pkl")
        shap_explainer = joblib.load(artifacts_dir / "shap_explainer.pkl")
        
        # Use real sensor data from the dataset (first row)
        sensor_input = SensorInput(
            Shaft_RPM=965.414073,
            Engine_Load=72.397307,
            Fuel_Flow=114.665107,
            Air_Pressure=1.025896,
            Ambient_Temp=27.055404,
            Oil_Temp=73.000474,
            Oil_Pressure=3.407503,
            Vibration_X=0.087248,
            Vibration_Y=0.076305,
            Vibration_Z=0.069988,
            Cylinder1_Pressure=157.710104,
            Cylinder1_Exhaust_Temp=418.761079,
            Cylinder2_Pressure=139.335694,
            Cylinder2_Exhaust_Temp=449.428109,
            Cylinder3_Pressure=151.140472,
            Cylinder3_Exhaust_Temp=400.142839,
            Cylinder4_Pressure=138.194303,
            Cylinder4_Exhaust_Temp=469.788241
        )
        
        # Execute prediction
        result = predict_fault(sensor_input, model, preprocessor, shap_explainer)
        
        # Verify result structure
        assert isinstance(result, PredictionResponse)
        assert isinstance(result.prediction_label, str)
        assert result.prediction_label in FAULT_LABELS.values()
        
        # Verify probabilities structure
        assert len(result.probabilities) == 8
        assert all(label in result.probabilities for label in FAULT_LABELS.values())
        
        # Verify SHAP values structure
        assert len(result.shap_values) == 18
        assert all(feature in result.shap_values for feature in FEATURE_NAMES)
        
        # The actual prediction should be "Normal" (class 0) for this sample
        assert result.prediction_label == "Normal"
        
        # Verify probabilities are valid (sum to 1.0, all in [0, 1])
        prob_sum = sum(result.probabilities.values())
        assert abs(prob_sum - 1.0) < 1e-6, f"Probabilities sum to {prob_sum}, expected 1.0"
        assert all(0.0 <= p <= 1.0 for p in result.probabilities.values())
        
        # Verify SHAP values are finite numbers
        assert all(np.isfinite(v) for v in result.shap_values.values())
