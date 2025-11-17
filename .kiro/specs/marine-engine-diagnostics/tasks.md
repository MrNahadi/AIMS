# Implementation Plan

- [x] 1. Set up project structure and dependencies





  - Create directory structure: `notebooks/`, `backend/`, `frontend/`, `backend/artifacts/`
  - Create `backend/requirements.txt` with dependencies: fastapi, uvicorn, pydantic, lightgbm, shap, scikit-learn, pandas, numpy, joblib
  - Create `frontend/package.json` with dependencies: react, recharts, axios
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [x] 2. Implement data exploration and cleaning notebook






  - [x] 2.1 Create `notebooks/01_Data_Exploration_Cleaning.ipynb`


    - Load `data/marine_engine_fault_dataset.csv` using pandas
    - Profile dataset: check dtypes, missing values, unique counts for all columns
    - Visualize Fault_Label distribution with bar chart to check class balance
    - Generate histograms for all 18 sensor features
    - Generate boxplots to identify outliers
    - Document cleaning decisions in markdown cells
    - _Requirements: 2.1, 2.2, 2.3_

- [x] 3. Implement preprocessing and feature engineering notebook




  - [x] 3.1 Create `notebooks/02_Feature_Engineering_Preprocessing.ipynb`


    - Load cleaned dataset from previous notebook
    - Separate features (18 sensor columns) from target (Fault_Label)
    - Split data: 80% train, 20% test using stratified split on Fault_Label
    - Initialize StandardScaler and fit on training features only
    - Transform both train and test features
    - Save fitted StandardScaler to `backend/artifacts/preprocessor.pkl` using joblib
    - _Requirements: 2.4, 2.5_

