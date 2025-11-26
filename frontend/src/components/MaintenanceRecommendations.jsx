import React from 'react';
import './MaintenanceRecommendations.css';

const RECOMMENDATIONS = {
    'Normal': {
        icon: '✓',
        title: 'System Operating Normally',
        priority: 'low',
        actions: [
            'Continue routine maintenance schedule',
            'Monitor sensor readings during operation',
            'Document current operating parameters'
        ]
    },
    'Lubrication Oil Degradation': {
        icon: '🛢️',
        title: 'Oil System Attention Required',
        priority: 'medium',
        actions: [
            'Schedule oil analysis and quality testing',
            'Check oil filter condition and replace if needed',
            'Inspect oil cooler for proper operation',
            'Verify oil pressure meets specifications'
        ]
    },
    'Bearing Wear': {
        icon: '⚠️',
        title: 'Critical: Bearing Inspection Required',
        priority: 'critical',
        actions: [
            'IMMEDIATE: Reduce engine load and schedule inspection',
            'Check bearing clearances and wear patterns',
            'Inspect lubrication system for proper oil delivery',
            'Prepare for potential bearing replacement'
        ]
    },
    'Turbocharger Fault': {
        icon: '⚠️',
        title: 'Critical: Turbocharger System Issue',
        priority: 'critical',
        actions: [
            'IMMEDIATE: Inspect turbocharger for damage',
            'Check exhaust system for restrictions',
            'Verify air intake system integrity',
            'Inspect turbine and compressor wheels for damage'
        ]
    },
    'Vibration Anomaly': {
        icon: '⚠️',
        title: 'Critical: Excessive Vibration Detected',
        priority: 'critical',
        actions: [
            'IMMEDIATE: Reduce speed and inspect engine mounts',
            'Check for loose or damaged components',
            'Verify shaft alignment and balance',
            'Inspect coupling and propeller shaft'
        ]
    },
    'Cooling System Fault': {
        icon: '🌡️',
        title: 'Cooling System Attention Required',
        priority: 'medium',
        actions: [
            'Check coolant level and quality',
            'Inspect heat exchangers for fouling',
            'Verify cooling pump operation',
            'Check thermostat operation'
        ]
    },
    'Fuel Injection Fault': {
        icon: '⛽',
        title: 'Fuel System Attention Required',
        priority: 'medium',
        actions: [
            'Inspect fuel injectors for proper spray pattern',
            'Check fuel filter condition',
            'Verify fuel pressure and flow rate',
            'Test fuel quality for contamination'
        ]
    },
    'Air Intake Restriction': {
        icon: '💨',
        title: 'Air Intake System Attention Required',
        priority: 'medium',
        actions: [
            'Inspect and clean air filters',
            'Check intake ducting for obstructions',
            'Verify turbocharger compressor operation',
            'Inspect intercooler for blockages'
        ]
    }
};

const MaintenanceRecommendations = ({ predictionLabel }) => {
    if (!predictionLabel) {
        return (
            <div className="maintenance-recommendations">
                <div className="recommendations-header">
                    <h3>Maintenance Recommendations</h3>
                </div>
                <div className="no-recommendations">
                    <p>Run analysis to receive maintenance recommendations</p>
                </div>
            </div>
        );
    }

    const recommendation = RECOMMENDATIONS[predictionLabel] || RECOMMENDATIONS['Normal'];

    return (
        <div className={`maintenance-recommendations priority-${recommendation.priority}`}>
            <div className="recommendations-header">
                <span className="recommendation-icon">{recommendation.icon}</span>
                <h3>{recommendation.title}</h3>
            </div>
            <div className="recommendations-content">
                <h4>Recommended Actions:</h4>
                <ul className="action-list">
                    {recommendation.actions.map((action, index) => (
                        <li key={index} className="action-item">
                            <span className="action-bullet">•</span>
                            <span className="action-text">{action}</span>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default MaintenanceRecommendations;
