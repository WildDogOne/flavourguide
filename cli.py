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
            table.add_row("fruit", ", ".join(ingredients[result]["fruit"]))
            table.add_row("herb_n_spice",", ".join(ingredients[result]["herb_n_spice"]))
            table.add_row("other", ", ".join(ingredients[result]["other"]))
            console = Console()
            console.print(table)
        else:
            print("No match found\nSimilar results to your search:")
            simlares = process.extract(search, keys)
            for result, confidence in simlares:
                print(f"{result} Confidence: {confidence}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ingredient")
    args = parser.parse_args()
    ingredient = args.ingredient
    ingredient_lookup(ingredient)
