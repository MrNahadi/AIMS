# Requirements Document

## Introduction

This document outlines the requirements for enhancing the AIMS glossary modal to improve its visual design consistency with the SoftModernSaaS design system and replace the text-based button with a more subtle info icon trigger. The glossary modal currently exists and functions properly, but the trigger button needs to be redesigned to use an icon-based approach that is less visually prominent while remaining accessible.

## Glossary

- **AIMS**: AI Marine Engineering System - the application that provides fault prediction for marine engines
- **Glossary Modal**: A modal dialog that displays explanations of key features and terminology used in the AIMS application
- **Info Icon**: A circular icon containing the letter "i" that indicates additional information is available
- **Icon Button**: A button component styled to display only an icon without visible text label
- **Design System**: The SoftModernSaaS design guidelines defined in design.json

## Requirements

### Requirement 1

**User Story:** As an engineer, I want the glossary trigger to be a subtle info icon instead of a prominent button, so that it doesn't compete visually with primary actions while remaining discoverable.

#### Acceptance Criteria

1. THE Glossary Modal SHALL be triggered by an icon button displaying an info icon (i) instead of a text button labeled "Glossary"
2. THE Icon Button SHALL use the iconography style defined in the design system with line-art/outline appearance
3. THE Icon Button SHALL have a default size of 20px as specified in the design system iconography guidelines
4. THE Icon Button SHALL use neutral.textSecondary color (#6B7280) for the icon
5. THE Icon Button SHALL include an aria-label attribute with value "Open glossary" for screen reader accessibility

### Requirement 2

**User Story:** As an engineer, I want the info icon button to provide clear visual feedback on interaction, so that I know it is clickable and responsive.

#### Acceptance Criteria

1. WHEN a user hovers over the info icon button, THE Icon Button SHALL change its background to neutral.background (#F7FAFC)
2. THE Icon Button SHALL have a circular shape using border-radius: var(--radius-full)
3. THE Icon Button SHALL have padding of 8px to create adequate touch target size
4. THE Icon Button SHALL have a minimum touch target size of 44px for accessibility compliance
5. WHEN a user focuses the icon button via keyboard, THE Icon Button SHALL display a visible focus ring using the accent.info color

### Requirement 3

**User Story:** As an engineer, I want the glossary modal to follow all design system rules consistently, so that it feels cohesive with the rest of the application.

#### Acceptance Criteria

1. THE Glossary Modal SHALL use the cardsAndModals component styling from the design system
2. THE Glossary Modal SHALL apply background color of base.white (#FFFFFF)
3. THE Glossary Modal SHALL use border-radius of borderRadius.xl (16px)
4. THE Glossary Modal SHALL apply padding of layoutAndSpacing.xl (32px) to the modal container
5. THE Glossary Modal SHALL apply the shadow definition: "0px 10px 15px -3px rgba(0,0,0,0.05), 0px 4px 6px -2px rgba(0,0,0,0.05)"

### Requirement 4

**User Story:** As an engineer, I want the glossary modal header to follow design system typography and spacing rules, so that it maintains visual consistency with other modal components.

#### Acceptance Criteria

1. THE Glossary Modal header SHALL use the "Heading (Large)" typography style with font-size 1.5rem (24px) and font-weight 700
2. THE Glossary Modal header SHALL use neutral.textPrimary color (#1A202C) for the title text
3. THE Glossary Modal header SHALL include a close icon button in the top-right corner
4. THE Close Icon Button SHALL follow the iconButton component styling from the design system
5. THE Glossary Modal header SHALL apply padding of layoutAndSpacing.lg (24px)

### Requirement 5

**User Story:** As an engineer, I want the glossary content sections to be clearly organized and easy to scan, so that I can quickly find the information I need.

#### Acceptance Criteria

1. THE Glossary Modal content SHALL apply padding of layoutAndSpacing.xl (32px)
2. THE Glossary Modal content sections SHALL be separated by 1px borders using neutral.borderLight color (#E2E8F0)
3. THE Glossary Modal section headings SHALL use the "Heading (Medium)" typography style with font-size 1.25rem (20px) and font-weight 600
4. THE Glossary Modal section body text SHALL use the "Body (Default)" typography style with font-size 1rem (16px) and neutral.textSecondary color
5. THE Glossary Modal SHALL apply spacing of layoutAndSpacing.lg (24px) between sections

### Requirement 6

**User Story:** As an engineer, I want the glossary modal to be responsive and work well on mobile devices, so that I can access help information regardless of my device.

#### Acceptance Criteria

1. WHEN the viewport width is less than 768px, THE Glossary Modal SHALL reduce padding to layoutAndSpacing.md (16px)
2. WHEN the viewport width is less than 768px, THE Glossary Modal header title SHALL reduce font-size to 1.25rem (20px)
3. WHEN the viewport width is less than 768px, THE Glossary Modal section headings SHALL reduce font-size to 1.125rem (18px)
4. THE Glossary Modal SHALL maintain readability and usability across all viewport sizes
5. THE Glossary Modal SHALL ensure the close button remains accessible on mobile devices with adequate touch target size