- [x] 4. Implement model training and evaluation notebook








  - [x] 4.1 Create `notebooks/03_Model_Training_Tuning.ipynb`


    - Load preprocessed train/test data from previous notebook
    - Initialize LightGBM classifier with objective='multiclass', num_class=8
    - Perform hyperparameter tuning using Optuna with 50 trials
    - Tune parameters: num_leaves (20-100), learning_rate (0.01-0.3), n_estimators (100-500), max_depth (3-10)
    - Train final model with best hyperparameters on full training set
    - Generate predictions on test set
    - Calculate and display classification report (precision, recall, F1-score per class)
    - Generate confusion matrix heatmap using seaborn
    - Verify F1-score (macro-average) > 0.90
    - Save trained model to `backend/artifacts/lgbm_model.pkl` using joblib
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 5. Implement explainability analysis notebook






  - [x] 5.1 Create `notebooks/04_Model_Explainability_Export.ipynb`

    - Load trained model and test data from previous notebook
    - Initialize shap.TreeExplainer with the LightGBM model
    - Compute SHAP values for test set
    - Generate global SHAP summary plot (beeswarm plot) showing feature importance
    - Generate SHAP summary bar plot showing mean absolute SHAP values
    - Create Partial Dependence Plots for top 5 most important features
    - Document interpretation guidelines in markdown cells
    - Save SHAP explainer to `backend/artifacts/shap_explainer.pkl` using joblib
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 6. Implement FastAPI backend structure







  - [x] 6.1 Create `backend/main.py` with FastAPI app initialization




    - Initialize FastAPI app with title="AIMS API", version="1.0"
    - Add CORS middleware to allow requests from http://localhost:3000
    - Create startup event handler to load model artifacts (lgbm_model.pkl, preprocessor.pkl, shap_explainer.pkl)
    - Store loaded artifacts in app.state for reuse across requests
    - _Requirements: 4.1, 4.2_



  - [x] 6.2 Create `backend/models/request.py` with Pydantic request model





    - Define SensorInput class inheriting from BaseModel
    - Add 18 float fields: Shaft_RPM, Engine_Load, Fuel_Flow, Air_Pressure, Ambient_Temp, Oil_Temp, Oil_Pressure, Vibration_X, Vibration_Y, Vibration_Z, Cylinder1_Pressure, Cylinder1_Exhaust_Temp, Cylinder2_Pressure, Cylinder2_Exhaust_Temp, Cylinder3_Pressure, Cylinder3_Exhaust_Temp, Cylinder4_Pressure, Cylinder4_Exhaust_Temp
    - Add field validators to ensure reasonable ranges (e.g., RPM > 0, temperatures > -50)



    - _Requirements: 4.2_




  - [x] 6.3 Create `backend/models/response.py` with Pydantic response model





    - Define PredictionResponse class inheriting from BaseModel
    - Add fields: prediction_label (str), probabilities (Dict[str, float]), shap_values (Dict[str, float])
    - _Requirements: 4.6_

  - [x] 6.4 Create `backend/services/predictor.py` with inference logic





    - Define FAULT_LABELS dictionary mapping 0-7 to human-readable strings
    - Implement predict_fault function that accepts SensorInput and loaded artifacts


    - Convert SensorInput to numpy array in correct feature order
    - Transform input using preprocessor
    - Generate prediction and probabilities using model.predict() and model.predict_proba()
    - Compute SHAP values for the input using shap_explainer
    - Map numeric prediction to label string
    - Format probabilities as dict with label strings as keys
    - Format SHAP values as dict with feature names as keys
    - Return PredictionResponse object
    - _Requirements: 4.3, 4.4, 4.5, 4.6_

  - [x] 6.5 Create POST /predict endpoint in `backend/main.py`





    - Define route handler that accepts SensorInput
    - Call predict_fault function with input and app.state artifacts
    - Return PredictionResponse
    - Add error handling: catch exceptions and return HTTP 500 with error message
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [x] 7. Implement React frontend structure






  - [x] 7.1 Create React app and component structure

    - Initialize React app in `frontend/` directory using create-react-app
    - Create `src/components/` directory
    - Create component files: SensorInputForm.jsx, PredictionDisplay.jsx, ExplainabilityDisplay.jsx, SystemHealthRadar.jsx
    - Create `src/App.jsx` as main container component
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4_


  - [x] 7.2 Implement SensorInputForm component

    - Create state for 18 sensor values using useState
    - Render 18 input fields (number type) with labels for each sensor
    - Implement handleInputChange to update sensor state
    - Create three preset scenario objects: NORMAL_SCENARIO, MINOR_FAULT_SCENARIO, CRITICAL_FAULT_SCENARIO
    - NORMAL_SCENARIO: RPM=950, Load=70, Fuel_Flow=120, Oil_Temp=75, Oil_Pressure=3.5, Vibration_X=0.05, Vibration_Y=0.05, Vibration_Z=0.05, all cylinder pressures=145, all exhaust temps=420
    - MINOR_FAULT_SCENARIO: Same as normal but Oil_Temp=110 (lubrication degradation indicator)
    - CRITICAL_FAULT_SCENARIO: Same as normal but Vibration_X=0.45, Vibration_Y=0.35, all exhaust temps=550 (turbocharger failure indicators)
    - Render three preset buttons that call loadScenario with respective scenario
    - Implement loadScenario to update all sensor states from scenario object
    - Render "Analyze" button that calls handleSubmit
    - Implement handleSubmit to POST sensor data to http://localhost:8000/predict using axios
    - Pass prediction response to parent component via callback prop
    - _Requirements: 5.1, 5.2, 5.3_


  - [x] 7.3 Implement PredictionDisplay component

    - Accept props: probabilities (object), predictionLabel (string)
    - Transform probabilities object into array format for Recharts: [{name: "Normal", value: 0.95}, ...]
    - Render Recharts PieChart with innerRadius (donut style)
    - Configure chart: 8 slices (one per fault type), custom colors
    - Highlight slice with maximum probability using different color/stroke
    - Render center text overlay showing predictionLabel and max probability percentage
    - _Requirements: 5.4, 5.5, 5.6_


  - [x] 7.4 Implement ExplainabilityDisplay component

    - Accept props: shapValues (object)
    - Transform shapValues object into array format: [{feature: "Oil_Temp", value: 0.23}, ...]
    - Sort array by absolute value (descending) to show most influential features first
    - Render Recharts BarChart with horizontal layout
    - Configure chart: Y-axis shows feature names, X-axis shows SHAP values
    - Apply conditional coloring: positive values (red), negative values (blue)
    - Add reference line at x=0 to separate positive/negative
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_


  - [x] 7.5 Implement SystemHealthRadar component

    - Accept props: sensorValues (object)
    - Define SAFE_RANGES object with min/max for key sensors: Shaft_RPM, Engine_Load, Oil_Temp, Oil_Pressure, Vibration_X, Vibration_Y, Vibration_Z, avg exhaust temp
    - Normalize sensor values to 0-100 scale based on safe ranges
    - Create two data arrays: current values and safe range boundary
    - Render Recharts RadarChart with two overlays: safe range (green polygon) and current values (blue line)
    - Highlight out-of-range values by changing point color to red
    - _Requirements: 7.1, 7.2, 7.3, 7.4_


  - [x] 7.6 Implement App.jsx main container

    - Create state for prediction results: predictionLabel, probabilities, shapValues, sensorValues
    - Render SensorInputForm with callback to update prediction state
    - Conditionally render PredictionDisplay, ExplainabilityDisplay, SystemHealthRadar when prediction exists
    - Add basic styling: grid layout with form on left, results on right
    - Add loading state during API request
    - Add error handling: display error message if API request fails
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4_

