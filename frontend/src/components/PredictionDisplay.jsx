import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import './PredictionDisplay.css';

const COLORS = [
    '#4caf50', // Normal - green
    '#ff9800', // Fuel Injection Fault - orange
    '#2196f3', // Cooling System Fault - blue
    '#f44336', // Turbocharger Fault - red
    '#9c27b0', // Bearing Wear - purple
    '#ff5722', // Lubrication Oil Degradation - deep orange
    '#795548', // Air Intake Restriction - brown
    '#e91e63'  // Vibration Anomaly - pink
];

const PredictionDisplay = ({ probabilities, predictionLabel, onViewDetails, hasShapValues }) => {
    if (!probabilities || !predictionLabel) {
        return (
            <div className="prediction-display">
                <div className="status-section no-prediction">
                    <div className="status-icon">⏳</div>
                    <div className="status-message">No prediction available</div>
                    <p className="status-detail">Please analyze sensor data to detect faults</p>
                </div>
            </div>
        );
    }

    // Transform probabilities object into array format
    const chartData = Object.entries(probabilities).map(([name, value]) => ({
        name,
        value: parseFloat((value * 100).toFixed(2))
    }));

    // Find the maximum probability
    const maxProb = Math.max(...chartData.map(d => d.value));

    // Define which fault types are critical based on severity
    const criticalFaults = [
        'Bearing Wear',
        'Turbocharger Fault',
        'Vibration Anomaly'
    ];

    const isCritical = criticalFaults.includes(predictionLabel) || (maxProb >= 98 && predictionLabel !== 'Normal');
    const isNormal = predictionLabel === 'Normal';

    // Sort data for bar labels (top 5)
    const sortedData = [...chartData].sort((a, b) => b.value - a.value).slice(0, 5);

    return (
        <div className={`prediction-display ${isCritical ? 'critical' : ''} ${isNormal ? 'normal' : ''}`}>
            <div className="status-section">
                {isCritical && (
                    <>
                        <div className="alert-icon">⚠️</div>
                        <h2 className="alert-title">CRITICAL FAULT DETECTED</h2>
                    </>
                )}
                {isNormal && (
                    <>
                        <div className="success-icon">✓</div>
                        <h2 className="success-title">SYSTEM NORMAL</h2>
                    </>
                )}
                {!isCritical && !isNormal && (
                    <>
                        <div className="warning-icon">⚠️</div>
                        <h2 className="warning-title">FAULT DETECTED</h2>
                    </>
                )}

                <div className="fault-label">{predictionLabel}</div>
                <div className="confidence-display">
                    Confidence: <strong>{maxProb.toFixed(1)}%</strong>
                </div>
            </div>

            <div className="chart-section">
                <div className="chart-container">
                    <ResponsiveContainer width="100%" height={200}>
                        <PieChart>
                            <Pie
                                data={chartData}
                                cx="50%"
                                cy="50%"
                                innerRadius={60}
                                outerRadius={85}
                                paddingAngle={2}
                                dataKey="value"
                            >
                                {chartData.map((entry, index) => (
                                    <Cell
                                        key={`cell-${index}`}
                                        fill={COLORS[index % COLORS.length]}
                                        stroke="none"
                                    />
                                ))}
                            </Pie>
                            <Tooltip
                                formatter={(value) => `${value}%`}
                                contentStyle={{
                                    background: '#FFFFFF',
                                    borderRadius: '8px',
                                    border: '1px solid #E2E8F0',
                                    boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.05)'
                                }}
                            />
                        </PieChart>
                    </ResponsiveContainer>
                </div>

                <div className="bar-labels">
                    {sortedData.map((entry, index) => (
                        <div key={index} className="bar-label-row">
                            <div className="bar-label-left">
                                <span
                                    className="bar-label-color"
                                    style={{ backgroundColor: COLORS[chartData.findIndex(d => d.name === entry.name)] }}
                                ></span>
                                <span className="bar-label-name">{entry.name}</span>
                            </div>
                            <span className="bar-label-value">{entry.value.toFixed(1)}%</span>
                        </div>
                    ))}
                </div>
            </div>

            {hasShapValues && (
                <button className="view-details-btn" onClick={onViewDetails}>
                    View Feature Importance
                </button>
            )}
        </div>
    );
};

export default PredictionDisplay;
