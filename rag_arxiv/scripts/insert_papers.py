import os
from os import listdir

from tqdm import tqdm

from rag_arxiv.processing.embeddings import generate_embeddings
from rag_arxiv.processing.process_files import process_file
from rag_arxiv.utils import connect_to_postgres

DATA_DIR = "../../data"


@connect_to_postgres
def main(conn, cur):
    """Insert all papers from `data` to the database."""
    categories = listdir(DATA_DIR)
    for category in categories:
        category_name = category.split("_")[1]

        # TODO: Maybe remove this, to add all categories
        if category_name != "AI":
            continue

        load_category_files(cur, f"{DATA_DIR}/{category}", category_name)

    conn.commit()


def load_category_files(cur, data_path: str, category_name: str):
    """Insert all papers of a category in the database."""
    papers = listdir(data_path)
    for paper_code in tqdm(papers):
        if _paper_is_in_db(cur, paper_code, category_name):
            continue

        if len(os.listdir(f"{data_path}/{paper_code}")) != 2:
            print(f"Paper {paper_code} Does not contain 2 files")
            continue

        name, abs, file_text = process_file(f"{data_path}/{paper_code}")
        embeddings = generate_embeddings(abs)

        if embeddings is None:
            print(f"No embeddings for paper {paper_code}")
            continue

        cur.execute(
            "INSERT INTO "
            "papers(abs_embedding, abs, name, code, category, paper_text) "
            "VALUES ("
            "%(embeddings)s, "
            "%(abs)s, "
            "%(name)s, "
            "%(code)s, "
            "%(category)s, "
            "%(paper_text)s"
            ")",
            {
                "embeddings": embeddings,
                "abs": abs,
                "name": name,
                "code": paper_code,
                "category": category_name,
                "paper_text": file_text,
            },
        )


def _paper_is_in_db(cur, paper_code, category_name):
    cur.execute(
        f"SELECT id "
        f"FROM papers "
        f"WHERE code=%(code)s "
        f"AND category=%(cat_name)s",
        {
            "code": paper_code,
            "cat_name": category_name,
        },
    )
    result = cur.fetchone()
    return result is not None


if __name__ == "__main__":
    main()
