import React from 'react';
import './GlossaryModal.css';

const GlossaryModal = ({ isOpen, onClose }) => {
    if (!isOpen) return null;

    return (
        <div className="glossary-overlay" onClick={onClose}>
            <div className="glossary-modal" onClick={(e) => e.stopPropagation()}>
                <div className="glossary-header">
                    <h2>AIMS Feature Glossary</h2>
                    <button className="close-btn" onClick={onClose} aria-label="Close glossary">
                        ✕
                    </button>
                </div>

                <div className="glossary-content">
                    <div className="glossary-section">
                        <div className="glossary-icon">🎯</div>
                        <h3>Fault Prediction</h3>
                        <p>
                            The AI system analyzes sensor data to predict potential faults in marine engine systems.
                            Each prediction includes a confidence score indicating the model's certainty.
                        </p>
                        <ul>
                            <li><strong>Normal:</strong> All systems operating within safe parameters</li>
                            <li><strong>Fuel Injection Fault:</strong> Issues with fuel delivery system</li>
                            <li><strong>Cooling System Fault:</strong> Temperature regulation problems</li>
                            <li><strong>Turbocharger Fault:</strong> Air compression system issues</li>
                            <li><strong>Bearing Wear:</strong> Mechanical component degradation</li>
                            <li><strong>Lubrication Oil Degradation:</strong> Oil quality issues</li>
                            <li><strong>Air Intake Restriction:</strong> Airflow blockage</li>
                            <li><strong>Vibration Anomaly:</strong> Unusual mechanical vibrations</li>
                        </ul>
                    </div>

                    <div className="glossary-section">
                        <div className="glossary-icon">📊</div>
                        <h3>Explainability (SHAP Values)</h3>
                        <p>
                            SHAP (SHapley Additive exPlanations) values show which sensor readings most influenced
                            the AI's prediction. This helps engineers understand the reasoning behind each diagnosis.
                        </p>
                        <ul>
                            <li><strong>Positive values (red):</strong> Push prediction toward the identified fault</li>
                            <li><strong>Negative values (blue):</strong> Push prediction away from the fault</li>
                            <li><strong>Larger absolute values:</strong> Indicate stronger influence on the prediction</li>
                        </ul>
                    </div>

                    <div className="glossary-section">
                        <div className="glossary-icon">🔍</div>
                        <h3>System Health Monitoring</h3>
                        <p>
                            Real-time comparison of current sensor readings against safe operating ranges.
                            The radar chart visualizes how close each parameter is to its optimal range.
                        </p>
                        <ul>
                            <li><strong>Green area:</strong> Safe operating range for all parameters</li>
                            <li><strong>Blue line:</strong> Current sensor values</li>
                            <li><strong>Out of range indicators:</strong> Parameters exceeding safe limits</li>
                        </ul>
                    </div>

                    <div className="glossary-section">
                        <div className="glossary-icon">⚙️</div>
                        <h3>Sensor Parameters</h3>
                        <p>Key measurements monitored by the system:</p>
                        <ul>
                            <li><strong>Shaft RPM:</strong> Engine rotational speed</li>
                            <li><strong>Engine Load:</strong> Power output percentage</li>
                            <li><strong>Oil Temperature/Pressure:</strong> Lubrication system health</li>
                            <li><strong>Vibration (X/Y/Z):</strong> Mechanical stability indicators</li>
                            <li><strong>Cylinder Pressure/Exhaust Temp:</strong> Combustion efficiency per cylinder</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default GlossaryModal;
