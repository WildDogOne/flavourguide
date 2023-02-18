import argparse
import json
from pprint import pprint

import requests


def download():
    url = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php"
    cocktails = []
    id = 1850
    go = 1
    while go == 1:
        params = {"i": id}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            cocktail = (response.json())
            if cocktail["drinks"]:
                cocktails.append(cocktail["drinks"])
            if id % 10 == 0:
                print(f"{id} Cocktails processed")
                json_object = json.dumps(cocktails, indent=4)
                with open("cocktails.json", "w") as outfile:
                    outfile.write(json_object)
            id += 1
        else:
            go = 0
            json_object = json.dumps(cocktails, indent=4)
            with open("cocktails.json", "w") as outfile:
                outfile.write(json_object)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Cocktail Organiser',
                                     description='A little CLI to download and organise cocktails')
    parser.add_argument("-d",
                        "--download",
                        help="Downloads the whole cocktail DB."
                             "This will take a long time",
                        action='store_true',
                        required=False)
    args = parser.parse_args()
    if args.download:
        download()
    else:
        parser.print_help()
