import React, { useState } from 'react';
import axios from 'axios';
import './SensorInputForm.css';

// Preset scenarios
const NORMAL_SCENARIO = {
    Shaft_RPM: 950,
    Engine_Load: 70,
    Fuel_Flow: 120,
    Air_Pressure: 2.5,
    Ambient_Temp: 25,
    Oil_Temp: 75,
    Oil_Pressure: 3.5,
    Vibration_X: 0.05,
    Vibration_Y: 0.05,
    Vibration_Z: 0.05,
    Cylinder1_Pressure: 145,
    Cylinder1_Exhaust_Temp: 420,
    Cylinder2_Pressure: 145,
    Cylinder2_Exhaust_Temp: 420,
    Cylinder3_Pressure: 145,
    Cylinder3_Exhaust_Temp: 420,
    Cylinder4_Pressure: 145,
    Cylinder4_Exhaust_Temp: 420
};

const MINOR_FAULT_SCENARIO = {
    ...NORMAL_SCENARIO,
    Oil_Temp: 110
};

const CRITICAL_FAULT_SCENARIO = {
    ...NORMAL_SCENARIO,
    Vibration_X: 0.45,
    Vibration_Y: 0.35,
    Cylinder1_Exhaust_Temp: 550,
    Cylinder2_Exhaust_Temp: 550,
    Cylinder3_Exhaust_Temp: 550,
    Cylinder4_Exhaust_Temp: 550
};

const SensorInputForm = ({ onPredictionReceived }) => {
    const [sensorValues, setSensorValues] = useState(NORMAL_SCENARIO);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleInputChange = (field, value) => {
        setSensorValues(prev => ({
            ...prev,
            [field]: parseFloat(value) || 0
        }));
    };

    const loadScenario = (scenario) => {
        setSensorValues(scenario);
        setError(null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('http://localhost:8000/predict', sensorValues);
            if (onPredictionReceived) {
                onPredictionReceived(response.data, sensorValues);
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Unable to connect to prediction service. Please try again.');
            console.error('Prediction error:', err);
        } finally {
            setLoading(false);
        }
    };

    const sensorFields = [
        { name: 'Shaft_RPM', label: 'Shaft RPM', unit: 'rpm' },
        { name: 'Engine_Load', label: 'Engine Load', unit: '%' },
        { name: 'Fuel_Flow', label: 'Fuel Flow', unit: 'L/h' },
        { name: 'Air_Pressure', label: 'Air Pressure', unit: 'bar' },
        { name: 'Ambient_Temp', label: 'Ambient Temperature', unit: '°C' },
        { name: 'Oil_Temp', label: 'Oil Temperature', unit: '°C' },
        { name: 'Oil_Pressure', label: 'Oil Pressure', unit: 'bar' },
        { name: 'Vibration_X', label: 'Vibration X', unit: 'mm/s' },
        { name: 'Vibration_Y', label: 'Vibration Y', unit: 'mm/s' },
        { name: 'Vibration_Z', label: 'Vibration Z', unit: 'mm/s' },
        { name: 'Cylinder1_Pressure', label: 'Cylinder 1 Pressure', unit: 'bar' },
        { name: 'Cylinder1_Exhaust_Temp', label: 'Cylinder 1 Exhaust Temp', unit: '°C' },
        { name: 'Cylinder2_Pressure', label: 'Cylinder 2 Pressure', unit: 'bar' },
        { name: 'Cylinder2_Exhaust_Temp', label: 'Cylinder 2 Exhaust Temp', unit: '°C' },
        { name: 'Cylinder3_Pressure', label: 'Cylinder 3 Pressure', unit: 'bar' },
        { name: 'Cylinder3_Exhaust_Temp', label: 'Cylinder 3 Exhaust Temp', unit: '°C' },
        { name: 'Cylinder4_Pressure', label: 'Cylinder 4 Pressure', unit: 'bar' },
        { name: 'Cylinder4_Exhaust_Temp', label: 'Cylinder 4 Exhaust Temp', unit: '°C' }
    ];

    return (
        <div className="sensor-input-form">
            <h2>Sensor Readings</h2>

            <div className="preset-buttons">
                <button
                    type="button"
                    onClick={() => loadScenario(NORMAL_SCENARIO)}
                    className="preset-btn normal"
                >
                    Load Scenario: Normal Operation
                </button>
                <button
                    type="button"
                    onClick={() => loadScenario(MINOR_FAULT_SCENARIO)}
                    className="preset-btn minor"
                >
                    Load Scenario: Minor Fault
                </button>
                <button
                    type="button"
                    onClick={() => loadScenario(CRITICAL_FAULT_SCENARIO)}
                    className="preset-btn critical"
                >
                    Load Scenario: Critical Fault
                </button>
            </div>

            <form onSubmit={handleSubmit}>
                <div className="sensor-inputs">
                    {sensorFields.map(field => (
                        <div key={field.name} className="input-group">
                            <label htmlFor={field.name}>
                                {field.label}
                                <span className="unit">({field.unit})</span>
                            </label>
                            <input
                                type="number"
                                id={field.name}
                                value={sensorValues[field.name]}
                                onChange={(e) => handleInputChange(field.name, e.target.value)}
                                step="any"
                                required
                            />
                        </div>
                    ))}
                </div>

                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}

                <button
                    type="submit"
                    className="analyze-btn"
                    disabled={loading}
                >
                    {loading ? 'Analyzing...' : 'Analyze'}
                </button>
            </form>
        </div>
    );
};

export default SensorInputForm;
