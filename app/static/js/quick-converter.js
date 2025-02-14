class QuickConverter {
    constructor() {
        console.log('QuickConverter: Initializing');

        // Input and output elements
        this.fromValue = document.getElementById('quickFromValue');
        this.toValue = document.getElementById('quickToValue');

        // Determine page type
        this.isConversionPage = window.location.pathname.startsWith('/convert/');

        // Select elements (main page) or data attributes (conversion page)
        if (!this.isConversionPage) {
            // Main page - use select elements
            this.fromUnitSelect = document.getElementById('quickFromUnit');
            this.toUnitSelect = document.getElementById('quickToUnit');
        } else {
            // Conversion page - use data attributes
            const container = document.querySelector('[data-category]');
            this.category = container ? container.getAttribute('data-category') : null;
            this.fromUnit = container ? container.getAttribute('data-from-unit') : null;
            this.toUnit = container ? container.getAttribute('data-to-unit') : null;
        }

        // Buttons
        this.swapBtn = document.getElementById('quickSwapBtn');
        this.copyBtn = document.getElementById('quickCopyBtn');
        this.shareBtn = document.getElementById('quickShareBtn');

        // Error display
        this.errorContainer = document.getElementById('quickConverterError');

        // Validate and initialize
        if (this.validateElements()) {
            this.parseUrlParameters();
            this.attachEventListeners();
        }
    }

    validateElements() {
        const elementsToCheck = [
            { element: this.fromValue, name: 'From Value Input' },
            { element: this.toValue, name: 'To Value Input' }
        ];

        // Add select elements check for main page
        if (!this.isConversionPage) {
            elementsToCheck.push(
                { element: this.fromUnitSelect, name: 'From Unit Select' },
                { element: this.toUnitSelect, name: 'To Unit Select' }
            );
        }

        const missingElements = elementsToCheck.filter(({ element, name }) => !element);

        if (missingElements.length > 0) {
            console.error('Critical elements not found:',
                missingElements.map(el => el.name).join(', ')
            );

            this.showError('Conversion elements could not be initialized.');
            return false;
        }

        return true;
    }

    parseUrlParameters() {
        const urlParams = new URLSearchParams(window.location.search);
        const valueParam = urlParams.get('value');

        // Handle URL value for conversion page
        if (this.isConversionPage && valueParam) {
            this.fromValue.value = valueParam;

            // Attempt conversion
            requestAnimationFrame(() => {
                this.attemptConversion();
            });
        }
    }

    attachEventListeners() {
        // Input value event
        if (this.fromValue) {
            this.fromValue.addEventListener('input', this.debouncedConversion.bind(this));
        }

        // Main page specific listeners
        if (!this.isConversionPage) {
            this.attachMainPageListeners();
        }

        // Buttons
        if (this.swapBtn) {
            this.swapBtn.addEventListener('click', this.swapUnits.bind(this));
        }
        if (this.copyBtn) {
            this.copyBtn.addEventListener('click', this.copyConversion.bind(this));
        }
        if (this.shareBtn) {
            this.shareBtn.addEventListener('click', this.shareConversion.bind(this));
        }
    }

    attachMainPageListeners() {
        // From unit selection
        this.fromUnitSelect.addEventListener('change', (e) => {
            this.filterToUnits();
            this.attemptConversion();
        });

        // To unit selection
        this.toUnitSelect.addEventListener('change', () => {
            this.attemptConversion();
        });
    }

    filterToUnits() {
        // Only for main page
        if (this.isConversionPage) return;

        const selectedFromUnit = this.fromUnitSelect.value;
        if (!selectedFromUnit) return;

        const [selectedCategory] = selectedFromUnit.split('|');

        // Hide/show to unit options based on category
        let firstMatchingOption = null;
        let currentToValue = this.toUnitSelect.value;
        let currentToOptionStillValid = false;

        Array.from(this.toUnitSelect.options).forEach(option => {
            if (option.value) {
                const [category] = option.value.split('|');
                const isMatching = category === selectedCategory;
                option.style.display = isMatching ? '' : 'none';

                if (isMatching) {
                    if (!firstMatchingOption) {
                        firstMatchingOption = option;
                    }

                    // Check if current to value is still valid
                    if (option.value === currentToValue) {
                        currentToOptionStillValid = true;
                    }
                }
            }
        });

        // Select first matching option if current selection is no longer valid
        if (!currentToOptionStillValid && firstMatchingOption) {
            this.toUnitSelect.value = firstMatchingOption.value;
        }
    }

    debouncedConversion() {
        if (this.conversionTimeout) {
            clearTimeout(this.conversionTimeout);
        }

        this.conversionTimeout = setTimeout(() => {
            this.attemptConversion();
        }, 300);
    }

    canConvert() {
        if (this.isConversionPage) {
            // Conversion page check
            return !!(
                this.fromValue?.value &&
                this.category &&
                this.fromUnit &&
                this.toUnit
            );
        } else {
            // Main page check
            return !!(
                this.fromValue?.value &&
                this.fromUnitSelect?.value &&
                this.toUnitSelect?.value
            );
        }
    }

    async attemptConversion() {
        // Validate conversion is possible
        if (!this.canConvert()) {
            console.log('QuickConverter: Cannot convert - missing inputs');
            return;
        }

        try {
            // Prepare conversion payload
            let payload;
            if (this.isConversionPage) {
                payload = {
                    category: this.category,
                    fromUnit: this.fromUnit,
                    toUnit: this.toUnit,
                    value: parseFloat(this.fromValue.value)
                };
            } else {
                const [fromCategory, fromUnit] = this.fromUnitSelect.value.split('|');
                const [toCategory, toUnit] = this.toUnitSelect.value.split('|');
                payload = {
                    category: fromCategory,
                    fromUnit: fromUnit,
                    toUnit: toUnit,
                    value: parseFloat(this.fromValue.value)
                };
            }

            console.log('QuickConverter: Conversion payload', payload);

            // Send conversion request
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            console.log('Conversion response:', data);

            // Handle conversion result
            if (data.success) {
                this.toValue.value = data.formatted;
                this.updateActionButtons(true);
            } else {
                this.toValue.value = '';
                this.updateActionButtons(false);
                this.showError(data.message || 'Conversion failed');
            }
        } catch (error) {
            console.error('QuickConverter: Conversion error', error);
            this.toValue.value = '';
            this.updateActionButtons(false);
            this.showError('An error occurred during conversion');
        }
    }

    updateActionButtons(enabled = false) {
        if (this.copyBtn) {
            this.copyBtn.disabled = !enabled;
        }
        if (this.shareBtn) {
            this.shareBtn.disabled = !enabled;
        }
    }

    showError(message) {
        if (this.errorContainer) {
            this.errorContainer.textContent = message;
            this.errorContainer.style.display = 'block';
        }
    }

    swapUnits() {
        if (this.isConversionPage) {
            // For conversion sub-page, redirect to swapped URL
            const currentUrl = window.location.pathname;
            const [category, units] = currentUrl.split('/').slice(2);
            const [fromUnit, toUnit] = units.split('-to-');

            // Construct new URL with swapped units
            const newUrl = `/convert/${category}/${toUnit}-to-${fromUnit}`;

            // If there's a value, pass it to the new page
            const valueParam = this.fromValue.value ? `?value=${this.toValue.value}` : '';

            window.location.href = newUrl + valueParam;
        } else {
            // For main page, swap unit selections
            const fromValue = this.fromUnitSelect.value;
            const toValue = this.toUnitSelect.value;

            this.fromUnitSelect.value = toValue;
            this.toUnitSelect.value = fromValue;

            // Refilter units and attempt conversion
            this.filterToUnits();

            // Swap input and output values
            const tempValue = this.fromValue.value;
            this.fromValue.value = this.toValue.value;
            this.toValue.value = tempValue;

            // Trigger conversion
            this.attemptConversion();
        }
    }

    copyConversion() {
        if (!this.fromValue.value || !this.toValue.value) return;

        // Get symbols for main page or conversion page
        let fromSymbol, toSymbol;
        if (this.isConversionPage) {
            fromSymbol = document.querySelector('.input-group-text:first-of-type').textContent;
            toSymbol = document.querySelector('.input-group-text:last-of-type').textContent;
        } else {
            const fromOption = this.fromUnitSelect.selectedOptions[0];
            const toOption = this.toUnitSelect.selectedOptions[0];

            const fromMatch = fromOption.text.match(/\((.*?)\)/);
            const toMatch = toOption.text.match(/\((.*?)\)/);

            fromSymbol = fromMatch ? fromMatch[1] : '';
            toSymbol = toMatch ? toMatch[1] : '';
        }

        const textToCopy = `${this.fromValue.value} ${fromSymbol} = ${this.toValue.value} ${toSymbol}`;

        navigator.clipboard.writeText(textToCopy)
            .then(() => this.showTooltip(this.copyBtn, 'Copied!'))
            .catch(err => console.error('Copy failed:', err));
    }

    shareConversion() {
        let category, fromUnit, toUnit;

        if (this.isConversionPage) {
            // Get from URL for conversion page
            const pathParts = window.location.pathname.split('/');
            category = pathParts[2];
            [fromUnit, toUnit] = pathParts[3].split('-to-');
        } else {
            // Get from select for main page
            const [fromCategory, fromUnitId] = this.fromUnitSelect.value.split('|');
            const [, toUnitId] = this.toUnitSelect.value.split('|');

            category = fromCategory;
            fromUnit = fromUnitId;
            toUnit = toUnitId;
        }

        const shareUrl = new URL(`/convert/${category}/${fromUnit}-to-${toUnit}`, window.location.origin);
        shareUrl.searchParams.set('value', this.fromValue.value);

        navigator.clipboard.writeText(shareUrl.toString())
            .then(() => this.showTooltip(this.shareBtn, 'Link copied!'))
            .catch(err => console.error('Share failed:', err));
    }

    showTooltip(element, message) {
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            const tooltip = bootstrap.Tooltip.getInstance(element) ||
                new bootstrap.Tooltip(element);

            element.setAttribute('data-bs-original-title', message);
            tooltip.show();

            setTimeout(() => tooltip.hide(), 1000);
        }
    }
}

// Initialize converter when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('QuickConverter: DOM fully loaded');
    new QuickConverter();
});