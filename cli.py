import argparse
import json
from pprint import pprint
from fuzzywuzzy import process
from rich.console import Console
from rich.table import Table


def load_db():
    with open('flavours.json', 'r') as openfile:
        db = json.load(openfile)
    return db


def ingredient_search(search):
    ingredients = load_db()
    keys = [key for key in ingredients]
    result = process.extractOne(search, keys)
    if result:
        result, confidence = result
        if confidence > 80:
            table = Table(title=result, show_header=False)
            table.add_row("Fruit", ", ".join(ingredients[result]["fruit"]))
            table.add_row("Herb and Spice", ", ".join(ingredients[result]["herb_n_spice"]))
            table.add_row("Other", ", ".join(ingredients[result]["other"]))
            console = Console()
            console.print(table)
        else:
            print("No match found\nSimilar results to your search:")
            similar = process.extract(search, keys)
            for result, confidence in similar:
                print(f"{result}")


def similar_finder():
    db = load_db()
    for key in db:
        results = process.extract(key, db.keys())
        for result in results:
            if result[0] != key:
                if result[1] > 90:
                    # print(f"{key} is similar to {result[0]} - Similarity Grade {result[1]}")
                    print(f'"{result[0]}": "{key}",')


def ingredient_lookup(lookup):
    db = load_db()
    results = process.extract(lookup, db.keys())
    for result in results:
        if result[0].lower() != lookup.lower():
            if result[1] > 50:
                print(f"Similar to {result[0]} - Similarity Grade {result[1]}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=False)
    parser.add_argument("-s", action='store_true', required=False)
    parser.add_argument("-l", required=False)
    args = parser.parse_args()
    pprint(args)
    ingredient = args.i
    lookup = args.l
    if ingredient:
        ingredient_search(ingredient)
    if lookup:
        ingredient_lookup(lookup)
    elif args.s:
        similar_finder()
