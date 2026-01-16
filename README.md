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

---

## System Architecture

The following diagram illustrates the three-tier architecture of AIMS, showing how data flows from the data science layer through the backend API to the frontend dashboard:

```mermaid
flowchart TB
    subgraph DS["Data Science Layer"]
        direction TB
        NB1["01_Data_Exploration_Cleaning.ipynb"]
        NB2["02_Feature_Engineering_Preprocessing.ipynb"]
        NB3["03_Model_Training_Tuning.ipynb"]
        NB4["04_Model_Explainability_Export.ipynb"]
        
        NB1 --> NB2 --> NB3 --> NB4
        
        NB4 --> ART["Serialized Artifacts"]
        ART --> M1["lgbm_model.pkl"]
        ART --> M2["preprocessor.pkl"]
        ART --> M3["shap_explainer.pkl"]
    end
    
    subgraph BE["Backend Layer - FastAPI"]
        direction TB
        API["POST /predict endpoint"]
        VAL["Pydantic Validation"]
        INF["Model Inference"]
        SHAP["SHAP Computation"]
        
        API --> VAL --> INF --> SHAP
    end
    
    subgraph FE["Frontend Layer - React"]
        direction TB
        FORM["SensorInputForm"]
        PRED["PredictionDisplay<br/>(Donut Chart)"]
        EXPL["ExplainabilityDisplay<br/>(SHAP Bar Chart)"]
        RADAR["SystemHealthRadar<br/>(Spider Chart)"]
    end
    
    DS --> |"Model Artifacts"| BE
    BE <--> |"HTTP/JSON"| FE
```

This architecture separates concerns cleanly: notebooks handle offline training and experimentation, the backend serves predictions via REST API, and the frontend provides an intuitive interface for engineers.

---

## ML Pipeline Flow

The machine learning pipeline processes raw sensor data through several stages to produce fault predictions with explanations:

```mermaid
flowchart LR
    subgraph Input["Input"]
        RAW["Raw Sensor Data<br/>(18 features)"]
    end
    
    subgraph Preprocessing["Preprocessing"]
        SCALE["StandardScaler<br/>Normalize features"]
        SMOTE["SMOTE<br/>Balance classes"]
    end
    
    subgraph Training["Training"]
        LGBM["LightGBM<br/>Gradient Boosting"]
        OPTUNA["Optuna<br/>Hyperparameter Tuning"]
    end
    
    subgraph Output["Output"]
        PRED["Fault Prediction<br/>(8 classes)"]
        CONF["Confidence Scores<br/>(Probabilities)"]
        SHAPV["SHAP Values<br/>(Explanations)"]
    end
    
    RAW --> SCALE --> SMOTE --> LGBM
    OPTUNA -.-> |"Optimize"| LGBM
    LGBM --> PRED
    LGBM --> CONF
    LGBM --> SHAPV
```

The pipeline ensures consistent preprocessing between training and inference, with SMOTE addressing class imbalance during training only.


---

## Fault Classification Categories

AIMS classifies engine conditions into 8 distinct categories. The following diagram shows the fault hierarchy and their primary sensor indicators:

```mermaid
mindmap
  root((Engine<br/>Faults))
    Normal
      All sensors nominal
      Baseline operation
    Mechanical
      Bearing Wear
        High vibration X,Y,Z
        Low oil pressure
      Vibration Anomaly
        Extreme single-axis vibration
        Misalignment indicators
    Thermal
      Cooling System Fault
        High oil temp
        High exhaust temps
      Lubrication Oil Degradation
        High oil temp
        Low oil pressure
    Combustion
      Fuel Injection Fault
        Abnormal fuel flow
        Uneven cylinder pressures
      Turbocharger Fault
        Low air pressure
        High exhaust temps
      Air Intake Restriction
        Low air pressure
        Reduced engine load
```

Each fault type has distinct sensor signatures that the model learns to recognize, enabling accurate root cause identification.

---

## Technology Stack

| Layer               | Technology                  | Purpose                         |
| ------------------- | --------------------------- | ------------------------------- |
| **ML Model**        | LightGBM                    | Gradient boosting classifier    |
| **Backend**         | FastAPI (Python)            | REST API for predictions        |
| **Frontend**        | React                       | Interactive dashboard           |
| **Explainability**  | SHAP                        | Feature importance explanations |
| **Charting**        | Recharts                    | Visualization components        |
| **Data Processing** | Pandas, NumPy, Scikit-learn | Data manipulation               |

---

## Data Flow Diagram

This sequence diagram shows how a prediction request flows through the system:

```mermaid
sequenceDiagram
    participant User as Engineer
    participant FE as React Frontend
    participant BE as FastAPI Backend
    participant Model as LightGBM Model
    participant SHAP as SHAP Explainer
    
    User->>FE: Enter sensor readings
    User->>FE: Click "Analyze"
    FE->>BE: POST /predict (18 sensor values)
    BE->>BE: Validate input (Pydantic)
    BE->>BE: Scale features (StandardScaler)
    BE->>Model: Predict fault class
    Model-->>BE: Probabilities (8 classes)
    BE->>SHAP: Compute explanations
    SHAP-->>BE: SHAP values (18 features)
    BE-->>FE: JSON response
    FE->>FE: Render charts
    FE-->>User: Display prediction + explanation
```

