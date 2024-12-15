import sys

from rag_arxiv.rag_query import rag


def main(query: str):
    response = rag(query)

    print(f"Response:\n{response}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query_llm.py <query>")
        quit()

    query = sys.argv[1]

    main(query)
