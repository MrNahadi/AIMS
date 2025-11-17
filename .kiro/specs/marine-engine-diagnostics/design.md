# Design Document

## Overview

AIMS (AI Marine engineering system) is a full-stack machine learning application consisting of three primary layers:

1. **Data Science Layer**: Jupyter notebooks for EDA, model training, and explainability analysis
2. **Backend Layer**: FastAPI REST API serving the trained LightGBM model with SHAP explanations
3. **Frontend Layer**: React single-page application providing the Engineer's Dashboard

The system follows a standard ML deployment pattern where offline training produces serialized artifacts (model, preprocessor, explainer) that are loaded by the API server for real-time inference. The frontend communicates with the backend via HTTP requests and renders interactive visualizations using modern charting libraries.

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Science Layer                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Jupyter Notebooks                                      │ │
│  │  • 01_Data_Exploration_Cleaning.ipynb                  │ │
│  │  • 02_Feature_Engineering_Preprocessing.ipynb          │ │
│  │  • 03_Model_Training_Tuning.ipynb                      │ │
│  │  • 04_Model_Explainability_Export.ipynb                │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Serialized Artifacts                                   │ │
│  │  • lgbm_model.pkl                                       │ │
│  │  • preprocessor.pkl                                     │ │
│  │  • shap_explainer.pkl                                   │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                      Backend Layer                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  FastAPI Application                                    │ │
│  │  • POST /predict endpoint                               │ │
│  │  • Pydantic validation models                           │ │
│  │  • Model loading and inference                          │ │
│  │  • SHAP value computation                               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↑
                      HTTP/JSON
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  React Application                                      │ │
│  │  • SensorInputForm component                            │ │
│  │  • PredictionDisplay component (Donut Chart)            │ │
│  │  • ExplainabilityDisplay component (SHAP Bar Chart)     │ │
│  │  • SystemHealthRadar component (Spider Chart)           │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Justification |
|-----------|-----------|---------------|
| ML Model | LightGBM | Faster training, lower memory usage, excellent performance on tabular data |
| Backend | FastAPI | Async architecture, automatic validation, self-documenting API (Swagger) |
| Frontend | React | Component-based architecture, rich ecosystem, excellent for interactive dashboards |
| Explainability | SHAP | Industry standard for model interpretability, supports tree-based models |
| Charting | Recharts / Chart.js | React-compatible, supports donut, bar, and radar charts |
| Data Processing | Pandas, NumPy, Scikit-learn | Standard Python data science stack |
| Serialization | Pickle / Joblib | Standard Python object serialization for model artifacts |

## Components and Interfaces

### 1. Data Science Components

#### 1.1 Data Exploration Module
- **Input**: `marine_engine_fault_dataset.csv` (10,000+ rows, 20 features)
- **Processing**:
  - Load dataset using pandas
  - Profile data: check dtypes, missing values, unique counts
  - Visualize target distribution (Fault_Label: 0-7)
  - Generate histograms and boxplots for sensor features
  - Identify outliers using IQR method
- **Output**: Cleaned dataset, documented insights

#### 1.2 Preprocessing Module
- **Input**: Cleaned dataset
- **Processing**:
  - Split data: 80% train, 20% test (stratified by Fault_Label)
  - Fit StandardScaler on training data
  - Transform both train and test sets
  - Optional: Create interaction features (e.g., temp_x_rpm)
- **Output**: `preprocessor.pkl` (fitted StandardScaler)

#### 1.3 Model Training Module
- **Input**: Preprocessed train/test data
- **Processing**:
  - Initialize LightGBM classifier with multi-class objective
  - Hyperparameter tuning using Optuna or GridSearchCV
    - Key parameters: num_leaves, learning_rate, n_estimators, max_depth
  - Train final model on full training set
  - Evaluate on test set: classification report, confusion matrix
- **Output**: `lgbm_model.pkl` (trained classifier)

