import json
import yaml
import argparse
import json
from pprint import pprint
from thefuzz import process
from thefuzz import fuzz
from rich.console import Console
from rich.table import Table

from functions.config import flavours_json, flavour_db


def load_flavour_db_json():
    with open(flavours_json, 'r') as openfile:
        db = json.load(openfile)
    return db


def load_cocktail_db_yaml():
    with open(flavour_db) as file:
        db = yaml.full_load(file)
    return db


def convert_to_yaml():
    db = load_flavour_db_json()
    with open(flavour_db, 'w') as file:
        documents = yaml.dump(db, file)


def ingredient_search(search):
    ingredients = load_cocktail_db_yaml()
    keys = [key for key in ingredients]
    result = process.extractOne(search, keys)
    if result:
        result, confidence = result
        if confidence > 90:
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
def ingredient_lookup(lookup):
    db = load_cocktail_db_yaml()
    for key in db.keys():
        confidence = fuzz.partial_ratio(lookup.lower(), key.lower)
        if key.lower() != lookup.lower():
            if confidence > 50:
                print(f"Similar to {key} - Similarity Grade {confidence}")
def similar_finder():
    db = load_cocktail_db_yaml()
    for key in db:
        results = process.extract(key, db.keys())
        for result in results:
            if result[0] != key:
                if result[1] > 90:
                    # print(f"{key} is similar to {result[0]} - Similarity Grade {result[1]}")
                    print(f'"{result[0]}": "{key}",')
