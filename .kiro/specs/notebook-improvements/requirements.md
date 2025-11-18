# Notebook Improvements - Requirements Document

## Introduction

This specification outlines improvements to the marine engine fault prediction notebooks to achieve F1-score > 0.90 while maintaining all existing functionality and ensuring backward compatibility.

## Glossary

- **F1-Score**: Harmonic mean of precision and recall, target > 0.90
- **SMOTE**: Synthetic Minority Over-sampling Technique for handling class imbalance
- **Class Weights**: Technique to penalize misclassification of minority classes
- **Cross-Validation**: K-fold validation for robust model evaluation
- **Feature Importance**: Measure of feature contribution to model predictions

## Requirements

### Requirement 1: Enhanced EDA in Notebook 01

**User Story:** As a data scientist, I want comprehensive exploratory analysis so that I can understand feature relationships and data quality.

#### Acceptance Criteria

1. THE System SHALL add correlation heatmap visualization after fault distribution analysis
2. THE System SHALL add feature distribution plots for top 5 most important sensors
3. THE System SHALL preserve all existing cells and outputs
4. THE System SHALL add clear markdown documentation for new analyses
5. THE System SHALL ensure visualizations are properly sized and labeled

### Requirement 2: Class Imbalance Handling in Notebook 02

**User Story:** As a data scientist, I want to handle class imbalance so that the model performs well on minority classes.

#### Acceptance Criteria

1. THE System SHALL implement SMOTE after train-test split
2. THE System SHALL create balanced training dataset while preserving test set
3. THE System SHALL document class distribution before and after SMOTE
4. THE System SHALL save both balanced and original datasets
5. THE System SHALL maintain backward compatibility with existing preprocessing

### Requirement 3: Model Performance Improvement in Notebook 03

**User Story:** As a data scientist, I want to achieve F1-score > 0.90 so that the model meets production requirements.

#### Acceptance Criteria

1. THE System SHALL add class weights to LightGBM hyperparameter tuning
2. THE System SHALL implement 5-fold cross-validation for robust evaluation
3. THE System SHALL add ensemble methods (voting classifier) if needed
4. THE System SHALL fix widget rendering issue by adding proper imports
5. THE System SHALL achieve macro-average F1-score > 0.90 on test set
6. THE System SHALL preserve all existing hyperparameter tuning code
7. THE System SHALL add comprehensive evaluation metrics (precision, recall, F1 per class)

### Requirement 4: Feature Importance Analysis in Notebook 03

**User Story:** As a data scientist, I want to understand feature importance so that I can interpret model decisions.

#### Acceptance Criteria

1. THE System SHALL extract and visualize feature importance from trained model
2. THE System SHALL create bar plot of top 15 most important features
3. THE System SHALL add feature importance table with numerical values
4. THE System SHALL document interpretation guidelines

### Requirement 5: Documentation and Compatibility

**User Story:** As a data scientist, I want clear documentation so that I can understand all changes and reproduce results.

#### Acceptance Criteria

1. THE System SHALL add markdown cells explaining each improvement
2. THE System SHALL document performance improvements with metrics
3. THE System SHALL maintain all existing cell execution order
4. THE System SHALL ensure all notebooks run end-to-end without errors
5. THE System SHALL add version notes in notebook headers
