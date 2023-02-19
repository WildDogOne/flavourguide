import argparse
import json
from pprint import pprint

from functions.cocktail import convert_to_yaml, search_ingredient, count, download

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Cocktail Organiser',
                                     description='A little CLI to download and organise cocktails')
    parser.add_argument("-d",
                        "--download",
                        help="Downloads the whole cocktail DB."
                             "This will take a long time",
                        action='store_true',
                        required=False)
    parser.add_argument("-s",
                        "--start",
                        help="Optional starting ID for download",
                        type=int,
                        nargs=1,
                        required=False)
    parser.add_argument("--convert-to-yaml",
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
    parser.add_argument("-a",
                        "--amount",
                        help="Amount of ingredients that need to be matched"
                             "Defaults to all",
                        type=int,
                        required=False)
    args = parser.parse_args()
    pprint(args)

    ingredient_search = args.ingredient
    amount = args.amount
    if args.download:
        if args.start:
            download(args.start[0])
        else:
            download()
    elif args.count:
        count()
    elif ingredient_search:
        search_ingredient(ingredient_search, amount)
    elif args.convert_to_yaml:
        convert_to_yaml()
    else:
        parser.print_help()
