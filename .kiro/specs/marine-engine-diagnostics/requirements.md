# Requirements Document

## Introduction

AIMS (AI Marine engineering system) is an intelligent diagnostic dashboard for marine engine faults that transforms raw sensor data into actionable maintenance intelligence. The system uses machine learning to predict specific fault types (e.g., Turbocharger Failure, Fuel Injection Fault) and provides explainable AI insights to help engineering panels, maintenance supervisors, and ship operators make proactive, data-driven maintenance decisions. The system moves beyond simple threshold-based alarms to provide root cause diagnostics with confidence scores and feature importance explanations.

## Glossary

- **AIMS**: AI Marine engineering system - the complete diagnostic dashboard system
- **LightGBM Model**: A gradient boosting machine learning classifier trained to predict marine engine fault types
- **SHAP Values**: SHapley Additive exPlanations - numerical values indicating how much each sensor feature contributes to a specific fault prediction
- **Preprocessor**: A data transformation component that scales and normalizes raw sensor inputs before model inference
- **FastAPI Backend**: The REST API server that loads the trained model and serves predictions
- **React Frontend**: The web-based user interface displaying the Engineer's Dashboard
- **Engineer's Dashboard**: The primary user interface showing predictions, confidence scores, and diagnostic visualizations
- **Fault Label**: The predicted category of engine malfunction (e.g., Normal, Turbocharger Failure, Lubrication Oil Degradation)
- **Sensor Reading**: A numerical measurement from engine monitoring equipment (e.g., Shaft_RPM, Oil_Temp, Vibration_X)
- **Prediction Confidence**: The probability score (0-100%) indicating model certainty for a specific fault classification
- **Demo Scenario**: A pre-configured set of sensor values representing Normal, Minor Fault, or Critical Fault conditions

## Requirements

### Requirement 1

**User Story:** As an engineering panel member, I want to see a trained machine learning model that achieves high accuracy on marine engine fault classification, so that I can trust the system's diagnostic predictions.

#### Acceptance Criteria

1. WHEN THE AIMS trains the LightGBM Model on the marine engine dataset, THE AIMS SHALL achieve an F1-score (macro-average) greater than 0.90 on the holdout test set
2. THE AIMS SHALL generate a classification report showing precision, recall, and F1-score for each Fault Label category
3. THE AIMS SHALL generate a confusion matrix visualization showing the model's prediction accuracy across all fault types
4. THE AIMS SHALL save the trained LightGBM Model as a serialized file for deployment

### Requirement 2

**User Story:** As a data scientist, I want comprehensive exploratory data analysis and preprocessing pipelines, so that the model is trained on clean, well-understood data.

#### Acceptance Criteria

1. THE AIMS SHALL load the marine engine fault dataset and profile all Sensor Readings for missing values, data types, and statistical distributions
2. THE AIMS SHALL visualize the distribution of Fault Label categories to identify class imbalance
3. THE AIMS SHALL document all data cleaning decisions in a Jupyter notebook
4. THE AIMS SHALL create a Preprocessor that scales and normalizes Sensor Readings using StandardScaler
5. THE AIMS SHALL save the fitted Preprocessor as a serialized file for consistent inference-time transformations

### Requirement 3

**User Story:** As a chief engineer, I want to understand why the system predicts a specific fault, so that I can validate the diagnosis and take appropriate action.

#### Acceptance Criteria

1. THE AIMS SHALL generate global SHAP Values showing which Sensor Readings are most important for fault classification across the entire dataset
2. THE AIMS SHALL generate local SHAP Values for individual predictions showing which Sensor Readings drove that specific diagnosis
3. THE AIMS SHALL create Partial Dependence Plots showing how individual Sensor Readings affect fault probability
4. THE AIMS SHALL save a SHAP explainer object as a serialized file for real-time explanation generation
5. THE AIMS SHALL document all explainability visualizations in a Jupyter notebook

### Requirement 4

**User Story:** As a maintenance supervisor, I want a REST API that accepts sensor readings and returns fault predictions with explanations, so that I can integrate diagnostics into existing monitoring systems.

