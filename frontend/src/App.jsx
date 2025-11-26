import React, { useState } from 'react';
import SensorInputForm from './components/SensorInputForm';
import PredictionDisplay from './components/PredictionDisplay';
import SystemHealthRadar from './components/SystemHealthRadar';
import MaintenanceRecommendations from './components/MaintenanceRecommendations';
import GlossaryModal from './components/GlossaryModal';
import ExplainabilityModal from './components/ExplainabilityModal';
import './App.css';

function App() {
    const [predictionLabel, setPredictionLabel] = useState(null);
    const [probabilities, setProbabilities] = useState(null);
    const [shapValues, setShapValues] = useState(null);
    const [sensorValues, setSensorValues] = useState(null);
    const [error, setError] = useState(null);
    const [isGlossaryOpen, setIsGlossaryOpen] = useState(false);
    const [isExplainabilityOpen, setIsExplainabilityOpen] = useState(false);

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
                    <div className="header-title">
                        <h1>AIMS - AI Marine Engineering System</h1>
                        <p>Engineer's Dashboard</p>
                    </div>
                    <button
                        className="info-icon-btn"
                        onClick={() => setIsGlossaryOpen(true)}
                        aria-label="Open glossary"
                        title="View glossary"
                    >
                        <svg
                            width="20"
                            height="20"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        >
                            <circle cx="12" cy="12" r="10"></circle>
                            <line x1="12" y1="16" x2="12" y2="12"></line>
                            <line x1="12" y1="8" x2="12.01" y2="8"></line>
                        </svg>
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
                    <div className="charts-row">
                        <PredictionDisplay
                            probabilities={probabilities}
                            predictionLabel={predictionLabel}
                            onViewDetails={() => setIsExplainabilityOpen(true)}
                            hasShapValues={!!shapValues}
                        />
                        <SystemHealthRadar sensorValues={sensorValues} />
                    </div>
                    <MaintenanceRecommendations predictionLabel={predictionLabel} />
                </div>
            </div>

            <GlossaryModal
                isOpen={isGlossaryOpen}
                onClose={() => setIsGlossaryOpen(false)}
            />

            <ExplainabilityModal
                isOpen={isExplainabilityOpen}
                onClose={() => setIsExplainabilityOpen(false)}
                shapValues={shapValues}
            />
        </div>
    );
}

export default App;
