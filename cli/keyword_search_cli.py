import argparse
import json
import string

_PUNCT_TABLE = str.maketrans("", "", string.punctuation)


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
            print(f"Searching for: {args.query.lower()}")

            with open("data/movies.json", "r") as f:
                data = json.load(f)

            results = []
            for movie in data["movies"]:
                if args.query.lower() in remove_punctuation(movie["title"]).lower():
                    results.append(movie)

            results = results[:5]  # the dataset is already ordered by ID

            for i, movie in enumerate(results, 1):
                print(f"{i}. {movie['title']}")
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()