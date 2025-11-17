# Requirements Document

## Introduction

This document outlines the requirements for redesigning the AIMS (AI Marine Engineering System) frontend user interface to align with the SoftModernSaaS design system. The redesign will transform the current functional but basic UI into a modern, approachable, and visually cohesive interface that follows established design principles including soft shadows, generous spacing, card-based layouts, and a muted color palette with purposeful accents.

## Glossary

- **AIMS**: AI Marine Engineering System - the application that provides fault prediction for marine engines
- **Frontend Application**: The React-based user interface that engineers interact with
- **Design System**: The SoftModernSaaS design guidelines defined in design.json
- **Sensor Input Form**: The component where users enter or load sensor data for analysis
- **Prediction Display**: The component showing fault prediction results and confidence scores
- **Explainability Display**: The component visualizing SHAP values to explain predictions
- **System Health Radar**: The component showing sensor values against safe operating ranges
- **Card Component**: A primary content container with white background, rounded corners, and soft shadows

## Requirements

### Requirement 1

**User Story:** As an engineer, I want the application to have a modern and approachable visual design, so that I feel confident and comfortable using the system for critical fault diagnosis.

#### Acceptance Criteria

1. THE Frontend Application SHALL apply the SoftModernSaaS color palette with base colors (white #FFFFFF, black #1A202C, offWhite #F9FAFB) and neutral colors for text and borders
2. THE Frontend Application SHALL use rounded corners with border-radius values of 8px (md), 12px (lg), or 16px (xl) for all card components and containers
3. THE Frontend Application SHALL apply soft diffused shadows (0px 10px 15px -3px rgba(0,0,0,0.05)) to card components to create depth and layering
4. THE Frontend Application SHALL use an 8-point grid spacing system with values of 8px (sm), 16px (md), 24px (lg), 32px (xl), and 48px (xxl)
5. THE Frontend Application SHALL replace the current gradient header background with the primary.main color (#2D3748) and apply appropriate contrast text

### Requirement 2

**User Story:** As an engineer, I want clear visual hierarchy and readable typography throughout the interface, so that I can quickly scan and understand information without strain.

#### Acceptance Criteria

1. THE Frontend Application SHALL use a clean geometric sans-serif font family (Inter, Roboto, or system-default font stack)
2. THE Frontend Application SHALL apply heading styles with font-size 24px and font-weight 700 for modal and section titles
3. THE Frontend Application SHALL apply label styles with font-size 14px and font-weight 600 for form field labels
4. THE Frontend Application SHALL apply body text styles with font-size 16px and font-weight 400 for descriptive text
5. THE Frontend Application SHALL use neutral.textPrimary (#1A202C) for primary text and neutral.textSecondary (#6B7280) for secondary text

### Requirement 3

**User Story:** As an engineer, I want the sensor input form to be presented in a clean card-based layout, so that I can easily focus on entering data without visual clutter.

#### Acceptance Criteria

1. THE Sensor Input Form SHALL be contained within a card component with white background, 16px border-radius, and soft shadow
2. THE Sensor Input Form SHALL apply 24px or 32px padding to the card container
3. THE Sensor Input Form SHALL style input fields with 1px solid border (#CBD5E0), 8px border-radius, and 12px vertical padding
4. WHEN an input field receives focus, THE Sensor Input Form SHALL change the border color to accent.info (#818CF8)
5. THE Sensor Input Form SHALL display field labels above inputs using the label typography style (14px, font-weight 600)

### Requirement 4

**User Story:** As an engineer, I want action buttons to follow consistent styling patterns, so that I can immediately identify primary actions versus secondary options.

#### Acceptance Criteria

1. THE Frontend Application SHALL style primary action buttons with primary.main background (#2D3748), white text, font-weight 600, 8px border-radius, and 12px vertical padding
2. THE Frontend Application SHALL style secondary action buttons with transparent background, neutral.textSecondary color, font-weight 600, 8px border-radius, and 1px solid border
3. THE Frontend Application SHALL apply a soft shadow (0px 4px 6px -1px rgba(0,0,0,0.05)) to primary buttons
4. WHEN a user hovers over a button, THE Frontend Application SHALL provide visual feedback through subtle background color changes
5. THE Frontend Application SHALL ensure all buttons have minimum touch target size of 44px height for accessibility

### Requirement 5

**User Story:** As an engineer, I want prediction results and analysis displays to be organized in distinct card sections, so that I can easily distinguish between different types of information.

#### Acceptance Criteria

1. THE Prediction Display SHALL be contained within a card component with white background, 16px border-radius, and soft shadow
2. THE Explainability Display SHALL be contained within a separate card component with consistent styling
3. THE System Health Radar SHALL be contained within a separate card component with consistent styling
4. THE Frontend Application SHALL apply 16px vertical spacing between adjacent card components
5. THE Frontend Application SHALL ensure each card has 24px internal padding for content

### Requirement 6

**User Story:** As an engineer, I want status indicators and alerts to use purposeful color coding, so that I can quickly identify the severity and type of information being presented.

#### Acceptance Criteria

1. THE Frontend Application SHALL use accent.success (#34D399) for successful operations and normal status indicators
2. THE Frontend Application SHALL use accent.warning (#FBBF24) for warning states and caution indicators
3. THE Frontend Application SHALL use accent.danger (#F87171) for error states and critical alerts
4. WHEN displaying an alert message, THE Frontend Application SHALL use a 4px left border with status-specific color and white card background
5. THE Frontend Application SHALL apply light background tints (successLight, warningLight, dangerLight) for alert containers when appropriate

### Requirement 7

**User Story:** As an engineer, I want the welcome screen to be inviting and informative, so that I understand the system capabilities before starting my first analysis.

#### Acceptance Criteria

1. THE Frontend Application SHALL display the welcome message in a centered card component with generous padding (40px or more)
2. THE Frontend Application SHALL present feature descriptions in a vertical list with clear iconography
3. THE Frontend Application SHALL style feature items with subtle background colors and 8px border-radius
4. THE Frontend Application SHALL use heading typography (24px, font-weight 700) for the welcome title
5. THE Frontend Application SHALL ensure feature descriptions use body text typography with adequate line-height (1.6 or greater)

### Requirement 8

**User Story:** As an engineer, I want the application to be responsive and work well on different screen sizes, so that I can access it from various devices in the field.

#### Acceptance Criteria

1. WHEN the viewport width is less than 1024px, THE Frontend Application SHALL switch from a two-column grid layout to a single-column layout
2. WHEN the viewport width is less than 768px, THE Frontend Application SHALL reduce heading font sizes proportionally
3. THE Frontend Application SHALL maintain minimum 16px horizontal padding on mobile viewports
4. THE Frontend Application SHALL ensure all interactive elements remain accessible with appropriate touch target sizes on mobile devices
5. THE Frontend Application SHALL preserve card-based layout structure across all breakpoints

### Requirement 9

**User Story:** As an engineer, I want loading states to be clearly communicated with appropriate visual feedback, so that I know the system is processing my request.

#### Acceptance Criteria

1. WHEN the system is processing a prediction, THE Frontend Application SHALL display a loading indicator within a card component
2. THE Frontend Application SHALL center the loading spinner and message within the container
3. THE Frontend Application SHALL use neutral.textSecondary color for loading message text
4. THE Frontend Application SHALL apply smooth animation to the loading spinner
5. THE Frontend Application SHALL ensure the loading state card maintains consistent styling with other cards (white background, shadow, border-radius)

### Requirement 10

**User Story:** As an engineer, I want consistent spacing and alignment throughout the interface, so that the application feels polished and professional.

#### Acceptance Criteria

1. THE Frontend Application SHALL apply consistent 20px padding to the main application container
2. THE Frontend Application SHALL use 20px gap spacing between grid columns in the two-column layout
3. THE Frontend Application SHALL maintain consistent internal padding (24px or 32px) across all card components
4. THE Frontend Application SHALL apply consistent vertical spacing (16px to 24px) between stacked elements within cards
5. THE Frontend Application SHALL ensure all text elements follow the 8-point grid system for margins and padding
