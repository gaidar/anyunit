// static/js/text_file_converter.js

document.addEventListener('DOMContentLoaded', function () {
    // DOM Elements
    const conversionFormatSelect = document.getElementById('conversion-format');
    const inputEditor = document.getElementById('input-editor');
    const outputContent = document.getElementById('output-content');
    const convertBtn = document.getElementById('convert-btn');
    const copyOutputBtn = document.getElementById('copy-output-btn');
    const downloadBtn = document.getElementById('download-btn');
    const loadSampleBtn = document.getElementById('load-sample-btn');
    const errorMessage = document.getElementById('error-message');

    // Event Listeners
    convertBtn.addEventListener('click', convertContent);
    copyOutputBtn.addEventListener('click', copyOutput);
    downloadBtn.addEventListener('click', downloadOutput);
    loadSampleBtn.addEventListener('click', loadSample);
    conversionFormatSelect.addEventListener('change', function () {
        inputEditor.placeholder = getInputPlaceholder(conversionFormatSelect.value);
    });

    // Initialize placeholder
    inputEditor.placeholder = getInputPlaceholder(conversionFormatSelect.value);

    // Conversion Functions
    function convertContent() {
        // Clear previous error messages
        errorMessage.style.display = 'none';
        errorMessage.textContent = '';

        const inputValue = inputEditor.value.trim();
        if (!inputValue) {
            showError('Please enter some content to convert.');
            return;
        }

        const conversionType = conversionFormatSelect.value;
        try {
            let result;
            switch (conversionType) {
                case 'json-to-xml':
                    result = convertJsonToXml(inputValue);
                    break;
                case 'json-to-csv':
                    result = convertJsonToCsv(inputValue);
                    break;
                case 'csv-to-json':
                    result = convertCsvToJson(inputValue);
                    break;
                case 'csv-to-xml':
                    result = convertCsvToXml(inputValue);
                    break;
                case 'xml-to-json':
                    result = convertXmlToJson(inputValue);
                    break;
                case 'xml-to-csv':
                    result = convertXmlToCsv(inputValue);
                    break;
                default:
                    showError('Invalid conversion type.');
                    return;
            }

            // Display the result
            outputContent.textContent = result;

            // Enable the copy and download buttons
            copyOutputBtn.disabled = false;
            downloadBtn.disabled = false;
        } catch (error) {
            showError(`Error during conversion: ${error.message}`);
            outputContent.textContent = '';
            copyOutputBtn.disabled = true;
            downloadBtn.disabled = true;
        }
    }

    // Sample Data Functions
    function loadSample() {
        const conversionType = conversionFormatSelect.value;
        let sampleData = '';

        switch (conversionType) {
            case 'json-to-xml':
            case 'json-to-csv':
                sampleData = `{
  "employees": [
    {
      "id": 1,
      "name": "John Doe",
      "position": "Software Engineer",
      "department": "Engineering",
      "salary": 85000
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "position": "Product Manager",
      "department": "Product",
      "salary": 95000
    },
    {
      "id": 3,
      "name": "Bob Johnson",
      "position": "UI Designer",
      "department": "Design",
      "salary": 75000
    }
  ]
}`;
                break;
            case 'csv-to-json':
            case 'csv-to-xml':
                sampleData = `id,name,position,department,salary
1,John Doe,Software Engineer,Engineering,85000
2,Jane Smith,Product Manager,Product,95000
3,Bob Johnson,UI Designer,Design,75000`;
                break;
            case 'xml-to-json':
            case 'xml-to-csv':
                sampleData = `<?xml version="1.0" encoding="UTF-8"?>
<employees>
  <employee>
    <id>1</id>
    <name>John Doe</name>
    <position>Software Engineer</position>
    <department>Engineering</department>
    <salary>85000</salary>
  </employee>
  <employee>
    <id>2</id>
    <name>Jane Smith</name>
    <position>Product Manager</position>
    <department>Product</department>
    <salary>95000</salary>
  </employee>
  <employee>
    <id>3</id>
    <name>Bob Johnson</name>
    <position>UI Designer</position>
    <department>Design</department>
    <salary>75000</salary>
  </employee>
</employees>`;
                break;
        }

        inputEditor.value = sampleData;
    }

    // Helper Functions
    function getInputPlaceholder(conversionType) {
        switch (conversionType) {
            case 'json-to-xml':
            case 'json-to-csv':
                return 'Enter JSON here...';
            case 'csv-to-json':
            case 'csv-to-xml':
                return 'Enter CSV here...';
            case 'xml-to-json':
            case 'xml-to-csv':
                return 'Enter XML here...';
            default:
                return 'Enter your text here...';
        }
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }

    function copyOutput() {
        const textToCopy = outputContent.textContent;
        navigator.clipboard.writeText(textToCopy).then(() => {
            // Provide visual feedback
            const originalText = copyOutputBtn.innerHTML;
            copyOutputBtn.innerHTML = '<i class="bi bi-check"></i> Copied!';
            setTimeout(() => {
                copyOutputBtn.innerHTML = originalText;
            }, 2000);
        }).catch(err => {
            showError('Failed to copy text: ' + err);
        });
    }

    function downloadOutput() {
        const outputText = outputContent.textContent;
        if (!outputText) return;

        const conversionType = conversionFormatSelect.value;
        let fileExtension;
        let mimeType;

        // Determine file extension and MIME type based on conversion output
        if (conversionType.endsWith('-to-xml')) {
            fileExtension = 'xml';
            mimeType = 'application/xml';
        } else if (conversionType.endsWith('-to-csv')) {
            fileExtension = 'csv';
            mimeType = 'text/csv';
        } else if (conversionType.endsWith('-to-json')) {
            fileExtension = 'json';
            mimeType = 'application/json';
        }

        const blob = new Blob([outputText], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `converted.${fileExtension}`;
        document.body.appendChild(a);
        a.click();

        // Clean up
        setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 0);
    }

    // Conversion Functions Implementation
    function convertJsonToXml(jsonStr) {
        try {
            const data = JSON.parse(jsonStr);
            return jsonToXml(data);
        } catch (e) {
            throw new Error('Invalid JSON: ' + e.message);
        }
    }

    function jsonToXml(obj, rootName = 'root') {
        let xml = '';

        function toXml(obj, name) {
            if (obj === null || obj === undefined) {
                return `<${name}></${name}>`;
            }

            if (Array.isArray(obj)) {
                return obj.map(item => {
                    if (typeof item === 'object' && item !== null) {
                        let singularName = name;
                        // Try to singularize the name (very basic approach)
                        if (name.endsWith('s')) {
                            singularName = name.substring(0, name.length - 1);
                        }
                        return toXml(item, singularName);
                    } else {
                        return `<${name}>${escapeXml(String(item))}</${name}>`;
                    }
                }).join('');
            }

            if (typeof obj === 'object') {
                let xmlContent = `<${name}>`;
                for (const key in obj) {
                    if (Object.prototype.hasOwnProperty.call(obj, key)) {
                        xmlContent += toXml(obj[key], key);
                    }
                }
                xmlContent += `</${name}>`;
                return xmlContent;
            }

            return `<${name}>${escapeXml(String(obj))}</${name}>`;
        }

        // Add XML declaration
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n';

        // Handle the root element based on input structure
        if (typeof obj === 'object' && !Array.isArray(obj) && Object.keys(obj).length === 1) {
            // Use the single property name as the root element
            const key = Object.keys(obj)[0];
            xml += toXml(obj[key], key);
        } else {
            // Use the provided root name
            xml += toXml(obj, rootName);
        }

        return xml;
    }

    function escapeXml(unsafe) {
        return unsafe
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&apos;');
    }

    function convertJsonToCsv(jsonStr) {
        try {
            const data = JSON.parse(jsonStr);
            return jsonToCsv(data);
        } catch (e) {
            throw new Error('Invalid JSON: ' + e.message);
        }
    }

    function jsonToCsv(data) {
        // Find the array to convert
        let arrayToConvert = data;

        // If data is an object with a single property that is an array, use that
        if (!Array.isArray(data) && typeof data === 'object') {
            const keys = Object.keys(data);
            if (keys.length === 1 && Array.isArray(data[keys[0]])) {
                arrayToConvert = data[keys[0]];
            } else {
                // If it's just an object, wrap it in an array
                arrayToConvert = [data];
            }
        }

        if (!Array.isArray(arrayToConvert)) {
            throw new Error('JSON must contain an array of objects to convert to CSV');
        }

        if (arrayToConvert.length === 0) {
            return '';
        }

        // Get all possible column headers from all objects
        const headers = new Set();
        arrayToConvert.forEach(item => {
            if (typeof item === 'object' && item !== null) {
                Object.keys(item).forEach(key => headers.add(key));
            }
        });

        // If there are no headers (array of primitives), handle differently
        if (headers.size === 0) {
            return arrayToConvert.map(item => String(item)).join('\n');
        }

        const headerRow = [...headers].join(',');
        const rows = arrayToConvert.map(item => {
            return [...headers].map(header => {
                const value = item[header];
                if (value === null || value === undefined) {
                    return '';
                }
                // Handle cells that contain commas or quotes
                if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
                    return `"${value.replace(/"/g, '""')}"`;
                }
                return String(value);
            }).join(',');
        });

        return [headerRow, ...rows].join('\n');
    }

    function convertCsvToJson(csvStr) {
        try {
            return csvToJson(csvStr);
        } catch (e) {
            throw new Error('Invalid CSV: ' + e.message);
        }
    }

    function csvToJson(csvStr) {
        // Parse CSV (handling quoted fields that may contain commas)
        const parseCSV = (text) => {
            const lines = text.split(/\r\n|\n/);
            return lines.map(line => {
                const fields = [];
                let field = '';
                let inQuotes = false;

                for (let i = 0; i < line.length; i++) {
                    const char = line[i];

                    if (char === '"') {
                        if (i + 1 < line.length && line[i + 1] === '"') {
                            // Handle escaped quotes (double double-quotes)
                            field += '"';
                            i++; // Skip the next quote
                        } else {
                            inQuotes = !inQuotes;
                        }
                    } else if (char === ',' && !inQuotes) {
                        fields.push(field);
                        field = '';
                    } else {
                        field += char;
                    }
                }

                fields.push(field); // Don't forget the last field
                return fields;
            });
        };

        const rows = parseCSV(csvStr);
        if (rows.length < 2) {
            throw new Error('CSV must have headers and at least one data row');
        }

        const headers = rows[0];
        const result = [];

        for (let i = 1; i < rows.length; i++) {
            if (rows[i].length === 0 || (rows[i].length === 1 && rows[i][0] === '')) {
                continue; // Skip empty rows
            }

            const obj = {};
            for (let j = 0; j < headers.length; j++) {
                if (j < rows[i].length) {
                    let value = rows[i][j];

                    // Try to convert numeric values
                    if (/^-?\d+$/.test(value)) {
                        // Integer
                        obj[headers[j]] = parseInt(value, 10);
                    } else if (/^-?\d+\.\d+$/.test(value)) {
                        // Float
                        obj[headers[j]] = parseFloat(value);
                    } else {
                        obj[headers[j]] = value;
                    }
                } else {
                    obj[headers[j]] = ''; // Handle missing fields
                }
            }
            result.push(obj);
        }

        return JSON.stringify(result, null, 2);
    }

    function convertCsvToXml(csvStr) {
        try {
            // First convert CSV to JSON
            const jsonStr = csvToJson(csvStr);
            const data = JSON.parse(jsonStr);

            // Then convert JSON to XML with a custom root name
            return jsonToXml({ rows: data }, 'rows');
        } catch (e) {
            throw new Error('Invalid CSV or conversion error: ' + e.message);
        }
    }

    function convertXmlToJson(xmlStr) {
        try {
            return xmlToJson(xmlStr);
        } catch (e) {
            throw new Error('Invalid XML: ' + e.message);
        }
    }

    function xmlToJson(xmlStr) {
        // Create a DOMParser
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xmlStr, "text/xml");

        // Check for parsing errors
        const parserError = xmlDoc.querySelector('parsererror');
        if (parserError) {
            throw new Error(parserError.textContent);
        }

        function elementToJson(element) {
            const obj = {};

            // Add attributes
            for (const attr of element.attributes) {
                obj[`@${attr.name}`] = attr.value;
            }

            // Process child nodes
            for (const child of element.childNodes) {
                if (child.nodeType === Node.ELEMENT_NODE) {
                    // Check if we've seen this tag before
                    if (obj[child.nodeName] !== undefined) {
                        if (!Array.isArray(obj[child.nodeName])) {
                            // Convert to array if this is the second occurrence
                            obj[child.nodeName] = [obj[child.nodeName]];
                        }
                        obj[child.nodeName].push(elementToJson(child));
                    } else {
                        obj[child.nodeName] = elementToJson(child);
                    }
                } else if (child.nodeType === Node.TEXT_NODE) {
                    const text = child.nodeValue.trim();
                    if (text) {
                        // If element has no other properties and only text, just use the text
                        if (Object.keys(obj).length === 0 && element.childNodes.length === 1) {
                            return text;
                        } else {
                            obj['#text'] = text;
                        }
                    }
                }
            }

            // If the object is empty, return an empty string
            if (Object.keys(obj).length === 0) {
                return '';
            }

            return obj;
        }

        const rootElement = xmlDoc.documentElement;
        const result = { [rootElement.nodeName]: elementToJson(rootElement) };

        return JSON.stringify(result, null, 2);
    }

    function convertXmlToCsv(xmlStr) {
        try {
            // First convert XML to JSON
            const jsonStr = xmlToJson(xmlStr);
            const data = JSON.parse(jsonStr);

            // We need to identify arrays in the JSON that can be converted to CSV
            // Find the first array in the JSON structure
            function findArrayInJson(obj) {
                if (Array.isArray(obj)) {
                    return obj;
                }

                if (typeof obj === 'object' && obj !== null) {
                    for (const key in obj) {
                        if (Object.prototype.hasOwnProperty.call(obj, key)) {
                            const value = obj[key];
                            if (Array.isArray(value)) {
                                return value;
                            }

                            const nestedArray = findArrayInJson(value);
                            if (nestedArray) {
                                return nestedArray;
                            }
                        }
                    }
                }

                return null;
            }

            // Try to find an array in the structure
            let arrayData = findArrayInJson(data);

            // If no array found, check if the root element contains similar child elements
            if (!arrayData) {
                // Get the root element name
                const rootKey = Object.keys(data)[0];
                const rootData = data[rootKey];

                // Check if rootData has properties with the same name (a common XML pattern)
                const childElementCounts = {};
                for (const key in rootData) {
                    if (Object.prototype.hasOwnProperty.call(rootData, key)) {
                        if (childElementCounts[key]) {
                            childElementCounts[key]++;
                        } else {
                            childElementCounts[key] = 1;
                        }
                    }
                }

                // Find element names that appear multiple times
                const repeatingElements = Object.keys(childElementCounts).filter(key => childElementCounts[key] > 1);

                if (repeatingElements.length > 0) {
                    // Convert these repeating elements to an array
                    arrayData = repeatingElements.map(elementName => rootData[elementName]);
                } else {
                    // If still no array found, wrap the entire root object in an array
                    arrayData = [rootData];
                }
            }

            // Once we have an array, convert it to CSV
            if (arrayData) {
                return jsonToCsv(arrayData);
            } else {
                throw new Error('Could not identify a suitable array structure in the XML for CSV conversion');
            }
        } catch (e) {
            throw new Error('Invalid XML or conversion error: ' + e.message);
        }
    }
});