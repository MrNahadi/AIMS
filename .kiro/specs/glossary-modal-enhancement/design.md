# Design Document

## Overview

This design document outlines the approach for enhancing the AIMS glossary modal to improve its visual consistency with the SoftModernSaaS design system and replace the text-based trigger button with a more subtle info icon. The enhancement focuses on two main areas:

1. **Icon Button Redesign**: Replace the current "📖 Glossary" text button with a clean info icon (i) that follows the design system's iconography guidelines
2. **Modal Styling Refinement**: Ensure the glossary modal strictly adheres to all design system rules for cards, modals, typography, and spacing

The existing functionality remains unchanged - this is purely a visual enhancement to improve consistency and reduce visual clutter in the header area.

## Architecture

### Component Structure

The glossary feature consists of two main components:

```
App.jsx
├── Header section
│   └── Info Icon Button (trigger)
└── GlossaryModal component
    ├── Modal overlay
    └── Modal content
        ├── Header (title + close button)
        └── Content sections
```

### Styling Approach

The enhancement will update:
1. **App.css** - Replace `.glossary-btn` styles with `.info-icon-btn` styles
2. **GlossaryModal.css** - Refine existing styles to strictly follow design system rules
3. **App.jsx** - Update button markup to use icon instead of text

All styling will reference CSS custom properties already defined in `index.css` from the frontend-ui-redesign implementation.

## Components and Interfaces

### 1. Info Icon Button Component

**Location**: App.jsx header section

**Current Implementation**:
```jsx
<button
    className="glossary-btn"
    onClick={() => setIsGlossaryOpen(true)}
    aria-label="Open glossary"
>
    📖 Glossary
</button>
```

**New Implementation**:
```jsx
<button
    className="info-icon-btn"
    onClick={() => setIsGlossaryOpen(true)}
    aria-label="Open glossary"
    title="View glossary"
>
    <svg 
        width="20" 
        height="20" 
        viewBox="0 0 24 24" 
        fill="none" 
        stroke="currentColor" 
        strokeWidth="2" 
        strokeLinecap="round" 
        strokeLinejoin="round"
    >
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="16" x2="12" y2="12"></line>
        <line x1="12" y1="8" x2="12.01" y2="8"></line>
    </svg>
</button>
```

**Design Rationale**:
- Uses inline SVG for the info icon to maintain design system's line-art style
- SVG allows for proper scaling and color inheritance
- Maintains accessibility with aria-label and title attributes
- Icon is 20px as specified in design system iconography guidelines

**CSS Styling** (App.css):

```css
.info-icon-btn {
    background: transparent;
    border: none;
    color: var(--color-text-secondary);
    padding: var(--spacing-sm);
    border-radius: var(--radius-full);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s ease, color 0.2s ease;
    min-width: 44px;
    min-height: 44px;
}

.info-icon-btn:hover {
    background: var(--color-background);
    color: var(--color-text-primary);
}

.info-icon-btn:focus {
    outline: none;
    box-shadow: 0 0 0 3px var(--color-info-light);
    border: 2px solid var(--color-info);
}

.info-icon-btn:active {
    background: var(--color-border-light);
}

.info-icon-btn svg {
    width: 20px;
    height: 20px;
    stroke-width: 2px;
}
```

**Key Design Decisions**:
- Transparent background by default to minimize visual weight
- Circular hover state (border-radius: full) as per iconButton design pattern
- 8px padding creates adequate touch target with min 44px size
- Smooth transitions for professional feel
- Focus state uses info color for consistency with other interactive elements
- Active state provides tactile feedback

### 2. Glossary Modal Refinement

**Location**: GlossaryModal.jsx and GlossaryModal.css

**Modal Overlay**:

Current implementation is mostly correct, but we'll ensure strict adherence:

```css
.glossary-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: var(--spacing-lg);
}
```

**Modal Container**:

Ensure exact compliance with cardsAndModals design pattern:

