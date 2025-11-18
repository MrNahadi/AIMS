# Implementation Plan

- [x] 1. Replace glossary text button with info icon button





  - Remove existing `.glossary-btn` CSS styles from App.css
  - Create new `.info-icon-btn` CSS class with transparent background, circular hover state, and proper focus styles
  - Update button markup in App.jsx to use inline SVG info icon (circle with "i")
  - Ensure icon button has 20px size, neutral.textSecondary color, and 44px minimum touch target
  - Add hover state with background color change to neutral.background
  - Add focus state with info color ring for keyboard accessibility
  - Maintain aria-label="Open glossary" and add title="View glossary" for accessibility
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 2. Refine glossary modal styling for design system compliance






  - [x] 2.1 Update modal container styling

    - Verify background uses var(--color-white)
    - Ensure border-radius uses var(--radius-xl) (16px)
    - Apply exact shadow specification: "0px 10px 15px -3px rgba(0,0,0,0.05), 0px 4px 6px -2px rgba(0,0,0,0.05)"
    - Verify max-width and responsive behavior
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_


  - [x] 2.2 Update modal header styling

    - Apply padding of var(--spacing-lg) (24px)
    - Set title font-size to 1.5rem (24px) and font-weight to var(--font-weight-bold) (700)
    - Use var(--color-text-primary) for title color
    - Add border-bottom with var(--color-border-light)
    - Update close button to follow iconButton pattern with circular hover state
    - Ensure close button has 44px minimum touch target
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_


  - [x] 2.3 Update modal content section styling

    - Apply padding of var(--spacing-xl) (32px) to content container
    - Set section spacing to var(--spacing-lg) (24px) between sections
    - Apply 1px borders between sections using var(--color-border-light)
    - Set section heading font-size to 1.25rem (20px) and font-weight to var(--font-weight-semibold) (600)
    - Use var(--color-text-primary) for section headings
    - Set body text font-size to 1rem (16px) and color to var(--color-text-secondary)
    - Ensure line-height of 1.6 for body text
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_


  - [x] 2.4 Update responsive styles for mobile

    - Reduce modal padding to var(--spacing-md) (16px) on viewports < 768px
    - Reduce header title font-size to 1.25rem (20px) on mobile
    - Reduce section heading font-size to 1.125rem (18px) on mobile
    - Reduce content padding to var(--spacing-lg) (24px) on mobile
    - Verify close button and icon button maintain 44px touch targets on mobile
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 3. Update header layout to accommodate icon button





  - Ensure header uses flexbox with space-between alignment
  - Verify icon button aligns properly with header title
  - Add appropriate gap spacing between header elements
  - Test header layout on mobile viewports
  - _Requirements: 1.1, 2.4_

- [x] 4. Test and verify implementation






  - [x] 4.1 Visual testing

    - Verify icon button renders at 20px with correct color
    - Check hover state shows circular background
    - Verify focus ring appears on keyboard focus
    - Confirm modal shadow matches design system specification
    - Check all typography sizes and weights are correct
    - Verify spacing matches design system values
    - _Requirements: All requirements_


  - [x] 4.2 Responsive testing

    - Test on desktop (>1024px) - verify full-size typography and spacing
    - Test on tablet (768px-1024px) - verify layout maintains integrity
    - Test on mobile (<768px) - verify reduced typography and padding
    - Confirm icon button maintains 44px touch target on all viewports
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [x] 4.3 Accessibility testing


    - Test keyboard navigation (Tab to button, Enter to open, Escape to close)
    - Verify aria-label is announced by screen readers
    - Check focus management (focus moves to modal, returns to button on close)
    - Verify all interactive elements have visible focus states
    - Test with NVDA or JAWS screen reader
    - _Requirements: 1.5, 2.5, 4.4, 6.5_

  - [x] 4.4 Cross-browser testing


    - Test in Chrome - verify SVG rendering and CSS custom properties
    - Test in Firefox - verify transitions and focus states
    - Test in Safari - verify shadow rendering and SVG support
    - Test in Edge - verify overall appearance and functionality
    - _Requirements: All requirements_
