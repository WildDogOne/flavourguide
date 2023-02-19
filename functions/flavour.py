import json
import yaml


def load_flavour_db_json():
    with open('flavours.json', 'r') as openfile:
        db = json.load(openfile)
    return db


def convert_to_yaml():
    db = load_flavour_db_json()
    with open(r'data/flavour.yml', 'w') as file:
        documents = yaml.dump(db, file)
