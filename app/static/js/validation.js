/* static/js/utils/validation.js */
const validateInput = (value) => {
    return !isNaN(value) && value !== '';
};

const formatNumber = (number) => {
    return new Intl.NumberFormat('en-US', {
        maximumSignificantDigits: 10
    }).format(number);
};