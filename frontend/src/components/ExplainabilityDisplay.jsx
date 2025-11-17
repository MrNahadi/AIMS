import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, Cell } from 'recharts';
import './ExplainabilityDisplay.css';

const ExplainabilityDisplay = ({ shapValues }) => {
    if (!shapValues || Object.keys(shapValues).length === 0) {
        return (
            <div className="explainability-display">
                <h2>Feature Importance (SHAP Values)</h2>
                <p className="no-data">No SHAP values available. Please analyze sensor data.</p>
            </div>
        );
    }

    // Transform shapValues object into array format
    const chartData = Object.entries(shapValues)
        .map(([feature, value]) => ({
            feature,
            value: parseFloat(value.toFixed(4)),
            absValue: Math.abs(parseFloat(value))
        }))
        // Sort by absolute value (descending) to show most influential features first
        .sort((a, b) => b.absValue - a.absValue);

    // Custom bar color based on positive/negative
    const getBarColor = (value) => {
        return value >= 0 ? '#f44336' : '#2196f3'; // Red for positive, blue for negative
    };

    return (
        <div className="explainability-display">
            <h2>Feature Importance (SHAP Values)</h2>

            <div className="shap-legend">
                <div className="legend-item">
                    <span className="legend-color positive"></span>
                    <span>Positive (pushes toward fault)</span>
                </div>
                <div className="legend-item">
                    <span className="legend-color negative"></span>
                    <span>Negative (pushes away from fault)</span>
                </div>
            </div>

            <ResponsiveContainer width="100%" height={500}>
                <BarChart
                    data={chartData}
                    layout="vertical"
                    margin={{ top: 5, right: 30, left: 150, bottom: 5 }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                        type="number"
                        label={{ value: 'SHAP Value', position: 'insideBottom', offset: -5 }}
                    />
                    <YAxis
                        type="category"
                        dataKey="feature"
                        width={140}
                        tick={{ fontSize: 12 }}
                    />
                    <Tooltip
                        formatter={(value) => value.toFixed(4)}
                        contentStyle={{ borderRadius: '8px', border: '1px solid #ddd' }}
                    />
                    <ReferenceLine x={0} stroke="#000" strokeWidth={2} />
                    <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                        {chartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={getBarColor(entry.value)} />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>

            <div className="shap-explanation">
                <p>
                    <strong>How to interpret:</strong> Features with larger absolute SHAP values have more influence on the prediction.
                    Positive values (red) push the prediction toward the identified fault, while negative values (blue) push away from it.
                </p>
            </div>
        </div>
    );
};

export default ExplainabilityDisplay;
