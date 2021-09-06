from abstract.AbstractConfigProvider import AbstractConfigProvider
from os import listdir
from os.path import isfile, join
import json
import importlib
import logging

logger = logging.getLogger(__name__)
_CONFIG_DIRECTORY = './config/'

class ConfigProvider(AbstractConfigProvider):
    def __init__(self, config_name):
        super().__init__(config_name)
        self.cfg = get_config(config_name)

    def get_source_class(self):
        source_cls = get_class(f"{self.cfg['source']['package']}.{self.cfg['source']['module']}", self.cfg['source']['class'])
        return source_cls

    def get_parser_class(self):
        parser_cls = get_class(f"{self.cfg['parser']['package']}.{self.cfg['parser']['module']}", self.cfg['parser']['class'])
        return parser_cls

    def get_sink_class(self):
        sink_cls = get_class(f"{self.cfg['sink']['package']}.{self.cfg['sink']['module']}", self.cfg['sink']['class'])
        return sink_cls

    def get_source_parameters(self):
        source_params = get_parameters(self.cfg, 'source')
        return source_params

    def get_parser_parameters(self):
        parser_params = get_parameters(self.cfg, 'parser')
        return parser_params

    def get_sink_parameters(self):
        sink_params = get_parameters(self.cfg, 'sink')
        return sink_params


def _load_module(module_name):
    module = importlib.import_module(module_name)
    return module


def get_class(module_name, class_name):
    module = None
    cls = None
    try:
        module = _load_module(module_name)
    except ModuleNotFoundError as e:
        logger.critical(f'{e}')
    if module:
        try:
            cls = getattr(module, class_name)
        except AttributeError as e:
            logger.critical(f'{e}')
    return cls


def _get_config_files():
    config_files = [f for f in listdir(_CONFIG_DIRECTORY)
                        if (isfile(join(_CONFIG_DIRECTORY, f))
                        and f != 'ConfigReader.py'
                        and f != '__init__.py'
                        and f != 'ClassLoader.py')]
    return config_files


def get_config(name):
    config_files = _get_config_files()
    for file in config_files:
        try:
            with open(join(_CONFIG_DIRECTORY, file), 'r') as f:
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
            with open(join(_CONFIG_DIRECTORY, file), 'r') as f:
                cfg = json.loads(f.read())
                if cfg['name']:
                    names.append(cfg['name'])
        except Exception as e:
            print(f'{file}: {e}')
    return names


def get_parameters(cfg, sequence_part):
    params = {}
    params.update({p['name']:p['value'] for p in cfg[sequence_part]['parameters']})
    return params
