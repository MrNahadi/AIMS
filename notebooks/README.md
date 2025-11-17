# AIMS Model Training Notebooks

This directory contains Jupyter notebooks for the complete machine learning pipeline: data exploration, preprocessing, model training, and explainability analysis.

## Notebook Execution Order

The notebooks must be executed in the following order, as each notebook depends on outputs from the previous ones:

### 1. 01_Data_Exploration_Cleaning.ipynb

**Purpose**: Explore and understand the marine engine fault dataset

**Inputs**:
- `../data/marine_engine_fault_dataset.csv`

**Key Steps**:
- Load dataset and profile all columns (dtypes, missing values, unique counts)
- Visualize Fault_Label distribution to check class balance
- Generate histograms for all 18 sensor features
- Create boxplots to identify outliers
- Document data quality issues and cleaning decisions

**Outputs**:
- Cleaned dataset (in-memory, passed to next notebook)
- Data quality insights documented in markdown cells

**Expected Results**:
- Dataset should have ~10,000 rows with 20 columns (18 sensors + Timestamp + Fault_Label)
- Fault_Label should contain values 0-7
- No missing values after cleaning
- Outliers identified and documented

---

### 2. 02_Feature_Engineering_Preprocessing.ipynb

**Purpose**: Prepare data for model training with proper scaling and splitting

**Inputs**:
- Cleaned dataset from notebook 01 (or reload from CSV)

**Key Steps**:
- Separate features (18 sensor columns) from target (Fault_Label)
- Split data: 80% train, 20% test using stratified split on Fault_Label
- Initialize StandardScaler and fit on training features only
- Transform both train and test features
- Save fitted StandardScaler for deployment

**Outputs**:
- `../backend/artifacts/preprocessor.pkl` (fitted StandardScaler)
- Preprocessed train/test datasets (in-memory)

**Expected Results**:
- Train set: ~8,000 samples
- Test set: ~2,000 samples
- All features scaled to mean=0, std=1
- Class distribution preserved in both splits

---

### 3. 03_Model_Training_Tuning.ipynb

**Purpose**: Train and optimize LightGBM classifier for fault prediction

**Inputs**:
- Preprocessed train/test data from notebook 02

**Key Steps**:
- Initialize LightGBM classifier with objective='multiclass', num_class=8
- Perform hyperparameter tuning using Optuna with 50 trials
- Tune parameters:
  - `num_leaves`: 20-100
  - `learning_rate`: 0.01-0.3
  - `n_estimators`: 100-500
  - `max_depth`: 3-10
- Train final model with best hyperparameters on full training set
- Generate predictions on test set
- Calculate classification report (precision, recall, F1-score per class)
- Generate confusion matrix heatmap
- Verify F1-score (macro-average) > 0.90

**Outputs**:
- `../backend/artifacts/lgbm_model.pkl` (trained LightGBM model)
- Classification report and confusion matrix visualizations

**Expected Results**:
- F1-score (macro-average): > 0.90
- All classes should have F1-score > 0.80
- Confusion matrix should show strong diagonal (correct predictions)

**Hyperparameter Tuning Results**:

Typical best parameters found (may vary by run):
```python
{
    'num_leaves': 45-65,
    'learning_rate': 0.05-0.15,
    'n_estimators': 200-400,
    'max_depth': 6-8
}
```

Performance metrics achieved:
- Accuracy: 92-95%
- F1-score (macro): 0.91-0.94
- Training time: 2-5 minutes (depending on hardware)

---

### 4. 04_Model_Explainability_Export.ipynb

**Purpose**: Generate SHAP explanations for model interpretability

**Inputs**:
- Trained model from notebook 03
- Test data from notebook 02

**Key Steps**:
- Load trained LightGBM model
- Initialize shap.TreeExplainer with the model
- Compute SHAP values for test set
- Generate global SHAP summary plot (beeswarm plot) showing feature importance
- Generate SHAP summary bar plot showing mean absolute SHAP values
- Create Partial Dependence Plots for top 5 most important features
- Document interpretation guidelines
- Save SHAP explainer for deployment

