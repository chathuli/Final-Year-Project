// Main JavaScript for Breast Cancer Detection System

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const resultsDiv = document.getElementById('results');
    
    if (form) {
        form.addEventListener('submit', handlePrediction);
    }
    
    // Add smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});

async function handlePrediction(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('dataFile');
    const textInput = document.getElementById('featuresInput');
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;
    
    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading-spinner"></span> Analyzing...';
    
    try {
        let features = [];
        
        // Get features from text input or file
        if (textInput.value.trim()) {
            features = textInput.value.split(',').map(f => parseFloat(f.trim()));
            console.log('Features from text input:', features.length);
        } else if (fileInput.files.length > 0) {
            // Handle file upload
            const fileContent = await readFile(fileInput.files[0]);
            console.log('File content loaded, length:', fileContent.length);
            features = parseCSV(fileContent);
            console.log('Parsed features:', features.length, features);
        } else {
            throw new Error('Please provide input data');
        }
        
        // Validate features
        if (features.length !== 30) {
            throw new Error(`Expected 30 features, got ${features.length}. Please check your input file format.`);
        }
        
        if (features.some(isNaN)) {
            throw new Error('Invalid feature values. Please check your input.');
        }
        
        console.log('Sending prediction request with features:', features);
        
        // Make prediction
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ features: features })
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Prediction failed');
        }
        
        const result = await response.json();
        console.log('Prediction result:', result);
        displayResults(result);
        
    } catch (error) {
        showError(error.message);
    } finally {
        // Reset button
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
    }
}

function displayResults(result) {
    const resultsDiv = document.getElementById('results');
    const isBenign = result.best_model.prediction === 0;
    const confidence = (result.best_model.confidence * 100).toFixed(1);
    
    const resultClass = isBenign ? 'result-benign' : 'result-malignant';
    const icon = isBenign ? '✓' : '⚠';
    const diagnosis = result.best_model.prediction_label;
    const progressClass = isBenign ? 'progress-bar-success' : 'progress-bar-danger';
    
    let html = `
        <div class="result-card ${resultClass}">
            <div class="text-center">
                <div class="result-icon">${icon}</div>
                <h2 class="result-title">${diagnosis}</h2>
                <p class="mb-0">The analysis indicates a <strong>${diagnosis.toLowerCase()}</strong> diagnosis</p>
                <p class="mt-2"><small>Best Model: ${result.best_model.name}</small></p>
            </div>
            
            <div class="confidence-container">
                <div class="confidence-label">
                    <span>Confidence Level</span>
                    <span><strong>${confidence}%</strong></span>
                </div>
                <div class="progress-custom">
                    <div class="progress-bar-custom ${progressClass}" 
                         style="width: ${confidence}%">
                        ${confidence}%
                    </div>
                </div>
            </div>
    `;
    
    // Risk Assessment
    if (result.risk_assessment) {
        const riskColor = result.risk_assessment.color;
        html += `
            <div class="mt-3 p-3 rounded" style="background: rgba(var(--bs-${riskColor}-rgb), 0.1); border: 2px solid var(--bs-${riskColor});">
                <strong>Risk Level: ${result.risk_assessment.level}</strong>
                <p class="mb-0 mt-1">${result.risk_assessment.message}</p>
            </div>
        `;
    }
    
    // Model Comparison
    if (result.all_models && Object.keys(result.all_models).length > 1) {
        html += `
            <div class="mt-4">
                <h5>🤖 Model Comparison</h5>
                <div class="table-responsive">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Model</th>
                                <th>Prediction</th>
                                <th>Confidence</th>
                            </tr>
                        </thead>
                        <tbody>
        `;
        
        for (const [modelName, modelResult] of Object.entries(result.all_models)) {
            const modelBadge = modelResult.prediction_label === 'Benign' ? 'success' : 'danger';
            html += `
                <tr>
                    <td><strong>${modelName}</strong></td>
                    <td><span class="badge bg-${modelBadge}">${modelResult.prediction_label}</span></td>
                    <td>${(modelResult.confidence * 100).toFixed(1)}%</td>
                </tr>
            `;
        }
        
        html += `
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }
    
    // Feature Importance
    if (result.feature_importance && result.feature_importance.length > 0) {
        html += `
            <div class="mt-4">
                <h5>📊 Top Contributing Features</h5>
                <div class="feature-importance">
        `;
        
        result.feature_importance.slice(0, 5).forEach(feature => {
            const importance = (feature.importance * 100).toFixed(1);
            html += `
                <div class="importance-bar">
                    <div class="importance-label">${feature.name}</div>
                    <div class="importance-progress">
                        <div class="importance-fill" style="width: ${importance}%"></div>
                    </div>
                    <div class="importance-value">${feature.value.toFixed(3)}</div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    }
    
    // Download Report Button
    if (result.prediction_id) {
        html += `
            <div class="mt-4 text-center">
                <button class="btn btn-analyze" onclick="downloadReport(${result.prediction_id})">
                    📄 Download PDF Report
                </button>
            </div>
        `;
    }
    
    html += `
            <div class="disclaimer mt-4">
                <div class="info-card-icon">⚕️</div>
                <strong>Medical Disclaimer:</strong> This is an AI-assisted prediction tool for educational purposes. 
                Always consult with qualified healthcare professionals for medical diagnosis and treatment decisions.
            </div>
        </div>
    `;
    
    resultsDiv.innerHTML = html;
    resultsDiv.classList.remove('d-none');
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function downloadReport(predictionId) {
    window.location.href = `/api/generate-report/${predictionId}`;
}

function showError(message) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <div class="alert alert-danger" role="alert">
            <h4 class="alert-heading">Error</h4>
            <p>${message}</p>
        </div>
    `;
    resultsDiv.classList.remove('d-none');
}

function readFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(new Error('Failed to read file'));
        reader.readAsText(file);
    });
}

function parseCSV(content) {
    const lines = content.trim().split('\n');
    
    // Skip header if present (check if first line contains non-numeric values)
    let dataLine;
    if (lines.length > 1) {
        const firstLine = lines[0].split(',');
        const hasHeader = firstLine.some(v => isNaN(parseFloat(v)));
        dataLine = hasHeader ? lines[1] : lines[0];
    } else {
        dataLine = lines[0];
    }
    
    const values = dataLine.split(',');
    
    // Parse all numeric values
    const features = values
        .map(v => v.trim())
        .filter(v => v !== '' && !isNaN(parseFloat(v)))
        .map(v => parseFloat(v));
    
    // Take first 30 features
    return features.slice(0, 30);
}

// Add input validation
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('input', function() {
        if (this.value < 0) this.value = 0;
    });
});
