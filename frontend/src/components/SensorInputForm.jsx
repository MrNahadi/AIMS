import React, { useState } from 'react';
import axios from 'axios';
import './SensorInputForm.css';

// Base normal scenario
const BASE_NORMAL = {
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

// Preset scenarios organized by category
const PRESET_SCENARIOS = {
    normal: [
        {
            name: 'Normal - Idle',
            description: 'Low load operation',
            values: { ...BASE_NORMAL, Engine_Load: 45, Shaft_RPM: 850 }
        },
        {
            name: 'Normal - Cruise',
            description: 'Standard operation',
            values: BASE_NORMAL
        },
        {
            name: 'Normal - High Load',
            description: 'Heavy load operation',
            values: { ...BASE_NORMAL, Engine_Load: 95, Shaft_RPM: 1050, Fuel_Flow: 145 }
        }
    ],
    minor: [
        {
            name: 'Oil Degradation',
            description: 'Elevated oil temp & low pressure',
            values: { ...BASE_NORMAL, Oil_Temp: 102, Oil_Pressure: 2.8 }
        },
        {
            name: 'Cooling Issue',
            description: 'Slightly elevated temperatures',
            values: { ...BASE_NORMAL, Oil_Temp: 92, Ambient_Temp: 32, Cylinder1_Exhaust_Temp: 460, Cylinder2_Exhaust_Temp: 460, Cylinder3_Exhaust_Temp: 460, Cylinder4_Exhaust_Temp: 460 }
        },
        {
            name: 'Fuel Injection',
            description: 'Low fuel flow',
            values: { ...BASE_NORMAL, Fuel_Flow: 85, Engine_Load: 75 }
        },
        {
            name: 'Air Intake',
            description: 'Reduced air pressure',
            values: { ...BASE_NORMAL, Air_Pressure: 2.0, Engine_Load: 75 }
        }
    ],
    critical: [
        {
            name: 'Bearing Wear',
            description: 'High vibration levels',
            values: { ...BASE_NORMAL, Vibration_X: 0.45, Vibration_Y: 0.35, Vibration_Z: 0.30 }
        },
        {
            name: 'Turbocharger Fault',
            description: 'Very high exhaust temps',
            values: { ...BASE_NORMAL, Cylinder1_Exhaust_Temp: 550, Cylinder2_Exhaust_Temp: 550, Cylinder3_Exhaust_Temp: 550, Cylinder4_Exhaust_Temp: 550, Air_Pressure: 2.0 }
        },
        {
            name: 'Severe Vibration',
            description: 'Critical vibration anomaly',
            values: { ...BASE_NORMAL, Vibration_X: 0.40, Vibration_Y: 0.38, Vibration_Z: 0.35, Cylinder1_Exhaust_Temp: 480, Cylinder2_Exhaust_Temp: 480, Cylinder3_Exhaust_Temp: 480, Cylinder4_Exhaust_Temp: 480 }
        },
        {
            name: 'Multiple Faults',
            description: 'Combined critical conditions',
            values: { ...BASE_NORMAL, Vibration_X: 0.35, Oil_Temp: 105, Oil_Pressure: 2.3, Cylinder1_Exhaust_Temp: 530, Cylinder2_Exhaust_Temp: 530, Cylinder3_Exhaust_Temp: 530, Cylinder4_Exhaust_Temp: 530 }
        }
    ]
};

const SensorInputForm = ({ onPredictionReceived }) => {
    const [sensorValues, setSensorValues] = useState(BASE_NORMAL);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [currentScenarioIndex, setCurrentScenarioIndex] = useState({ normal: 0, minor: 0, critical: 0 });
    const [currentScenarioName, setCurrentScenarioName] = useState('Normal - Cruise');

    const handleInputChange = (field, value) => {
        setSensorValues(prev => ({
            ...prev,
            [field]: parseFloat(value) || 0
        }));
        setCurrentScenarioName('Custom');
    };

    const loadScenario = (category) => {
        const scenarios = PRESET_SCENARIOS[category];
        const currentIndex = currentScenarioIndex[category];
        const nextIndex = (currentIndex + 1) % scenarios.length;

        const scenario = scenarios[nextIndex];
        setSensorValues(scenario.values);
        setCurrentScenarioName(scenario.name);
        setCurrentScenarioIndex(prev => ({ ...prev, [category]: nextIndex }));
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

            <div className="preset-section">
                <div className="current-scenario">
                    <span className="scenario-label">Current Scenario:</span>
                    <span className="scenario-name">{currentScenarioName}</span>
                </div>

                <div className="preset-buttons">
                    <button
                        type="button"
                        onClick={() => loadScenario('normal')}
                        className="preset-btn normal"
                        title="Click to cycle through normal scenarios"
                    >
                        Normal Operation
                    </button>
                    <button
                        type="button"
                        onClick={() => loadScenario('minor')}
                        className="preset-btn minor"
                        title="Click to cycle through minor fault scenarios"
                    >
                        Minor Fault
                    </button>
                    <button
                        type="button"
                        onClick={() => loadScenario('critical')}
                        className="preset-btn critical"
                        title="Click to cycle through critical fault scenarios"
                    >
                        Critical Fault
                    </button>
                </div>
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
