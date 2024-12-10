"""Processing of documents text."""


def process_file(file_path: str) -> tuple[str, str, str]:
    """Process a single file.

    Returns:
        A tuple containing:
            - The paper name;
            - The abstract text;
            - And the document main text (raw).
    """
    raise NotImplementedError


def process_paper_text(text: str) -> str:
    """Return the processed text.

    This removes all unwanted content from the main text.
    """
    raise NotImplementedError
