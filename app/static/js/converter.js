// static/js/services/converter.js
class Converter {
    constructor() {
        this.fromInput = document.getElementById('fromValue');
        this.toInput = document.getElementById('toValue');
        this.category = document.querySelector('[data-category]')?.dataset.category;
        this.fromUnit = document.querySelector('[data-from-unit]')?.dataset.fromUnit;
        this.toUnit = document.querySelector('[data-to-unit]')?.dataset.toUnit;

        this.conversionHistory = [];
        this.maxHistoryItems = 10;

        this.initializeConverter();
        this.loadHistory();
    }

    initializeConverter() {
        if (this.fromInput && this.toInput) {
            this.fromInput.addEventListener('input', () => this.handleConversion());

            // Add copy button functionality
            const copyBtn = document.getElementById('copyResult');
            if (copyBtn) {
                copyBtn.addEventListener('click', () => this.copyToClipboard());
            }

            // Add swap button functionality
            const swapBtn = document.getElementById('swapUnits');
            if (swapBtn) {
                swapBtn.addEventListener('click', () => this.swapUnits());
            }

            // Initialize tooltips
            this.initTooltips();
        }
    }

    async handleConversion() {
        const value = this.fromInput.value;
        if (!value) {
            this.toInput.value = '';
            return;
        }

        try {
            const response = await fetch(`/api/convert`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    category: this.category,
                    fromUnit: this.fromUnit,
                    toUnit: this.toUnit,
                    value: parseFloat(value)
                })
            });

            const data = await response.json();
            if (data.success) {
                this.toInput.value = this.formatResult(data.result);
                this.addToHistory({
                    fromValue: value,
                    fromUnit: this.fromUnit,
                    toValue: data.result,
                    toUnit: this.toUnit,
                    timestamp: new Date()
                });
            } else {
                this.showError(data.error || 'Conversion failed');
            }
        } catch (error) {
            console.error('Conversion error:', error);
            this.showError('An error occurred during conversion');
        }
    }

    formatResult(value) {
        // Handle different number formats based on magnitude
        if (Math.abs(value) >= 1e6 || Math.abs(value) <= 1e-6) {
            return value.toExponential(6);
        }
        return Number(value.toPrecision(10)).toString();
    }

    copyToClipboard() {
        const textToCopy = `${this.fromInput.value} ${this.fromUnit} = ${this.toInput.value} ${this.toUnit}`;
        navigator.clipboard.writeText(textToCopy).then(() => {
            this.showTooltip('Copied!');
        }).catch(err => {
            console.error('Failed to copy:', err);
            this.showError('Failed to copy to clipboard');
        });
    }

    swapUnits() {
        // Swap URL parameters
        const newUrl = window.location.pathname.replace(
            `${this.fromUnit}-to-${this.toUnit}`,
            `${this.toUnit}-to-${this.fromUnit}`
        );
        window.location.href = newUrl;
    }

    addToHistory(conversion) {
        this.conversionHistory.unshift(conversion);
        if (this.conversionHistory.length > this.maxHistoryItems) {
            this.conversionHistory.pop();
        }
        localStorage.setItem('conversionHistory', JSON.stringify(this.conversionHistory));
        this.updateHistoryUI();
    }

    loadHistory() {
        const savedHistory = localStorage.getItem('conversionHistory');
        if (savedHistory) {
            this.conversionHistory = JSON.parse(savedHistory);
            this.updateHistoryUI();
        }
    }

    updateHistoryUI() {
        const historyContainer = document.getElementById('conversionHistory');
        if (!historyContainer) return;

        const historyHTML = this.conversionHistory.map(item => `
            <div class="history-item">
                <span class="timestamp">${new Date(item.timestamp).toLocaleString()}</span>
                <div class="conversion">
                    ${item.fromValue} ${item.fromUnit} = ${item.toValue} ${item.toUnit}
                </div>
            </div>
        `).join('');

        historyContainer.innerHTML = historyHTML || '<p>No conversion history</p>';
    }

    showError(message) {
        const errorContainer = document.getElementById('errorContainer');
        if (errorContainer) {
            errorContainer.textContent = message;
            errorContainer.style.display = 'block';
            setTimeout(() => {
                errorContainer.style.display = 'none';
            }, 3000);
        }
    }

    showTooltip(message) {
        const tooltip = document.getElementById('copyTooltip');
        if (tooltip) {
            tooltip.setAttribute('data-original-title', message);
            bootstrap.Tooltip.getInstance(tooltip).show();
            setTimeout(() => {
                bootstrap.Tooltip.getInstance(tooltip).hide();
            }, 1000);
        }
    }

    initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
}

// Initialize converter when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Converter();
});