import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
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

const PredictionDisplay = ({ probabilities, predictionLabel }) => {
    if (!probabilities || !predictionLabel) {
        return (
            <div className="prediction-display">
                <h2>Fault Prediction</h2>
                <p className="no-data">No prediction available. Please analyze sensor data.</p>
            </div>
        );
    }

    // Transform probabilities object into array format for Recharts
    const chartData = Object.entries(probabilities).map(([name, value]) => ({
        name,
        value: parseFloat((value * 100).toFixed(2))
    }));

    // Find the maximum probability
    const maxProb = Math.max(...chartData.map(d => d.value));

    // Custom label for center of donut
    const renderCenterLabel = () => {
        return (
            <text
                x="50%"
                y="50%"
                textAnchor="middle"
                dominantBaseline="middle"
                className="donut-center-text"
            >
                <tspan x="50%" dy="-0.5em" fontSize="18" fontWeight="600" fill="#333">
                    {predictionLabel}
                </tspan>
                <tspan x="50%" dy="1.5em" fontSize="24" fontWeight="700" fill="#1e3c72">
                    {maxProb.toFixed(1)}%
                </tspan>
            </text>
        );
    };

    return (
        <div className="prediction-display">
            <h2>Fault Prediction</h2>

            <div className="prediction-content">
                <div className="prediction-label">
                    <span className="label-text">Predicted Fault:</span>
                    <span className={`label-value ${maxProb > 90 ? 'high-confidence' : 'medium-confidence'}`}>
                        {predictionLabel}
                    </span>
                    <span className="confidence-badge">
                        Confidence: {maxProb.toFixed(1)}%
                    </span>
                </div>

                <ResponsiveContainer width="100%" height={350}>
                    <PieChart>
                        <Pie
                            data={chartData}
                            cx="50%"
                            cy="50%"
                            innerRadius={80}
                            outerRadius={120}
                            paddingAngle={2}
                            dataKey="value"
                        >
                            {chartData.map((entry, index) => (
                                <Cell
                                    key={`cell-${index}`}
                                    fill={COLORS[index % COLORS.length]}
                                    stroke={entry.value === maxProb ? '#000' : 'none'}
                                    strokeWidth={entry.value === maxProb ? 3 : 0}
                                />
                            ))}
                        </Pie>
                        <Tooltip
                            formatter={(value) => `${value}%`}
                            contentStyle={{
                                borderRadius: 'var(--radius-md)',
                                border: '1px solid var(--color-border-default)',
                                background: 'var(--color-white)'
                            }}
                        />
                        <Legend
                            verticalAlign="bottom"
                            height={36}
                            formatter={(value, entry) => `${value}: ${entry.payload.value}%`}
                        />
                        {renderCenterLabel()}
                    </PieChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default PredictionDisplay;
