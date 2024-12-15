"""Script to update table schema if generated with old `create_db`"""

from rag_arxiv.utils import connect_to_postgres


@connect_to_postgres
def main(conn, cur):
    cur.execute(
        """ALTER TABLE papers
        ADD COLUMN paper_text TEXT;
        """
    )
    cur.execute(
        """ALTER TABLE papers
        ALTER COLUMN code SET NOT NULL;
        """
    )
    cur.execute(
        """ALTER TABLE papers
        ALTER COLUMN category SET NOT NULL;
        """
    )

    conn.commit()


if __name__ == "__main__":
    main()
