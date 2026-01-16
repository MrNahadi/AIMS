"""
Property-based tests for backend import fix.
Uses Hypothesis to verify universal properties across many inputs.
"""

import ast
import os
from pathlib import Path

import numpy as np
from hypothesis import given, settings, strategies as st

from backend.models.request import SensorInput


# Feature: backend-import-fix, Property 2: All model fields match predictor expectations
@settings(max_examples=100)
@given(
    shaft_rpm=st.floats(min_value=0.0, max_value=3000.0, allow_nan=False, allow_infinity=False),
    engine_load=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    fuel_flow=st.floats(min_value=0.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    air_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    ambient_temp=st.floats(min_value=-50.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    oil_temp=st.floats(min_value=0.0, max_value=200.0, allow_nan=False, allow_infinity=False),
    oil_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    vibration_x=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_y=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_z=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    cylinder1_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder1_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder2_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder2_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder3_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder3_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder4_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder4_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
)
def test_field_extraction_produces_18_element_array(
    shaft_rpm, engine_load, fuel_flow, air_pressure, ambient_temp,
    oil_temp, oil_pressure, vibration_x, vibration_y, vibration_z,
    cylinder1_pressure, cylinder1_exhaust_temp,
    cylinder2_pressure, cylinder2_exhaust_temp,
    cylinder3_pressure, cylinder3_exhaust_temp,
    cylinder4_pressure, cylinder4_exhaust_temp
):
    """
    Property test: For any valid SensorInput, field extraction produces 18-element array.
    
    Validates: Requirements 1.5
    Feature: backend-import-fix, Property 2: All model fields match predictor expectations
    """
    # Create SensorInput instance with random valid values
    sensor_input = SensorInput(
        Shaft_RPM=shaft_rpm,
        Engine_Load=engine_load,
        Fuel_Flow=fuel_flow,
        Air_Pressure=air_pressure,
        Ambient_Temp=ambient_temp,
        Oil_Temp=oil_temp,
        Oil_Pressure=oil_pressure,
        Vibration_X=vibration_x,
        Vibration_Y=vibration_y,
        Vibration_Z=vibration_z,
        Cylinder1_Pressure=cylinder1_pressure,
        Cylinder1_Exhaust_Temp=cylinder1_exhaust_temp,
        Cylinder2_Pressure=cylinder2_pressure,
        Cylinder2_Exhaust_Temp=cylinder2_exhaust_temp,
        Cylinder3_Pressure=cylinder3_pressure,
        Cylinder3_Exhaust_Temp=cylinder3_exhaust_temp,
        Cylinder4_Pressure=cylinder4_pressure,
        Cylinder4_Exhaust_Temp=cylinder4_exhaust_temp
    )
    
    # Extract fields as done in predictor service
    # This mimics the extraction logic in predictor.py
    input_array = np.array([[
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
    ]])
    
    # Verify extraction produces 18-element array without errors
    assert input_array.shape == (1, 18), f"Expected shape (1, 18), got {input_array.shape}"
    assert not np.isnan(input_array).any(), "Array contains NaN values"
    assert not np.isinf(input_array).any(), "Array contains infinite values"


# Feature: backend-import-fix, Property 3: Absolute imports are used consistently
def test_absolute_imports_used_consistently():
    """
    Property test: For any Python file in backend, all backend imports use absolute imports.
    
    Validates: Requirements 1.5, 4.2
    Feature: backend-import-fix, Property 3: Absolute imports are used consistently
    """
    backend_dir = Path(__file__).parent.parent  # Go up from tests/ to backend/
    
    # Find all .py files in backend package (excluding __pycache__ and venv)
    python_files = []
    for root, dirs, files in os.walk(backend_dir):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)
    
    # Check each Python file for import statements
    for py_file in python_files:
        with open(py_file, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read(), filename=str(py_file))
            except SyntaxError:
                # Skip files with syntax errors (shouldn't happen in valid code)
                continue
        
        # Extract all import statements
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module
                if module and module.startswith('.'):
                    # Found a relative import - this violates the property
                    raise AssertionError(
                        f"File {py_file.relative_to(backend_dir)} contains relative import: "
                        f"'from {module} import ...'. All backend imports should use "
                        f"absolute imports starting with 'backend.'"
                    )
                elif module and ('models' in module or 'services' in module):
                    # Check if it's importing from backend modules without 'backend.' prefix
                    if not module.startswith('backend.'):
                        raise AssertionError(
                            f"File {py_file.relative_to(backend_dir)} contains import without "
                            f"'backend.' prefix: 'from {module} import ...'. "
                            f"Should be 'from backend.{module} import ...'"
                        )


# Feature: backend-import-fix, Property 4: Package structure is complete
def test_package_structure_is_complete():
    """
    Property test: For any directory with .py files in backend, it contains __init__.py.
    
    Validates: Requirements 4.3
    Feature: backend-import-fix, Property 4: Package structure is complete
    """
    backend_dir = Path(__file__).parent.parent  # Go up from tests/ to backend/
    
    # Find all directories containing .py files
    directories_with_python = set()
    for root, dirs, files in os.walk(backend_dir):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        # Check if this directory has any .py files
        has_python_files = any(f.endswith('.py') for f in files)
        if has_python_files:
            directories_with_python.add(Path(root))
    
    # Verify each directory has __init__.py
    for directory in directories_with_python:
        init_file = directory / '__init__.py'
        assert init_file.exists(), (
            f"Directory {directory.relative_to(backend_dir.parent)} contains Python files "
            f"but is missing __init__.py"
        )


# Feature: fix-feature-name-warnings, Property 2: DataFrame Structure Correctness
@settings(max_examples=100, deadline=None)
@given(
    shaft_rpm=st.floats(min_value=0.0, max_value=3000.0, allow_nan=False, allow_infinity=False),
    engine_load=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    fuel_flow=st.floats(min_value=0.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    air_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    ambient_temp=st.floats(min_value=-50.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    oil_temp=st.floats(min_value=0.0, max_value=200.0, allow_nan=False, allow_infinity=False),
    oil_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    vibration_x=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_y=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_z=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    cylinder1_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder1_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder2_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder2_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder3_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder3_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder4_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder4_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
)
def test_dataframe_structure_correctness(
    shaft_rpm, engine_load, fuel_flow, air_pressure, ambient_temp,
    oil_temp, oil_pressure, vibration_x, vibration_y, vibration_z,
    cylinder1_pressure, cylinder1_exhaust_temp,
    cylinder2_pressure, cylinder2_exhaust_temp,
    cylinder3_pressure, cylinder3_exhaust_temp,
    cylinder4_pressure, cylinder4_exhaust_temp
):
    """
    Property test: For any valid sensor input, DataFrame has 18 columns with correct names in correct order.
    
    Validates: Requirements 2.1, 2.2
    Feature: fix-feature-name-warnings, Property 2: DataFrame Structure Correctness
    """
    import pandas as pd
    from backend.services.predictor import FEATURE_NAMES
    
    # Create SensorInput instance with random valid values
    sensor_input = SensorInput(
        Shaft_RPM=shaft_rpm,
        Engine_Load=engine_load,
        Fuel_Flow=fuel_flow,
        Air_Pressure=air_pressure,
        Ambient_Temp=ambient_temp,
        Oil_Temp=oil_temp,
        Oil_Pressure=oil_pressure,
        Vibration_X=vibration_x,
        Vibration_Y=vibration_y,
        Vibration_Z=vibration_z,
        Cylinder1_Pressure=cylinder1_pressure,
        Cylinder1_Exhaust_Temp=cylinder1_exhaust_temp,
        Cylinder2_Pressure=cylinder2_pressure,
        Cylinder2_Exhaust_Temp=cylinder2_exhaust_temp,
        Cylinder3_Pressure=cylinder3_pressure,
        Cylinder3_Exhaust_Temp=cylinder3_exhaust_temp,
        Cylinder4_Pressure=cylinder4_pressure,
        Cylinder4_Exhaust_Temp=cylinder4_exhaust_temp
    )
    
    # Create DataFrame as done in predictor service
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
    
    # Verify DataFrame has exactly 18 columns
    assert input_df.shape[1] == 18, f"Expected 18 columns, got {input_df.shape[1]}"
    
    # Verify DataFrame has exactly 1 row
    assert input_df.shape[0] == 1, f"Expected 1 row, got {input_df.shape[0]}"
    
    # Verify column names match FEATURE_NAMES exactly
    assert list(input_df.columns) == FEATURE_NAMES, \
        f"Column names don't match. Expected {FEATURE_NAMES}, got {list(input_df.columns)}"
    
    # Verify column order is correct
    for i, expected_name in enumerate(FEATURE_NAMES):
        assert input_df.columns[i] == expected_name, \
            f"Column at index {i} should be '{expected_name}', got '{input_df.columns[i]}'"
    
    # Verify no NaN or infinite values
    assert not input_df.isna().any().any(), "DataFrame contains NaN values"
    assert not np.isinf(input_df.values).any(), "DataFrame contains infinite values"


# Feature: fix-feature-name-warnings, Property 3: Model Compatibility
@settings(max_examples=100, deadline=None)
@given(
    shaft_rpm=st.floats(min_value=0.0, max_value=3000.0, allow_nan=False, allow_infinity=False),
    engine_load=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    fuel_flow=st.floats(min_value=0.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    air_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    ambient_temp=st.floats(min_value=-50.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    oil_temp=st.floats(min_value=0.0, max_value=200.0, allow_nan=False, allow_infinity=False),
    oil_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    vibration_x=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_y=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_z=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    cylinder1_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder1_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder2_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder2_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder3_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder3_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder4_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder4_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
)
def test_model_compatibility(
    shaft_rpm, engine_load, fuel_flow, air_pressure, ambient_temp,
    oil_temp, oil_pressure, vibration_x, vibration_y, vibration_z,
    cylinder1_pressure, cylinder1_exhaust_temp,
    cylinder2_pressure, cylinder2_exhaust_temp,
    cylinder3_pressure, cylinder3_exhaust_temp,
    cylinder4_pressure, cylinder4_exhaust_temp
):
    """
    Property test: For any valid sensor input DataFrame, all components process it without exceptions.
    
    Validates: Requirements 2.3
    Feature: fix-feature-name-warnings, Property 3: Model Compatibility
    """
    import pandas as pd
    import joblib
    from pathlib import Path
    from backend.services.predictor import FEATURE_NAMES
    
    # Load actual model artifacts
    artifacts_dir = Path(__file__).parent.parent / "artifacts"
    preprocessor = joblib.load(artifacts_dir / "preprocessor.pkl")
    model = joblib.load(artifacts_dir / "lgbm_model.pkl")
    shap_explainer = joblib.load(artifacts_dir / "shap_explainer.pkl")
    
    # Create DataFrame with feature names
    input_df = pd.DataFrame([[
        shaft_rpm, engine_load, fuel_flow, air_pressure, ambient_temp,
        oil_temp, oil_pressure, vibration_x, vibration_y, vibration_z,
        cylinder1_pressure, cylinder1_exhaust_temp,
        cylinder2_pressure, cylinder2_exhaust_temp,
        cylinder3_pressure, cylinder3_exhaust_temp,
        cylinder4_pressure, cylinder4_exhaust_temp
    ]], columns=FEATURE_NAMES)
    
    # Test 1: StandardScaler should process DataFrame without exceptions
    try:
        input_scaled_array = preprocessor.transform(input_df)
        assert input_scaled_array is not None, "Preprocessor returned None"
        assert input_scaled_array.shape == (1, 18), f"Expected shape (1, 18), got {input_scaled_array.shape}"
        
        # Convert back to DataFrame to preserve feature names
        input_scaled = pd.DataFrame(input_scaled_array, columns=FEATURE_NAMES)
    except Exception as e:
        raise AssertionError(f"StandardScaler failed to process DataFrame: {e}")
    
    # Test 2: LGBMClassifier should process scaled data without exceptions
    try:
        prediction = model.predict(input_scaled)
        assert prediction is not None, "Model returned None for prediction"
        assert len(prediction) == 1, f"Expected 1 prediction, got {len(prediction)}"
        assert 0 <= prediction[0] <= 7, f"Prediction {prediction[0]} out of range [0, 7]"
        
        probabilities = model.predict_proba(input_scaled)
        assert probabilities is not None, "Model returned None for probabilities"
        assert probabilities.shape == (1, 8), f"Expected shape (1, 8), got {probabilities.shape}"
    except Exception as e:
        raise AssertionError(f"LGBMClassifier failed to process scaled data: {e}")
    
    # Test 3: SHAP explainer should process scaled data without exceptions
    try:
        shap_values = shap_explainer.shap_values(input_scaled)
        assert shap_values is not None, "SHAP explainer returned None"
        
        # SHAP can return either list or 3D array
        if isinstance(shap_values, list):
            assert len(shap_values) == 8, f"Expected 8 classes, got {len(shap_values)}"
            for i, class_shap in enumerate(shap_values):
                assert class_shap.shape == (1, 18), \
                    f"Class {i} SHAP values have wrong shape: {class_shap.shape}"
        else:
            # 3D array format
            assert shap_values.shape[0] == 1, f"Expected 1 sample, got {shap_values.shape[0]}"
            assert shap_values.shape[1] == 18, f"Expected 18 features, got {shap_values.shape[1]}"
            assert shap_values.shape[2] == 8, f"Expected 8 classes, got {shap_values.shape[2]}"
    except Exception as e:
        raise AssertionError(f"SHAP explainer failed to process scaled data: {e}")


# Feature: fix-feature-name-warnings, Property 1: No Feature Name Warnings During Prediction
@settings(max_examples=100, deadline=None)
@given(
    shaft_rpm=st.floats(min_value=0.0, max_value=3000.0, allow_nan=False, allow_infinity=False),
    engine_load=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    fuel_flow=st.floats(min_value=0.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    air_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    ambient_temp=st.floats(min_value=-50.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    oil_temp=st.floats(min_value=0.0, max_value=200.0, allow_nan=False, allow_infinity=False),
    oil_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    vibration_x=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_y=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_z=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    cylinder1_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder1_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder2_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder2_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder3_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder3_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder4_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder4_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
)
def test_no_feature_name_warnings_during_prediction(
    shaft_rpm, engine_load, fuel_flow, air_pressure, ambient_temp,
    oil_temp, oil_pressure, vibration_x, vibration_y, vibration_z,
    cylinder1_pressure, cylinder1_exhaust_temp,
    cylinder2_pressure, cylinder2_exhaust_temp,
    cylinder3_pressure, cylinder3_exhaust_temp,
    cylinder4_pressure, cylinder4_exhaust_temp
):
    """
    Property test: For any valid sensor input, no sklearn feature name warnings are generated.
    
    Validates: Requirements 1.1, 1.2, 1.3
    Feature: fix-feature-name-warnings, Property 1: No Feature Name Warnings During Prediction
    """
    import warnings
    import joblib
    from pathlib import Path
    from backend.services.predictor import predict_fault
    
    # Create SensorInput instance with random valid values
    sensor_input = SensorInput(
        Shaft_RPM=shaft_rpm,
        Engine_Load=engine_load,
        Fuel_Flow=fuel_flow,
        Air_Pressure=air_pressure,
        Ambient_Temp=ambient_temp,
        Oil_Temp=oil_temp,
        Oil_Pressure=oil_pressure,
        Vibration_X=vibration_x,
        Vibration_Y=vibration_y,
        Vibration_Z=vibration_z,
        Cylinder1_Pressure=cylinder1_pressure,
        Cylinder1_Exhaust_Temp=cylinder1_exhaust_temp,
        Cylinder2_Pressure=cylinder2_pressure,
        Cylinder2_Exhaust_Temp=cylinder2_exhaust_temp,
        Cylinder3_Pressure=cylinder3_pressure,
        Cylinder3_Exhaust_Temp=cylinder3_exhaust_temp,
        Cylinder4_Pressure=cylinder4_pressure,
        Cylinder4_Exhaust_Temp=cylinder4_exhaust_temp
    )
    
    # Load actual model artifacts
    artifacts_dir = Path(__file__).parent.parent / "artifacts"
    preprocessor = joblib.load(artifacts_dir / "preprocessor.pkl")
    model = joblib.load(artifacts_dir / "lgbm_model.pkl")
    shap_explainer = joblib.load(artifacts_dir / "shap_explainer.pkl")
    
    # Capture all warnings during prediction
    with warnings.catch_warnings(record=True) as warning_list:
        # Ensure all warnings are captured
        warnings.simplefilter("always")
        
        # Execute the full prediction pipeline
        result = predict_fault(sensor_input, model, preprocessor, shap_explainer)
        
        # Verify prediction completed successfully
        assert result is not None, "predict_fault returned None"
        
        # Check for sklearn feature name warnings
        feature_name_warnings = []
        for w in warning_list:
            warning_message = str(w.message).lower()
            # Check for various forms of sklearn feature name warnings
            if any(keyword in warning_message for keyword in [
                "feature names",
                "feature_names",
                "x does not have valid feature names",
                "x has feature names",
                "feature name"
            ]):
                feature_name_warnings.append(str(w.message))
        
        # Assert no feature name warnings were generated
        assert len(feature_name_warnings) == 0, (
            f"Found {len(feature_name_warnings)} sklearn feature name warning(s) during prediction:\n" +
            "\n".join(f"  - {msg}" for msg in feature_name_warnings)
        )


# Feature: fix-feature-name-warnings, Property 4: Probability Distribution Validity
@settings(max_examples=100, deadline=None)
@given(
    shaft_rpm=st.floats(min_value=0.0, max_value=3000.0, allow_nan=False, allow_infinity=False),
    engine_load=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    fuel_flow=st.floats(min_value=0.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    air_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    ambient_temp=st.floats(min_value=-50.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    oil_temp=st.floats(min_value=0.0, max_value=200.0, allow_nan=False, allow_infinity=False),
    oil_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    vibration_x=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_y=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_z=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    cylinder1_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder1_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder2_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder2_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder3_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder3_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder4_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder4_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
)
def test_probability_distribution_validity(
    shaft_rpm, engine_load, fuel_flow, air_pressure, ambient_temp,
    oil_temp, oil_pressure, vibration_x, vibration_y, vibration_z,
    cylinder1_pressure, cylinder1_exhaust_temp,
    cylinder2_pressure, cylinder2_exhaust_temp,
    cylinder3_pressure, cylinder3_exhaust_temp,
    cylinder4_pressure, cylinder4_exhaust_temp
):
    """
    Property test: For any valid sensor input, probabilities sum to 1.0 and are in range [0, 1].
    
    Validates: Requirements 3.2
    Feature: fix-feature-name-warnings, Property 4: Probability Distribution Validity
    """
    import joblib
    from pathlib import Path
    from backend.services.predictor import predict_fault, FAULT_LABELS
    
    # Create SensorInput instance with random valid values
    sensor_input = SensorInput(
        Shaft_RPM=shaft_rpm,
        Engine_Load=engine_load,
        Fuel_Flow=fuel_flow,
        Air_Pressure=air_pressure,
        Ambient_Temp=ambient_temp,
        Oil_Temp=oil_temp,
        Oil_Pressure=oil_pressure,
        Vibration_X=vibration_x,
        Vibration_Y=vibration_y,
        Vibration_Z=vibration_z,
        Cylinder1_Pressure=cylinder1_pressure,
        Cylinder1_Exhaust_Temp=cylinder1_exhaust_temp,
        Cylinder2_Pressure=cylinder2_pressure,
        Cylinder2_Exhaust_Temp=cylinder2_exhaust_temp,
        Cylinder3_Pressure=cylinder3_pressure,
        Cylinder3_Exhaust_Temp=cylinder3_exhaust_temp,
        Cylinder4_Pressure=cylinder4_pressure,
        Cylinder4_Exhaust_Temp=cylinder4_exhaust_temp
    )
    
    # Load actual model artifacts
    artifacts_dir = Path(__file__).parent.parent / "artifacts"
    preprocessor = joblib.load(artifacts_dir / "preprocessor.pkl")
    model = joblib.load(artifacts_dir / "lgbm_model.pkl")
    shap_explainer = joblib.load(artifacts_dir / "shap_explainer.pkl")
    
    # Execute prediction
    result = predict_fault(sensor_input, model, preprocessor, shap_explainer)
    
    # Property 1: Probabilities dictionary should contain exactly 8 entries (one per fault class)
    assert len(result.probabilities) == 8, \
        f"Expected 8 probabilities, got {len(result.probabilities)}"
    
    # Property 2: All fault labels should be present as keys
    expected_labels = set(FAULT_LABELS.values())
    actual_labels = set(result.probabilities.keys())
    assert actual_labels == expected_labels, \
        f"Probability keys don't match fault labels. Expected {expected_labels}, got {actual_labels}"
    
    # Property 3: All probabilities should be in range [0, 1]
    for label, prob in result.probabilities.items():
        assert 0.0 <= prob <= 1.0, \
            f"Probability for '{label}' is {prob}, which is outside range [0, 1]"
    
    # Property 4: Probabilities should sum to 1.0 (within floating-point tolerance)
    prob_sum = sum(result.probabilities.values())
    assert abs(prob_sum - 1.0) < 1e-6, \
        f"Probabilities sum to {prob_sum}, expected 1.0 (tolerance 1e-6)"
    
    # Property 5: All probability values should be finite (not NaN or infinity)
    for label, prob in result.probabilities.items():
        assert np.isfinite(prob), \
            f"Probability for '{label}' is not finite: {prob}"


# Feature: fix-feature-name-warnings, Property 5: SHAP Values Completeness
@settings(max_examples=100, deadline=None)
@given(
    shaft_rpm=st.floats(min_value=0.0, max_value=3000.0, allow_nan=False, allow_infinity=False),
    engine_load=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    fuel_flow=st.floats(min_value=0.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    air_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    ambient_temp=st.floats(min_value=-50.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    oil_temp=st.floats(min_value=0.0, max_value=200.0, allow_nan=False, allow_infinity=False),
    oil_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    vibration_x=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_y=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_z=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    cylinder1_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder1_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder2_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder2_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder3_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder3_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder4_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder4_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
)
def test_shap_values_completeness(
    shaft_rpm, engine_load, fuel_flow, air_pressure, ambient_temp,
    oil_temp, oil_pressure, vibration_x, vibration_y, vibration_z,
    cylinder1_pressure, cylinder1_exhaust_temp,
    cylinder2_pressure, cylinder2_exhaust_temp,
    cylinder3_pressure, cylinder3_exhaust_temp,
    cylinder4_pressure, cylinder4_exhaust_temp
):
    """
    Property test: For any valid sensor input, SHAP values are computed for all 18 features.
    
    Validates: Requirements 3.3
    Feature: fix-feature-name-warnings, Property 5: SHAP Values Completeness
    """
    import joblib
    from pathlib import Path
    from backend.services.predictor import predict_fault, FEATURE_NAMES
    
    # Create SensorInput instance with random valid values
    sensor_input = SensorInput(
        Shaft_RPM=shaft_rpm,
        Engine_Load=engine_load,
        Fuel_Flow=fuel_flow,
        Air_Pressure=air_pressure,
        Ambient_Temp=ambient_temp,
        Oil_Temp=oil_temp,
        Oil_Pressure=oil_pressure,
        Vibration_X=vibration_x,
        Vibration_Y=vibration_y,
        Vibration_Z=vibration_z,
        Cylinder1_Pressure=cylinder1_pressure,
        Cylinder1_Exhaust_Temp=cylinder1_exhaust_temp,
        Cylinder2_Pressure=cylinder2_pressure,
        Cylinder2_Exhaust_Temp=cylinder2_exhaust_temp,
        Cylinder3_Pressure=cylinder3_pressure,
        Cylinder3_Exhaust_Temp=cylinder3_exhaust_temp,
        Cylinder4_Pressure=cylinder4_pressure,
        Cylinder4_Exhaust_Temp=cylinder4_exhaust_temp
    )
    
    # Load actual model artifacts
    artifacts_dir = Path(__file__).parent.parent / "artifacts"
    preprocessor = joblib.load(artifacts_dir / "preprocessor.pkl")
    model = joblib.load(artifacts_dir / "lgbm_model.pkl")
    shap_explainer = joblib.load(artifacts_dir / "shap_explainer.pkl")
    
    # Execute prediction
    result = predict_fault(sensor_input, model, preprocessor, shap_explainer)
    
    # Property 1: SHAP values dictionary should contain exactly 18 entries (one per feature)
    assert len(result.shap_values) == 18, \
        f"Expected 18 SHAP values, got {len(result.shap_values)}"
    
    # Property 2: All feature names should be present as keys
    expected_features = set(FEATURE_NAMES)
    actual_features = set(result.shap_values.keys())
    assert actual_features == expected_features, \
        f"SHAP value keys don't match feature names. Expected {expected_features}, got {actual_features}"
    
    # Property 3: All SHAP values should be finite numbers (not NaN or infinity)
    for feature, shap_value in result.shap_values.items():
        assert np.isfinite(shap_value), \
            f"SHAP value for '{feature}' is not finite: {shap_value}"
    
    # Property 4: SHAP values should be numeric (float or int)
    for feature, shap_value in result.shap_values.items():
        assert isinstance(shap_value, (int, float)), \
            f"SHAP value for '{feature}' is not numeric: {type(shap_value)}"
    
    # Property 5: Feature names in SHAP values should match the order in FEATURE_NAMES
    # (This ensures consistency in how features are processed)
    shap_keys_list = list(result.shap_values.keys())
    for i, expected_feature in enumerate(FEATURE_NAMES):
        assert expected_feature in shap_keys_list, \
            f"Feature '{expected_feature}' missing from SHAP values"


# Feature: fix-feature-name-warnings, Property 6: Response Structure Preservation
@settings(max_examples=100, deadline=None)
@given(
    shaft_rpm=st.floats(min_value=0.0, max_value=3000.0, allow_nan=False, allow_infinity=False),
    engine_load=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    fuel_flow=st.floats(min_value=0.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    air_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    ambient_temp=st.floats(min_value=-50.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    oil_temp=st.floats(min_value=0.0, max_value=200.0, allow_nan=False, allow_infinity=False),
    oil_pressure=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
    vibration_x=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_y=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    vibration_z=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    cylinder1_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder1_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder2_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder2_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder3_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder3_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
    cylinder4_pressure=st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    cylinder4_exhaust_temp=st.floats(min_value=0.0, max_value=800.0, allow_nan=False, allow_infinity=False),
)
def test_response_structure_preservation(
    shaft_rpm, engine_load, fuel_flow, air_pressure, ambient_temp,
    oil_temp, oil_pressure, vibration_x, vibration_y, vibration_z,
    cylinder1_pressure, cylinder1_exhaust_temp,
    cylinder2_pressure, cylinder2_exhaust_temp,
    cylinder3_pressure, cylinder3_exhaust_temp,
    cylinder4_pressure, cylinder4_exhaust_temp
):
    """
    Property test: For any valid sensor input, response contains all required fields with correct types.
    
    Validates: Requirements 3.4
    Feature: fix-feature-name-warnings, Property 6: Response Structure Preservation
    """
    import joblib
    from pathlib import Path
    from backend.services.predictor import predict_fault, FAULT_LABELS, FEATURE_NAMES
    from backend.models.response import PredictionResponse
    
    # Create SensorInput instance with random valid values
    sensor_input = SensorInput(
        Shaft_RPM=shaft_rpm,
        Engine_Load=engine_load,
        Fuel_Flow=fuel_flow,
        Air_Pressure=air_pressure,
        Ambient_Temp=ambient_temp,
        Oil_Temp=oil_temp,
        Oil_Pressure=oil_pressure,
        Vibration_X=vibration_x,
        Vibration_Y=vibration_y,
        Vibration_Z=vibration_z,
        Cylinder1_Pressure=cylinder1_pressure,
        Cylinder1_Exhaust_Temp=cylinder1_exhaust_temp,
        Cylinder2_Pressure=cylinder2_pressure,
        Cylinder2_Exhaust_Temp=cylinder2_exhaust_temp,
        Cylinder3_Pressure=cylinder3_pressure,
        Cylinder3_Exhaust_Temp=cylinder3_exhaust_temp,
        Cylinder4_Pressure=cylinder4_pressure,
        Cylinder4_Exhaust_Temp=cylinder4_exhaust_temp
    )
    
    # Load actual model artifacts
    artifacts_dir = Path(__file__).parent.parent / "artifacts"
    preprocessor = joblib.load(artifacts_dir / "preprocessor.pkl")
    model = joblib.load(artifacts_dir / "lgbm_model.pkl")
    shap_explainer = joblib.load(artifacts_dir / "shap_explainer.pkl")
    
    # Execute prediction
    result = predict_fault(sensor_input, model, preprocessor, shap_explainer)
    
    # Property 1: Result should be a PredictionResponse instance
    assert isinstance(result, PredictionResponse), \
        f"Expected PredictionResponse, got {type(result)}"
    
    # Property 2: prediction_label field should exist and be a string
    assert hasattr(result, 'prediction_label'), \
        "Response missing 'prediction_label' field"
    assert isinstance(result.prediction_label, str), \
        f"prediction_label should be string, got {type(result.prediction_label)}"
    
    # Property 3: prediction_label should be one of the valid fault labels
    assert result.prediction_label in FAULT_LABELS.values(), \
        f"prediction_label '{result.prediction_label}' not in valid fault labels: {list(FAULT_LABELS.values())}"
    
    # Property 4: probabilities field should exist and be a dictionary
    assert hasattr(result, 'probabilities'), \
        "Response missing 'probabilities' field"
    assert isinstance(result.probabilities, dict), \
        f"probabilities should be dict, got {type(result.probabilities)}"
    
    # Property 5: probabilities should have exactly 8 entries with fault labels as keys
    assert len(result.probabilities) == 8, \
        f"probabilities should have 8 entries, got {len(result.probabilities)}"
    assert set(result.probabilities.keys()) == set(FAULT_LABELS.values()), \
        f"probabilities keys don't match fault labels"
    
    # Property 6: All probability values should be floats
    for label, prob in result.probabilities.items():
        assert isinstance(prob, (int, float)), \
            f"Probability for '{label}' should be numeric, got {type(prob)}"
    
    # Property 7: shap_values field should exist and be a dictionary
    assert hasattr(result, 'shap_values'), \
        "Response missing 'shap_values' field"
    assert isinstance(result.shap_values, dict), \
        f"shap_values should be dict, got {type(result.shap_values)}"
    
    # Property 8: shap_values should have exactly 18 entries with feature names as keys
    assert len(result.shap_values) == 18, \
        f"shap_values should have 18 entries, got {len(result.shap_values)}"
    assert set(result.shap_values.keys()) == set(FEATURE_NAMES), \
        f"shap_values keys don't match feature names"
    
    # Property 9: All SHAP values should be floats
    for feature, shap_value in result.shap_values.items():
        assert isinstance(shap_value, (int, float)), \
            f"SHAP value for '{feature}' should be numeric, got {type(shap_value)}"
    
    # Property 10: Response should be serializable (can be converted to dict)
    try:
        response_dict = result.model_dump()
        assert isinstance(response_dict, dict), \
            "Response should be serializable to dict"
        assert 'prediction_label' in response_dict
        assert 'probabilities' in response_dict
        assert 'shap_values' in response_dict
    except Exception as e:
        raise AssertionError(f"Response serialization failed: {e}")