#### Acceptance Criteria

1. THE FastAPI Backend SHALL expose a POST endpoint at /predict that accepts JSON-formatted Sensor Readings
2. WHEN THE FastAPI Backend receives a prediction request, THE FastAPI Backend SHALL validate input data using a Pydantic model
3. WHEN THE FastAPI Backend receives valid Sensor Readings, THE FastAPI Backend SHALL load the Preprocessor and transform the input data
4. WHEN THE FastAPI Backend transforms input data, THE FastAPI Backend SHALL load the LightGBM Model and generate a Fault Label prediction
5. WHEN THE FastAPI Backend generates a prediction, THE FastAPI Backend SHALL load the SHAP explainer and calculate local SHAP Values for the input
6. THE FastAPI Backend SHALL return a JSON response containing the predicted Fault Label, Prediction Confidence scores for all fault types, and SHAP Values for each Sensor Reading

### Requirement 5

**User Story:** As an engineering panel member, I want a visual dashboard that displays fault predictions with confidence scores, so that I can quickly assess engine health status.

#### Acceptance Criteria

1. THE React Frontend SHALL display a form where users can input Sensor Reading values
2. THE React Frontend SHALL provide preset buttons to load Demo Scenario configurations for Normal Operation, Minor Fault, and Critical Fault
3. WHEN a user clicks the Analyze button, THE React Frontend SHALL send Sensor Readings to the FastAPI Backend /predict endpoint
4. WHEN THE React Frontend receives a prediction response, THE React Frontend SHALL display a donut chart showing Prediction Confidence distribution across all Fault Label categories
5. THE React Frontend SHALL highlight the highest probability Fault Label in the donut chart
6. THE React Frontend SHALL display the predicted Fault Label in large, clear text

### Requirement 6

**User Story:** As a chief engineer, I want to see which sensor readings are driving a fault prediction, so that I can focus my diagnostic efforts on the most relevant systems.

#### Acceptance Criteria

1. THE React Frontend SHALL display a diverging horizontal bar chart visualizing SHAP Values from the prediction response
2. THE React Frontend SHALL render Sensor Readings with positive SHAP Values (pushing toward the fault) in red
3. THE React Frontend SHALL render Sensor Readings with negative SHAP Values (pushing away from the fault) in blue
4. THE React Frontend SHALL sort the SHAP Values bar chart by absolute magnitude with the most influential features at the top
5. THE React Frontend SHALL label each bar with the Sensor Reading name and its SHAP Value

### Requirement 7

**User Story:** As a ship operator, I want an at-a-glance visualization of current sensor readings compared to safe operating ranges, so that I can identify which parameters are out of bounds.

#### Acceptance Criteria

1. THE React Frontend SHALL display a spider chart (radar chart) plotting current Sensor Reading values
2. THE React Frontend SHALL overlay a safe operating range polygon on the spider chart for visual comparison
3. WHEN Sensor Readings exceed safe thresholds, THE React Frontend SHALL highlight those parameters in red on the spider chart
4. THE React Frontend SHALL update the spider chart dynamically when new Sensor Readings are analyzed

### Requirement 8

**User Story:** As a project lead, I want a demonstration flow that showcases the system's capabilities across normal, minor fault, and critical fault scenarios, so that I can present the value proposition to stakeholders.

#### Acceptance Criteria

1. WHERE the Demo Scenario is Normal Operation, THE React Frontend SHALL load Sensor Readings that result in a Prediction Confidence greater than 0.95 for the Normal Fault Label
2. WHERE the Demo Scenario is Minor Fault, THE React Frontend SHALL load Sensor Readings that result in a split Prediction Confidence between Normal and a specific fault type (e.g., 60% Normal, 35% Lubrication Oil Degradation)
3. WHERE the Demo Scenario is Critical Fault, THE React Frontend SHALL load Sensor Readings that result in a Prediction Confidence greater than 0.90 for a critical Fault Label (e.g., Turbocharger Failure)
4. THE Engineer's Dashboard SHALL clearly demonstrate the diagnostic value by showing relevant SHAP Values and spider chart indicators for each Demo Scenario
