import React from 'react';
import './ExplainabilityDisplay.css';

const ExplainabilityDisplay = ({ shapValues }) => {
    // React hooks must be called before any early returns
    const [tooltip, setTooltip] = React.useState({ visible: false, feature: '', value: 0, x: 0, y: 0 });

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
        .sort((a, b) => b.absValue - a.absValue)
        // Limit to top 8 features
        .slice(0, 8);

    // Find max absolute value for scaling
    const maxAbsValue = Math.max(...chartData.map(d => d.absValue));

    // Render custom tooltip with design system styling
    const renderTooltip = () => {
        if (!tooltip.visible) return null;
        return (
            <div
                className="shap-tooltip"
                style={{
                    position: 'fixed',
                    left: `${tooltip.x}px`,
                    top: `${tooltip.y}px`,
                    transform: 'translate(-50%, -120%)',
                    pointerEvents: 'none',
                    zIndex: 1000
                }}
            >
                <p className="tooltip-feature">{tooltip.feature}</p>
                <p className="tooltip-value">SHAP Value: {tooltip.value.toFixed(4)}</p>
            </div>
        );
    };

    const handleMouseEnter = (entry, event) => {
        setTooltip({
            visible: true,
            feature: entry.feature,
            value: entry.value,
            x: event.clientX,
            y: event.clientY
        });
    };

    const handleMouseLeave = () => {
        setTooltip({ visible: false, feature: '', value: 0, x: 0, y: 0 });
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

            <div className="shap-chart-container">
                <div className="shap-bars">
                    {chartData.map((entry, index) => {
                        const widthPercent = (entry.absValue / maxAbsValue) * 50; // 50% max for diverging chart
                        const isPositive = entry.value >= 0;

                        return (
                            <div key={index} className="bar-row">
                                <div className="bar-wrapper-diverging">
                                    {/* Left side - negative values */}
                                    <div className="bar-side left">
                                        {!isPositive && (
                                            <div
                                                className="bar negative"
                                                style={{ width: `${widthPercent}%` }}
                                                onMouseEnter={(e) => handleMouseEnter(entry, e)}
                                                onMouseMove={(e) => setTooltip(prev => ({ ...prev, x: e.clientX, y: e.clientY }))}
                                                onMouseLeave={handleMouseLeave}
                                            >
                                                <div className="bar-fill"></div>
                                            </div>
                                        )}
                                    </div>
                                    {/* Center line */}
                                    <div className="center-line"></div>
                                    {/* Right side - positive values */}
                                    <div className="bar-side right">
                                        {isPositive && (
                                            <div
                                                className="bar positive"
                                                style={{ width: `${widthPercent}%` }}
                                                onMouseEnter={(e) => handleMouseEnter(entry, e)}
                                                onMouseMove={(e) => setTooltip(prev => ({ ...prev, x: e.clientX, y: e.clientY }))}
                                                onMouseLeave={handleMouseLeave}
                                            >
                                                <div className="bar-fill"></div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>

            {renderTooltip()}

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
