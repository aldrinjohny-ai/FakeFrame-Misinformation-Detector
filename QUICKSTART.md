# 🚀 Quick Start Guide

Get FakeFrame running in 5 minutes!

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Start the Server

```bash
cd backend
python app.py
```

You should see:
```
==================================================
FakeFrame - Multimodal Misinformation Detector
==================================================

Loading CLIP model: openai/clip-vit-base-patch32...
Using device: cpu
CLIP model loaded successfully!
System ready!
 * Running on http://0.0.0.0:5000
```

## Step 3: Open Your Browser

Navigate to: `http://localhost:5000`

## Step 4: Test the System

1. Upload any image (dog, cat, landscape, etc.)
2. Enter a matching caption: "A dog playing in the park"
3. Click "Check Authenticity"
4. See the results!

## Example Test Cases

### Test 1: Match (Should score high)
- Find any dog image online
- Caption: "A dog"
- Expected: MATCH with score > 0.30

### Test 2: Mismatch (Should score low)
- Use the same dog image
- Caption: "A car on the highway"
- Expected: POSSIBLE MISMATCH with score < 0.30

## Troubleshooting

**Model downloading?** First run downloads ~600MB. Wait patiently.

**Port already in use?** Change port in `backend/app.py` line 95.

**Import errors?** Make sure you activated your virtual environment.

## What's Next?

- Read the full README.md for detailed documentation
- Check dataset/example_dataset.md for testing ideas
- Customize the threshold in backend/app.py
- Improve the frontend styling

Enjoy detecting misinformation! 🔍
