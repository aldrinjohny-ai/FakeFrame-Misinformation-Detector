"""
FakeFrame Backend API
Flask application for multimodal misinformation detection
"""

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from clip_model import CLIPModelHandler
from similarity import SimilarityCalculator
from utils import allowed_file, validate_image, validate_caption, create_directories

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary directories
create_directories()

# Initialize CLIP model and similarity calculator
print("Initializing FakeFrame system...")
clip_handler = CLIPModelHandler()
similarity_calc = SimilarityCalculator(threshold=0.23)
print("System ready!")

@app.route('/')
def index():
    """Serve the frontend HTML page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('../frontend', path)

@app.route('/api/check', methods=['POST'])
def check_authenticity():
    """
    Main API endpoint for checking image-caption consistency
    Expects:
        - image: Image file
        - caption: Text caption
    Returns:
        JSON with similarity score, result, and confidence
    """
    try:
        # Validate request has both image and caption
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        if 'caption' not in request.form:
            return jsonify({'error': 'No caption provided'}), 400
        
        image_file = request.files['image']
        caption = request.form['caption']
        
        # Validate image file
        if image_file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        if not allowed_file(image_file.filename):
            return jsonify({'error': 'Invalid image format'}), 400
        
        # Validate caption
        is_valid, error_msg = validate_caption(caption)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Save uploaded image temporarily
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)
        
        # Validate saved image
        if not validate_image(image_path):
            os.remove(image_path)
            return jsonify({'error': 'Invalid or corrupted image'}), 400
        
        # Encode image and text using CLIP
        print(f"Processing: {filename} with caption: '{caption[:50]}...'")
        image_embedding = clip_handler.encode_image(image_path)
        text_embedding = clip_handler.encode_text(caption)
        
        # Compute similarity
        similarity_score = similarity_calc.compute_similarity(
            image_embedding, 
            text_embedding
        )
        
        # Classify result
        result = similarity_calc.classify(similarity_score)
        
        # Clean up uploaded file
        os.remove(image_path)
        
        # Add explanation to result
        result['explanation'] = generate_explanation(result)
        
        print(f"Result: {result['result']} (Score: {result['similarity_score']})")
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

def generate_explanation(result):
    """
    Generate detailed explanation of similarity score
    """
    score = result['similarity_score']
    classification = result['result']
    confidence = result['confidence']

    # Interpret similarity score
    if score >= 0.40:
        interpretation = "strong semantic alignment"
    elif score >= 0.23:
        interpretation = "moderate semantic similarity"
    elif score >= 0.15:
        interpretation = "weak relationship between image and caption"
    else:
        interpretation = "almost no semantic relationship"

    if classification == "MATCH":
        return (
            f"The image and caption show {interpretation}. "
            f"The similarity score ({score:.2f}) is above the detection threshold, "
            f"suggesting the caption likely describes the image content. "
            f"Confidence level: {confidence}."
        )
    else:
        return (
            f"Potential misinformation detected. The image and caption show "
            f"{interpretation}. The similarity score ({score:.2f}) is below the "
            f"threshold, indicating the caption may be unrelated or misleading. "
            f"Confidence level: {confidence}."
        )

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model': 'CLIP ViT-B/32'}), 200

if __name__ == '__main__':
    print("\n" + "="*50)
    print("FakeFrame - Multimodal Misinformation Detector")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
