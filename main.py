from pprint import pprint
import pandas as pd
from tomark import Tomark


def main():
    url = 'https://www.smartblend.co.uk/flavour-guide'

    tables = pd.read_html(url, header=0)
    flavours = tables[0]
    ingredients = {}
    for index, row in flavours.iterrows():
        ingredients[row["Main Ingredient"]] = {
            "fruit": row["Fruit"].replace("  ", " ").split(", "),
            "herb_n_spice": row["Herb and Spice"].replace("  ", " ").split(", "),
            "other": row["Other"].replace("  ", " ").split(", ")
        }
    # pprint(ingredients)
    y = []
    for x in ingredients:
        y.append({
            "Ingredient": x,
            "Fruit": ingredients[x]["fruit"],
            "Herb and Spice": ingredients[x]["herb_n_spice"],
            "Other": ingredients[x]["other"],
        })
        # pprint(y)
        # quit()
    markdown = Tomark.table(y)
    markdown = markdown.replace("[", "").replace("]", "").replace("'", "")
    with open("flavours.md", "w") as file1:
        file1.writelines(markdown)



if __name__ == '__main__':
    main()
