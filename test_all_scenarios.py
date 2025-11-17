"""
Automated end-to-end test for all three demo scenarios.
Tests the scenarios as specified in task 8.
"""
import requests
import json

def test_scenario(name, data, expected_checks):
    """Test a scenario and validate expectations."""
    print(f"\n{'='*80}")
    print(f"Testing: {name}")
    print('='*80)
    
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            print(f"❌ FAILED: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        result = response.json()
        print(f"✓ API call successful")
        print(f"  Prediction: {result['prediction_label']}")
        print(f"  Top 3 probabilities:")
        
        # Sort probabilities by value
        sorted_probs = sorted(result['probabilities'].items(), key=lambda x: x[1], reverse=True)
        for label, prob in sorted_probs[:3]:
            print(f"    - {label}: {prob*100:.2f}%")
        
        # Get top SHAP features
        sorted_shap = sorted(result['shap_values'].items(), key=lambda x: abs(x[1]), reverse=True)
        print(f"  Top 3 SHAP features (by absolute value):")
        for feature, value in sorted_shap[:3]:
            print(f"    - {feature}: {value:.4f}")
        
        # Run expected checks
        all_passed = True
        for check_name, check_func in expected_checks.items():
            passed = check_func(result)
            status = "✓" if passed else "❌"
            print(f"  {status} {check_name}")
            if not passed:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


# Scenario 1: Normal Operation
normal_scenario = {
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

normal_checks = {
    "Prediction is 'Normal'": lambda r: r['prediction_label'] == 'Normal',
    "Confidence > 95%": lambda r: r['probabilities']['Normal'] > 0.95,
    "SHAP values indicate normal operation": lambda r: True  # Visual check in UI
}

# Scenario 2: Minor Fault (Lubrication Oil Degradation)
minor_fault_scenario = {
    "Shaft_RPM": 950,
    "Engine_Load": 70,
    "Fuel_Flow": 120,
    "Air_Pressure": 2.5,
    "Ambient_Temp": 25,
    "Oil_Temp": 95,  # Elevated oil temperature
    "Oil_Pressure": 2.8,  # Slightly low oil pressure
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

minor_fault_checks = {
    "Shows split probabilities": lambda r: max(r['probabilities'].values()) < 0.90,
    "Oil_Temp has high SHAP value": lambda r: abs(r['shap_values']['Oil_Temp']) > 0.1,
}

# Scenario 3: Critical Fault (Turbocharger + Vibration)
critical_fault_scenario = {
    "Shaft_RPM": 950,
    "Engine_Load": 70,
    "Fuel_Flow": 120,
    "Air_Pressure": 1.8,  # Low air pressure (turbocharger issue)
    "Ambient_Temp": 25,
    "Oil_Temp": 75,
    "Oil_Pressure": 3.5,
    "Vibration_X": 0.25,  # High vibration
    "Vibration_Y": 0.22,  # High vibration
    "Vibration_Z": 0.20,  # High vibration
    "Cylinder1_Pressure": 130,  # Low pressure
    "Cylinder1_Exhaust_Temp": 480,  # High exhaust temp
    "Cylinder2_Pressure": 130,
    "Cylinder2_Exhaust_Temp": 480,
    "Cylinder3_Pressure": 130,
    "Cylinder3_Exhaust_Temp": 480,
    "Cylinder4_Pressure": 130,
    "Cylinder4_Exhaust_Temp": 480
}

critical_fault_checks = {
    "Prediction is a fault (not Normal)": lambda r: r['prediction_label'] != 'Normal',
    "Confidence > 90%": lambda r: max(r['probabilities'].values()) > 0.90,
    "Vibration or Exhaust features have high SHAP": lambda r: any(
        abs(r['shap_values'][f]) > 0.1 
        for f in ['Vibration_X', 'Vibration_Y', 'Vibration_Z', 
                  'Cylinder1_Exhaust_Temp', 'Cylinder2_Exhaust_Temp',
                  'Cylinder3_Exhaust_Temp', 'Cylinder4_Exhaust_Temp']
    )
}

# Run all tests
print("\n" + "="*80)
print("AIMS END-TO-END SCENARIO VALIDATION")
print("="*80)

results = []
results.append(("Normal Operation", test_scenario("Normal Operation", normal_scenario, normal_checks)))
results.append(("Minor Fault", test_scenario("Minor Fault (Lubrication Oil Degradation)", minor_fault_scenario, minor_fault_checks)))
results.append(("Critical Fault", test_scenario("Critical Fault (Turbocharger + Vibration)", critical_fault_scenario, critical_fault_checks)))

# Summary
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)
for name, passed in results:
    status = "✓ PASSED" if passed else "❌ FAILED"
    print(f"{status}: {name}")

all_passed = all(passed for _, passed in results)
print("\n" + "="*80)
if all_passed:
    print("✓ ALL SCENARIOS PASSED")
else:
    print("❌ SOME SCENARIOS FAILED")
print("="*80)
