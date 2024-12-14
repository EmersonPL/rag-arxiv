from rag_arxiv.utils import connect_to_postgres


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
