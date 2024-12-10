from decouple import config
from openai import OpenAI


def generate_embeddings(text: str):
    # TODO: Implement actual embeddings
    return [0.5] * config("EMBEDDINGS_SIZE")

    api_key = config("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key, max_retries=0)
    response = client.embeddings.create(
        input=text, model=config("EMBEDDINGS_MODEL"), encoding_format="float"
    )
    embeddings = response["data"]["embedding"]

    return embeddings
