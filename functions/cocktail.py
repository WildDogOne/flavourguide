import fuzzywuzzy.fuzz
import yaml
import json
from pprint import pprint
# from fuzzywuzzy import process
from rich.console import Console
from rich.table import Table
import requests
from thefuzz import process
from thefuzz import fuzz

from functions.config import cocktails_json, cocktails_downloaded, cocktails_custom, cocktail_db
from functions.flavour import load_flavour_db_yaml


def count():
    db = load_cocktail_db_yaml()
    print(len(db))


def load_cocktail_db_json():
    with open(cocktails_json, 'r') as openfile:
        db = json.load(openfile)
    return db


def load_cocktail_db_yaml():
    with open(cocktail_db) as file:
        db = yaml.full_load(file)
    return db


def merge_cocktail_db():
    with open(cocktails_downloaded) as file:
        downloaded = yaml.full_load(file)
    with open(cocktails_custom) as file:
        custom = yaml.full_load(file)
    db = downloaded + custom
    with open(cocktail_db, 'w') as file:
        documents = yaml.dump(db, file)


def convert_to_yaml():
    db = load_cocktail_db_json()
    with open(cocktails_downloaded, 'w') as file:
        documents = yaml.dump(db, file)


def download(id=11000):
    url = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php"
    cocktails = []
    go = 1
    while go == 1:
        params = {"i": id}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            cocktail = (response.json())
            if cocktail["drinks"]:
                cocktails.append(cocktail["drinks"][0])
            if len(cocktails) % 10 == 0 and len(cocktails) > 0:
                print(f"{len(cocktails)} Cocktails processed")
            json_object = json.dumps(cocktails, indent=4)
            with open(cocktails_json, "w") as outfile:
                outfile.write(json_object)
            id += 1
        else:
            go = 0
            pprint(response.text)
            json_object = json.dumps(cocktails, indent=4)
            with open(cocktails_json, "w") as outfile:
                outfile.write(json_object)


def search_ingredient(searches=None, amount=None):
    if type(searches) == str:
        searches = [searches]
    db = load_cocktail_db_yaml()
    table = Table(title=", ".join(searches), show_header=True)
    table.add_column("Cocktail")
    table.add_column("Ingredients")
    table.add_column("Matched Ingredient Count")
    cocktail_hits = {}
    for search in searches:
        for cocktail in db:
            ingredients = []
            for x in cocktail:
                if "Ingredient" in x:
                    ingredient = cocktail[x]
                    if ingredient:
                        ingredients.append(ingredient)
            for ingredient in ingredients:
                confidence = fuzz.partial_ratio(search.lower(), ingredient.lower())
                if confidence > 90:
                    cocktail_name = cocktail["strDrink"]
                    if cocktail_name not in cocktail_hits:
                        cocktail_hits[cocktail_name] = {"ingredients": ", ".join(ingredients).title(),
                                                        "hits": 1}
                        break
                    else:
                        cocktail_hits[cocktail_name]["hits"] += 1
                        break
    # sorted_cocktail_hits = sorted(cocktail_hits.items(), key=lambda item: item[1])

    for key, value in cocktail_hits.items():
        if amount:
            if value["hits"] >= amount:
                table.add_row(key, value["ingredients"], str(value["hits"]))
        elif len(searches) == value["hits"]:
            table.add_row(key, value["ingredients"], str(value["hits"]))
    if len(table.rows) > 0:
        console = Console()
        console.print(table)
    else:
        print(f"No results found for your search {', '.join(searches)}")


def search_cocktail(search):
    db = load_cocktail_db_yaml()
    for cocktail in db:
        cocktail_name = cocktail["strDrink"]
        confidence = fuzz.partial_ratio(search.lower(), cocktail_name.lower())
        if confidence > 90:
            table = Table(title=cocktail_name, show_header=True)
            table.add_column("Ingredient")
            table.add_column("Amount")
            # pprint(cocktail)
            for key, value in cocktail.items():
                if "ingredient" in key.lower() and value:
                    amount = key.replace("Ingredient", "Measure")
                    table.add_row(value, cocktail[amount])
            if len(table.rows) > 0:
                instructions = cocktail["strInstructions"]
                console = Console()
                console.print(table)
                if instructions:
                    print(instructions + "\n")
            else:
                print(f"No results found for your search {search}")


def expand_cocktail(search):
    db = load_cocktail_db_yaml()
    flavour_db = load_flavour_db_yaml()
    for cocktail in db:
        cocktail_name = cocktail["strDrink"]
        confidence = fuzz.partial_ratio(search.lower(), cocktail_name.lower())
        if confidence > 99:
            table = Table(title=cocktail_name, show_header=True)
            table.add_column("Ingredient")
            table.add_column("Fruit")
            table.add_column("Herb and Spice")
            table.add_column("Other")
            for key, value in cocktail.items():
                if "ingredient" in key.lower() and value:
                    add = {"fruit": [],
                           "herb_n_spice": [],
                           "other": []}
                    for flavour_key, flavour_value in flavour_db.items():
                        f_confidence = fuzz.partial_ratio(value.lower(), flavour_key.lower())
                        if f_confidence > 95:
                            add = flavour_value
                            # pprint(add)
                            # quit()
                    table.add_row(value,
                                  ", ".join(add["fruit"]),
                                  ", ".join(add["herb_n_spice"]),
                                  ", ".join(add["other"]))
            if len(table.rows) > 0:
                console = Console()
                console.print(table)
            else:
                print(f"No results found for your search {search}")
            #break
