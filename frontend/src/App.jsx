import React, { useState } from 'react';
import SensorInputForm from './components/SensorInputForm';
import PredictionDisplay from './components/PredictionDisplay';
import ExplainabilityDisplay from './components/ExplainabilityDisplay';
import SystemHealthRadar from './components/SystemHealthRadar';
import './App.css';

function App() {
    const [predictionLabel, setPredictionLabel] = useState(null);
    const [probabilities, setProbabilities] = useState(null);
    const [shapValues, setShapValues] = useState(null);
    const [sensorValues, setSensorValues] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handlePredictionReceived = (predictionData, inputSensorValues) => {
        try {
            setPredictionLabel(predictionData.prediction_label);
            setProbabilities(predictionData.probabilities);
            setShapValues(predictionData.shap_values);
            setSensorValues(inputSensorValues);
            setError(null);
        } catch (err) {
            setError('Failed to process prediction response');
            console.error('Error processing prediction:', err);
        }
    };

    const hasPrediction = predictionLabel && probabilities && shapValues && sensorValues;

    return (
        <div className="app">
            <header className="app-header">
                <h1>AIMS - AI Marine Engineering System</h1>
                <p>Engineer's Dashboard</p>
            </header>

            {error && (
                <div className="app-error">
                    <span className="error-icon">❌</span>
                    <span>{error}</span>
                </div>
            )}

            <div className="app-container">
                <div className="app-left">
                    <SensorInputForm onPredictionReceived={handlePredictionReceived} />
                </div>

                <div className="app-right">
                    {loading && (
                        <div className="loading-overlay">
                            <div className="loading-spinner"></div>
                            <p>Analyzing sensor data...</p>
                        </div>
                    )}

                    {!hasPrediction && !loading && (
                        <div className="welcome-message">
                            <h2>Welcome to AIMS</h2>
                            <p>Load a preset scenario or enter sensor values manually, then click "Analyze" to get started.</p>
                            <div className="features-list">
                                <div className="feature-item">
                                    <span className="feature-icon">🎯</span>
                                    <div>
                                        <strong>Fault Prediction</strong>
                                        <p>AI-powered diagnosis with confidence scores</p>
                                    </div>
                                </div>
                                <div className="feature-item">
                                    <span className="feature-icon">📊</span>
                                    <div>
                                        <strong>Explainability</strong>
                                        <p>Understand which sensors drive each prediction</p>
                                    </div>
                                </div>
                                <div className="feature-item">
                                    <span className="feature-icon">🔍</span>
                                    <div>
                                        <strong>Health Monitoring</strong>
                                        <p>Real-time comparison against safe operating ranges</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {hasPrediction && (
                        <>
                            <PredictionDisplay
                                probabilities={probabilities}
                                predictionLabel={predictionLabel}
                            />
                            <ExplainabilityDisplay shapValues={shapValues} />
                            <SystemHealthRadar sensorValues={sensorValues} />
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}

export default App;
