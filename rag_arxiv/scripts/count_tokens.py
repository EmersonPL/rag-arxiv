from decouple import config
from tqdm import tqdm

from rag_arxiv.utils import connect_to_postgres

import google.generativeai as genai


@connect_to_postgres
def main(conn, cur):
    model_name = config("GENERATION_MODEL")
    max_prompt_size = config("MAXIMUM_NUMBER_OF_TOKENS", cast=int)
    api_key = config("GEMINI_API_KEY")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    cur.execute("SELECT id, paper_text FROM papers")
    papers = cur.fetchall()
    total_tokens = 0
    max_tokens = {"id": None, "tokens": 0}
    min_tokens = {"id": None, "tokens": float("inf")}
    for paper_id, paper_text in tqdm(papers):
        if not paper_text or paper_text.strip() == "":
            print(
                f"Paper with id {paper_id} has an invalid 'paper_text' (None, empty, or whitespace). Skipping..."
            )
            continue
        token_count = model.count_tokens(paper_text).total_tokens
        total_tokens += token_count
        if token_count > max_tokens["tokens"]:
            max_tokens = {"id": paper_id, "tokens": token_count}
        if token_count < min_tokens["tokens"]:
            min_tokens = {"id": paper_id, "tokens": token_count}
    avg_tokens = total_tokens / len(papers) if papers else 0
    print(f"Total tokens: {total_tokens}")
    print(f"Average tokens per paper: {avg_tokens}")
    print(
        f"Paper with max tokens: {max_tokens['id']} ({max_tokens['tokens']} tokens)"
    )
    print(
        f"Paper with min tokens: {min_tokens['id']} ({min_tokens['tokens']} tokens)"
    )


if __name__ == "__main__":
    main()