The entire prediction cycle completes in under 100ms, enabling real-time diagnostics.

---

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


---

## Usage Workflow

```mermaid
flowchart TD
    START([Start]) --> CHOOSE{Choose Input Method}
    
    CHOOSE --> |"Quick Test"| SCENARIO["Load Demo Scenario"]
    CHOOSE --> |"Custom"| MANUAL["Enter Manual Values"]
    
    SCENARIO --> NORMAL["Normal Operation"]
    SCENARIO --> MINOR["Minor Fault"]
    SCENARIO --> CRITICAL["Critical Fault"]
    
    NORMAL --> ANALYZE
    MINOR --> ANALYZE
    CRITICAL --> ANALYZE
    MANUAL --> ANALYZE
    
    ANALYZE["Click Analyze Button"] --> RESULTS["View Results"]
    
    RESULTS --> DONUT["Donut Chart<br/>Fault Probabilities"]
    RESULTS --> SHAPBAR["SHAP Bar Chart<br/>Feature Contributions"]
    RESULTS --> SPIDER["Spider Chart<br/>System Health Radar"]
    
    DONUT --> INTERPRET["Interpret Results"]
    SHAPBAR --> INTERPRET
    SPIDER --> INTERPRET
    
    INTERPRET --> ACTION{Take Action?}
    ACTION --> |"Yes"| MAINTAIN["Schedule Maintenance"]
    ACTION --> |"No"| MONITOR["Continue Monitoring"]
    
    MAINTAIN --> END([End])
    MONITOR --> START
```

---

## Demo Scenarios

### 1. Normal Operation Scenario
- Click "Load Scenario: Normal Operation"
- Click "Analyze"
- Expected Result:
  - Prediction: "Normal" with >95% confidence
  - SHAP plot shows mostly blue bars (features pushing away from faults)
  - Spider chart shows all values within safe range polygon

### 2. Minor Fault Scenario
- Click "Load Scenario: Minor Fault"
- Click "Analyze"
- Expected Result:
  - Prediction: Split probabilities (e.g., 60% Normal, 35% Lubrication Oil Degradation)
  - SHAP plot highlights Oil_Temp as top red bar (positive contribution)
  - Spider chart shows Oil_Temp outside safe range

### 3. Critical Fault Scenario
- Click "Load Scenario: Critical Fault"
- Click "Analyze"
- Expected Result:
  - Prediction: Critical fault (e.g., "Turbocharger Fault") with >90% confidence
  - SHAP plot highlights Vibration_X and Exhaust_Temp as top red bars
  - Spider chart shows multiple parameters outside safe range (red highlights)

---

## Sensor Inputs

The system accepts 18 sensor readings organized into functional groups:

```mermaid
graph TB
    subgraph Operational["Operational Parameters"]
        S1["Shaft_RPM"]
        S2["Engine_Load"]
        S3["Fuel_Flow"]
    end
    
    subgraph Pressure["Pressure Sensors"]
        S4["Air_Pressure"]
        S5["Oil_Pressure"]
        S6["Cylinder1-4_Pressure"]
    end
    
    subgraph Thermal["Thermal Sensors"]
        S7["Ambient_Temp"]
        S8["Oil_Temp"]
        S9["Cylinder1-4_Exhaust_Temp"]
    end
    
    subgraph Vibration["Vibration Sensors"]
        S10["Vibration_X"]
        S11["Vibration_Y"]
        S12["Vibration_Z"]
    end
    
    Operational --> MODEL["LightGBM Model"]
    Pressure --> MODEL
    Thermal --> MODEL
    Vibration --> MODEL
    
    MODEL --> PREDICTION["Fault Prediction"]
```

---

## Model Performance

```mermaid
pie title Fault Detection Accuracy by Class
    "Normal (97%)" : 97
    "Fuel Injection (88%)" : 88
    "Cooling System (90%)" : 90
    "Turbocharger (89%)" : 89
    "Bearing Wear (92%)" : 92
    "Lubrication (91%)" : 91
    "Air Intake (88%)" : 88
    "Vibration (94%)" : 94
```

Key metrics:
- Overall Accuracy: 94%
- Macro F1-Score: 0.91
- All fault classes achieve F1 > 0.88


---

## Troubleshooting

### Backend Issues

| Problem                           | Solution                              |
| --------------------------------- | ------------------------------------- |
| `ModuleNotFoundError`             | Run `pip install -r requirements.txt` |
| `FileNotFoundError` for artifacts | Run Jupyter notebooks in order        |
| CORS errors                       | Verify CORS middleware in `main.py`   |
| Port 8000 in use                  | Use `--port 8001` flag                |

### Frontend Issues

| Problem               | Solution                                 |
| --------------------- | ---------------------------------------- |
| `npm install` fails   | Clear cache: `npm cache clean --force`   |
| Cannot connect to API | Ensure backend is running on port 8000   |
| Charts not rendering  | Install Recharts: `npm install recharts` |

---

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
├── docs/
│   └── *.md                    # Documentation files
└── README.md
```

---

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

---

## API Documentation

For detailed API documentation, start the backend server and visit:
`http://localhost:8000/docs`

See `backend/README.md` for more details on API endpoints.

---

## Model Training

For information on training the machine learning model, see `notebooks/README.md`.

---

## License

None

---

## Contributors

- Zadock Mosonik Kiprono
- Farid Nahadi Muigu
