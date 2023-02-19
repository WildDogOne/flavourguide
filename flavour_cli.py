import argparse

from functions.flavour import convert_to_yaml, ingredient_search, ingredient_lookup, similar_finder, downloader

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Flavor Guide CLI',
                                     description='A little CLI application to search through Flavour DB', )
    parser.add_argument("-i",
                        "--ingredient",
                        help="Ingredient to look for, will take closest match if possible.",
                        required=False)
    parser.add_argument("-s",
                        "--similarlookup",
                        help="Checks if there are similar ingredients in the DB."
                             "This is mostly for Debugging. Should always result in zero results.",
                        action='store_true',
                        required=False)
    parser.add_argument("-d",
                        "--download",
                        help="Download initial Flavour Guide DB",
                        action='store_true',
                        required=False)
    parser.add_argument("-l",
                        "--lookup",
                        help="Search for similar ingredients."
                             "Mostly usefull if you don't know what you are looking for exactly.",
                        required=False)
    parser.add_argument("--convert-to-yaml",
                        help="Converts the flavours.json to flavours.yml",
                        action='store_true',
                        required=False)
    args = parser.parse_args()
    # pprint(args)
    ingredient = args.ingredient
    lookup = args.lookup
    if ingredient:
        ingredient_search(ingredient)
    elif lookup:
        ingredient_lookup(lookup)
    elif args.convert_to_yaml:
        convert_to_yaml()
    elif args.similarlookup:
        similar_finder()
    elif args.download:
        downloader()
    else:
        parser.print_help()
