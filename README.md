# Flavour Guide CLI

This is a little application to download, and normalise the [Flavour Guide](https://www.smartblend.co.uk/flavour-guide).
May support other DBs in the future.

## Installation && Usage

- Clone Repository
- Make sure you have python 3+
- Install requirements.txt (pip install -r requirements.txt)
- Run flavour_cli or cocktail_cli to interact with the DBs

### flavour_cli.py

Used to interact with the flavour guide DB.

If it is necessary to download a new DB, it should always be followed by convert-to-yaml as the yaml files are used
instead of json.

```
usage: Flavor Guide CLI [-h] [-i INGREDIENT] [-s] [-d] [-l LOOKUP] [--convert-to-yaml]

A little CLI application to search through Flavour DB

options:
  -h, --help            show this help message and exit
  -i INGREDIENT, --ingredient INGREDIENT
                        Ingredient to look for, will take closest match if possible.
  -s, --similarlookup   Checks if there are similar ingredients in the DB.This is mostly for Debugging. Should always result in zero results.
  -d, --download        Download initial Flavour Guide DB
  -l LOOKUP, --lookup LOOKUP
                        Search for similar ingredients.Mostly usefull if you don't know what you are looking for exactly.
  --convert-to-yaml     Converts the flavours.json to flavours.yml
```

### cocktail_cli.py

This script is used to interagt with the cocktail DB.

```
usage: Cocktail Organiser [-h] [-d] [-s START] [--convert-to-yaml] [--count] [-m] [-c COCKTAIL] [-e EXPAND] [-i INGREDIENT [INGREDIENT ...]] [-a AMOUNT]

A little CLI to download and organise cocktails

options:
  -h, --help            show this help message and exit
  -d, --download        Downloads the whole cocktail DB.This will take a long time
  -s START, --start START
                        Optional starting ID for download
  --convert-to-yaml     Downloads the whole cocktail DB.This will take a long time
  --count               Count how many entries are in the DB
  -m, --merge           Merge Cocktail DB with Custom Cocktailsby default takes cocktails_downloaded.yml and cocktails_custom.yml from the Data dir.
  -c COCKTAIL, --cocktail COCKTAIL
                        Search for cocktail by name
  -e EXPAND, --expand EXPAND
                        Search for cocktail by name, and list ingredients which may be interesting to add
  -i INGREDIENT [INGREDIENT ...], --ingredient INGREDIENT [INGREDIENT ...]
                        Search for cocktail by ingredient
  -a AMOUNT, --amount AMOUNT
                        Amount of ingredients that need to be matchedDefaults to all
```