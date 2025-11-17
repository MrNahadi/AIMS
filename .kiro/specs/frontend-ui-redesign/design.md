# Design Document

## Overview

This design document outlines the approach for redesigning the AIMS frontend application to align with the SoftModernSaaS design system. The redesign will transform the existing functional React application into a modern, approachable interface that follows card-based layouts, soft visual styling, and purposeful color usage while maintaining all existing functionality.

The redesign will focus on:
- Applying the SoftModernSaaS design system consistently across all components
- Refactoring CSS to use design tokens and variables
- Enhancing visual hierarchy and spacing
- Improving button and form styling
- Maintaining responsive behavior with enhanced mobile experience
- Preserving all existing functionality and data flow

## Architecture

### Component Structure

The application maintains its existing React component architecture:

```
App.jsx (Main container)
├── SensorInputForm.jsx (Left panel - data input)
└── Right panel (conditional rendering)
    ├── Welcome message (initial state)
    ├── Loading state
    └── Results (after analysis)
        ├── PredictionDisplay.jsx
        ├── ExplainabilityDisplay.jsx
        └── SystemHealthRadar.jsx
```

### Styling Approach

The redesign will use a CSS variables approach to implement the design system:

1. **Global CSS Variables** - Define design tokens in a root CSS file
2. **Component-Specific Styles** - Update individual component CSS files to use variables
3. **Shared Utilities** - Create reusable CSS classes for common patterns (cards, buttons, etc.)

### Design System Integration

All styling will reference the SoftModernSaaS design system defined in `design.json`:
- Color palette (base, neutral, primary, accent)
- Typography scale and weights
- Spacing system (8-point grid)
- Border radius values
- Shadow definitions

## Components and Interfaces

### 1. Global Styles and Design Tokens

**File**: `frontend/src/index.css`

Create CSS custom properties for the entire design system:

```css
:root {
  /* Base Colors */
  --color-white: #FFFFFF;
  --color-black: #1A202C;
  --color-off-white: #F9FAFB;
  
  /* Neutral Colors */
  --color-text-primary: #1A202C;
  --color-text-secondary: #6B7280;
  --color-text-placeholder: #A0AEC0;
  --color-border-light: #E2E8F0;
  --color-border-default: #CBD5E0;
  --color-background: #F7FAFC;
  
  /* Primary Colors */
  --color-primary-main: #2D3748;
  --color-primary-contrast: #FFFFFF;
  
  /* Accent Colors */
  --color-success: #34D399;
  --color-success-light: #F0FDF4;
  --color-warning: #FBBF24;
  --color-warning-light: #FFFBEB;
  --color-danger: #F87171;
  --color-danger-light: #FEF2F2;
  --color-info: #818CF8;
  --color-info-light: #EEF2FF;
  
  /* Shadows */
  --shadow-sm: 0px 4px 6px -1px rgba(0, 0, 0, 0.05);
  --shadow-md: 0px 10px 15px -3px rgba(0, 0, 0, 0.05), 0px 4px 6px -2px rgba(0, 0, 0, 0.05);
  
  /* Spacing (8-point grid) */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-xxl: 48px;
  
  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
  
  /* Typography */
  --font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Roboto', 'Segoe UI', sans-serif;
  --font-size-base: 16px;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
}
```

### 2. App Component Redesign

**File**: `frontend/src/App.jsx` and `frontend/src/App.css`

**Changes**:
- Update header to use `--color-primary-main` instead of gradient
- Apply card styling to error messages with 4px left border
- Ensure proper spacing using design system variables
- Update grid layout with consistent gaps

**Key CSS Updates**:
```css
.app-header {
  background: var(--color-primary-main);
  color: var(--color-primary-contrast);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
}

.app-error {
  background: var(--color-white);
  border-left: 4px solid var(--color-danger);
  border-radius: var(--radius-md);
  padding: var(--spacing-md) var(--spacing-lg);
  box-shadow: var(--shadow-sm);
}

.app-container {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg);
}
```

### 3. Sensor Input Form Redesign

**File**: `frontend/src/components/SensorInputForm.jsx` and `SensorInputForm.css`

**Changes**:
- Wrap entire form in a card container
- Update input field styling with proper borders and focus states
- Redesign preset buttons to follow button design patterns
- Apply proper label typography
- Update submit button to primary button style

**Card Container**:
```css
.sensor-input-form {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-md);
}
```

**Input Fields**:
```css
.input-group input {
  background: var(--color-white);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-md);
  padding: 12px var(--spacing-md);
  color: var(--color-text-primary);
  font-size: var(--font-size-base);
}

.input-group input:focus {
  outline: none;
  border-color: var(--color-info);
  box-shadow: 0 0 0 3px var(--color-info-light);
}
```

**Buttons**:
```css
.analyze-btn {
  background: var(--color-primary-main);
  color: var(--color-primary-contrast);
  font-weight: var(--font-weight-semibold);
  border-radius: var(--radius-md);
  padding: 12px var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: none;
  cursor: pointer;
  width: 100%;
}

.preset-btn {
  background: transparent;
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-md);
  padding: 12px var(--spacing-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
}
```

### 4. Prediction Display Redesign

**File**: `frontend/src/components/PredictionDisplay.jsx` and `PredictionDisplay.css`

