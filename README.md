## Flavour Guide CLI

This is a little application to download, and normalise the [Flavour Guide](https://www.smartblend.co.uk/flavour-guide).
May support other DBs in the future.

### main.py

This script is used to generate the flavours.json which will be used as the DB for cli.py.
It also generates flavours.md, which is just a prettified table of the ingredients.

### cli.py

A little CLI application to search through Flavour Guide DB (flavours.json)

```
optional arguments:
  -h, --help            show this help message and exit
  -i INGREDIENT, --ingredient INGREDIENT
                        Ingredient to look for, will take closest match if possible.
  -s, --similarlookup   Checks if there are similar ingredients in the DB.This is mostly for Debugging. Should always result in zero results.
  -l LOOKUP, --lookup LOOKUP
                        Search for similar ingredients.Mostly usefull if you don't know what you are looking for exactly.
```