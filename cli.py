import argparse
import json
from pprint import pprint

def ingredient_lookup(search):
    with open('flavours.json', 'r') as openfile:
        ingredients = json.load(openfile)
    result = [ingredients[key] for key in ingredients if search.lower() in key.lower()]
    if result:
        pprint(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ingredient")
    args = parser.parse_args()
    ingredient = args.ingredient
    ingredient_lookup(ingredient)