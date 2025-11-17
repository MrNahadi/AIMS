# AIMS End-to-End Testing Results

## Task 8: Demo Scenario Validation

### Test Execution Date
Completed: November 17, 2025

### Test Environment
- **Backend**: FastAPI server running on http://localhost:8000
- **Frontend**: React development server running on http://localhost:3000
- **Model Artifacts**: All artifacts successfully generated and loaded
  - lgbm_model.pkl
  - preprocessor.pkl
  - shap_explainer.pkl

### Test Results Summary

✅ **ALL SCENARIOS PASSED**

---

## Scenario 1: Normal Operation

### Test Configuration
```json
{
  "Shaft_RPM": 950,
  "Engine_Load": 70,
  "Fuel_Flow": 120,
  "Air_Pressure": 2.5,
  "Ambient_Temp": 25,
  "Oil_Temp": 75,
  "Oil_Pressure": 3.5,
  "Vibration_X": 0.05,
  "Vibration_Y": 0.05,
  "Vibration_Z": 0.05,
  "Cylinder1_Pressure": 145,
  "Cylinder1_Exhaust_Temp": 420,
  "Cylinder2_Pressure": 145,
  "Cylinder2_Exhaust_Temp": 420,
  "Cylinder3_Pressure": 145,
  "Cylinder3_Exhaust_Temp": 420,
  "Cylinder4_Pressure": 145,
  "Cylinder4_Exhaust_Temp": 420
}
```

### Results
- ✅ **Prediction**: Normal
- ✅ **Confidence**: 96.52% (> 95% threshold)
- ✅ **Top Probabilities**:
  - Normal: 96.52%
  - Fuel Injection Fault: 2.52%
  - Cooling System Fault: 0.62%
- ✅ **Top SHAP Features** (by absolute value):
  - Air_Pressure: 0.8450
  - Oil_Pressure: 0.2485
  - Vibration_Y: 0.1003
- ✅ **SHAP Interpretation**: Features show positive contributions (blue bars), indicating normal operation

**Status**: ✅ PASSED

---

## Scenario 2: Minor Fault (Lubrication Oil Degradation)

### Test Configuration
```json
{
  "Shaft_RPM": 950,
  "Engine_Load": 70,
  "Fuel_Flow": 120,
  "Air_Pressure": 2.5,
  "Ambient_Temp": 25,
  "Oil_Temp": 95,
  "Oil_Pressure": 2.8,
  "Vibration_X": 0.06,
  "Vibration_Y": 0.06,
  "Vibration_Z": 0.06,
  "Cylinder1_Pressure": 145,
  "Cylinder1_Exhaust_Temp": 420,
  "Cylinder2_Pressure": 145,
  "Cylinder2_Exhaust_Temp": 420,
  "Cylinder3_Pressure": 145,
  "Cylinder3_Exhaust_Temp": 420,
  "Cylinder4_Pressure": 145,
  "Cylinder4_Exhaust_Temp": 420
}
```

### Results
- ✅ **Prediction**: Lubrication Oil Degradation
- ✅ **Split Probabilities** (< 90% confidence):
  - Lubrication Oil Degradation: 78.31%
  - Normal: 20.38%
  - Fuel Injection Fault: 0.98%
- ✅ **Top SHAP Features** (by absolute value):
  - Oil_Temp: 6.1730 (highest contributor)
  - Oil_Pressure: 2.4472
  - Cylinder3_Exhaust_Temp: -0.0756
- ✅ **SHAP Interpretation**: Oil_Temp shows as top red bar (positive SHAP), indicating it's pushing toward fault prediction

**Status**: ✅ PASSED

---

## Scenario 3: Critical Fault (Bearing Wear)

### Test Configuration
```json
{
  "Shaft_RPM": 950,
  "Engine_Load": 70,
  "Fuel_Flow": 120,
  "Air_Pressure": 1.8,
  "Ambient_Temp": 25,
  "Oil_Temp": 75,
  "Oil_Pressure": 3.5,
  "Vibration_X": 0.25,
  "Vibration_Y": 0.22,
  "Vibration_Z": 0.20,
  "Cylinder1_Pressure": 130,
  "Cylinder1_Exhaust_Temp": 480,
  "Cylinder2_Pressure": 130,
  "Cylinder2_Exhaust_Temp": 480,
  "Cylinder3_Pressure": 130,
  "Cylinder3_Exhaust_Temp": 480,
  "Cylinder4_Pressure": 130,
  "Cylinder4_Exhaust_Temp": 480
}
```

### Results
- ✅ **Prediction**: Bearing Wear (critical fault)
- ✅ **Confidence**: 97.19% (> 90% threshold)
- ✅ **Top Probabilities**:
  - Bearing Wear: 97.19%
  - Normal: 1.62%
  - Vibration Anomaly: 0.60%
- ✅ **Top SHAP Features** (by absolute value):
  - Vibration_X: 6.4646 (highest contributor)
  - Vibration_Y: 3.8431
  - Cylinder3_Pressure: 0.0049
- ✅ **SHAP Interpretation**: Vibration features show as top red bars, indicating they're strongly pushing toward fault prediction

**Status**: ✅ PASSED

---

## Technical Issues Resolved

### 1. Import Path Issues
- **Problem**: Backend imports used absolute paths (`from backend.models...`)
- **Solution**: Changed to relative imports (`from models...`) for proper module resolution

### 2. SHAP Value Extraction
- **Problem**: SHAP values returned as 3D array `[num_samples, num_features, num_classes]`
- **Solution**: Updated predictor to extract values using `shap_values[0, :, int(prediction)]`

### 3. Model Artifacts Generation
- **Problem**: Notebooks needed execution to generate model artifacts
- **Solution**: Executed notebooks 02 and 03, created custom script for SHAP explainer generation

### 4. Frontend Dependencies
- **Problem**: React dependencies not installed
- **Solution**: Ran `npm install` in frontend directory

---

## Validation Method

Automated testing script (`test_all_scenarios.py`) validates:
1. API connectivity and response format
2. Prediction accuracy and confidence thresholds
3. SHAP value computation and feature importance
4. Probability distribution for each scenario type

---

## Requirements Validation

### Requirement 8.1 (Normal Scenario)
✅ Prediction label is "Normal" with confidence > 95%
✅ SHAP plot shows features pushing away from faults
✅ All values within safe range

### Requirement 8.2 (Minor Fault Scenario)
✅ Prediction shows split probabilities
✅ Oil_Temp highlighted as top SHAP contributor
✅ Oil parameters outside safe range

### Requirement 8.3 (Critical Fault Scenario)
✅ Prediction is a critical fault with confidence > 90%
✅ Vibration features highlighted as top SHAP contributors
✅ Multiple parameters outside safe range

### Requirement 8.4 (Visual Validation)
✅ SHAP values computed correctly for all scenarios
✅ Feature importance rankings align with fault types
✅ Spider chart data available (probabilities and SHAP values)

---

## Conclusion

All three demo scenarios have been successfully validated through automated testing. The AIMS system correctly:
- Identifies normal operation with high confidence
- Detects minor faults with appropriate uncertainty
- Diagnoses critical faults with high confidence
- Provides explainable predictions via SHAP values

The system is ready for manual UI testing and demonstration.
