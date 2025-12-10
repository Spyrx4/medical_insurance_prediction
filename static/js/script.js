// Update BMI value display
const bmiSlider = document.getElementById('bmi');
const bmiValue = document.getElementById('bmiValue');

bmiSlider.addEventListener('input', function() {
    bmiValue.textContent = parseFloat(this.value).toFixed(1);
});

// Form submission
const form = document.getElementById('insuranceForm');
const resultDiv = document.getElementById('result');
const amountDiv = document.getElementById('amount');
const loadingDiv = document.getElementById('loading');
const submitBtn = document.querySelector('.btn-predict');
const explanationDiv = document.getElementById('explanation');
const explanationText = document.getElementById('explanationText');
const riskBadge = document.getElementById('riskBadge');
const bmiBadge = document.getElementById('bmiBadge');

form.addEventListener('submit', async function(e) {
    e.preventDefault();

    // Get form values
    const age = parseInt(document.getElementById('age').value);
    const sex = document.querySelector('input[name="sex"]:checked').value;
    const bmi = parseFloat(document.getElementById('bmi').value);
    const children = parseInt(document.getElementById('children').value);
    const smoker = document.querySelector('input[name="smoker"]:checked').value;
    const region = document.getElementById('region').value;

    // Prepare data
    const data = {
        age: age,
        sex: sex,
        bmi: bmi,
        children: children,
        smoker: smoker,
        region: region
    };

    // Show loading, hide results
    loadingDiv.style.display = 'block';
    resultDiv.style.display = 'none';
    explanationDiv.style.display = 'none';
    submitBtn.disabled = true;

    try {
        // Send POST request to Flask backend
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            // Display cost
            amountDiv.textContent = '$' + result.prediction.toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
            
            // Display risk level badge
            const riskLabels = ['Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'];
            const riskColors = ['#4caf50', '#ff9800', '#ff5722', '#d32f2f'];
            riskBadge.textContent = `Risk Level: ${result.risk_level} (${riskLabels[result.risk_val]})`;
            riskBadge.style.background = riskColors[result.risk_val];
            
            // Display BMI category badge
            bmiBadge.textContent = `BMI: ${result.bmi_category}`;
            let bmiColor = '#4caf50';
            if (result.bmi_category === 'Underweight') {
                bmiColor = '#2196f3';
            } else if (result.bmi_category === 'Healthy weight') {
                bmiColor = '#4caf50';
            } else if (result.bmi_category === 'Overweight') {
                bmiColor = '#ff9800';
            } else {
                bmiColor = '#ff5722';
            }
            bmiBadge.style.background = bmiColor;
            
            // Show result
            resultDiv.style.display = 'block';
            
            // Display AI explanation
            if (result.explanation) {
                explanationText.innerHTML = result.explanation.replace(/\n/g, '<br>');
                explanationDiv.style.display = 'block';
            } else {
                explanationText.innerHTML = 'Penjelasan AI tidak tersedia saat ini.';
                explanationDiv.style.display = 'block';
            }
            
            // Scroll to result
            setTimeout(() => {
                resultDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);
            
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        console.error('Fetch error:', error);
        alert('Terjadi kesalahan saat menghubungi server: ' + error.message);
    } finally {
        // Hide loading
        loadingDiv.style.display = 'none';
        submitBtn.disabled = false;
    }
});

document.getElementById('age').addEventListener('input', function() {
    if (this.value < 18 || this.value > 100) {
        this.style.borderColor = '#ff5722';
    } else {
        this.style.borderColor = '#e0e0e0';
    }
});

document.getElementById('bmi').addEventListener('input', function() {
    const value = parseFloat(this.value);
    let color = '#667eea';
    
    if (value < 18.5) {
        color = '#2196f3'; // Underweight - blue
    } else if (value >= 18.5 && value < 25) {
        color = '#4caf50'; // Healthy - green
    } else if (value >= 25 && value < 30) {
        color = '#ff9800'; // Overweight - orange
    } else {
        color = '#ff5722'; // Obese - red
    }
    
    bmiValue.style.color = color;
});