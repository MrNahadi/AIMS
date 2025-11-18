# Implementation Guide - Code Snippets to Add

## 📊 NOTEBOOK 01: Data Exploration & Cleaning

### Add After "## 3. Fault Label Distribution Analysis"

```markdown
## 4. Correlation Analysis

Analyzing correlations between sensor features to identify relationships and potential multicollinearity.
```

```python
# Correlation matrix for sensor features
correlation_matrix = df[sensor_features].corr()

# Create correlation heatmap
plt.figure(figsize=(16, 14))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=0.5,
            cbar_kws={"shrink": 0.8})
plt.title('Correlation Heatmap - 18 Sensor Features', fontsize=16, pad=20)
plt.tight_layout()
plt.show()

# Identify highly correlated pairs
high_corr_pairs = []
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        if abs(correlation_matrix.iloc[i, j]) > 0.8:
            high_corr_pairs.append({
                'Feature 1': correlation_matrix.columns[i],
                'Feature 2': correlation_matrix.columns[j],
                'Correlation': correlation_matrix.iloc[i, j]
            })

if high_corr_pairs:
    print("\n🔍 Highly Correlated Feature Pairs (|r| > 0.8):")
    print("=" * 80)
    for pair in high_corr_pairs:
        print(f"{pair['Feature 1']:30s} <-> {pair['Feature 2']:30s} : {pair['Correlation']:.3f}")
else:
    print("\n✅ No highly correlated feature pairs found (|r| > 0.8)")
```

```markdown
## 5. Feature Distribution Analysis

Examining the distribution of sensor features to understand data characteristics and identify potential outliers.
```

```python
# Plot distributions for all 18 features
fig, axes = plt.subplots(6, 3, figsize=(18, 20))
axes = axes.ravel()

for idx, feature in enumerate(sensor_features):
    axes[idx].hist(df[feature], bins=50, alpha=0.7, color='steelblue', edgecolor='black')
    axes[idx].set_title(f'{feature}', fontsize=10, fontweight='bold')
    axes[idx].set_xlabel('Value')
    axes[idx].set_ylabel('Frequency')
    axes[idx].grid(True, alpha=0.3)

plt.tight_layout()
plt.suptitle('Distribution of All 18 Sensor Features', fontsize=16, y=1.001)
plt.show()
```

```python
# Compare distributions: Normal vs Fault conditions
fig, axes = plt.subplots(6, 3, figsize=(18, 20))
axes = axes.ravel()

for idx, feature in enumerate(sensor_features):
    # Normal condition
    normal_data = df[df['Fault_Label'] == 0][feature]
    # All fault conditions
    fault_data = df[df['Fault_Label'] != 0][feature]
    
    axes[idx].hist(normal_data, bins=30, alpha=0.6, label='Normal', color='green', density=True)
    axes[idx].hist(fault_data, bins=30, alpha=0.6, label='Fault', color='red', density=True)
    axes[idx].set_title(f'{feature}', fontsize=10, fontweight='bold')
    axes[idx].set_xlabel('Value')
    axes[idx].set_ylabel('Density')
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)

plt.tight_layout()
plt.suptitle('Feature Distributions: Normal vs Fault Conditions', fontsize=16, y=1.001)
plt.show()
```

```markdown
## 6. Outlier Detection Summary

Using the IQR (Interquartile Range) method to identify potential outliers in sensor readings.
```

```python
# Detect outliers using IQR method
outlier_summary = []

for feature in sensor_features:
    Q1 = df[feature].quantile(0.25)
    Q3 = df[feature].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
    outlier_count = len(outliers)
    outlier_percentage = (outlier_count / len(df)) * 100
    
    outlier_summary.append({
        'Feature': feature,
        'Outlier Count': outlier_count,
        'Percentage': outlier_percentage,
        'Lower Bound': lower_bound,
        'Upper Bound': upper_bound
    })

outlier_df = pd.DataFrame(outlier_summary).sort_values('Outlier Count', ascending=False)

# Visualize outlier counts
plt.figure(figsize=(12, 8))
sns.barplot(data=outlier_df, x='Outlier Count', y='Feature', palette='viridis')
plt.title('Outlier Count by Feature (IQR Method)', fontsize=14, fontweight='bold')
plt.xlabel('Number of Outliers')
plt.ylabel('Sensor Feature')
plt.tight_layout()
plt.show()

# Display outlier summary table
print("\n📊 Outlier Detection Summary:")
print("=" * 100)
print(outlier_df.to_string(index=False))
print(f"\n✅ Total outliers detected: {outlier_df['Outlier Count'].sum():,} across all features")
```

---

## 🔧 NOTEBOOK 02: Feature Engineering & Preprocessing

### Add After "## 3. Train-Test Split (Stratified)"

```markdown
## 4. Handle Class Imbalance with SMOTE

Applying Synthetic Minority Over-sampling Technique (SMOTE) to balance the training dataset.

**Why SMOTE?**
- Original dataset has class imbalance (Normal: 65%, Faults: 35%)
- SMOTE 