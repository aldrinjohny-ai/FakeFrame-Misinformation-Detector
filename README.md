# 🔍 FakeFrame - Multimodal Misinformation Detector

A complete AI system that detects whether a news image and its caption are semantically consistent using OpenAI CLIP embeddings.

## 🎯 Project Overview

FakeFrame analyzes both images and text captions using the CLIP ViT-B/32 model to determine if they match semantically. If the similarity score falls below a defined threshold (0.30), the system flags the pair as potential misinformation.

## 🏗️ System Architecture

```
User Input (Image + Caption)
         ↓
Image Encoder (CLIP ViT-B/32) | Text Encoder (CLIP Transformer)
         ↓                     ↓
Image Embedding (512 vector) | Text Embedding (512 vector)
         ↓                     ↓
         Cosine Similarity
                ↓
         Threshold Classifier
                ↓
         Result Output
```

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **AI Model**: OpenAI CLIP ViT-B/32 (via HuggingFace Transformers)
- **Deep Learning**: PyTorch
- **Frontend**: HTML, CSS, JavaScript
- **Libraries**: Scikit-learn, NumPy, Pillow, Matplotlib

## 📁 Project Structure

```
FakeFrame/
│
├── backend/
│   ├── app.py              # Flask API server
│   ├── clip_model.py       # CLIP model handler
│   ├── similarity.py       # Similarity computation
│   └── utils.py            # Helper functions
│
├── frontend/
│   ├── index.html          # Main webpage
│   ├── script.js           # Frontend logic
│   └── styles.css          # Styling
│
├── models/                 # Model cache directory
├── dataset/                # Sample dataset directory
├── uploads/                # Temporary upload directory
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## ⚙️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download the Project

```bash
cd FakeFrame
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- PyTorch (deep learning)
- Transformers (CLIP model)
- Pillow (image processing)
- NumPy, Scikit-learn (numerical computing)
- And other dependencies

### Step 4: Run the Application

```bash
cd backend
python app.py
```

The server will start on `http://localhost:5000`

### Step 5: Open in Browser

Navigate to `http://localhost:5000` in your web browser.

## 🚀 Usage

1. **Upload an Image**: Click the file input and select an image (PNG, JPG, JPEG, GIF, BMP, WEBP)
2. **Enter Caption**: Type or paste the caption/description for the image
3. **Check Authenticity**: Click the "Check Authenticity" button
4. **View Results**: See the similarity score, classification, and confidence level

## 📊 Classification Logic

The system uses the following threshold-based classification:

- **Similarity ≥ 0.30** → MATCH (Image and caption are consistent)
- **Similarity < 0.30** → POSSIBLE MISMATCH (Potential misinformation)

### Confidence Levels

**For MATCH:**
- High: Score ≥ 0.50
- Medium: Score ≥ 0.40
- Low: Score ≥ 0.30

**For MISMATCH:**
- High: Score < 0.15
- Medium: Score < 0.25
- Low: Score < 0.30

## 🔬 How It Works

### 1. Image Encoding
The CLIP image encoder processes the uploaded image and converts it into a 512-dimensional embedding vector that captures visual semantics.

### 2. Text Encoding
The CLIP text encoder processes the caption and converts it into a 512-dimensional embedding vector that captures textual semantics.

### 3. Similarity Computation
Cosine similarity is computed between the two normalized embeddings:

```
similarity = (image_embedding · text_embedding) / (||image_embedding|| × ||text_embedding||)
```

### 4. Classification
The similarity score is compared against the threshold (0.30) to determine if the image-caption pair is consistent.

## 📝 API Endpoints

### POST /api/check
Check image-caption consistency

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body:
  - `image`: Image file
  - `caption`: Text caption

**Response:**
```json
{
  "result": "MATCH" | "POSSIBLE MISMATCH",
  "similarity_score": 0.4523,
  "confidence": "High" | "Medium" | "Low",
  "explanation": "Detailed explanation text..."
}
```

### GET /api/health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "model": "CLIP ViT-B/32"
}
```

## 📦 Example Dataset Format

Create test cases in the `dataset/` directory:

```
dataset/
├── match_examples/
│   ├── dog_image.jpg
│   └── dog_caption.txt ("A golden retriever playing in the park")
│
└── mismatch_examples/
    ├── cat_image.jpg
    └── wrong_caption.txt ("A car driving on the highway")
```

## 🎨 Features

✅ Upload and preview images  
✅ Real-time character counter for captions  
✅ CLIP-based semantic similarity analysis  
✅ Visual similarity score bar  
✅ Confidence level indicators  
✅ Detailed explanations  
✅ Responsive design  
✅ Error handling and validation  

## 🔧 Customization

### Adjust Threshold
Edit `backend/app.py`:
```python
similarity_calc = SimilarityCalculator(threshold=0.35)  # Change from 0.30
```

### Change Model
Edit `backend/clip_model.py`:
```python
def __init__(self, model_name="openai/clip-vit-large-patch14"):  # Use larger model
```

## 🐛 Troubleshooting

### Issue: Model download is slow
**Solution**: The first run downloads the CLIP model (~600MB). Be patient or download manually.

### Issue: CUDA out of memory
**Solution**: The system automatically uses CPU if GPU is unavailable. For GPU issues, reduce batch size or use CPU.

### Issue: Port 5000 already in use
**Solution**: Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📚 Learn More

- [CLIP Paper](https://arxiv.org/abs/2103.00020)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🤝 Contributing

This is a beginner-friendly educational project. Feel free to:
- Add more features
- Improve the UI
- Optimize the model
- Add batch processing
- Create a dataset

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Built as a demonstration of multimodal AI for misinformation detection.

---

**Note**: This system is a proof-of-concept. Real-world misinformation detection requires more sophisticated approaches, human verification, and consideration of context, source credibility, and other factors.
