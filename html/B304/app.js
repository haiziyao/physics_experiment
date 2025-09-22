// Physics Experiment Calculator - JavaScript Implementation
class PhysicsCalculator {
    constructor() {
        this.data = {
            gratingConstant: 3.333333e-6,
            spectralOrder: 1,
            deltaTheta: 0.00833333,
            deltaD: 1.111111e-8,
            standardWavelengths: {
                'yellow1': 576.96,
                'yellow2': 579.07,
                'green': 546.07,
                'blue1': 435.83
            },
            measurements: {}
        };
        
        this.results = {};
        this.errors = {};
        
        this.initializeEventListeners();
        this.loadInitialData();
        this.setupTabSwitching();
    }

    // Convert degrees-minutes-seconds to decimal degrees
    dmsToDecimal(degrees, minutes, seconds = 0) {
        return degrees + minutes / 60.0 + seconds / 3600.0;
    }

    // Convert decimal degrees to degrees-minutes format
    decimalToDegMin(decimalDegrees) {
        const degrees = Math.floor(decimalDegrees);
        const minutes = Math.round((decimalDegrees - degrees) * 60);
        return {
            degrees, 
            minutes, 
            formatted: `${degrees}°${minutes}′`
        };
    }

    // Parse angle input in format "186°20′" or "186°20'"
    parseAngleInput(angleStr) {
        const regex = /(\d+)°(\d+)[′']/;
        const match = angleStr.match(regex);
        if (match) {
            const degrees = parseInt(match[1]);
            const minutes = parseInt(match[2]);
            return this.dmsToDecimal(degrees, minutes);
        }
        return null;
    }

    // Calculate angle difference
    calculateAngleDifference(angle1, angle2) {
        return Math.abs(angle2 - angle1);
    }

    // Calculate average of two angle differences (divided by 4)
    calAngleAvg(angleA1, angleA2, angleB1, angleB2) {
        const diffA = this.calculateAngleDifference(angleA1, angleA2);
        const diffB = this.calculateAngleDifference(angleB1, angleB2);
        return (diffA + diffB) / 4.0;
    }

    // Calculate average of three measurements
    calThreeAngleAvg(angle1, angle2, angle3) {
        return (angle1 + angle2 + angle3) / 3.0;
    }

    // Calculate wavelength using grating equation: d * sin(θ) = k * λ
    calculateWavelength(theta, d, k) {
        const thetaRad = theta * Math.PI / 180.0;
        return (d * Math.sin(thetaRad)) / k;
    }

    // Calculate percentage error
    calculatePercentError(measured, standard) {
        return Math.abs((measured - standard) / standard) * 100;
    }

    // Calculate wavelength error using error propagation
    calculateWavelengthError(theta, d, k, deltaTheta, deltaD) {
        const thetaRad = theta * Math.PI / 180.0;
        const deltaThetaRad = deltaTheta * Math.PI / 180.0;
        
        // Partial derivatives for error propagation
        const dLambda_dTheta = (d * Math.cos(thetaRad)) / k;
        const dLambda_dD = Math.sin(thetaRad) / k;
        
        // Error propagation formula
        const errorSquared = Math.pow(dLambda_dTheta * deltaThetaRad, 2) + 
                           Math.pow(dLambda_dD * deltaD, 2);
        
        return Math.sqrt(errorSquared);
    }

    // Setup tab switching functionality
    setupTabSwitching() {
        const tabButtons = document.querySelectorAll('.tab-button');
        const tabContents = document.querySelectorAll('.tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const tabName = button.getAttribute('data-tab');
                
                // Remove active class from all buttons and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));

                // Add active class to clicked button
                button.classList.add('active');
                
                // Show corresponding tab content
                const targetTab = document.getElementById(`${tabName}-tab`);
                if (targetTab) {
                    targetTab.classList.add('active');
                }
            });
        });
    }

    // Initialize event listeners
    initializeEventListeners() {
        // Parameter inputs
        const gratingConstantInput = document.getElementById('grating-constant');
        if (gratingConstantInput) {
            gratingConstantInput.addEventListener('input', (e) => {
                this.data.gratingConstant = parseFloat(e.target.value);
                this.calculateResults();
            });
        }

        const spectralOrderInput = document.getElementById('spectral-order');
        if (spectralOrderInput) {
            spectralOrderInput.addEventListener('input', (e) => {
                this.data.spectralOrder = parseInt(e.target.value);
                this.calculateResults();
            });
        }

        const deltaThetaInput = document.getElementById('delta-theta');
        if (deltaThetaInput) {
            deltaThetaInput.addEventListener('input', (e) => {
                this.data.deltaTheta = parseFloat(e.target.value);
                this.calculateResults();
            });
        }

        const deltaDInput = document.getElementById('delta-d');
        if (deltaDInput) {
            deltaDInput.addEventListener('input', (e) => {
                this.data.deltaD = parseFloat(e.target.value);
                this.calculateResults();
            });
        }

        // Angle inputs with real-time calculation
        document.querySelectorAll('.angle-input').forEach(input => {
            input.addEventListener('input', () => {
                this.collectMeasurements();
                this.calculateResults();
            });
        });

        // Action buttons
        const calculateBtn = document.getElementById('calculate-btn');
        if (calculateBtn) {
            calculateBtn.addEventListener('click', () => {
                this.calculateResults();
            });
        }

        const resetBtn = document.getElementById('reset-btn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.resetToDefaults();
            });
        }
    }

    // Load initial measurement data
    loadInitialData() {
        const initialData = {
            yellow1: { A: [[186, 20], [206, 14]], B: [[6, 20], [26, 37]] },
            yellow2: { A: [[186, 18], [206, 20]], B: [[6, 18], [26, 20]] },
            green1: { A: [[186, 57], [205, 45]], B: [[6, 57], [25, 45]] },
            green2: { A: [[186, 50], [205, 40]], B: [[6, 50], [25, 40]] },
            green3: { A: [[186, 55], [205, 33]], B: [[6, 55], [25, 33]] },
            blue1: { A: [[188, 45], [203, 45]], B: [[8, 45], [23, 45]] }
        };

        // Set initial values in input fields (already done in HTML)
        this.collectMeasurements();
        this.calculateResults();
    }

    // Collect measurements from input fields
    collectMeasurements() {
        this.data.measurements = {};
        
        document.querySelectorAll('.angle-input').forEach(input => {
            const color = input.dataset.color;
            const side = input.dataset.side;
            const angleNum = input.dataset.angle;
            
            if (!this.data.measurements[color]) {
                this.data.measurements[color] = { A: [], B: [] };
            }
            
            const angleValue = this.parseAngleInput(input.value);
            if (angleValue !== null) {
                if (angleNum === '1') {
                    this.data.measurements[color][side][0] = angleValue;
                } else {
                    this.data.measurements[color][side][1] = angleValue;
                }
            }
        });
    }

    // Main calculation function
    calculateResults() {
        this.collectMeasurements();
        
        const measurements = this.data.measurements;
        const results = {};

        // Calculate for each color
        Object.keys(measurements).forEach(color => {
            const data = measurements[color];
            if (data.A && data.B && data.A.length === 2 && data.B.length === 2) {
                const avgAngle = this.calAngleAvg(data.A[0], data.A[1], data.B[0], data.B[1]);
                const wavelength = this.calculateWavelength(
                    avgAngle, 
                    this.data.gratingConstant, 
                    this.data.spectralOrder
                );
                const wavelengthNm = wavelength * 1e9; // Convert to nanometers
                
                results[color] = {
                    avgAngle: avgAngle,
                    wavelength: wavelength,
                    wavelengthNm: wavelengthNm,
                    angleA: this.calculateAngleDifference(data.A[0], data.A[1]),
                    angleB: this.calculateAngleDifference(data.B[0], data.B[1])
                };
            }
        });

        // Calculate averages for green light (3 measurements)
        if (results.green1 && results.green2 && results.green3) {
            const avgGreenAngle = this.calThreeAngleAvg(
                results.green1.avgAngle,
                results.green2.avgAngle,
                results.green3.avgAngle
            );
            const avgGreenWavelength = this.calculateWavelength(
                avgGreenAngle,
                this.data.gratingConstant,
                this.data.spectralOrder
            );
            
            results.green = {
                avgAngle: avgGreenAngle,
                wavelength: avgGreenWavelength,
                wavelengthNm: avgGreenWavelength * 1e9
            };
        }

        // Calculate percentage errors
        Object.keys(results).forEach(color => {
            const standardKey = color === 'green' ? 'green' : color;
            if (this.data.standardWavelengths[standardKey]) {
                results[color].percentError = this.calculatePercentError(
                    results[color].wavelengthNm,
                    this.data.standardWavelengths[standardKey]
                );
            }
        });

        // Calculate error propagation
        this.calculateErrorAnalysis(results);

        this.results = results;
        this.displayResults();
        this.displayErrorAnalysis();
    }

    // Calculate error analysis
    calculateErrorAnalysis(results) {
        this.errors = {};
        
        Object.keys(results).forEach(color => {
            if (results[color].avgAngle) {
                const wavelengthError = this.calculateWavelengthError(
                    results[color].avgAngle,
                    this.data.gratingConstant,
                    this.data.spectralOrder,
                    this.data.deltaTheta,
                    this.data.deltaD
                );
                
                this.errors[color] = {
                    wavelengthError: wavelengthError,
                    wavelengthErrorNm: wavelengthError * 1e9,
                    relativeError: (wavelengthError / results[color].wavelength) * 100
                };
            }
        });
    }

    // Display results in the results tab with specific order and angle format
    displayResults() {
        const container = document.getElementById('results-container');
        if (!container) return;
        
        let html = `
            <div class="results-card">
                <h4>平均衍射角计算结果</h4>
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>光源</th>
                            <th>平均衍射角</th>
                            <th>计算波长 (nm)</th>
                            <th>标准波长 (nm)</th>
                            <th>相对误差 (%)</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        const colorNames = {
            'yellow1': '黄色1',
            'yellow2': '黄色2',
            'green': '绿色平均',
            'blue1': '蓝色1'
        };

        // Explicitly order the results to ensure green appears before blue
        const orderedResults = [];
        
        // Add yellow1 first
        if (this.results.yellow1) {
            orderedResults.push({ color: 'yellow1', data: this.results.yellow1 });
        }
        
        // Add yellow2 second
        if (this.results.yellow2) {
            orderedResults.push({ color: 'yellow2', data: this.results.yellow2 });
        }
        
        // Add green third (this is the average that should appear above blue)
        if (this.results.green) {
            orderedResults.push({ color: 'green', data: this.results.green });
        }
        
        // Add blue1 last
        if (this.results.blue1) {
            orderedResults.push({ color: 'blue1', data: this.results.blue1 });
        }
        
        // Generate table rows in the correct order
        orderedResults.forEach(item => {
            const color = item.color;
            const result = item.data;
            const standardKey = color === 'green' ? 'green' : color;
            const standardWavelength = this.data.standardWavelengths[standardKey];
            
            // Format the angle with both decimal and degrees-minutes format
            const decimalAngle = result.avgAngle.toFixed(4);
            const degMinFormat = this.decimalToDegMin(result.avgAngle);
            const angleDisplay = `${decimalAngle}° (${degMinFormat.formatted})`;
            
            html += `
                <tr>
                    <td>${colorNames[color]}</td>
                    <td>${angleDisplay}</td>
                    <td>${result.wavelengthNm.toFixed(2)}</td>
                    <td>${standardWavelength ? standardWavelength.toFixed(2) : 'N/A'}</td>
                    <td class="${this.getErrorClass(result.percentError)}">${result.percentError ? result.percentError.toFixed(2) : 'N/A'}</td>
                </tr>
            `;
        });

        html += `
                    </tbody>
                </table>
            </div>
        `;

        // Add individual measurements details
        html += `
            <div class="results-card">
                <h4>详细测量数据</h4>
                <div class="results-grid">
        `;

        Object.keys(this.results).forEach(color => {
            if (this.results[color].angleA !== undefined) {
                const result = this.results[color];
                html += `
                    <div class="result-item">
                        <div class="result-label">${this.getColorName(color)} - A边角度差</div>
                        <div class="result-value">${result.angleA.toFixed(4)}<span class="result-unit">°</span></div>
                    </div>
                    <div class="result-item">
                        <div class="result-label">${this.getColorName(color)} - B边角度差</div>
                        <div class="result-value">${result.angleB.toFixed(4)}<span class="result-unit">°</span></div>
                    </div>
                `;
            }
        });

        html += `
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    // Display error analysis
    displayErrorAnalysis() {
        const container = document.getElementById('error-container');
        if (!container) return;
        
        let html = `
            <div class="error-card">
                <h4>不确定度分析</h4>
                <div class="error-summary">
        `;

        // Use the same explicit ordering for error analysis
        const errorOrder = ['yellow1', 'yellow2', 'green', 'blue1'];
        
        errorOrder.forEach(color => {
            if (this.errors[color]) {
                const error = this.errors[color];
                html += `
                    <div class="error-item">
                        <div class="result-label">${this.getColorName(color)}</div>
                        <div class="result-value">${error.wavelengthErrorNm.toFixed(3)}<span class="result-unit">nm</span></div>
                        <div class="error-percentage ${this.getErrorClass(error.relativeError)}">${error.relativeError.toFixed(2)}%</div>
                    </div>
                `;
            }
        });

        html += `
                </div>
            </div>
        `;

        // Add error propagation formula explanation
        html += `
            <div class="error-card">
                <h4>误差传播公式</h4>
                <p>波长不确定度计算公式：</p>
                <div class="scientific-notation">
                    δλ = √[(∂λ/∂θ)²(δθ)² + (∂λ/∂d)²(δd)²]
                </div>
                <p>其中：</p>
                <ul>
                    <li>∂λ/∂θ = (d·cos(θ))/k</li>
                    <li>∂λ/∂d = sin(θ)/k</li>
                    <li>δθ = ${this.data.deltaTheta.toFixed(6)}°</li>
                    <li>δd = ${this.data.deltaD.toExponential(3)} m</li>
                </ul>
            </div>
        `;

        container.innerHTML = html;
    }

    // Helper function to get color name in Chinese
    getColorName(color) {
        const names = {
            'yellow1': '黄色1',
            'yellow2': '黄色2',
            'green1': '绿色1',
            'green2': '绿色2',
            'green3': '绿色3',
            'green': '绿色平均',
            'blue1': '蓝色1'
        };
        return names[color] || color;
    }

    // Helper function to get error class based on percentage
    getErrorClass(percentage) {
        if (percentage < 1) return 'low';
        if (percentage < 3) return 'medium';
        return 'high';
    }

    // Reset to default values
    resetToDefaults() {
        // Reset parameters
        const gratingConstantInput = document.getElementById('grating-constant');
        const spectralOrderInput = document.getElementById('spectral-order');
        const deltaThetaInput = document.getElementById('delta-theta');
        const deltaDInput = document.getElementById('delta-d');

        if (gratingConstantInput) gratingConstantInput.value = '3.333333e-6';
        if (spectralOrderInput) spectralOrderInput.value = '1';
        if (deltaThetaInput) deltaThetaInput.value = '0.00833333';
        if (deltaDInput) deltaDInput.value = '1.111111e-8';

        // Reset angle inputs to default values
        const defaultValues = {
            'yellow1-A-1': '186°20′',
            'yellow1-A-2': '206°14′',
            'yellow1-B-1': '6°20′',
            'yellow1-B-2': '26°37′',
            'yellow2-A-1': '186°18′',
            'yellow2-A-2': '206°20′',
            'yellow2-B-1': '6°18′',
            'yellow2-B-2': '26°20′',
            'green1-A-1': '186°57′',
            'green1-A-2': '205°45′',
            'green1-B-1': '6°57′',
            'green1-B-2': '25°45′',
            'green2-A-1': '186°50′',
            'green2-A-2': '205°40′',
            'green2-B-1': '6°50′',
            'green2-B-2': '25°40′',
            'green3-A-1': '186°55′',
            'green3-A-2': '205°33′',
            'green3-B-1': '6°55′',
            'green3-B-2': '25°33′',
            'blue1-A-1': '188°45′',
            'blue1-A-2': '203°45′',
            'blue1-B-1': '8°45′',
            'blue1-B-2': '23°45′'
        };

        document.querySelectorAll('.angle-input').forEach(input => {
            const key = `${input.dataset.color}-${input.dataset.side}-${input.dataset.angle}`;
            if (defaultValues[key]) {
                input.value = defaultValues[key];
            }
        });

        // Reset data and recalculate
        this.data.gratingConstant = 3.333333e-6;
        this.data.spectralOrder = 1;
        this.data.deltaTheta = 0.00833333;
        this.data.deltaD = 1.111111e-8;
        
        this.calculateResults();
    }
}

// Initialize the calculator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.calculator = new PhysicsCalculator();
});

// Add some utility functions for formatting
function formatScientific(value, precision = 3) {
    return value.toExponential(precision);
}

function formatAngle(degrees, minutes = null) {
    if (minutes === null) {
        const deg = Math.floor(degrees);
        const min = Math.round((degrees - deg) * 60);
        return `${deg}°${min}′`;
    }
    return `${degrees}°${minutes}′`;
}