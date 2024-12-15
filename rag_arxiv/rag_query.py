from decouple import config

from rag_arxiv.processing.embeddings import generate_embeddings
from rag_arxiv.prompt.generate_prompt import get_prompt_template
from rag_arxiv.retrieval.retrieve_papers import (
    retrieve_closest_neighbors,
    retrieve_papers_text,
)

import google.generativeai as genai


def rag(query: str) -> str:
    """Run the RAG for a given query.

    Returns:
        A string containing the generated results.
    """
    num_of_neighbors = config("MAXIMUM_NUMBER_OF_RAG_PAPERS")

    query_emb = generate_embeddings(query)
    neighbors = retrieve_closest_neighbors(
        query_emb=query_emb, num_neighbors=num_of_neighbors
    )
    papers_text = retrieve_papers_text(neighbors)

    response = generate_response(query, papers_text)
    return response


def generate_response(query: str, papers: list[str]) -> str:
    model_name = config("GENERATION_MODEL")
    max_prompt_size = config("MAXIMUM_NUMBER_OF_TOKENS", cast=int)
    api_key = config("GEMINI_API_KEY")

    system, user = get_prompt_template()

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name, system_instruction=system)

    final_user_prompt = user.format(query=query, papers=papers)
    papers_to_remove = 0
    while model.count_tokens(final_user_prompt).total_tokens > max_prompt_size:
        # Remove some papers, if they contain too many tokens.
        papers_to_remove += 1
        used_papers = papers[:-papers_to_remove]

        final_user_prompt = user.format(query=query, papers=used_papers)

    response = model.generate_content(final_user_prompt)

    return response.candidates[0].content.parts[0].text
