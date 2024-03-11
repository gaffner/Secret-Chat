import json
import os

SETTINGS_PATH = os.path.join('settings.json')

with open(SETTINGS_PATH, 'rb') as configuration_file:
    SETTINGS = json.load(configuration_file)
