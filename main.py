import json
from pprint import pprint
import pandas as pd
from tomark import Tomark


def fixes(element):
    element = element.replace("Cardamom And Nutmeg", "Cardamom, Nutmeg")
    element = element.replace("Citrus ", "Citrus, ")
    element = element.replace("Berries ", "Berries, ")
    element = element.replace("Caramel ", "Caramel, ")
    element = element.replace("Cardamom ", "Cardamom, ")
    element = element.replace("Chamomile ", "Chamomile, ")
    element = element.replace("Coconut ", "Coconut, ")
    #element = element.replace("Grapefruit", "Grapefruit, ")
    #element = element.replace("Chocolate (Dark And White)", "Chocolate")
    #element = element.replace("Goji Berry", "Goji").replace("Goji", "Goji Berry") # Cannot Fix
    return element


def splitter(element):
    cleanup = element.replace("  ", " ").replace(".", ",").title()
    cleanup = fixes(cleanup)
    split = cleanup.split(", ")
    return split


def main():
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
    with open("flavours.json", "w") as outfile:
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


if __name__ == '__main__':
    main()
