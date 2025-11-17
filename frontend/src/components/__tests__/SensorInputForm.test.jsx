import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SensorInputForm from '../SensorInputForm';

// Mock axios
jest.mock('axios', () => ({
    post: jest.fn()
}));

// Get the mocked axios
const axios = require('axios');

describe('SensorInputForm', () => {
    const mockOnPredictionReceived = jest.fn();

    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('renders 18 input fields', () => {
        render(<SensorInputForm onPredictionReceived={mockOnPredictionReceived} />);

        // Check for all 18 sensor input fields
        expect(screen.getByLabelText(/Shaft RPM/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Engine Load/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Fuel Flow/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Air Pressure/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Ambient Temperature/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Oil Temperature/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Oil Pressure/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Vibration X/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Vibration Y/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Vibration Z/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Cylinder 1 Pressure/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Cylinder 1 Exhaust Temp/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Cylinder 2 Pressure/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Cylinder 2 Exhaust Temp/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Cylinder 3 Pressure/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Cylinder 3 Exhaust Temp/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Cylinder 4 Pressure/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Cylinder 4 Exhaust Temp/i)).toBeInTheDocument();
    });

    test('preset buttons exist (Normal, Minor, Critical)', () => {
        render(<SensorInputForm onPredictionReceived={mockOnPredictionReceived} />);

        expect(screen.getByText(/Load Scenario: Normal Operation/i)).toBeInTheDocument();
        expect(screen.getByText(/Load Scenario: Minor Fault/i)).toBeInTheDocument();
        expect(screen.getByText(/Load Scenario: Critical Fault/i)).toBeInTheDocument();
    });

    test('loadScenario updates input values for Normal scenario', () => {
        render(<SensorInputForm onPredictionReceived={mockOnPredictionReceived} />);

        const normalButton = screen.getByText(/Load Scenario: Normal Operation/i);
        fireEvent.click(normalButton);

        // Verify some key values from NORMAL_SCENARIO
        expect(screen.getByLabelText(/Shaft RPM/i)).toHaveValue(950);
        expect(screen.getByLabelText(/Engine Load/i)).toHaveValue(70);
        expect(screen.getByLabelText(/Oil Temperature/i)).toHaveValue(75);
        expect(screen.getByLabelText(/Vibration X/i)).toHaveValue(0.05);
    });

    test('loadScenario updates input values for Minor Fault scenario', () => {
        render(<SensorInputForm onPredictionReceived={mockOnPredictionReceived} />);

        const minorButton = screen.getByText(/Load Scenario: Minor Fault/i);
        fireEvent.click(minorButton);

        // Verify Oil_Temp is elevated to 110 (minor fault indicator)
        expect(screen.getByLabelText(/Oil Temperature/i)).toHaveValue(110);
        expect(screen.getByLabelText(/Shaft RPM/i)).toHaveValue(950);
    });

    test('loadScenario updates input values for Critical Fault scenario', () => {
        render(<SensorInputForm onPredictionReceived={mockOnPredictionReceived} />);

        const criticalButton = screen.getByText(/Load Scenario: Critical Fault/i);
        fireEvent.click(criticalButton);

        // Verify critical fault indicators
        expect(screen.getByLabelText(/Vibration X/i)).toHaveValue(0.45);
        expect(screen.getByLabelText(/Vibration Y/i)).toHaveValue(0.35);
        expect(screen.getByLabelText(/Cylinder 1 Exhaust Temp/i)).toHaveValue(550);
    });

    test('handleSubmit calls API with correct payload', async () => {
        const mockResponse = {
            data: {
                prediction_label: 'Normal',
                probabilities: { Normal: 0.95 },
                shap_values: { Shaft_RPM: 0.1 }
            }
        };
        axios.post.mockResolvedValue(mockResponse);

        render(<SensorInputForm onPredictionReceived={mockOnPredictionReceived} />);

        const analyzeButton = screen.getByText(/Analyze/i);
        fireEvent.click(analyzeButton);

        await waitFor(() => {
            expect(axios.post).toHaveBeenCalledWith(
                'http://localhost:8000/predict',
                expect.objectContaining({
                    Shaft_RPM: 950,
                    Engine_Load: 70,
                    Oil_Temp: 75,
                    Vibration_X: 0.05
                })
            );
        });

        expect(mockOnPredictionReceived).toHaveBeenCalledWith(
            mockResponse.data,
            expect.any(Object)
        );
    });

    test('displays error message when API call fails', async () => {
        axios.post.mockRejectedValue({
            response: { data: { detail: 'API Error' } }
        });

        render(<SensorInputForm onPredictionReceived={mockOnPredictionReceived} />);

        const analyzeButton = screen.getByText(/Analyze/i);
        fireEvent.click(analyzeButton);

        await waitFor(() => {
            expect(screen.getByText(/API Error/i)).toBeInTheDocument();
        });
    });
});
