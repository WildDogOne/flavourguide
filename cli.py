import argparse
import json
from pprint import pprint
from fuzzywuzzy import process
from rich.console import Console
from rich.table import Table


def ingredient_lookup(search):
    with open('flavours.json', 'r') as openfile:
        ingredients = json.load(openfile)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ingredient")
    args = parser.parse_args()
    ingredient = args.ingredient
    ingredient_lookup(ingredient)