**Outputs**:
- `../backend/artifacts/shap_explainer.pkl` (fitted SHAP TreeExplainer)
- SHAP visualizations (summary plots, PDP plots)

**Expected Results**:
- Top influential features typically include:
  - Vibration_X, Vibration_Y, Vibration_Z (for vibration anomalies)
  - Oil_Temp, Oil_Pressure (for lubrication faults)
  - Exhaust temperatures (for turbocharger/cooling faults)
  - Shaft_RPM, Engine_Load (general indicators)
- SHAP values should sum to (prediction - base_value) for each sample
- PDP plots should show clear relationships between features and fault probabilities

---

## Quick Start

To run all notebooks in sequence:

1. Ensure you have Jupyter installed:
```bash
pip install jupyter notebook
```

2. Start Jupyter:
```bash
jupyter notebook
```

3. Execute notebooks in order (1 → 2 → 3 → 4)

4. Verify that all three artifact files are created in `../backend/artifacts/`:
   - `lgbm_model.pkl`
   - `preprocessor.pkl`
   - `shap_explainer.pkl`

## Dependencies

All required packages are listed in `../backend/requirements.txt`. Install with:

```bash
pip install -r ../backend/requirements.txt
```

Key packages for notebooks:
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `matplotlib`, `seaborn`: Visualization
- `scikit-learn`: Preprocessing and metrics
- `lightgbm`: Model training
- `shap`: Explainability
- `optuna`: Hyperparameter tuning
- `joblib`: Model serialization

## Expected Outputs

After running all notebooks, you should have:

### Artifact Files

```
backend/artifacts/
├── lgbm_model.pkl          # ~2-5 MB
├── preprocessor.pkl        # ~10-50 KB
└── shap_explainer.pkl      # ~2-5 MB
```

### Model Performance

- **Accuracy**: 92-95%
- **F1-score (macro)**: 0.91-0.94
- **Per-class F1-scores**: All > 0.80

### Feature Importance (Typical Rankings)

1. Vibration_X
2. Vibration_Y
3. Oil_Temp
4. Cylinder1_Exhaust_Temp
5. Cylinder2_Exhaust_Temp
6. Oil_Pressure
7. Shaft_RPM
8. Engine_Load
9. Vibration_Z
10. Fuel_Flow

(Rankings may vary based on data and hyperparameters)

## Hyperparameter Tuning Notes

### Optuna Configuration

The hyperparameter search uses Optuna with the following configuration:

- **Number of trials**: 50
- **Optimization metric**: F1-score (macro-average)
- **Search space**:
  - `num_leaves`: Integer range [20, 100]
  - `learning_rate`: Float range [0.01, 0.3]
  - `n_estimators`: Integer range [100, 500]
  - `max_depth`: Integer range [3, 10]

### Tuning Results

Typical optimization results:
- Best trial found: Trial 30-45 (varies)
- Best F1-score: 0.91-0.94
- Optimization time: 10-20 minutes

### Manual Tuning Tips

If you want to manually tune hyperparameters:

1. **Increase `num_leaves`** if model is underfitting (low train/test scores)
2. **Decrease `learning_rate`** and increase `n_estimators` for better convergence
3. **Increase `max_depth`** for more complex patterns (risk of overfitting)
4. **Add regularization** (`reg_alpha`, `reg_lambda`) if overfitting occurs

## Troubleshooting

### Notebook 01 Issues

**Problem**: Dataset not found
- Solution: Ensure `../data/marine_engine_fault_dataset.csv` exists
- Check file path is correct relative to notebooks directory

**Problem**: Memory errors with large dataset
- Solution: Use `pd.read_csv(..., nrows=10000)` to limit rows
- Consider using `dtype` parameter to reduce memory usage

### Notebook 02 Issues

**Problem**: Artifacts directory doesn't exist
- Solution: Create directory: `mkdir -p ../backend/artifacts`

**Problem**: Stratified split fails
- Solution: Ensure all classes have at least 2 samples
- Check for class imbalance in Fault_Label

