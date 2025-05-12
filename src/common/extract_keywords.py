from keybert import KeyBERT
import re
from src.common.generate_embeddings import Vector,model
from typing import List
import numpy as np

kw_model = KeyBERT(model=model)

def clean_text(text:str):
    """Remove the unnecessary parts of the text."""
    # Lowercase, remove trim whitespaces
    text = text.lower().strip()
    # Remove urls
    text = re.sub(r"http\S+|@\S+|[^a-z\s]", "", text)
    return text

def extract_keywords(texts:List[str], embeddings:List[Vector])->List[str]:
    """Extract keywords from the given texts using keybert model"""
    # Prepare the texts.
    clean_texts=[clean_text(text) for text in texts]
    # Prepare the embeddings. Keybert only accepts numpy arrays. 
    np_embeddings=[np.array(vector) for vector in embeddings]
    # Extract top keywords and their scores
    keyword_scores=kw_model.extract_keywords(
        clean_texts,
        stop_words='english',
        top_n=10,
        keyphrase_ngram_range=(1, 2),
        doc_embeddings=np_embeddings
    )
    # Return only the keywords
    return [keyword for keyword,_ in keyword_scores]