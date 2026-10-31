import argparse
import json
import string
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

_PUNCT_TABLE = str.maketrans("", "", string.punctuation)

def preprocess(text: str) -> str:
    return remove_punctuation(text).lower()


def load_stopwords() -> set[str]:
    with open("data/stopwords.txt", "r") as f:
        words = f.read().splitlines()
    return {preprocess(w) for w in words}  # "aren't" -> "arent"


def tokenize(text: str, stopwords: set[str]) -> list[str]:
    tokens = preprocess(text).split()
    tokens = [t for t in tokens if t and t not in stopwords]
    return [stemmer.stem(t) for t in tokens]  # "running" -> "run"

def remove_punctuation(text: str) -> str:
    return text.translate(_PUNCT_TABLE)

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query.lower().split()}")
            
            with open("data/movies.json", "r") as f:
                data = json.load(f)
            stopwords = load_stopwords()  # once, reused for every title
            query_tokens = tokenize(args.query, stopwords)
            results = []
            for movie in data["movies"]:
                title_tokens = tokenize(movie["title"], stopwords)
                if any(q in t for q in query_tokens for t in title_tokens):
                    results.append(movie)

            results = results[:5]  # the dataset is already ordered by ID

            for i, movie in enumerate(results, 1):
                print(f"{i}. {movie['title']}")
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()