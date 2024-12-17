"""Utilities for testing."""

from sklearn.metrics.pairwise import cosine_similarity

from rag_arxiv.processing.embeddings import generate_embeddings


def calculate_similarity_of_texts(text1: str, text2: str) -> float:
    """
    Calculates the cosine similarity between two texts.

    Args:
        text1 (str): The first input text.
        text2 (str): The second input text.

    Returns:
        float: Cosine similarity score between the two text embeddings.
    """
    embedding1 = generate_embeddings(text1)
    embedding2 = generate_embeddings(text2)
    return cosine_similarity([embedding1], [embedding2])[0][0]
