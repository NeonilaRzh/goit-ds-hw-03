import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://guest_user:Q3iQttayHojhp9bo@cluster0.fen4bxy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi("1"),
)
db = client["quotes_database"]


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def import_data(collection_name, data):
    collection = db[collection_name]
    collection.insert_many(data)


def main():
    quotes = load_json("quotes.json")
    authors = load_json("authors.json")

    import_data("quotes", quotes)
    import_data("authors", authors)


if __name__ == "__main__":
    main()