```css
.glossary-modal {
    background: var(--color-white);
    border-radius: var(--radius-xl);
    max-width: 700px;
    width: 100%;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0px 10px 15px -3px rgba(0, 0, 0, 0.05), 
                0px 4px 6px -2px rgba(0, 0, 0, 0.05);
}
```

**Key Changes**:
- Explicitly set shadow to match design system specification
- Ensure border-radius uses xl value (16px)
- Maintain white background

**Modal Header**:

```css
.glossary-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-lg);
    border-bottom: 1px solid var(--color-border-light);
}

.glossary-header h2 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: var(--font-weight-bold);
    color: var(--color-text-primary);
}

.close-btn {
    background: transparent;
    border: none;
    color: var(--color-text-secondary);
    font-size: 1.5rem;
    cursor: pointer;
    padding: var(--spacing-sm);
    border-radius: var(--radius-full);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 44px;
    min-height: 44px;
    transition: background-color 0.2s ease;
}

.close-btn:hover {
    background: var(--color-background);
}

.close-btn:focus {
    outline: none;
    box-shadow: 0 0 0 3px var(--color-info-light);
}
```

**Key Changes**:
- Header padding uses lg (24px) as specified
- Title uses Heading (Large) typography: 1.5rem, font-weight 700
- Close button follows iconButton pattern
- Border-bottom separates header from content

**Modal Content**:

```css
.glossary-content {
    overflow-y: auto;
    padding: var(--spacing-xl);
    flex: 1;
}

.glossary-section {
    padding-bottom: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
    border-bottom: 1px solid var(--color-border-light);
}

.glossary-section:last-child {
    border-bottom: none;
    padding-bottom: 0;
    margin-bottom: 0;
}

.glossary-icon {
    font-size: 2rem;
    margin-bottom: var(--spacing-md);
}

.glossary-section h3 {
    font-size: 1.25rem;
    font-weight: var(--font-weight-semibold);
    color: var(--color-text-primary);
    margin: 0 0 var(--spacing-md) 0;
}

.glossary-section p {
    color: var(--color-text-secondary);
    line-height: 1.6;
    margin: 0 0 var(--spacing-md) 0;
    font-size: 1rem;
}

.glossary-section ul {
    margin: 0;
    padding-left: var(--spacing-lg);
    color: var(--color-text-secondary);
}

.glossary-section li {
    margin-bottom: var(--spacing-xs);
    line-height: 1.6;
}

.glossary-section li strong {
    color: var(--color-text-primary);
    font-weight: var(--font-weight-semibold);
}
```

**Key Changes**:
- Content padding uses xl (32px) as specified
- Section spacing uses lg (24px) between sections
- Section headings use Heading (Medium): 1.25rem, font-weight 600
- Body text uses Body (Default): 1rem, neutral.textSecondary
- Proper line-height (1.6) for readability

**Responsive Styles**:

```css
@media (max-width: 768px) {
    .glossary-overlay {
        padding: var(--spacing-md);
    }

    .glossary-header {
        padding: var(--spacing-md) var(--spacing-lg);
    }

    .glossary-header h2 {
        font-size: 1.25rem;
    }

    .glossary-content {
        padding: var(--spacing-lg);
    }

    .glossary-section h3 {
        font-size: 1.125rem;
    }
}
```

**Key Changes**:
- Reduced padding on mobile for better space utilization
- Proportionally smaller typography on mobile
- Maintains readability and usability

### 3. Header Layout Adjustment

**Location**: App.css

The header layout needs minor adjustment to accommodate the icon button:

```css
.app-header {
    background: var(--color-primary-main);
    color: var(--color-primary-contrast);
    padding: var(--spacing-lg);
    box-shadow: var(--shadow-sm);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header-content {
    display: flex;
    align-items: center;
    gap: var(--spacing-lg);
    flex: 1;
}

.header-title {
    flex: 1;
}

.header-title h1 {
    margin: 0;
    font-size: 1.75rem;
    font-weight: var(--font-weight-bold);
}

.header-title p {
    margin: 0.25rem 0 0 0;
    opacity: 0.9;
    font-size: 0.95rem;
}
```