### Notebook 03 Issues

**Problem**: Optuna optimization is slow
- Solution: Reduce number of trials (e.g., 20 instead of 50)
- Use `n_jobs=-1` for parallel optimization

**Problem**: F1-score < 0.90
- Solution: Check data quality in notebook 01
- Try different hyperparameter ranges
- Ensure preprocessing was applied correctly

**Problem**: LightGBM installation issues
- Solution: Install with conda: `conda install -c conda-forge lightgbm`
- Or use pip: `pip install lightgbm --upgrade`

### Notebook 04 Issues

**Problem**: SHAP computation is very slow
- Solution: Compute SHAP values on a sample: `shap_values = explainer.shap_values(X_test[:1000])`
- Use `check_additivity=False` for faster computation

**Problem**: SHAP plots not displaying
- Solution: Ensure matplotlib backend is set: `%matplotlib inline`
- Try `plt.show()` after SHAP plot commands

**Problem**: Memory errors during SHAP computation
- Solution: Process data in batches
- Reduce test set size for SHAP analysis

## Data Schema

### Input Features (18 sensors)

| Feature | Description | Typical Range | Unit |
|---------|-------------|---------------|------|
| Shaft_RPM | Engine shaft rotation speed | 800-1200 | RPM |
| Engine_Load | Engine load percentage | 0-100 | % |
| Fuel_Flow | Fuel consumption rate | 80-200 | L/h |
| Air_Pressure | Intake air pressure | 1.5-3.5 | bar |
| Ambient_Temp | Ambient temperature | 15-35 | °C |
| Oil_Temp | Lubrication oil temperature | 60-110 | °C |
| Oil_Pressure | Lubrication oil pressure | 2.0-5.0 | bar |
| Vibration_X | Vibration in X-axis | 0-0.5 | mm/s |
| Vibration_Y | Vibration in Y-axis | 0-0.5 | mm/s |
| Vibration_Z | Vibration in Z-axis | 0-0.5 | mm/s |
| Cylinder1_Pressure | Cylinder 1 compression pressure | 120-160 | bar |
| Cylinder1_Exhaust_Temp | Cylinder 1 exhaust temperature | 350-550 | °C |
| Cylinder2_Pressure | Cylinder 2 compression pressure | 120-160 | bar |
| Cylinder2_Exhaust_Temp | Cylinder 2 exhaust temperature | 350-550 | °C |
| Cylinder3_Pressure | Cylinder 3 compression pressure | 120-160 | bar |
| Cylinder3_Exhaust_Temp | Cylinder 3 exhaust temperature | 350-550 | °C |
| Cylinder4_Pressure | Cylinder 4 compression pressure | 120-160 | bar |
| Cylinder4_Exhaust_Temp | Cylinder 4 exhaust temperature | 350-550 | °C |

### Target Variable

| Feature | Description | Values |
|---------|-------------|--------|
| Fault_Label | Fault type classification | 0-7 (see mapping below) |

### Fault Label Mapping

| Code | Fault Type |
|------|------------|
| 0 | Normal |
| 1 | Fuel Injection Fault |
| 2 | Cooling System Fault |
| 3 | Turbocharger Fault |
| 4 | Bearing Wear |
| 5 | Lubrication Oil Degradation |
| 6 | Air Intake Restriction |
| 7 | Vibration Anomaly |

## Best Practices

1. **Always run notebooks in order** - Each notebook depends on previous outputs
2. **Save checkpoints** - Use Jupyter's checkpoint feature before long computations
3. **Document changes** - Add markdown cells explaining any modifications
4. **Version control artifacts** - Consider using DVC or Git LFS for .pkl files
5. **Monitor memory usage** - Use `%memit` magic command to track memory
6. **Reproducibility** - Set random seeds for consistent results

## Additional Resources

- [LightGBM Documentation](https://lightgbm.readthedocs.io/)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [Optuna Documentation](https://optuna.readthedocs.io/)
- [Scikit-learn Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
