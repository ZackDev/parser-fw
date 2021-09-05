from os import listdir
from os.path import isfile, join
import json

_DIRECTORY = './seqconf/'

def _get_config_files():
    config_files = [f for f in listdir(_DIRECTORY)
                        if (isfile(join(_DIRECTORY, f))
                        and f != 'ConfigReader.py'
                        and f != '__init__.py'
                        and f != 'ClassLoader.py')]
    return config_files

def get_config(name):
    config_files = _get_config_files()
    for file in config_files:
        try:
            with open(join(_DIRECTORY, file), 'r') as f:
                cfg = json.loads(f.read())
                if cfg['name'] != None and cfg['name'] == name:
                    return cfg
        except Exception as e:
            print(f'{file}: {e}')
    return None

def get_config_names():
    names = []
    config_files = _get_config_files()
    for file in config_files:
        try:
            with open(join(_DIRECTORY, file), 'r') as f:
                cfg = json.loads(f.read())
                if cfg['name']:
                    names.append(cfg['name'])
        except Exception as e:
            print(f'{file}: {e}')
    return names
