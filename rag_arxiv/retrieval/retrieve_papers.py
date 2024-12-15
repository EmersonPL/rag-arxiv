from rag_arxiv.processing.process_files import process_paper_text
from rag_arxiv.utils import connect_to_postgres


# TODO: use a better solution
DATA_DIR = "data/cs_AI/"


@connect_to_postgres
def retrieve_closest_neighbors(
    conn, cur, query_emb: list[float], num_neighbors: int
) -> list[str]:
    """Return the code of the closest papers for the embeddings of a query."""
    cur.execute(
        "SELECT code FROM papers "
        f"ORDER BY abs_embedding <=> %(embedding)s::vector "
        f"LIMIT %(num_neighbors)s;",
        {"embedding": query_emb, "num_neighbors": num_neighbors},
    )
    results = cur.fetchall()
    # The returned values are a tuple of each selected field.
    results = [r[0] for r in results]

    return results


def retrieve_papers_text(papers_code: list[str]) -> list[str]:
    """Return the text of the papers."""
    texts = []
    for paper in papers_code:
        paper_path = f"{DATA_DIR}{paper}/article.pdf"
        text = process_paper_text(path=paper_path)
        texts.append(text)

    return texts
