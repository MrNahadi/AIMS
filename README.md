# AIMS - AI Marine Engineering System

An intelligent diagnostic dashboard for marine engine faults that transforms raw sensor data into actionable maintenance intelligence. AIMS uses machine learning to predict specific fault types and provides explainable AI insights to help engineering teams make proactive, data-driven maintenance decisions.

## Overview

AIMS moves beyond simple threshold-based alarms to provide root cause diagnostics with confidence scores and feature importance explanations. The system predicts 8 different fault categories:

- Normal Operation
- Fuel Injection Fault
- Cooling System Fault
- Turbocharger Fault
- Bearing Wear
- Lubrication Oil Degradation
- Air Intake Restriction
- Vibration Anomaly

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Science Layer                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Jupyter Notebooks                                     │ │
│  │  • 01_Data_Exploration_Cleaning.ipynb                  │ │
│  │  • 02_Feature_Engineering_Preprocessing.ipynb          │ │
│  │  • 03_Model_Training_Tuning.ipynb                      │ │
│  │  • 04_Model_Explainability_Export.ipynb                │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Serialized Artifacts                                  │ │
│  │  • lgbm_model.pkl                                      │ │
│  │  • preprocessor.pkl                                    │ │
│  │  • shap_explainer.pkl                                  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                      Backend Layer                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  FastAPI Application                                   │ │
│  │  • POST /predict endpoint                              │ │
│  │  • Pydantic validation models                          │ │
│  │  • Model loading and inference                         │ │
│  │  • SHAP value computation                              │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↑
                      HTTP/JSON
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  React Application                                     │ │
│  │  • SensorInputForm component                           │ │
│  │  • PredictionDisplay component (Donut Chart)           │ │
│  │  • ExplainabilityDisplay component (SHAP Bar Chart)    │ │
│  │  • SystemHealthRadar component (Spider Chart)          │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

- **ML Model**: LightGBM (gradient boosting classifier)
- **Backend**: FastAPI (Python)
- **Frontend**: React
- **Explainability**: SHAP (SHapley Additive exPlanations)
- **Charting**: Recharts
- **Data Processing**: Pandas, NumPy, Scikit-learn

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure model artifacts exist in `backend/artifacts/`:
   - `lgbm_model.pkl`
   - `preprocessor.pkl`
   - `shap_explainer.pkl`

   If artifacts don't exist, run the Jupyter notebooks in order (see `notebooks/README.md`)

4. Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation (Swagger UI) at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will open in your browser at `http://localhost:3000`

## Usage Instructions

### Demo Scenarios

The Engineer's Dashboard includes three preset scenarios to demonstrate the system's capabilities:

#### 1. Normal Operation Scenario
- Click "Load Scenario: Normal Operation"
- Click "Analyze"
- Expected Result:
  - Prediction: "Normal" with >95% confidence
  - SHAP plot shows mostly blue bars (features pushing away from faults)
  - Spider chart shows all values within safe range polygon

#### 2. Minor Fault Scenario
- Click "Load Scenario: Minor Fault"
- Click "Analyze"
- Expected Result:
  - Prediction: Split probabilities (e.g., 60% Normal, 35% Lubrication Oil Degradation)
  - SHAP plot highlights Oil_Temp as top red bar (positive contribution)
  - Spider chart shows Oil_Temp outside safe range

#### 3. Critical Fault Scenario
- Click "Load Scenario: Critical Fault"
- Click "Analyze"
- Expected Result:
  - Prediction: Critical fault (e.g., "Turbocharger Fault") with >90% confidence
  - SHAP plot highlights Vibration_X and Exhaust_Temp as top red bars
  - Spider chart shows multiple parameters outside safe range (red highlights)

### Manual Input

You can also manually enter sensor readings for custom diagnostics:

1. Fill in all 18 sensor fields with values
2. Click "Analyze"
3. View the prediction, confidence scores, SHAP explanations, and health radar

## Sensor Inputs

The system accepts 18 sensor readings:

- Shaft_RPM
- Engine_Load
- Fuel_Flow
- Air_Pressure
- Ambient_Temp
- Oil_Temp
- Oil_Pressure
- Vibration_X, Vibration_Y, Vibration_Z
- Cylinder1_Pressure, Cylinder1_Exhaust_Temp
- Cylinder2_Pressure, Cylinder2_Exhaust_Temp
- Cylinder3_Pressure, Cylinder3_Exhaust_Temp
- Cylinder4_Pressure, Cylinder4_Exhaust_Temp

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError` when starting backend
- Solution: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Problem**: `FileNotFoundError` for model artifacts
- Solution: Run the Jupyter notebooks in order to generate the required .pkl files
- Check that files exist in `backend/artifacts/`

**Problem**: CORS errors in browser console
- Solution: Verify CORS middleware is configured in `backend/main.py` to allow `http://localhost:3000`

**Problem**: Port 8000 already in use
- Solution: Stop other processes using port 8000 or change the port: `uvicorn main:app --port 8001`

### Frontend Issues

**Problem**: `npm install` fails
- Solution: Clear npm cache: `npm cache clean --force` and retry
- Try deleting `node_modules` and `package-lock.json`, then reinstall

**Problem**: "Cannot connect to prediction service" error
- Solution: Ensure backend is running on `http://localhost:8000`
- Check browser console for specific error messages

**Problem**: Charts not rendering
- Solution: Check browser console for errors
- Ensure Recharts is installed: `npm install recharts`

**Problem**: Port 3000 already in use
- Solution: Set a different port: `PORT=3001 npm start` (Linux/Mac) or modify package.json scripts

### Model Performance Issues

**Problem**: Low prediction accuracy
- Solution: Retrain the model with more data or different hyperparameters
- Review notebook 03_Model_Training_Tuning.ipynb for tuning options

**Problem**: SHAP values computation is slow
- Solution: SHAP TreeExplainer is optimized for tree models, but large datasets may be slow
- Consider computing SHAP values on a sample of data

### Data Issues

**Problem**: Missing or corrupted dataset
- Solution: Ensure `data/marine_engine_fault_dataset.csv` exists and is properly formatted
- Check for missing values or incorrect data types in notebook 01

## Project Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models/                 # Pydantic models
│   ├── services/               # Business logic
│   ├── artifacts/              # Trained model files
│   ├── tests/                  # Backend tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   └── App.jsx             # Main application
│   ├── public/
│   └── package.json
├── notebooks/
│   ├── 01_Data_Exploration_Cleaning.ipynb
│   ├── 02_Feature_Engineering_Preprocessing.ipynb
│   ├── 03_Model_Training_Tuning.ipynb
│   └── 04_Model_Explainability_Export.ipynb
├── data/
│   └── marine_engine_fault_dataset.csv
└── README.md
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## API Documentation

For detailed API documentation, start the backend server and visit:
`http://localhost:8000/docs`

See `backend/README.md` for more details on API endpoints.

## Model Training

For information on training the machine learning model, see `notebooks/README.md`.

## License

None

## Contributors

- Zadock Mosonik Kiprono
- Farid Nahadi Muigu
