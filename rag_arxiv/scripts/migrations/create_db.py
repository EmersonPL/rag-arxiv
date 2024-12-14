from decouple import config

from rag_arxiv.utils import connect_to_postgres

CREATE_PAPERS_TABLE_SQL = """
    CREATE TABLE papers (
        id bigserial PRIMARY KEY,
        abs_embedding vector({}),
        abs text,
        name varchar(255),
        code varchar(12) unique,
        category varchar(2)
);
"""


@connect_to_postgres
def main(conn, cur):
    embeddings_size = config("EMBEDDINGS_SIZE", cast=int)

    cur.execute(CREATE_PAPERS_TABLE_SQL.format(embeddings_size))
    conn.commit()


if __name__ == "__main__":
    main()
