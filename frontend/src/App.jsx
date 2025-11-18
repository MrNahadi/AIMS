import React, { useState } from 'react';
import SensorInputForm from './components/SensorInputForm';
import PredictionDisplay from './components/PredictionDisplay';
import ExplainabilityDisplay from './components/ExplainabilityDisplay';
import SystemHealthRadar from './components/SystemHealthRadar';
import GlossaryModal from './components/GlossaryModal';
import './App.css';

function App() {
    const [predictionLabel, setPredictionLabel] = useState(null);
    const [probabilities, setProbabilities] = useState(null);
    const [shapValues, setShapValues] = useState(null);
    const [sensorValues, setSensorValues] = useState(null);
    const [error, setError] = useState(null);
    const [isGlossaryOpen, setIsGlossaryOpen] = useState(false);

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

    return (
        <div className="app">
            <header className="app-header">
                <div className="header-content">
                    <div>
                        <h1>AIMS - AI Marine Engineering System</h1>
                        <p>Engineer's Dashboard</p>
                    </div>
                    <button
                        className="glossary-btn"
                        onClick={() => setIsGlossaryOpen(true)}
                        aria-label="Open glossary"
                    >
                        📖 Glossary
                    </button>
                </div>
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
                    <PredictionDisplay
                        probabilities={probabilities}
                        predictionLabel={predictionLabel}
                    />
                    <ExplainabilityDisplay shapValues={shapValues} />
                    <SystemHealthRadar sensorValues={sensorValues} />
                </div>
            </div>

            <GlossaryModal
                isOpen={isGlossaryOpen}
                onClose={() => setIsGlossaryOpen(false)}
            />
        </div>
    );
}

export default App;
