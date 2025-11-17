import React from 'react';
import { render, screen } from '@testing-library/react';
import PredictionDisplay from '../PredictionDisplay';

describe('PredictionDisplay', () => {
    const mockProbabilities = {
        'Normal': 0.95,
        'Fuel Injection Fault': 0.02,
        'Cooling System Fault': 0.01,
        'Turbocharger Fault': 0.01,
        'Bearing Wear': 0.005,
        'Lubrication Oil Degradation': 0.003,
        'Air Intake Restriction': 0.001,
        'Vibration Anomaly': 0.001
    };

    test('renders donut chart with mock probabilities', () => {
        render(
            <PredictionDisplay
                probabilities={mockProbabilities}
                predictionLabel="Normal"
            />
        );

        // Check that the component renders
        expect(screen.getByText(/Fault Prediction/i)).toBeInTheDocument();

        // Check that the predicted label is displayed
        expect(screen.getByText('Normal')).toBeInTheDocument();
    });

    test('predicted label displays correctly', () => {
        render(
            <PredictionDisplay
                probabilities={mockProbabilities}
                predictionLabel="Normal"
            />
        );

        // Check for the predicted fault label
        expect(screen.getByText(/Predicted Fault:/i)).toBeInTheDocument();
        expect(screen.getByText('Normal')).toBeInTheDocument();
    });

    test('displays confidence percentage', () => {
        render(
            <PredictionDisplay
                probabilities={mockProbabilities}
                predictionLabel="Normal"
            />
        );

        // Check that confidence is displayed (95%)
        expect(screen.getByText(/Confidence: 95.0%/i)).toBeInTheDocument();
    });

    test('highest probability slice is highlighted with high confidence badge', () => {
        render(
            <PredictionDisplay
                probabilities={mockProbabilities}
                predictionLabel="Normal"
            />
        );

        // The label value should have the high-confidence class when > 90%
        const labelValue = screen.getByText('Normal');
        expect(labelValue).toHaveClass('label-value');
        expect(labelValue).toHaveClass('high-confidence');
    });

    test('displays medium confidence for lower probabilities', () => {
        const lowConfidenceProbabilities = {
            'Normal': 0.60,
            'Fuel Injection Fault': 0.35,
            'Cooling System Fault': 0.02,
            'Turbocharger Fault': 0.01,
            'Bearing Wear': 0.01,
            'Lubrication Oil Degradation': 0.005,
            'Air Intake Restriction': 0.003,
            'Vibration Anomaly': 0.002
        };

        render(
            <PredictionDisplay
                probabilities={lowConfidenceProbabilities}
                predictionLabel="Normal"
            />
        );

        const labelValue = screen.getByText('Normal');
        expect(labelValue).toHaveClass('medium-confidence');
    });

    test('displays no data message when no probabilities provided', () => {
        render(<PredictionDisplay probabilities={null} predictionLabel={null} />);

        expect(screen.getByText(/No prediction available/i)).toBeInTheDocument();
    });

    test('renders chart component', () => {
        const { container } = render(
            <PredictionDisplay
                probabilities={mockProbabilities}
                predictionLabel="Normal"
            />
        );

        // Check that the chart container renders
        const chartContainer = container.querySelector('.recharts-responsive-container');
        expect(chartContainer).toBeInTheDocument();
    });
});
