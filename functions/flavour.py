import json

import pandas as pd
import yaml
from rich.console import Console
from rich.table import Table
from thefuzz import fuzz
from thefuzz import process
from tomark import Tomark

from functions.config import flavours_json, flavour_db


def load_flavour_db_json():
    with open(flavours_json, 'r') as openfile:
        db = json.load(openfile)
    return db


def load_flavour_db_yaml():
    with open(flavour_db) as file:
        db = yaml.full_load(file)
    return db


def convert_to_yaml():
    db = load_flavour_db_json()
    with open(flavour_db, 'w') as file:
        documents = yaml.dump(db, file)


def ingredient_search(search):
    ingredients = load_flavour_db_yaml()
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
    db = load_flavour_db_yaml()
    for key in db.keys():
        confidence = fuzz.partial_ratio(lookup.lower(), key.lower)
        if key.lower() != lookup.lower():
            if confidence > 50:
                print(f"Similar to {key} - Similarity Grade {confidence}")


def similar_finder():
    db = load_flavour_db_yaml()
    for key in db:
        results = process.extract(key, db.keys())
        for result in results:
            if result[0] != key:
                if result[1] > 90:
                    # print(f"{key} is similar to {result[0]} - Similarity Grade {result[1]}")
                    print(f'"{result[0]}": "{key}",')


def fixes(element):
    replacements = {"  ": " ",
                    ".": ",",
                    "Cardamom And Nutmeg": "Cardamom, Nutmeg",
                    "Kaffir Lime Leaf": "Kaffir Leaf",
                    "Chocolate (Dark And White)": "Chocolate",
                    "All Spice Berries": "Allspice",
                    "Figs": "Fig",
                    "Grapefruit Papaya": "Grapefruit, Papaya",
                    "Lime Orange": "Lime, Orange",
                    "Maple Syrup Pecan": "Maple Syrup, Pecan",
                    "Orange Blossom Water": "Orange Blossom",
                    "Passion Fruit": "Passionfruit",
                    "Peach ": "Peach, ",
                    "Peaches": "Peach",
                    "Strawberries": "Strawberry",
                    "Pears": "Pear",
                    "Almonds": "Almond",
                    "Clove,": "Cloves,",
                    "Currants": "Currant",
                    "Grapes": "Grape",
                    "Prunes": "Prune",
                    "Raisins": "Raisin",
                    "Oranges": "Orange",
                    "Jasmin,": "Jasmine,",
                    "Citrus ": "Citrus, ",
                    "Berries ": "Berries, ",
                    "Caramel ": "Caramel, ",
                    "Cardamom ": "Cardamom, ",
                    "Chamomile ": "Chamomile, ",
                    "Coconut ": "Coconut, ",
                    "Chocolate ": "Chocolate, ",
                    "Passionfruit ": "Passionfruit, ",
                    "Pineapple ": "Pineapple, ",
                    "Rhubarb ": "Rhubarb, ",
                    "Goji Berry": "Goji",
                    "Goji": "Goji Berry"}
    for key, value in replacements.items():
        element = element.replace(key, value)
    return element


def splitter(element):
    element = element.title()
    cleanup = fixes(element)
    split = cleanup.split(", ")
    return split


def downloader():
    url = 'https://www.smartblend.co.uk/flavour-guide'
    tables = pd.read_html(url, header=0)
    flavours = tables[0]
    ingredients = {}
    for index, row in flavours.iterrows():
        ingredients[row["Main Ingredient"].title()] = {
            "fruit": splitter(row["Fruit"]),
            "herb_n_spice": splitter(row["Herb and Spice"]),
            "other": splitter(row["Other"])
        }
    ingredients = cleaner(ingredients)
    y = []
    for x in ingredients:
        y.append({
            "Ingredient": x,
            "Fruit": ingredients[x]["fruit"],
            "Herb and Spice": ingredients[x]["herb_n_spice"],
            "Other": ingredients[x]["other"],
        })
    markdown = Tomark.table(y)
    markdown = markdown.replace("[", "").replace("]", "").replace("'", "")
    with open("flavours.md", "w") as file1:
        file1.writelines(markdown)
    json_object = json.dumps(ingredients, indent=4)
    with open(flavours_json, "w") as outfile:
        outfile.write(json_object)


def cleaner(data):
    type = {}
    for key in data:
        for x in data[key]:
            for y in data[key][x]:
                if "," in y or "." in y:
                    data[key][x].remove(y)
                    y = y.replace(",", "")
                    # y = y.replace(".", "")
                    data[key][x].append(y)
                if y not in type:
                    type[y] = x
    outdata = dict(data)
    for key in data:
        for x in data[key]:
            for y in data[key][x]:
                if y not in outdata:
                    outdata[y] = {
                        "fruit": [],
                        "herb_n_spice": [],
                        "other": [],
                    }
                if "fruit" not in outdata[y]:
                    outdata[y]["fruit"] = []
                if "herb_n_spice" not in outdata[y]:
                    outdata[y]["herb_n_spice"] = []
                if "other" not in outdata[y]:
                    outdata[y]["other"] = []
                if key in type:
                    if key not in outdata[y][type[key]]:
                        outdata[y][type[key]].append(key)
    outdata = dict(sorted(outdata.items()))
    return outdata
