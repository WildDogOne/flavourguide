import argparse
import json
from pprint import pprint
from fuzzywuzzy import process
from rich.console import Console
from rich.table import Table
import requests


def load_cocktail_db():
    with open('cocktails.json', 'r') as openfile:
        db = json.load(openfile)
    return db


def download():
    url = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php"
    cocktails = []
    id = 11000
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
            with open("cocktails.json", "w") as outfile:
                outfile.write(json_object)
            id += 1
        else:
            go = 0
            pprint(response.text)
            json_object = json.dumps(cocktails, indent=4)
            with open("cocktails.json", "w") as outfile:
                outfile.write(json_object)


def count():
    db = load_cocktail_db()
    print(len(db))


def search_ingredient(searches=None):
    if type(searches) == str:
        searches = [searches]
    db = load_cocktail_db()
    table = Table(title=", ".join(searches), show_header=True)
    table.add_column("Cocktail")
    table.add_column("Ingredients")
    cocktail_hits = {}
    for search in searches:
        for cocktail in db:
            ingredients = []
            for x in cocktail:
                if "Ingredient" in x:
                    ingredient = cocktail[x]
                    if ingredient:
                        ingredients.append(ingredient)
            result = process.extract(search, ingredients)
            for x in result:
                ingredient = x[0]
                confidence = x[1]
                if confidence > 90:
                    cocktail_name = cocktail["strDrink"]
                    if cocktail_name not in cocktail_hits:
                        cocktail_hits[cocktail_name] = {"ingredients": ", ".join(ingredients),
                                                        "hits": 1}
                    else:
                        cocktail_hits[cocktail_name]["hits"] += 1
                    # pprint(cocktail)
                    # table.add_row(cocktail_name, ", ".join(ingredients))
    # pprint(cocktail_hits)

    for key, value in cocktail_hits.items():
        if len(searches) == value["hits"]:
            table.add_row(key, value["ingredients"])
        # pprint(value["hits"])
    if len(table.rows) > 0:
        console = Console()
        console.print(table)
    else:
        print(f"No results found for your search {', '.join(searches)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Cocktail Organiser',
                                     description='A little CLI to download and organise cocktails')
    parser.add_argument("-d",
                        "--download",
                        help="Downloads the whole cocktail DB."
                             "This will take a long time",
                        action='store_true',
                        required=False)
    parser.add_argument("-c",
                        "--count",
                        help="Count how many entries are in the DB",
                        action='store_true',
                        required=False)
    parser.add_argument("-i",
                        "--ingredient",
                        help="Search for cocktail by ingredient",
                        nargs="+",
                        required=False)
    args = parser.parse_args()
    ingredient_search = args.ingredient
    if args.download:
        download()
    elif args.count:
        count()
    elif ingredient_search:
        search_ingredient(ingredient_search)
    else:
        parser.print_help()
