import os
import csv
from PIL import Image
import torch
import clip
from similarity import cosine_similarity

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

DATASET_PATH = "dataset"
IMAGE_FOLDER = os.path.join(DATASET_PATH, "images")
CSV_FILE = os.path.join(DATASET_PATH, "captions.csv")

def get_image_embedding(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
    return image_features

def get_text_embedding(text):
    text_input = clip.tokenize([text]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text_input)
    return text_features

def compute_similarity(img_emb, txt_emb):
    return cosine_similarity(img_emb.cpu().numpy(), txt_emb.cpu().numpy())

print("\nRunning calibration...\n")

scores = []

with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        image_name = row["image_name"]
        caption = row["caption"]
        label = int(row["label"])

        image_path = os.path.join(IMAGE_FOLDER, image_name)

        img_emb = get_image_embedding(image_path)
        txt_emb = get_text_embedding(caption)

        score = compute_similarity(img_emb, txt_emb).item()

        scores.append(score)

        print(f"{image_name} | {caption} | similarity: {score:.4f} | label: {label}")

print("\nCalibration complete.\n")