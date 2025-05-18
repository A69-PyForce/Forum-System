/**
 * characterLimitStyles.js
 * This script monitors text fields and applies styling based on character count:
 * - Orange warning when approaching the limit (within 20 characters)
 * - Red styling when the limit is exceeded
 */

(function () {
    // CSS styles to be applied
    const redExceededStyle = `
    border-color: #ff3333 !important;
    box-shadow: 0 0 0 3px rgba(255, 51, 51, 0.25) !important;
  `;

    const orangeWarningStyle = `
    border-color: #ff9933 !important;
    box-shadow: 0 0 0 3px rgba(255, 153, 51, 0.25) !important;
  `;

    // Function to create and inject style elements
    function injectStyles() {
        const styleElement = document.createElement('style');
        styleElement.textContent = `
      .character-limit-exceeded {
        ${redExceededStyle}
      }
      .character-limit-warning {
        ${orangeWarningStyle}
      }
    `;
        document.head.appendChild(styleElement);
    }

    // Track fields and their limits
    const fieldLimits = new Map();
    const warningThreshold = 20; // Characters remaining before showing warning

    // Function to check if limit is exceeded/approaching and apply/remove styling
    function checkLimit(element) {
        const limit = fieldLimits.get(element);
        if (!limit) return;

        const currentLength = element.value.length;
        const charsRemaining = limit - currentLength;

        // Remove both classes first
        element.classList.remove('character-limit-exceeded');
        element.classList.remove('character-limit-warning');

        // Apply appropriate class based on remaining characters
        if (currentLength > limit) {
            element.classList.add('character-limit-exceeded');
        } else if (charsRemaining <= warningThreshold) {
            element.classList.add('character-limit-warning');
        }
    }

    // Function to set up tracking for a specific field
    function setupFieldTracking(element, limit, customWarningThreshold) {
        // Store the limit for this element
        fieldLimits.set(element, limit);

        // Use custom warning threshold if provided, otherwise use default
        const fieldWarningThreshold = customWarningThreshold !== undefined ? customWarningThreshold : warningThreshold;

        // Add input event listener to check limit on each keystroke
        element.addEventListener('input', () => {
            const currentLength = element.value.length;
            const charsRemaining = limit - currentLength;

            // Remove both classes first
            element.classList.remove('character-limit-exceeded');
            element.classList.remove('character-limit-warning');

            // Apply appropriate class based on remaining characters
            if (currentLength > limit) {
                element.classList.add('character-limit-exceeded');
            } else if (charsRemaining <= fieldWarningThreshold) {
                element.classList.add('character-limit-warning');
            }
        });

        // Initial check
        const currentLength = element.value.length;
        const charsRemaining = limit - currentLength;

        if (currentLength > limit) {
            element.classList.add('character-limit-exceeded');
        } else if (charsRemaining <= fieldWarningThreshold) {
            element.classList.add('character-limit-warning');
        }
    }

    // Function to automatically set up tracking based on maxlength attribute
    function autoSetupFields() {
        const textElements = document.querySelectorAll('input[type="text"], input[type="email"], textarea');

        textElements.forEach(element => {
            // Check if the element has a maxlength attribute
            if (element.hasAttribute('maxlength')) {
                const maxLength = parseInt(element.getAttribute('maxlength'));
                setupFieldTracking(element, maxLength);
            }
        });
    }

    // Function to initialize the styling
    function init() {
        injectStyles();
        autoSetupFields();
        console.log('Character limit styling initialized');
    }

    // Initialize when DOM is fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose methods for external use
    window.characterLimitStyles = {
        // Add tracking to a specific element with a custom limit
        trackElement: function (element, charLimit, customWarningThreshold) {
            setupFieldTracking(element, charLimit, customWarningThreshold);
        },

        // Add tracking to all elements matching a selector with the same limit
        trackBySelector: function (selector, charLimit, customWarningThreshold) {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => setupFieldTracking(el, charLimit, customWarningThreshold));
        },

        // Set the global warning threshold (characters remaining)
        setWarningThreshold: function (characters) {
            warningThreshold = characters;
        },

        // Customize the warning style
        setWarningStyle: function (styleRules) {
            const styleElement = document.createElement('style');
            styleElement.textContent = `.character-limit-warning { ${styleRules} }`;
            document.head.appendChild(styleElement);
        },

        // Customize the exceeded style
        setExceededStyle: function (styleRules) {
            const styleElement = document.createElement('style');
            styleElement.textContent = `.character-limit-exceeded { ${styleRules} }`;
            document.head.appendChild(styleElement);
        }
    };
})();