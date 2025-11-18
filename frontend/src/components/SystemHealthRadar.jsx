import React from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import './SystemHealthRadar.css';

// Safe operating ranges for key sensors
const SAFE_RANGES = {
    Shaft_RPM: { min: 850, max: 1100, label: 'RPM' },
    Engine_Load: { min: 40, max: 100, label: 'Load (%)' },
    Oil_Temp: { min: 60, max: 95, label: 'Oil Temp' },
    Oil_Pressure: { min: 2.5, max: 4.5, label: 'Oil Press' },
    Vibration_X: { min: 0, max: 0.1, label: 'Vib X' },
    Vibration_Y: { min: 0, max: 0.1, label: 'Vib Y' },
    Vibration_Z: { min: 0, max: 0.1, label: 'Vib Z' },
    Avg_Exhaust_Temp: { min: 350, max: 500, label: 'Avg Exhaust' }
};

const SystemHealthRadar = ({ sensorValues }) => {
    if (!sensorValues || Object.keys(sensorValues).length === 0) {
        return (
            <div className="system-health-radar">
                <h2>System Health Overview</h2>
                <p className="no-data">No sensor data available. Please analyze sensor data.</p>
            </div>
        );
    }

    // Calculate average exhaust temperature
    const avgExhaustTemp = (
        (sensorValues.Cylinder1_Exhaust_Temp || 0) +
        (sensorValues.Cylinder2_Exhaust_Temp || 0) +
        (sensorValues.Cylinder3_Exhaust_Temp || 0) +
        (sensorValues.Cylinder4_Exhaust_Temp || 0)
    ) / 4;

    // Normalize sensor values to 0-100 scale based on safe ranges
    const normalizeValue = (value, min, max) => {
        const normalized = ((value - min) / (max - min)) * 100;
        return Math.max(0, Math.min(100, normalized));
    };

    // Check if value is out of range
    const isOutOfRange = (value, min, max) => {
        return value < min || value > max;
    };

    // Prepare data for radar chart
    const radarData = [
        {
            parameter: SAFE_RANGES.Shaft_RPM.label,
            current: normalizeValue(sensorValues.Shaft_RPM, SAFE_RANGES.Shaft_RPM.min, SAFE_RANGES.Shaft_RPM.max),
            safe: 100,
            outOfRange: isOutOfRange(sensorValues.Shaft_RPM, SAFE_RANGES.Shaft_RPM.min, SAFE_RANGES.Shaft_RPM.max),
            actualValue: sensorValues.Shaft_RPM
        },
        {
            parameter: SAFE_RANGES.Engine_Load.label,
            current: normalizeValue(sensorValues.Engine_Load, SAFE_RANGES.Engine_Load.min, SAFE_RANGES.Engine_Load.max),
            safe: 100,
            outOfRange: isOutOfRange(sensorValues.Engine_Load, SAFE_RANGES.Engine_Load.min, SAFE_RANGES.Engine_Load.max),
            actualValue: sensorValues.Engine_Load
        },
        {
            parameter: SAFE_RANGES.Oil_Temp.label,
            current: normalizeValue(sensorValues.Oil_Temp, SAFE_RANGES.Oil_Temp.min, SAFE_RANGES.Oil_Temp.max),
            safe: 100,
            outOfRange: isOutOfRange(sensorValues.Oil_Temp, SAFE_RANGES.Oil_Temp.min, SAFE_RANGES.Oil_Temp.max),
            actualValue: sensorValues.Oil_Temp
        },
        {
            parameter: SAFE_RANGES.Oil_Pressure.label,
            current: normalizeValue(sensorValues.Oil_Pressure, SAFE_RANGES.Oil_Pressure.min, SAFE_RANGES.Oil_Pressure.max),
            safe: 100,
            outOfRange: isOutOfRange(sensorValues.Oil_Pressure, SAFE_RANGES.Oil_Pressure.min, SAFE_RANGES.Oil_Pressure.max),
            actualValue: sensorValues.Oil_Pressure
        },
        {
            parameter: SAFE_RANGES.Vibration_X.label,
            current: normalizeValue(sensorValues.Vibration_X, SAFE_RANGES.Vibration_X.min, SAFE_RANGES.Vibration_X.max),
            safe: 100,
            outOfRange: isOutOfRange(sensorValues.Vibration_X, SAFE_RANGES.Vibration_X.min, SAFE_RANGES.Vibration_X.max),
            actualValue: sensorValues.Vibration_X
        },
        {
            parameter: SAFE_RANGES.Vibration_Y.label,
            current: normalizeValue(sensorValues.Vibration_Y, SAFE_RANGES.Vibration_Y.min, SAFE_RANGES.Vibration_Y.max),
            safe: 100,
            outOfRange: isOutOfRange(sensorValues.Vibration_Y, SAFE_RANGES.Vibration_Y.min, SAFE_RANGES.Vibration_Y.max),
            actualValue: sensorValues.Vibration_Y
        },
        {
            parameter: SAFE_RANGES.Vibration_Z.label,
            current: normalizeValue(sensorValues.Vibration_Z, SAFE_RANGES.Vibration_Z.min, SAFE_RANGES.Vibration_Z.max),
            safe: 100,
            outOfRange: isOutOfRange(sensorValues.Vibration_Z, SAFE_RANGES.Vibration_Z.min, SAFE_RANGES.Vibration_Z.max),
            actualValue: sensorValues.Vibration_Z
        },
        {
            parameter: SAFE_RANGES.Avg_Exhaust_Temp.label,
            current: normalizeValue(avgExhaustTemp, SAFE_RANGES.Avg_Exhaust_Temp.min, SAFE_RANGES.Avg_Exhaust_Temp.max),
            safe: 100,
            outOfRange: isOutOfRange(avgExhaustTemp, SAFE_RANGES.Avg_Exhaust_Temp.min, SAFE_RANGES.Avg_Exhaust_Temp.max),
            actualValue: avgExhaustTemp.toFixed(1)
        }
    ];

    const outOfRangeCount = radarData.filter(d => d.outOfRange).length;

    return (
        <div className="system-health-radar">
            <h2>System Health Overview</h2>

            {outOfRangeCount > 0 && (
                <div className="warning-badge">
                    ⚠️ {outOfRangeCount} parameter{outOfRangeCount > 1 ? 's' : ''} out of safe range
                </div>
            )}

            <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={radarData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="parameter" tick={{ fontSize: 12 }} />
                    <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fontSize: 10 }} />
                    <Radar
                        name="Safe Range"
                        dataKey="safe"
                        stroke="#4caf50"
                        fill="#4caf50"
                        fillOpacity={0.2}
                    />
                    <Radar
                        name="Current Values"
                        dataKey="current"
                        stroke="#2196f3"
                        fill="#2196f3"
                        fillOpacity={0.5}
                        dot={{ fill: '#2196f3', r: 4 }}
                    />
                    <Legend />
                    <Tooltip
                        content={({ payload }) => {
                            if (payload && payload.length > 0) {
                                const data = payload[0].payload;
                                return (
                                    <div className="custom-tooltip">
                                        <p className="tooltip-label">{data.parameter}</p>
                                        <p className="tooltip-value">
                                            Value: {data.actualValue}
                                            {data.outOfRange && <span className="out-of-range-badge">OUT OF RANGE</span>}
                                        </p>
                                    </div>
                                );
                            }
                            return null;
                        }}
                    />
                </RadarChart>
            </ResponsiveContainer>

            <div className="parameter-status">
                {radarData.map((item, index) => (
                    <div key={index} className={`status-item ${item.outOfRange ? 'out-of-range' : 'in-range'}`}>
                        <span className="status-dot"></span>
                        <span className="status-label">{item.parameter}: {item.actualValue}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SystemHealthRadar;
