import pytest
from rag_arxiv.tests.example_questions_for_test import (
    Q1,
    EXPECTED_A1,
    Q2,
    EXPECTED_A2,
)
from rag_arxiv.rag_query import rag
from rag_arxiv.tests.utils import calculate_similarity_of_texts

# Define test cases as pairs of question and expected answer
test_data = [
    (Q1, EXPECTED_A1),
    (Q2, EXPECTED_A2),
]


@pytest.mark.parametrize("question, expected_answer", test_data)
def test_cosine_similarity_with_rag_query(question, expected_answer):
    """
    Test if the generated answers from rag(query) have a high cosine similarity with the expected answers.
    """
    generated_answer = rag(question)

    # Calculate cosine similarity between the generated and expected answers
    similarity_score = calculate_similarity_of_texts(
        generated_answer, expected_answer
    )

    assert (
        similarity_score > 0.75
    ), f"Low similarity ({similarity_score}) for question: {question};\nExpected answer: {expected_answer}\nGenerated answer: {generated_answer}"
