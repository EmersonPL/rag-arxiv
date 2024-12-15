"""Processing of documents text."""

import json

from pypdf import PdfReader


def process_file(paper_path: str) -> tuple[str, str, str]:
    """Process a single paper.

    Expects a directory containing `abstract.json` and `article.pdf`
    Returns:
        A tuple containing:
            - The paper name;
            - The abstract text;
            - And the document main text (raw).
    """
    file_text = process_paper_text(f"{paper_path}/article.pdf")
    abstract, name = process_paper_metadate(f"{paper_path}/abstract.json")

    return name, abstract, file_text


def process_paper_text(path: str) -> str:
    """Return the processed text.

    This removes all unwanted content from the main text.
    """
    file_text = ""

    reader = PdfReader(path)
    for i, page in enumerate(reader.pages):
        txt = page.extract_text(0)
        clean_text = txt.replace("\n", " ")
        clean_text = clean_text.replace("- ", "")
        # Remove characters not allowed on Postgres text column
        clean_text = clean_text.replace("\x00", "\uFFFD")

        clean_text = clean_text.encode("ascii", errors="replace")
        clean_text = clean_text.decode("utf-8", errors="replace")

        abstract_index = clean_text.find("abstract")
        if abstract_index != -1 and i <= 1:
            clean_text = clean_text[abstract_index:]

        file_text += clean_text

    return file_text


def process_paper_metadate(path: str) -> tuple[str, str]:
    """Return the abstract and title of a paper."""
    with open(path, "r", encoding="utf-8") as f:
        info = json.load(f)

    return info["Abstract"], info["Title"]
