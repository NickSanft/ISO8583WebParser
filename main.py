from flask import Flask, render_template_string

# Create a Flask application instance
app = Flask(__name__)

# Define the HTML template with embedded CSS (Tailwind) and JavaScript for the parser
# This single string contains the entire frontend application.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="h-full bg-gray-900">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ISO8583 Parser</title>
    <!-- Tailwind CSS for styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom styles for a cleaner look */
        body {
            font-family: 'Inter', sans-serif;
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: #1f2937;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #4b5563;
            border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: #6b7280;
        }
        .glow-shadow {
             box-shadow: 0 0 5px rgba(59, 130, 246, 0.5), 0 0 10px rgba(59, 130, 246, 0.3);
        }
    </style>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
</head>
<body class="h-full text-gray-200 antialiased">
    <div id="notification" class="fixed top-5 right-5 bg-red-600 text-white py-2 px-4 rounded-lg shadow-lg transition-opacity duration-300 opacity-0 z-50"></div>
    <div class="container mx-auto p-4 lg:p-8">
        <header class="text-center mb-8">
            <h1 class="text-4xl font-bold text-white tracking-tight">ISO8583 Message Parser</h1>
            <p class="text-lg text-gray-400 mt-2">A developer tool to unpack and analyze ISO8583 hex strings.</p>
        </header>

        <!-- Binary/Hex Converter -->
        <div class="bg-gray-800 border border-gray-700 rounded-lg p-6 mb-6">
            <h2 class="text-xl font-semibold text-white mb-4">Binary &lt;-&gt; Hex Converter</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label for="binary-input" class="block text-sm font-medium text-gray-300 mb-2">Binary</label>
                    <input type="text" id="binary-input" class="font-mono bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" placeholder="Enter binary string...">
                </div>
                <div>
                    <label for="hex-converter-input" class="block text-sm font-medium text-gray-300 mb-2">Hexadecimal</label>
                    <input type="text" id="hex-converter-input" class="font-mono bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" placeholder="Enter hex string...">
                </div>
            </div>
        </div>

        <main class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Left Column: Inputs -->
            <div class="space-y-6">
                <!-- Hex String Input -->
                <div>
                    <label for="hex-input" class="block text-sm font-medium text-gray-300 mb-2">ISO8583 Hex String</label>
                    <textarea id="hex-input" rows="8" class="font-mono bg-gray-800 border border-gray-600 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-3 custom-scrollbar" placeholder="Paste your hex string here..."></textarea>
                </div>

                <!-- Action Buttons -->
                <div class="flex flex-col sm:flex-row gap-4">
                    <button id="to-ascii-btn" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-md transition duration-300 ease-in-out transform hover:scale-105">
                        Convert to ASCII
                    </button>
                    <button id="unpack-btn" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md transition duration-300 ease-in-out transform hover:scale-105 glow-shadow">
                        Unpack to JSON
                    </button>
                </div>

                <!-- Field Format Builder -->
                <div class="bg-gray-800 border border-gray-700 rounded-lg p-4">
                    <h3 class="text-lg font-semibold text-white mb-3">Field Format Builder</h3>
                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 items-end">
                        <div>
                            <label for="field-num" class="block text-xs font-medium text-gray-400">Field</label>
                            <input type="number" id="field-num" class="mt-1 font-mono bg-gray-700 border border-gray-600 text-white text-sm rounded-lg block w-full p-2" placeholder="e.g., 3">
                        </div>
                        <div>
                            <label for="field-datatype" class="block text-xs font-medium text-gray-400">Data Type</label>
                             <input type="text" id="field-datatype" class="mt-1 font-mono bg-gray-700 border border-gray-600 text-white text-sm rounded-lg block w-full p-2" placeholder="e.g., n, ans, b">
                        </div>
                         <div>
                            <label for="field-format" class="block text-xs font-medium text-gray-400">Format</label>
                            <select id="field-format" class="mt-1 font-mono bg-gray-700 border border-gray-600 text-white text-sm rounded-lg block w-full p-2">
                                <option value="FIXED">FIXED</option>
                                <option value="LLVAR">LLVAR</option>
                                <option value="LLLVAR">LLLVAR</option>
                            </select>
                        </div>
                        <div>
                            <label for="field-len" class="block text-xs font-medium text-gray-400">Length</label>
                            <input type="number" id="field-len" class="mt-1 font-mono bg-gray-700 border border-gray-600 text-white text-sm rounded-lg block w-full p-2" placeholder="e.g., 6">
                        </div>
                    </div>
                     <button id="add-field-btn" class="mt-4 w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 px-4 rounded-md transition duration-300">
                        Add Field Definition
                    </button>
                </div>


                <!-- Field Format Editor -->
                <div>
                    <label for="format-editor" class="block text-sm font-medium text-gray-300 mb-2">Field Format Definition</label>
                    <textarea id="format-editor" rows="10" class="font-mono bg-gray-800 border border-gray-600 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-3 custom-scrollbar" placeholder="Define field formats, e.g., 3: n-6, 4: n-12, ... or use the builder above."></textarea>
                </div>
            </div>

            <!-- Right Column: Output -->
            <div class="bg-gray-800 border border-gray-700 rounded-lg p-1">
                 <div class="h-full bg-gray-900 rounded-md">
                    <div class="flex justify-between items-center bg-gray-800 rounded-t-md p-3 border-b border-gray-700">
                         <h2 class="text-lg font-semibold text-white">Parser Output</h2>
                         <button id="copy-btn" class="text-sm bg-gray-700 hover:bg-gray-600 text-gray-300 font-medium py-1 px-3 rounded-md transition duration-200">Copy</button>
                    </div>
                    <pre id="output-area" class="p-4 text-sm text-yellow-300 whitespace-pre-wrap break-all custom-scrollbar h-[calc(100%-50px)] overflow-auto"><code class="language-json">... output will be displayed here ...</code></pre>
                 </div>
            </div>
        </main>

        <footer class="text-center mt-8 text-gray-500 text-sm">
            <p>Built with Flask & Tailwind CSS. For educational and development purposes.</p>
        </footer>
    </div>

    <script>
        // --- UTILITY FUNCTIONS ---
        const hexToAscii = (hexStr) => {
            let asciiStr = '';
            for (let i = 0; i < hexStr.length; i += 2) {
                asciiStr += String.fromCharCode(parseInt(hexStr.substr(i, 2), 16));
            }
            return asciiStr;
        };

        const hexToBinary = (hex) => {
             if (!/^[0-9A-Fa-f]*$/.test(hex)) return ''; // prevent invalid chars
            return hex.split('').map(i =>
                parseInt(i, 16).toString(2).padStart(4, '0')
            ).join('');
        };

        const binaryToHex = (binary) => {
            if (!/^[01]*$/.test(binary)) return ''; // prevent invalid chars
            let hex = '';
            for (let i = 0; i < binary.length; i += 4) {
                const chunk = binary.substr(i, 4).padEnd(4, '0');
                hex += parseInt(chunk, 2).toString(16).toUpperCase();
            }
            return hex;
        };

        const asciiToHex = (str) => {
            let hex = '';
            for (let i = 0; i < str.length; i++) {
                let charCode = str.charCodeAt(i).toString(16);
                hex += (charCode.length < 2 ? '0' : '') + charCode;
            }
            return hex;
        };

        const showNotification = (message) => {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.classList.remove('opacity-0');
            setTimeout(() => {
                notification.classList.add('opacity-0');
            }, 3000);
        };


        // --- CORE PARSER LOGIC ---
        class Iso8583Parser {
            constructor(hexString, formatDefinition) {
                this.hex = hexString.replace(/\\s+/g, '');
                this.format = this.parseFormatDefinition(formatDefinition);
                this.cursor = 0;
                this.unpackedData = {};
                this.errors = [];
            }

            // Parses the user-defined format string into a structured object
            parseFormatDefinition(definition) {
                const format = {};
                const lines = definition.split('\\n');
                lines.forEach(line => {
                    const parts = line.split(':');
                    if (parts.length === 2) {
                        const field = parseInt(parts[0].trim(), 10);
                        const spec = parts[1].trim();

                        let type, length, dataType;

                        // Example formats: 'n-6', 'ans-LLVAR', 'b-16'
                        const specParts = spec.split('-');
                        dataType = specParts[0]; // n, an, ans, b, etc.
                        const lenPart = specParts[1];

                        if (lenPart.toUpperCase() === 'LLVAR') {
                            type = 'LLVAR';
                            length = 0;
                        } else if (lenPart.toUpperCase() === 'LLLVAR') {
                            type = 'LLLVAR';
                            length = 0;
                        } else {
                            type = 'FIXED';
                            length = parseInt(lenPart, 10);
                        }

                        if (!isNaN(field)) {
                            format[field] = { type, length, dataType };
                        }
                    }
                });
                return format;
            }

            // Read a specified number of hex characters from the string
            read(charCount) {
                if (this.cursor + charCount > this.hex.length) {
                    this.errors.push(`Read error: Tried to read ${charCount} chars from cursor ${this.cursor}, but hex length is ${this.hex.length}.`);
                    return null;
                }
                const data = this.hex.substring(this.cursor, this.cursor + charCount);
                this.cursor += charCount;
                return data;
            }

            unpack() {
                try {
                    // 1. MTI (Message Type Indicator)
                    const mtiHex = this.read(8);
                    if(!mtiHex) return;
                    this.unpackedData['MTI'] = hexToAscii(mtiHex);

                    // 2. Bitmaps
                    const primaryBitmapHex = this.read(16);
                    if(!primaryBitmapHex) return;
                    let binaryBitmap = hexToBinary(primaryBitmapHex);
                    this.unpackedData['Primary Bitmap (Hex)'] = primaryBitmapHex;

                    let presentFields = [];
                    if (binaryBitmap[0] === '1') { // Secondary bitmap exists
                        const secondaryBitmapHex = this.read(16);
                        if(!secondaryBitmapHex) return;
                        binaryBitmap += hexToBinary(secondaryBitmapHex);
                        this.unpackedData['Secondary Bitmap (Hex)'] = secondaryBitmapHex;
                    }

                    this.unpackedData['Bitmap (Binary)'] = binaryBitmap;

                    for (let i = 0; i < binaryBitmap.length; i++) {
                        if (binaryBitmap[i] === '1') {
                            presentFields.push(i + 1);
                        }
                    }
                    this.unpackedData['Present Fields'] = presentFields;

                    // 3. Data Fields
                    const fieldsData = {};
                    for (const field of presentFields) {
                        if (field === 1) continue; // Skip bitmap field itself

                        const fieldFormat = this.format[field];
                        if (!fieldFormat) {
                            this.errors.push(`Field ${field}: No format definition found. Stopping parse.`);
                            break;
                        }

                        let value = null;
                        if (fieldFormat.type === 'FIXED') {
                           value = this.parseFixed(fieldFormat);
                        } else if (fieldFormat.type === 'LLVAR') {
                            value = this.parseVar(2, fieldFormat);
                        } else if (fieldFormat.type === 'LLLVAR') {
                            value = this.parseVar(4, fieldFormat);
                        }

                        if (value === null) {
                             this.errors.push(`Field ${field}: Failed to parse value.`);
                             break;
                        }

                        fieldsData[field] = value;
                    }
                    this.unpackedData['Fields'] = fieldsData;

                } catch (e) {
                    this.errors.push(`An unexpected error occurred: ${e.message}`);
                }

                if(this.errors.length > 0) {
                    this.unpackedData['ERRORS'] = this.errors;
                }

                return this.unpackedData;
            }

            parseFixed(format) {
                // For binary data, length is in bytes, so hex chars = length * 2
                // For ASCII/numeric, length is in chars, so hex chars = length * 2 (since each char is packed into 2 hex digits)
                const readLength = format.dataType === 'b' ? format.length * 2 : format.length * 2;
                const dataHex = this.read(readLength);
                if (!dataHex) return null;

                if (format.dataType === 'b') {
                    return dataHex.toUpperCase();
                }
                return hexToAscii(dataHex);
            }

            parseVar(lenDigits, format) {
                // The length prefix itself is ASCII encoded, so 1 byte = 2 hex chars.
                const lenHex = this.read(lenDigits * 2);
                if(!lenHex) return null;

                const length = parseInt(hexToAscii(lenHex), 10);
                if (isNaN(length)) {
                    this.errors.push(`Invalid length for VAR field. Hex: ${lenHex}`);
                    return null;
                }

                const readLength = format.dataType === 'b' ? length * 2 : length * 2;
                const dataHex = this.read(readLength);
                if (!dataHex) return null;

                if (format.dataType === 'b') {
                    return dataHex.toUpperCase();
                }
                return hexToAscii(dataHex);
            }
        }


        // --- EVENT LISTENERS & DOM MANIPULATION ---
        document.addEventListener('DOMContentLoaded', () => {
            const hexInput = document.getElementById('hex-input');
            const formatEditor = document.getElementById('format-editor');
            const outputArea = document.getElementById('output-area').querySelector('code');
            const toAsciiBtn = document.getElementById('to-ascii-btn');
            const unpackBtn = document.getElementById('unpack-btn');
            const copyBtn = document.getElementById('copy-btn');
            const binaryInput = document.getElementById('binary-input');
            const hexConverterInput = document.getElementById('hex-converter-input');
            const addFieldBtn = document.getElementById('add-field-btn');
            const fieldFormatSelect = document.getElementById('field-format');
            const fieldLenInput = document.getElementById('field-len');

            // Example data
            hexInput.value = "31313030700000000000000031373132333435363738393031323334353637323234343535303030303030303030303234";
            formatEditor.value = `2: n-LLVAR \\n3: n-6 \\n4: n-12`;

            // --- Converter Logic ---
            binaryInput.addEventListener('input', (e) => {
                hexConverterInput.value = binaryToHex(e.target.value);
            });

            hexConverterInput.addEventListener('input', (e) => {
                binaryInput.value = hexToBinary(e.target.value);
            });

            // --- Field Builder Logic ---
            fieldFormatSelect.addEventListener('change', (e) => {
                // Disable length for variable types
                if(e.target.value === 'LLVAR' || e.target.value === 'LLLVAR') {
                    fieldLenInput.disabled = true;
                    fieldLenInput.value = '';
                    fieldLenInput.placeholder = 'N/A';
                } else {
                    fieldLenInput.disabled = false;
                    fieldLenInput.placeholder = 'e.g., 6';
                }
            });

            addFieldBtn.addEventListener('click', () => {
                const fieldNum = document.getElementById('field-num').value;
                const dataType = document.getElementById('field-datatype').value;
                const format = document.getElementById('field-format').value;
                const len = document.getElementById('field-len').value;

                if (!fieldNum || !dataType) {
                    showNotification('Field number and Data Type are required.');
                    return;
                }

                let formatStr;
                if (format === 'FIXED') {
                    if (!len) {
                        showNotification('Length is required for FIXED format.');
                        return;
                    }
                    formatStr = `${dataType}-${len}`;
                } else {
                    formatStr = `${dataType}-${format}`;
                }

                const newLine = `${fieldNum}: ${formatStr}`;

                // Append with a newline if editor is not empty
                formatEditor.value += (formatEditor.value ? '\\n' : '') + newLine;

                // Clear inputs for next entry
                document.getElementById('field-num').value = '';
                document.getElementById('field-datatype').value = '';
                document.getElementById('field-len').value = '';
            });


            toAsciiBtn.addEventListener('click', () => {
                const hexStr = hexInput.value.replace(/\\s+/g, '');
                if (hexStr) {
                    const ascii = hexToAscii(hexStr);
                    outputArea.textContent = JSON.stringify({ ascii: ascii }, null, 2);
                } else {
                    outputArea.textContent = '{"error": "Hex input is empty."}';
                }
            });

            unpackBtn.addEventListener('click', () => {
                const hexStr = hexInput.value.replace(/\\s+/g, '');
                const formatDef = formatEditor.value;
                if (!hexStr || !formatDef) {
                    outputArea.textContent = '{"error": "Hex string and format definition must be provided."}';
                    return;
                }
                const parser = new Iso8583Parser(hexStr, formatDef);
                const result = parser.unpack();
                outputArea.textContent = JSON.stringify(result, null, 2);
            });

            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(outputArea.textContent).then(() => {
                    const originalText = copyBtn.textContent;
                    copyBtn.textContent = 'Copied!';
                    setTimeout(() => {
                        copyBtn.textContent = originalText;
                    }, 1500);
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            });

        });
    </script>
</body>
</html>
"""


# Define the main route for the web application
@app.route('/')
def index():
    """
    Serves the main HTML page.
    The entire frontend logic is contained within the HTML_TEMPLATE string.
    """
    return render_template_string(HTML_TEMPLATE)


# Run the Flask application
if __name__ == '__main__':
    # Running in debug mode is useful for development.
    # For production, use a proper WSGI server like Gunicorn or uWSGI.
    app.run(debug=True, port=5001)

