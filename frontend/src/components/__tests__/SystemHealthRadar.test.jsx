import React from 'react';
import { render, screen } from '@testing-library/react';
import SystemHealthRadar from '../SystemHealthRadar';

describe('SystemHealthRadar', () => {
    const mockSensorValues = {
        Shaft_RPM: 950,
        Engine_Load: 70,
        Oil_Temp: 75,
        Oil_Pressure: 3.5,
        Vibration_X: 0.05,
        Vibration_Y: 0.05,
        Vibration_Z: 0.05,
        Cylinder1_Exhaust_Temp: 420,
        Cylinder2_Exhaust_Temp: 420,
        Cylinder3_Exhaust_Temp: 420,
        Cylinder4_Exhaust_Temp: 420
    };

    test('renders radar chart with mock sensor values', () => {
        render(<SystemHealthRadar sensorValues={mockSensorValues} />);

        // Check that the component renders
        expect(screen.getByText(/System Health Overview/i)).toBeInTheDocument();
    });

    test('renders radar chart component', () => {
        const { container } = render(<SystemHealthRadar sensorValues={mockSensorValues} />);

        // Check for radar chart container
        const radarChart = container.querySelector('.recharts-responsive-container');
        expect(radarChart).toBeInTheDocument();
    });

    test('displays parameter status list', () => {
        render(<SystemHealthRadar sensorValues={mockSensorValues} />);

        // Check for parameter status items
        expect(screen.getByText(/RPM:/i)).toBeInTheDocument();
        expect(screen.getByText(/Load \(%\):/i)).toBeInTheDocument();
        expect(screen.getByText(/Oil Temp:/i)).toBeInTheDocument();
        expect(screen.getByText(/Oil Press:/i)).toBeInTheDocument();
    });

    test('out-of-range values highlighted in red', () => {
        const outOfRangeSensorValues = {
            ...mockSensorValues,
            Oil_Temp: 110, // Out of safe range (60-95)
            Vibration_X: 0.45 // Out of safe range (0-0.1)
        };

        render(<SystemHealthRadar sensorValues={outOfRangeSensorValues} />);

        // Check for warning banner
        expect(screen.getByText(/parameter.*out of safe range/i)).toBeInTheDocument();

        // Check for warning icon
        expect(screen.getByText(/⚠️/)).toBeInTheDocument();
    });

    test('displays no warning when all values in range', () => {
        render(<SystemHealthRadar sensorValues={mockSensorValues} />);

        // Should not display warning banner for normal values
        const warningBanner = screen.queryByText(/parameter.*out of safe range/i);
        expect(warningBanner).not.toBeInTheDocument();
    });

    test('displays no data message when no sensor values provided', () => {
        render(<SystemHealthRadar sensorValues={null} />);

        expect(screen.getByText(/No sensor data available/i)).toBeInTheDocument();
    });

    test('displays no data message when empty sensor values provided', () => {
        render(<SystemHealthRadar sensorValues={{}} />);

        expect(screen.getByText(/No sensor data available/i)).toBeInTheDocument();
    });

    test('calculates average exhaust temperature correctly', () => {
        const { container } = render(<SystemHealthRadar sensorValues={mockSensorValues} />);

        // Average exhaust temp should be 420 (all cylinders at 420)
        expect(screen.getByText(/Avg Exhaust: 420/i)).toBeInTheDocument();
    });

    test('displays multiple out-of-range parameters', () => {
        const multipleOutOfRange = {
            ...mockSensorValues,
            Oil_Temp: 110, // Out of range
            Vibration_X: 0.45, // Out of range
            Vibration_Y: 0.35 // Out of range
        };

        render(<SystemHealthRadar sensorValues={multipleOutOfRange} />);

        // Should show count of out-of-range parameters
        expect(screen.getByText(/3 parameters out of safe range/i)).toBeInTheDocument();
    });

    test('renders chart with sensor data', () => {
        const { container } = render(<SystemHealthRadar sensorValues={mockSensorValues} />);

        // Check that the chart container renders
        const chartContainer = container.querySelector('.recharts-responsive-container');
        expect(chartContainer).toBeInTheDocument();
    });
});