#### 1.4 Explainability Module
- **Input**: Trained model, test data
- **Processing**:
  - Initialize `shap.TreeExplainer` with LightGBM model
  - Compute global SHAP values (summary plot)
  - Compute Partial Dependence Plots for top 5 features
  - Document interpretation guidelines
- **Output**: `shap_explainer.pkl` (fitted explainer)

### 2. Backend Components

#### 2.1 FastAPI Application Structure

```
backend/
├── main.py                 # FastAPI app initialization
├── models/
│   ├── request.py          # Pydantic request models
│   └── response.py         # Pydantic response models
├── services/
│   ├── model_loader.py     # Load serialized artifacts
│   └── predictor.py        # Inference and SHAP computation
├── artifacts/
│   ├── lgbm_model.pkl
│   ├── preprocessor.pkl
│   └── shap_explainer.pkl
└── requirements.txt
```

#### 2.2 API Endpoint Design

**POST /predict**

Request Schema (Pydantic):
```python
class SensorInput(BaseModel):
    Shaft_RPM: float
    Engine_Load: float
    Fuel_Flow: float
    Air_Pressure: float
    Ambient_Temp: float
    Oil_Temp: float
    Oil_Pressure: float
    Vibration_X: float
    Vibration_Y: float
    Vibration_Z: float
    Cylinder1_Pressure: float
    Cylinder1_Exhaust_Temp: float
    Cylinder2_Pressure: float
    Cylinder2_Exhaust_Temp: float
    Cylinder3_Pressure: float
    Cylinder3_Exhaust_Temp: float
    Cylinder4_Pressure: float
    Cylinder4_Exhaust_Temp: float
```

Response Schema (Pydantic):
```python
class PredictionResponse(BaseModel):
    prediction_label: str  # e.g., "Normal", "Turbocharger Failure"
    probabilities: Dict[str, float]  # All 8 class probabilities
    shap_values: Dict[str, float]  # Feature name -> SHAP value
```

#### 2.3 Inference Pipeline

1. **Validation**: Pydantic validates incoming JSON against SensorInput schema
2. **Preprocessing**: Load preprocessor.pkl, transform input to numpy array
3. **Prediction**: Load lgbm_model.pkl, call predict() and predict_proba()
4. **Explanation**: Load shap_explainer.pkl, compute SHAP values for input
5. **Response**: Map numeric label to human-readable string, format JSON response

### 3. Frontend Components

#### 3.1 Component Hierarchy

```
App
├── SensorInputForm
│   ├── InputField (x18 sensor inputs)
│   ├── PresetButton (Normal, Minor, Critical)
│   └── AnalyzeButton
├── PredictionDisplay
│   ├── DonutChart (Recharts PieChart)
│   └── PredictionLabel
├── ExplainabilityDisplay
│   └── ShapBarChart (Recharts BarChart)
└── SystemHealthRadar
    └── RadarChart (Recharts RadarChart)
```

#### 3.2 Component Specifications

**SensorInputForm**
- State: 18 sensor values (controlled inputs)
- Methods:
  - `handleInputChange(field, value)`: Update sensor state
  - `loadScenario(scenarioType)`: Load preset values
  - `handleSubmit()`: POST to /predict, update parent state
- Presets:
  - Normal: RPM=950, Load=70, Oil_Temp=75, Vibration_X=0.05, etc.
  - Minor: RPM=950, Load=70, Oil_Temp=110, Vibration_X=0.05, etc.
  - Critical: RPM=950, Load=70, Oil_Temp=75, Vibration_X=0.45, Exhaust_Temp=550, etc.

**PredictionDisplay**
- Props: `probabilities` (object), `predictionLabel` (string)
- Rendering:
  - Donut chart with 8 slices (one per fault type)
  - Highlight slice with max probability
  - Center text: predicted label + confidence %

**ExplainabilityDisplay**
- Props: `shapValues` (object)
- Rendering:
  - Horizontal bar chart, sorted by absolute SHAP value
  - Positive values: red bars (right)
  - Negative values: blue bars (left)
  - Y-axis: feature names, X-axis: SHAP value