- [x] 8. Create demo scenario validation






  - [x] 8.1 Test Normal scenario end-to-end


    - Start backend server: `uvicorn main:app --reload`
    - Start frontend dev server: `npm start`
    - Click "Load Scenario: Normal Operation" button
    - Click "Analyze" button
    - Verify prediction label is "Normal" with confidence > 95%
    - Verify SHAP plot shows mostly blue bars (features pushing away from faults)
    - Verify spider chart shows all values within safe range polygon
    - _Requirements: 8.1_


  - [x] 8.2 Test Minor Fault scenario end-to-end

    - Click "Load Scenario: Minor Fault" button
    - Click "Analyze" button
    - Verify prediction shows split probabilities (e.g., 60% Normal, 35% Lubrication Oil Degradation)
    - Verify SHAP plot highlights Oil_Temp as top red bar (positive SHAP)
    - Verify spider chart shows Oil_Temp outside safe range
    - _Requirements: 8.2_


  - [x] 8.3 Test Critical Fault scenario end-to-end

    - Click "Load Scenario: Critical Fault" button
    - Click "Analyze" button
    - Verify prediction label is a critical fault (e.g., "Turbocharger Fault" or "Vibration Anomaly") with confidence > 90%
    - Verify SHAP plot highlights Vibration_X and Exhaust_Temp as top red bars
    - Verify spider chart shows multiple parameters outside safe range (red highlights)
    - _Requirements: 8.3, 8.4_

- [x] 9. Create backend unit tests





  - [x] 9.1 Create `backend/tests/test_models.py`


    - Test SensorInput validation with valid data (should pass)
    - Test SensorInput validation with missing fields (should raise ValidationError)
    - Test SensorInput validation with invalid types (should raise ValidationError)
    - Test PredictionResponse serialization
    - _Requirements: 4.2, 4.6_


  - [x] 9.2 Create `backend/tests/test_predictor.py`

    - Mock preprocessor, model, and explainer objects
    - Test predict_fault with valid input (should return PredictionResponse)
    - Test FAULT_LABELS mapping (verify all 8 labels exist)
    - Test SHAP values dictionary has correct feature names
    - _Requirements: 4.3, 4.4, 4.5, 4.6_

  - [x] 9.3 Create `backend/tests/test_endpoints.py`


    - Use FastAPI TestClient
    - Test POST /predict with valid payload (should return 200)
    - Test POST /predict with invalid payload (should return 422)
    - Test response schema matches PredictionResponse
    - _Requirements: 4.1, 4.2, 4.6_

- [x] 10. Create frontend component tests





  - [x] 10.1 Create `frontend/src/components/__tests__/SensorInputForm.test.jsx`


    - Test component renders 18 input fields
    - Test preset buttons exist (Normal, Minor, Critical)
    - Test loadScenario updates input values
    - Test handleSubmit calls API with correct payload (mock axios)
    - _Requirements: 5.1, 5.2, 5.3_


  - [x] 10.2 Create `frontend/src/components/__tests__/PredictionDisplay.test.jsx`

    - Test component renders donut chart with mock probabilities
    - Test predicted label displays correctly
    - Test highest probability slice is highlighted
    - _Requirements: 5.4, 5.5, 5.6_

  - [x] 10.3 Create `frontend/src/components/__tests__/ExplainabilityDisplay.test.jsx`


    - Test component renders bar chart with mock SHAP values
    - Test bars are sorted by absolute value
    - Test positive values render in red, negative in blue
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_



  - [x] 10.4 Create `frontend/src/components/__tests__/SystemHealthRadar.test.jsx`

    - Test component renders radar chart with mock sensor values
    - Test safe range polygon displays
    - Test out-of-range values highlighted in red
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 11. Create documentation






  - [x] 11.1 Create `README.md` in project root

    - Add project overview and architecture diagram
    - Add setup instructions for backend (pip install, uvicorn command)
    - Add setup instructions for frontend (npm install, npm start)
    - Add usage instructions for demo scenarios
    - Add troubleshooting section
    - _Requirements: All_


  - [x] 11.2 Create `backend/README.md`

    - Document API endpoints with request/response examples
    - Document model artifact requirements
    - Add link to Swagger UI (http://localhost:8000/docs)
    - _Requirements: 4.1, 4.2, 4.6_


  - [x] 11.3 Create `notebooks/README.md`

    - Document notebook execution order
    - Document expected outputs (pkl files)
    - Add notes on hyperparameter tuning results
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5_
