import json

SETTINGS_PATH = 'settings.json'

with open(SETTINGS_PATH, 'rb') as configuration_file:
    SETTINGS = json.load(configuration_file)
