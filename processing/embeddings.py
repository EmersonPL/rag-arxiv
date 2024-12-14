from decouple import config
import google.generativeai as genai


def generate_embeddings(text: str) -> list[float] | None:
    api_key = config("GEMINI_API_KEY")

    genai.configure(api_key=api_key)

    result = genai.embed_content(
        model=config("EMBEDDINGS_MODEL"),
        content=text,
    )
    embeddings = result.get("embedding")

    return embeddings
