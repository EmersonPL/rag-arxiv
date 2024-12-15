"""Script to add paper text to the DB.

Must run if:
    - using a DB that's incomplete (probably due to usage of former schema)
    - when changing a step in the file text processing.

If using in an incomplete DB, override_text may be False, for faster execution.
If changing a processing step, override_text must be True.
"""

import sys

from tqdm import tqdm

from rag_arxiv.processing.process_files import process_paper_text
from rag_arxiv.utils import connect_to_postgres

DATA_DIR = "../../data/cs_AI"


@connect_to_postgres
def main(conn, cur, override_text: bool = False):
    if override_text:
        cur.execute(
            """
            SELECT code FROM papers;
            """
        )
    else:
        cur.execute("""SELECT code FROM papers WHERE paper_text IS null;""")

    papers_to_update = cur.fetchall()
    codes = [r[0] for r in papers_to_update]
    for code in tqdm(codes):
        path = f"{DATA_DIR}/{code}/article.pdf"
        text = process_paper_text(path)

        try:
            cur.execute(
                """
                UPDATE papers SET paper_text = %(text)s WHERE code = %(code)s;
                """,
                {"text": text, "code": code},
            )
        except Exception as e:
            print(f"Failed to add text for {code}: {e}")

    conn.commit()


if __name__ == "__main__":
    override_text = False
    if len(sys.argv) > 1 and sys.argv[1] == "--override":
        override_text = True

    main(override_text=override_text)