**Changes**:
- Apply card container styling
- Update heading typography
- Redesign confidence badge with appropriate accent colors
- Ensure proper internal spacing
- Update chart tooltip styling

**Card Styling**:
```css
.prediction-display {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-md);
  margin-bottom: var(--spacing-md);
}

.prediction-display h2 {
  font-size: 1.25rem;
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-lg);
}
```

**Confidence Badge**:
```css
.confidence-badge {
  display: inline-block;
  padding: var(--spacing-xs) 10px;
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  font-weight: var(--font-weight-medium);
  background: var(--color-info-light);
  color: var(--color-info);
  border: 1px solid var(--color-info);
}
```

### 5. Explainability Display Redesign

**File**: `frontend/src/components/ExplainabilityDisplay.jsx` and `ExplainabilityDisplay.css`

**Changes**:
- Apply card container styling
- Update legend styling with proper spacing
- Ensure chart colors align with design system where possible
- Update explanation text typography

**Legend Styling**:
```css
.shap-legend {
  display: flex;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
  padding: var(--spacing-md);
  background: var(--color-off-white);
  border-radius: var(--radius-md);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}
```

### 6. System Health Radar Redesign

**File**: `frontend/src/components/SystemHealthRadar.jsx` and `SystemHealthRadar.css`

**Changes**:
- Apply card container styling
- Redesign warning banner with proper alert styling
- Update parameter status indicators
- Improve tooltip styling

**Warning Banner (Alert Component)**:
```css
.warning-banner {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--color-white);
  border-left: 4px solid var(--color-warning);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
}
```

**Status Indicators**:
```css
.parameter-status {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
}

.status-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: var(--radius-full);
}

.status-item.in-range .status-dot {
  background: var(--color-success);
}

.status-item.out-of-range .status-dot {
  background: var(--color-danger);
}
```

### 7. Welcome Message Redesign

**File**: `frontend/src/App.css`

**Changes**:
- Apply card styling to welcome container
- Update feature item cards with subtle backgrounds
- Improve typography hierarchy
- Ensure proper spacing

**Feature Cards**:
```css
.feature-item {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: var(--color-off-white);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
}

.feature-item strong {
  font-size: 1.1rem;
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.feature-item p {
  color: var(--color-text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
}
```

### 8. Loading State Redesign

**File**: `frontend/src/App.css`

**Changes**:
- Apply card styling to loading overlay
- Update spinner colors to match design system
- Improve text styling

```css
.loading-overlay {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xxl) var(--spacing-lg);
  box-shadow: var(--shadow-md);
}

.loading-spinner {
  border: 4px solid var(--color-border-light);
  border-top: 4px solid var(--color-primary-main);
}
```

## Data Models

No changes to data models. The redesign maintains all existing data structures:

- **Sensor Values**: Object with 18 sensor readings
- **Prediction Response**: Contains prediction_label, probabilities, and shap_values
- **Component State**: Existing useState hooks remain unchanged

## Error Handling

Error handling logic remains unchanged. Visual presentation updates:

- Error messages displayed in alert-style cards with 4px left border
- Use `--color-danger` for error states
- Maintain clear error messaging with appropriate iconography

## Testing Strategy

### Visual Regression Testing

1. **Component-Level Testing**:
   - Verify each component renders with new styles
   - Test responsive behavior at breakpoints (768px, 1024px)
   - Validate color contrast ratios for accessibility

2. **Integration Testing**:
   - Test complete user flow from input to results
   - Verify all interactive states (hover, focus, active)
   - Ensure loading and error states display correctly

3. **Cross-Browser Testing**:
   - Test in Chrome, Firefox, Safari, Edge
   - Verify CSS variable support
   - Check shadow and border-radius rendering

### Functional Testing

1. **Existing Functionality**:
   - All preset scenarios load correctly
   - Manual input changes work as expected
   - Prediction API calls function properly
   - Charts render with correct data

2. **Responsive Behavior**:
   - Layout switches to single column on mobile
   - Touch targets meet minimum 44px requirement
   - Horizontal scrolling is prevented

### Accessibility Testing

1. **Keyboard Navigation**:
   - All interactive elements are keyboard accessible
   - Focus states are clearly visible
   - Tab order is logical

2. **Screen Reader Testing**:
   - Form labels are properly associated
   - ARIA labels added where needed
   - Semantic HTML maintained

3. **Color Contrast**:
   - Text meets WCAG AA standards (4.5:1 for normal text)
   - Interactive elements have sufficient contrast
   - Focus indicators are visible

## Implementation Notes

### Migration Strategy

1. **Phase 1**: Set up design tokens in index.css
2. **Phase 2**: Update App.jsx and App.css
3. **Phase 3**: Update SensorInputForm component
4. **Phase 4**: Update display components (Prediction, Explainability, SystemHealth)
5. **Phase 5**: Final polish and responsive testing

### Browser Compatibility

- CSS custom properties are supported in all modern browsers
- Fallbacks not required for target audience (engineers using modern browsers)
- Grid and Flexbox have excellent support

### Performance Considerations

- No performance impact expected from CSS changes
- Existing React rendering behavior unchanged
- Chart libraries (Recharts) remain the same

### Future Enhancements

Potential improvements beyond this redesign:
- Dark mode support using CSS variables
- Animation and transition refinements
- Additional chart customization options
- Enhanced mobile-specific interactions
