from pymongo.server_api import ServerApi
from pymongo import MongoClient, errors


client = MongoClient(
    "mongodb+srv://guest_user:Q3iQttayHojhp9bo@cluster0.fen4bxy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi("1"),
)
db = client["cat_database"]
collection = db["cats"]


def read_all_cats():
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except errors.PyMongoError as e:
        print(f"Error occurred: {e}")


def read_cat_by_name(name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("Cat not found.")
    except errors.PyMongoError as e:
        print(f"Error occurred: {e}")


def update_cat_age(name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count:
            print("Cat's age updated.")
        else:
            print("Cat not found.")
    except errors.PyMongoError as e:
        print(f"Error occurred: {e}")


def add_feature_to_cat(name, feature):
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.matched_count:
            print("Feature added to cat.")
        else:
            print("Cat not found.")
    except errors.PyMongoError as e:
        print(f"Error occurred: {e}")


def delete_cat_by_name(name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print("Cat deleted.")
        else:
            print("Cat not found.")
    except errors.PyMongoError as e:
        print(f"Error occurred: {e}")


def delete_all_cats():
    try:
        result = collection.delete_many({})
        print(f"All cats deleted, count: {result.deleted_count}")
    except errors.PyMongoError as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    try:
        collection.insert_many(
            [
                {
                    "name": "barsik",
                    "age": 8,
                    "features": ["ходить в капці", "дає себе гладити"],
                },
                {
                    "name": "murzik",
                    "age": 2,
                    "features": ["любить спати на сонці", "грає з мишкою"],
                },
            ]
        )
    except errors.PyMongoError as e:
        print(f"Error occurred while inserting initial data: {e}")

    print("All cats:")
    read_all_cats()

    print("\nCat with name 'barsik':")
    read_cat_by_name("barsik")

    print("\nUpdating age of 'barsik' to 9...")
    update_cat_age("barsik", 9)

    print("\nAdding feature to 'barsik'...")
    add_feature_to_cat("barsik", "любить морозиво")

    print("\nDeleting cat 'murzik'...")
    delete_cat_by_name("murzik")

    print("\nDeleting all cats...")
    delete_all_cats()
