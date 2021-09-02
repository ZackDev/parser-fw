from os import listdir
from os.path import isfile, join
import json

class Test:
    def __init__(self, a, b):
        print(a)
        print(b)
        pass

def get_config(name):
    config_files = [f for f in listdir('./') if (isfile(join('./', f)) and f != 'ConfigReader.py')]
    for file in config_files:
        with open(file, 'r') as f:
            js = json.loads(f.read())
            if js['name'] == name:
                return js
    return None


if __name__ == '__main__':
    cfg = get_config('daily_cases')
    Test(a=cfg['name'], b='1')
