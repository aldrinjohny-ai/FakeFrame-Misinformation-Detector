"""
CLIP Model Handler
Loads and manages the CLIP ViT-B/32 model for encoding images and text
"""

import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

class CLIPModelHandler:
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        """
        Initialize CLIP model and processor
        Args:
            model_name: HuggingFace model identifier
        """
        print(f"Loading CLIP model: {model_name}...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Load CLIP model and processor from HuggingFace
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        
        # Set model to evaluation mode
        self.model.eval()
        print("CLIP model loaded successfully!")
    
    def encode_image(self, image_path):
        """
        Encode an image into a 512-dimensional embedding vector
        Args:
            image_path: Path to the image file
        Returns:
            numpy array of shape (512,) representing the image embedding
        """
        try:
            # Open and preprocess the image
            image = Image.open(image_path).convert("RGB")
            
            # Process image through CLIP processor
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate image embedding
            with torch.no_grad():
                image_features = self.model.get_image_features(**inputs)
            
            # Normalize the embedding (important for cosine similarity)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            
            # Convert to numpy and return
            return image_features.cpu().numpy()[0]
        
        except Exception as e:
            raise Exception(f"Error encoding image: {str(e)}")
    
    def encode_text(self, text):
        """
        Encode text caption into a 512-dimensional embedding vector
        Args:
            text: Text caption string
        Returns:
            numpy array of shape (512,) representing the text embedding
        """
        try:
            # Process text through CLIP processor
            inputs = self.processor(text=[text], return_tensors="pt", padding=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate text embedding
            with torch.no_grad():
                text_features = self.model.get_text_features(**inputs)
            
            # Normalize the embedding (important for cosine similarity)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
            
            # Convert to numpy and return
            return text_features.cpu().numpy()[0]
        
        except Exception as e:
            raise Exception(f"Error encoding text: {str(e)}")