**SystemHealthRadar**
- Props: `sensorValues` (object)
- Rendering:
  - Radar chart with 8-10 key sensors
  - Overlay safe range polygon (static)
  - Highlight out-of-range values in red

## Data Models

### Fault Label Mapping

Based on the dataset, the Fault_Label column contains numeric codes 0-7:

```python
FAULT_LABELS = {
    0: "Normal",
    1: "Fuel Injection Fault",
    2: "Cooling System Fault",
    3: "Turbocharger Fault",
    4: "Bearing Wear",
    5: "Lubrication Oil Degradation",
    6: "Air Intake Restriction",
    7: "Vibration Anomaly"
}
```

### Sensor Feature List

The dataset contains 18 sensor features (excluding Timestamp and Fault_Label):
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

### Safe Operating Ranges (for Spider Chart)

```python
SAFE_RANGES = {
    "Shaft_RPM": (850, 1100),
    "Engine_Load": (40, 100),
    "Oil_Temp": (60, 95),
    "Oil_Pressure": (2.5, 4.5),
    "Vibration_X": (0, 0.1),
    "Vibration_Y": (0, 0.1),
    "Vibration_Z": (0, 0.1),
    "Cylinder1_Exhaust_Temp": (350, 500),
    "Cylinder2_Exhaust_Temp": (350, 500),
    "Cylinder3_Exhaust_Temp": (350, 500),
    "Cylinder4_Exhaust_Temp": (350, 500)
}
```

## Error Handling

### Backend Error Scenarios

1. **Invalid Input Data**
   - Trigger: Missing fields, wrong data types, out-of-range values
   - Response: HTTP 422 Unprocessable Entity with Pydantic validation errors
   - Example: `{"detail": [{"loc": ["body", "Shaft_RPM"], "msg": "field required"}]}`

2. **Model Loading Failure**
   - Trigger: Missing .pkl files, corrupted artifacts
   - Response: HTTP 500 Internal Server Error
   - Logging: Log full traceback to server console
   - Mitigation: Validate artifact existence on startup

3. **Prediction Failure**
   - Trigger: Unexpected model error during inference
   - Response: HTTP 500 Internal Server Error
   - Logging: Log input data and error details
   - Mitigation: Add try-except around model.predict()

### Frontend Error Scenarios

1. **API Request Failure**
   - Trigger: Network error, backend unavailable
   - Handling: Display error toast notification
   - Message: "Unable to connect to prediction service. Please try again."

2. **Invalid API Response**
   - Trigger: Malformed JSON, missing fields
   - Handling: Display error message, log to console
   - Message: "Received invalid response from server."

3. **Empty/Invalid Input**
   - Trigger: User submits form with missing values
   - Handling: Client-side validation, highlight missing fields
   - Message: "Please fill in all sensor readings."

## Testing Strategy

### Data Science Testing

1. **Data Quality Tests**
   - Verify no missing values after cleaning
   - Verify all features are numeric
   - Verify target labels are in range [0, 7]

2. **Model Performance Tests**
   - Assert F1-score > 0.90 on test set
   - Assert no class has F1-score < 0.80
   - Verify confusion matrix diagonal dominance

3. **Explainability Tests**
   - Verify SHAP values sum to (prediction - base_value)
   - Verify SHAP explainer works on sample inputs
   - Verify PDP plots generate without errors

### Backend Testing

1. **Unit Tests** (pytest)
   - Test Pydantic model validation (valid/invalid inputs)
   - Test preprocessor transformation (mock data)
   - Test prediction logic (mock model)
   - Test SHAP computation (mock explainer)

2. **Integration Tests**
   - Test /predict endpoint with valid payload
   - Test /predict endpoint with invalid payload (422 response)
   - Test response schema matches PredictionResponse
   - Test with actual model artifacts (smoke test)

