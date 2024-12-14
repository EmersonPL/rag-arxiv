import psycopg2
from pgvector.psycopg2 import register_vector


def connect_to_postgres(func):
    """Decorator to handle connector and cursor for functions that run on PG"""

    def connection(*args, **kwargs):
        conn = psycopg2.connect(
            database="rag_arxiv",
            user="admin",
            password="admin",
            host="localhost",
            port=5432,
        )
        register_vector(conn)

        cur = conn.cursor()

        result = func(conn, cur, *args, **kwargs)

        cur.close()
        conn.close()

        return result

    return connection
