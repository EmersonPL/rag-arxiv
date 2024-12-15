from decouple import config

from rag_arxiv.utils import connect_to_postgres


@connect_to_postgres
def main(conn, cur):
    embeddings_size = config("EMBEDDINGS_SIZE", cast=int)

    cur.execute(
        """CREATE TABLE papers (
            id bigserial PRIMARY KEY,
            abs_embedding vector(%(embeddings_size)s),
            abs text,
            name varchar(255),
            code varchar(12) unique not null ,
            category varchar(2) not null,
            paper_text text
        );""",
        {"embeddings_size": embeddings_size},
    )
    conn.commit()


if __name__ == "__main__":
    main()
