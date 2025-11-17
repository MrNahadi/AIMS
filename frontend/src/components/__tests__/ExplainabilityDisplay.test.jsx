import React from 'react';
import { render, screen } from '@testing-library/react';
import ExplainabilityDisplay from '../ExplainabilityDisplay';

describe('ExplainabilityDisplay', () => {
    const mockShapValues = {
        'Oil_Temp': 0.23,
        'Vibration_X': 0.15,
        'Shaft_RPM': -0.12,
        'Engine_Load': 0.08,
        'Fuel_Flow': -0.05,
        'Oil_Pressure': -0.03,
        'Vibration_Y': 0.02,
        'Cylinder1_Exhaust_Temp': 0.18
    };

    test('renders bar chart with mock SHAP values', () => {
        render(<ExplainabilityDisplay shapValues={mockShapValues} />);

        // Check that the component renders
        expect(screen.getByText(/Feature Importance \(SHAP Values\)/i)).toBeInTheDocument();

        // Check for legend items
        expect(screen.getByText(/Positive \(pushes toward fault\)/i)).toBeInTheDocument();
        expect(screen.getByText(/Negative \(pushes away from fault\)/i)).toBeInTheDocument();
    });

    test('renders chart component', () => {
        const { container } = render(<ExplainabilityDisplay shapValues={mockShapValues} />);

        // Check that the chart container renders
        const chartContainer = container.querySelector('.recharts-responsive-container');
        expect(chartContainer).toBeInTheDocument();
    });

    test('displays interpretation guide', () => {
        render(<ExplainabilityDisplay shapValues={mockShapValues} />);

        expect(screen.getByText(/How to interpret:/i)).toBeInTheDocument();
        expect(screen.getByText(/Features with larger absolute SHAP values/i)).toBeInTheDocument();
    });

    test('displays no data message when no SHAP values provided', () => {
        render(<ExplainabilityDisplay shapValues={null} />);

        expect(screen.getByText(/No SHAP values available/i)).toBeInTheDocument();
    });

    test('displays no data message when empty SHAP values provided', () => {
        render(<ExplainabilityDisplay shapValues={{}} />);

        expect(screen.getByText(/No SHAP values available/i)).toBeInTheDocument();
    });

    test('renders with positive and negative values', () => {
        const { container } = render(<ExplainabilityDisplay shapValues={mockShapValues} />);

        // Check that the chart container renders
        const chartContainer = container.querySelector('.recharts-responsive-container');
        expect(chartContainer).toBeInTheDocument();
    });

    test('handles mixed positive and negative SHAP values', () => {
        const mixedShapValues = {
            'Feature_A': 0.5,
            'Feature_B': -0.3,
            'Feature_C': 0.2,
            'Feature_D': -0.1
        };

        render(<ExplainabilityDisplay shapValues={mixedShapValues} />);

        // Component should render without errors
        expect(screen.getByText(/Feature Importance/i)).toBeInTheDocument();
    });

    test('renders chart with SHAP values', () => {
        const { container } = render(<ExplainabilityDisplay shapValues={mockShapValues} />);

        // Check that the chart container renders
        const chartContainer = container.querySelector('.recharts-responsive-container');
        expect(chartContainer).toBeInTheDocument();
    });
});
