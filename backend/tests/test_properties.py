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
