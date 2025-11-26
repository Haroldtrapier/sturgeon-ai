"""
backend/ml_utils.py
Utility functions for ML model management and feature engineering
"""

from typing import List, Dict
import numpy as np
from datetime import datetime, timedelta

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract important keywords from text
    Simple implementation - can be enhanced with NLP
    """
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    words = text.lower().split()
    keywords = [w for w in words if w not in stop_words and len(w) > 3]
    
    # Count frequencies
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:max_keywords]]


def calculate_similarity_score(
    historical_opportunities: List[Dict],
    new_opportunity: Dict
) -> float:
    """
    Calculate similarity between new opportunity and historical wins
    """
    if not historical_opportunities:
        return 0.1
    
    max_similarity = 0.0
    
    for hist in historical_opportunities:
        similarity = 0.0
        
        # NAICS similarity (40%)
        if hist.get('naics') == new_opportunity.get('naics'):
            similarity += 0.4
        elif hist.get('naics', '')[:3] == new_opportunity.get('naics', '')[:3]:
            similarity += 0.2
        
        # Agency similarity (30%)
        if hist.get('agency') == new_opportunity.get('agency'):
            similarity += 0.3
        
        # Set-aside similarity (15%)
        if hist.get('set_aside') == new_opportunity.get('set_aside'):
            similarity += 0.15
        
        # Keyword similarity (15%)
        hist_keywords = set(extract_keywords(hist.get('title', '')))
        new_keywords = set(extract_keywords(new_opportunity.get('title', '')))
        
        if hist_keywords and new_keywords:
            intersection = hist_keywords & new_keywords
            union = hist_keywords | new_keywords
            keyword_sim = len(intersection) / len(union)
            similarity += keyword_sim * 0.15
        
        max_similarity = max(max_similarity, similarity)
    
    return max_similarity


def normalize_contract_value(value: float) -> float:
    """Normalize contract value for model input"""
    return np.log1p(value) / 20.0  # Log scale and normalize


def calculate_days_until_deadline(deadline_str: str) -> int:
    """Calculate days until deadline"""
    try:
        deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
        days = (deadline - datetime.now()).days
        return max(0, days)
    except:
        return 30  # Default to 30 days


def prepare_training_data(
    opportunities: List[Dict]
) -> tuple:
    """
    Prepare training data from historical opportunities
    
    Returns:
        (X, y) - features and labels
    """
    from ml_models import WinPredictionModel
    
    model = WinPredictionModel()
    X = []
    y = []
    
    for opp in opportunities:
        if 'outcome' not in opp:  # Skip if no outcome
            continue
        
        features = model.extract_features(opp)
        X.append(features[0])
        y.append(1 if opp['outcome'] == 'won' else 0)
    
    return np.array(X), np.array(y)
