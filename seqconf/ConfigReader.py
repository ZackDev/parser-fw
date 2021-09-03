from os import listdir
from os.path import isfile, join
import json

def get_config(name):
    config_files = [f for f in listdir('./seqconf') if (isfile(join('./seqconf', f)) and f != 'ConfigReader.py' and f != '__init__.py')]
    for file in config_files:
        try:
            with open('./seqconf/' + file, 'r') as f:
                js = json.loads(f.read())
                if js['name'] == name:
                    return js
        except Exception as e:
            print(f'{file}: {e}')
    return None
