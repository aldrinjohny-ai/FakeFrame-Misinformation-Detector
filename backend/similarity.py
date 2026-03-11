"""
Similarity Calculator
Computes cosine similarity between image and text embeddings
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityCalculator:
    def __init__(self, threshold=0.30):
        """
        Initialize similarity calculator with classification threshold
        Args:
            threshold: Minimum similarity score for MATCH classification
        """
        self.threshold = threshold
    
    def compute_similarity(self, embedding1, embedding2):
        """
        Compute cosine similarity between two embeddings
        Args:
            embedding1: First embedding vector (512,)
            embedding2: Second embedding vector (512,)
        Returns:
            float: Cosine similarity score between -1 and 1
        """
        # Reshape embeddings for sklearn cosine_similarity function
        emb1 = embedding1.reshape(1, -1)
        emb2 = embedding2.reshape(1, -1)
        
        # Compute cosine similarity
        similarity = cosine_similarity(emb1, emb2)[0][0]
        
        return float(similarity)
    
    def classify(self, similarity_score):
        """
        Classify the similarity score as MATCH or MISMATCH
        Args:
            similarity_score: Cosine similarity value
        Returns:
            dict: Classification result with confidence level
        """
        # Determine if image and caption match
        if similarity_score >= self.threshold:
            result = "MATCH"
            confidence = self._calculate_confidence(similarity_score, is_match=True)
        else:
            result = "POSSIBLE MISMATCH"
            confidence = self._calculate_confidence(similarity_score, is_match=False)
        
        return {
            "result": result,
            "confidence": confidence,
            "similarity_score": round(similarity_score, 4)
        }
    
    def _calculate_confidence(self, score, is_match):
        """
        Calculate confidence level based on how far the score is from threshold
        Args:
            score: Similarity score
            is_match: Boolean indicating if classified as match
        Returns:
            str: Confidence level (High, Medium, Low)
        """
        distance_from_threshold = abs(score - self.threshold)
        
        if is_match:
            # For matches, higher score = higher confidence
            if score >= 0.50:
                return "High"
            elif score >= 0.40:
                return "Medium"
            else:
                return "Low"
        else:
            # For mismatches, lower score = higher confidence
            if score < 0.15:
                return "High"
            elif score < 0.25:
                return "Medium"
            else:
                return "Low"
