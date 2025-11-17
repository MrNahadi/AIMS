import joblib
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from models.request import SensorInput
from models.response import PredictionResponse
from services.predictor import predict_fault


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup event handler to load model artifacts.
    Artifacts are stored in app.state for reuse across requests.
    """
    artifacts_dir = os.path.join(os.path.dirname(__file__), "artifacts")
    
    # Load model artifacts
    model_path = os.path.join(artifacts_dir, "lgbm_model.pkl")
    preprocessor_path = os.path.join(artifacts_dir, "preprocessor.pkl")
    explainer_path = os.path.join(artifacts_dir, "shap_explainer.pkl")
    
    try:
        app.state.model = joblib.load(model_path)
        app.state.preprocessor = joblib.load(preprocessor_path)
        app.state.shap_explainer = joblib.load(explainer_path)
        print("✓ Model artifacts loaded successfully")
    except FileNotFoundError as e:
        print(f"⚠ Warning: Could not load model artifacts: {e}")
        print("  Make sure to run the notebooks to generate the artifacts first.")
        app.state.model = None
        app.state.preprocessor = None
        app.state.shap_explainer = None
    
    yield
    
    # Cleanup (if needed)
    print("Shutting down AIMS API")


# Initialize FastAPI app
app = FastAPI(
    title="AIMS API",
    version="1.0",
    description="AI Marine engineering system - Intelligent diagnostic API for marine engine faults",
    lifespan=lifespan
)

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "AIMS API is running",
        "version": "1.0",
        "status": "healthy"
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(sensor_input: SensorInput):
    """
    Predict marine engine fault from sensor readings.
    
    Args:
        sensor_input: Validated sensor readings (18 features)
    
    Returns:
        PredictionResponse containing:
        - prediction_label: Human-readable fault type
        - probabilities: Confidence scores for all 8 fault types
        - shap_values: Feature importance explanations
    
    Raises:
        HTTPException: 500 if model artifacts are not loaded or prediction fails
    """
    try:
        # Check if model artifacts are loaded
        if app.state.model is None or app.state.preprocessor is None or app.state.shap_explainer is None:
            raise HTTPException(
                status_code=500,
                detail="Model artifacts not loaded. Please ensure notebooks have been run to generate model files."
            )
        
        # Call predict_fault function with input and app.state artifacts
        prediction_response = predict_fault(
            sensor_input=sensor_input,
            model=app.state.model,
            preprocessor=app.state.preprocessor,
            shap_explainer=app.state.shap_explainer
        )
        
        return prediction_response
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Catch any unexpected errors and return HTTP 500
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