**Design Rationale**:
- Flexbox layout allows icon button to sit naturally at the end
- Gap spacing maintains consistent spacing between elements
- Icon button aligns vertically with title content

## Data Models

No changes to data models. The glossary modal uses static content and boolean state for open/close.

**Existing State**:
```javascript
const [isGlossaryOpen, setIsGlossaryOpen] = useState(false);
```

This remains unchanged.

## Error Handling

No error handling changes required. The glossary modal is a static content display with no API calls or data fetching.

## Testing Strategy

### Visual Testing

1. **Icon Button Appearance**:
   - Verify icon renders correctly at 20px size
   - Check color is neutral.textSecondary (#6B7280)
   - Confirm circular shape on hover
   - Test hover background color change
   - Verify focus ring appears on keyboard focus
   - Check active state feedback

2. **Modal Styling**:
   - Verify modal background is white
   - Check border-radius is 16px
   - Confirm shadow matches design system specification
   - Verify header uses correct typography (24px, bold)
   - Check section headings use correct typography (20px, semibold)
   - Verify body text uses correct color and size

3. **Spacing Verification**:
   - Check header padding is 24px
   - Verify content padding is 32px
   - Confirm section spacing is 24px
   - Check icon button padding creates 44px touch target

### Responsive Testing

1. **Desktop (>1024px)**:
   - Modal displays centered with max-width 700px
   - Icon button visible and accessible
   - All typography at full size

2. **Tablet (768px - 1024px)**:
   - Modal maintains proper sizing
   - Icon button remains accessible
   - Typography scales appropriately

3. **Mobile (<768px)**:
   - Modal padding reduces to 16px
   - Header title reduces to 20px
   - Section headings reduce to 18px
   - Icon button maintains 44px touch target
   - Close button remains accessible

### Accessibility Testing

1. **Keyboard Navigation**:
   - Tab to info icon button
   - Press Enter/Space to open modal
   - Tab through modal content
   - Tab to close button
   - Press Enter/Space or Escape to close modal

2. **Screen Reader Testing**:
   - Verify aria-label "Open glossary" is announced
   - Check modal title is properly announced
   - Verify close button has proper label
   - Test with NVDA/JAWS on Windows

3. **Focus Management**:
   - Focus moves to modal when opened
   - Focus returns to trigger button when closed
   - Focus ring is clearly visible on all interactive elements

### Cross-Browser Testing

Test in:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

Verify:
- SVG icon renders correctly
- CSS custom properties work
- Transitions are smooth
- Focus states are visible

## Implementation Notes

### Icon Selection

The info icon uses a standard circle with "i" design:
- Circle outline (stroke)
- Vertical line for "i" body
- Dot for "i" top
- Follows line-art style with 2px stroke width

This is a universally recognized symbol for information/help.

### Removal of Old Styles

The following CSS classes will be removed from App.css:
- `.glossary-btn`
- `.glossary-btn:hover`
- Media query styles for `.glossary-btn`

### Migration Path

1. Update App.css with new `.info-icon-btn` styles
2. Remove old `.glossary-btn` styles
3. Update App.jsx button markup to use SVG icon
4. Refine GlossaryModal.css to ensure strict design system compliance
5. Test all interactive states and responsive behavior

### Browser Compatibility

- SVG inline support: All modern browsers
- CSS custom properties: All modern browsers
- Flexbox: All modern browsers
- No fallbacks needed for target audience

### Performance Considerations

- Inline SVG has negligible performance impact
- No additional HTTP requests for icon
- CSS transitions are GPU-accelerated
- Modal rendering performance unchanged

## Future Enhancements

Potential improvements beyond this enhancement:
- Add keyboard shortcut (e.g., "?" key) to open glossary
- Add search/filter functionality for glossary content
- Add deep linking to specific glossary sections
- Consider adding glossary tooltips inline in the UI
