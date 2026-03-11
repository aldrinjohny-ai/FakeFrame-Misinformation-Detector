// DOM Elements
const imageInput = document.getElementById('imageInput');
const captionInput = document.getElementById('captionInput');
const checkButton = document.getElementById('checkButton');
const resetButton = document.getElementById('resetButton');
const imagePreview = document.getElementById('imagePreview');
const charCount = document.getElementById('charCount');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultSection = document.getElementById('resultSection');
const resultCard = document.getElementById('resultCard');
const resultIcon = document.getElementById('resultIcon');
const resultText = document.getElementById('resultText');
const similarityScore = document.getElementById('similarityScore');
const confidence = document.getElementById('confidence');
const similarityFill = document.getElementById('similarityFill');
const explanation = document.getElementById('explanation');

// Image preview handler
imageInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            imagePreview.innerHTML = `<img src="${event.target.result}" alt="Preview">`;
        };
        reader.readAsDataURL(file);
    }
});

// Character counter
captionInput.addEventListener('input', function() {
    charCount.textContent = this.value.length;
});

// Main check button handler
checkButton.addEventListener('click', async function() {
    // Validate inputs
    if (!imageInput.files[0]) {
        alert('Please upload an image');
        return;
    }
    
    if (!captionInput.value.trim()) {
        alert('Please enter a caption');
        return;
    }
    
    // Prepare form data
    const formData = new FormData();
    formData.append('image', imageInput.files[0]);
    formData.append('caption', captionInput.value.trim());
    
    // Show loading state
    checkButton.disabled = true;
    loadingSpinner.classList.remove('hidden');
    resultSection.classList.add('hidden');
    
    try {
        // Send request to backend API
        const response = await fetch('/api/check', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Server error');
        }
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        alert(`Error: ${error.message}`);
        console.error('Error:', error);
    } finally {
        // Hide loading state
        loadingSpinner.classList.add('hidden');
        checkButton.disabled = false;
    }
});

// Display results function
function displayResults(data) {
    // Determine if match or mismatch
    const isMatch = data.result === 'MATCH';
    
    // Update result card styling
    resultCard.className = 'result-card ' + (isMatch ? 'match' : 'mismatch');
    
    // Update icon and text
    resultIcon.textContent = isMatch ? '✅' : '⚠️';
    resultText.textContent = data.result;
    resultText.style.color = isMatch ? '#4caf50' : '#f44336';
    
    // Update similarity score
    similarityScore.textContent = data.similarity_score.toFixed(4);
    
    // Update confidence
    confidence.textContent = data.confidence;
    confidence.style.color = getConfidenceColor(data.confidence);
    
    // Update similarity bar
    const percentage = Math.max(0, Math.min(100, data.similarity_score * 100));
    similarityFill.style.width = percentage + '%';
    
    // Update explanation
    explanation.textContent = data.explanation;
    
    // Show result section
    resultSection.classList.remove('hidden');
    
    // Scroll to results
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Get color based on confidence level
function getConfidenceColor(confidenceLevel) {
    switch(confidenceLevel) {
        case 'High':
            return '#4caf50';
        case 'Medium':
            return '#ff9800';
        case 'Low':
            return '#f44336';
        default:
            return '#666';
    }
}

// Reset button handler
resetButton.addEventListener('click', function() {
    // Clear inputs
    imageInput.value = '';
    captionInput.value = '';
    imagePreview.innerHTML = '';
    charCount.textContent = '0';
    
    // Hide result section
    resultSection.classList.add('hidden');
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Prevent form submission on Enter key in textarea
captionInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        checkButton.click();
    }
});
