from os import listdir

from processing.embeddings import generate_embeddings
from processing.process_files import process_file
from scripts.migrations.utils import connect_to_postgres

DATA_DIR = "../data/"


@connect_to_postgres
def main(conn, cur):
    """Insert all papers from `data` to the database."""
    categories = listdir(DATA_DIR)
    for category in categories:
        category_name = category.split("_")[1]
        load_category_files(cur, f"{DATA_DIR}/{category}", category_name)


@connect_to_postgres
def load_category_files(cur, data_path: str, category_name: str):
    """Insert all papers of a category in the database."""
    files = listdir(data_path)
    for file in files:
        code = file[:-4]

        if _paper_is_in_db(cur, code, category_name):
            continue

        name, abs, _ = process_file(f"{data_path}/{file}")
        embeddings = generate_embeddings(abs)

        cur.execute(
            f"INSERT INTO "
            f"papers(abs_embedding, abs, name, code, category)"
            f"VALUES ({embeddings}, {abs}, {name}, {code}, {category_name})",
        )


def _paper_is_in_db(cur, paper_code, category_name):
    cur.execute(
        f"SELECT id "
        f"FROM papers "
        f"WHERE papercode={paper_code} "
        f"AND category='{category_name}'"
    )
    result = cur.fetchone()
    return result is None


if __name__ == "__main__":
    main()
