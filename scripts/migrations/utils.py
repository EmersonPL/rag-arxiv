import psycopg2


def connect_to_postgres(func):
    """Decorator to handle connector and cursor for functions that run on PG"""

    def connection():
        conn = psycopg2.connect(
            database="rag_arxiv",
            user="admin",
            password="admin",
            host="localhost",
            port=5432
        )
        cur = conn.cursor()

        func(conn, cur)

        cur.close()
        conn.close()

    return connection