3. **Load Tests** (optional)
   - Use Locust or Apache Bench to test concurrent requests
   - Target: 100 requests/second with <500ms latency

### Frontend Testing

1. **Component Tests** (Jest + React Testing Library)
   - Test SensorInputForm renders all 18 inputs
   - Test preset buttons load correct values
   - Test form submission calls API with correct payload
   - Test PredictionDisplay renders donut chart
   - Test ExplainabilityDisplay renders bar chart
   - Test SystemHealthRadar renders radar chart

2. **Integration Tests**
   - Test full user flow: load scenario → analyze → view results
   - Mock API responses for predictable testing

3. **Manual Testing**
   - Test all three demo scenarios (Normal, Minor, Critical)
   - Verify visualizations render correctly
   - Verify responsive design on different screen sizes

### End-to-End Testing

1. **Scenario Tests**
   - Start backend server
   - Start frontend dev server
   - Load Normal scenario → verify prediction = "Normal"
   - Load Minor scenario → verify split probabilities
   - Load Critical scenario → verify high confidence for critical fault

## Deployment Considerations

### Local Development Setup

1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm start  # Runs on port 3000
   ```

3. **CORS Configuration**: FastAPI must allow requests from http://localhost:3000

### Production Considerations (Out of Scope for v1.0)

- Containerization: Docker for backend and frontend
- Reverse proxy: Nginx to serve frontend and proxy API requests
- Model versioning: Track model artifacts with DVC or MLflow
- Monitoring: Log prediction latency, error rates, feature drift
- Security: Add API authentication (JWT tokens)

## Design Decisions and Rationales

### 1. Why LightGBM over XGBoost?
- **Decision**: Use LightGBM for the classifier
- **Rationale**: LightGBM offers 2-3x faster training on large datasets, lower memory footprint, and comparable accuracy. For a demo system, training speed is valuable for iteration.

### 2. Why FastAPI over Flask?
- **Decision**: Use FastAPI for the backend
- **Rationale**: FastAPI provides automatic request validation (Pydantic), async support for better concurrency, and auto-generated API documentation (Swagger UI). This reduces boilerplate and improves developer experience.

### 3. Why SHAP over LIME?
- **Decision**: Use SHAP for explainability
- **Rationale**: SHAP has strong theoretical foundations (Shapley values), native support for tree-based models (TreeExplainer is fast), and produces both global and local explanations. LIME is model-agnostic but slower and less consistent.

### 4. Why Recharts for visualization?
- **Decision**: Use Recharts for React charts
- **Rationale**: Recharts is React-native (no D3 wrapper), has excellent documentation, supports all required chart types (donut, bar, radar), and has a clean API.

### 5. Why serialize with Pickle?
- **Decision**: Use pickle/joblib for model artifacts
- **Rationale**: Standard Python serialization, works seamlessly with scikit-learn and LightGBM, simple to implement. For production, consider ONNX or TorchScript for cross-platform compatibility.

### 6. Why single-page application?
- **Decision**: Build React as SPA (no routing)
- **Rationale**: The Engineer's Dashboard is a single view with multiple components. No need for routing complexity. Keeps the demo focused and simple.

### 7. Why preset scenarios?
- **Decision**: Hardcode three demo scenarios
- **Rationale**: Ensures consistent, impressive demo experience. Manually tuning sensor values to trigger specific predictions is time-consuming during live presentations.

## Future Enhancements (Out of Scope)

1. **Time-Series Integration**: Store predictions in InfluxDB, visualize trends over time
2. **Remaining Useful Life (RUL)**: Evolve from classification to regression (predict hours until failure)
3. **Real-Time Streaming**: Integrate with MQTT or Kafka for live sensor data
4. **Multi-Engine Dashboard**: Support monitoring multiple engines simultaneously
5. **Alert System**: Email/SMS notifications when critical faults are detected
6. **Model Retraining Pipeline**: Automated retraining with new data
7. **A/B Testing**: Compare multiple model versions in production
