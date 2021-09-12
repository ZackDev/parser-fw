from abstract.AbstractConfigProvider import AbstractConfigProvider
from os import listdir
from os.path import isfile, join
import json
import importlib
import logging


class ConfigProviderError(Exception):
    pass


class ConfigProvider(AbstractConfigProvider):

    ''' BEGIN static '''

    logger = logging.getLogger(__name__)
    _CONFIG_DIRECTORY = './config/'

    '''
    imports and returns the module specified by <module_name>
    raises ModuleNotFoundError
    '''
    def _load_module(module_name):
        module = importlib.import_module(module_name)
        return module


    '''
    returns the class identified by <module_name> and <class_name>
    raises AttributeError
    '''
    def get_class(module_name, class_name):
        module = ConfigProvider._load_module(module_name)
        cls = getattr(module, class_name)
        return cls


    '''
    returns a list of all files in the directory specified by _CONFIG_DIRECTORY
    '''
    def _get_config_files():
        config_files = [f for f in listdir(ConfigProvider._CONFIG_DIRECTORY)
                            if isfile(join(ConfigProvider._CONFIG_DIRECTORY, f))
                            and f != '.gitignore']
        return config_files


    '''
    returns the config's file content specified by <name>
    '''
    def get_config(name):
        config_files = ConfigProvider._get_config_files()
        for file in config_files:
            ConfigProvider.logger.debug(f'{file}')
            with open(join(ConfigProvider._CONFIG_DIRECTORY, file), 'r') as f:
                cfg = json.loads(f.read())
                if cfg['name'] != None and cfg['name'] == name:
                    return cfg

    '''
    returns the json names field of all config files
    '''
    def get_config_names():
        names = []
        config_files = ConfigProvider._get_config_files()
        for file in config_files:
            with open(join(ConfigProvider._CONFIG_DIRECTORY, file), 'r') as f:
                cfg = json.loads(f.read())
                if cfg['name']:
                    names.append(cfg['name'])
        return names

    ''' END static '''


    ''' BEGIN object '''

    def __init__(self, config_name):
        super().__init__(config_name)
        self.cfg = ConfigProvider.get_config(config_name)
        if self.cfg is None:
            raise ConfigProviderError(f'config: {config_name} not found')


    def get_source_class(self):
        try:
            source_cls = ConfigProvider.get_class(f"{self.cfg['source']['package']}.{self.cfg['source']['module']}", self.cfg['source']['class'])
            return source_cls
        except ModuleNotFoundError as e:
            ConfigProvider.logger.debug(f'{e}')
            raise ConfigProviderError from e
        except AttributeError as e:
            ConfigProvider.logger.debug(f'{e}')
            raise ConfigProviderError from e
        except Exception as e:
            ConfigProvider.logger.debug(f'{e}')
            raise ConfigProviderError from e


    def get_parser_class(self):
        try:
            parser_cls = ConfigProvider.get_class(f"{self.cfg['parser']['package']}.{self.cfg['parser']['module']}", self.cfg['parser']['class'])
            return parser_cls
        except ModuleNotFoundError as e:
            ConfigProvider.logger.debug(f'{e}')
            raise ConfigProviderError from e
        except AttributeError as e:
            ConfigProvider.logger.debug(f'{e}')
            raise ConfigProviderError from e
        except Exception as e:
            ConfigProvider.logger.debug(f'{e}')
            raise ConfigProviderError from e


    def get_sink_class(self):
        try:
            sink_cls = ConfigProvider.get_class(f"{self.cfg['sink']['package']}.{self.cfg['sink']['module']}", self.cfg['sink']['class'])
            return sink_cls
        except ModuleNotFoundError as e:
            ConfigProvider.logger.debug(f'{e}')
            raise ConfigProviderError from e
        except AttributeError as e:
            ConfigProvider.logger.debug(f'{e}')
            raise ConfigProviderError from e
        except Exception as e:
            ConfigProvider.logger.debug(f'{e}')
            raise ConfigProviderError from e


    def get_source_parameters(self):
        try:
            source_params = self.get_parameters('source')
            return source_params
        except AttributeError as e:
            ConfigProvider.logger.debug(f'get_source_parameters(): {e}')
            raise ConfigProviderError from e
        except Exception as e:
            ConfigProvider.logger.debug(f'get_source_parameters(): {e}')
            raise ConfigProviderError from e


    def get_parser_parameters(self):
        try:
            parser_params = self.get_parameters('parser')
            return parser_params
        except AttributeError as e:
            ConfigProvider.logger.debug(f'get_parser_parameters(): {e}')
            raise ConfigProviderError from e
        except Exception as e:
            ConfigProvider.logger.debug(f'get_parser_parameters(): {e}')
            raise ConfigProviderError from e


    def get_sink_parameters(self):
        try:
            sink_params = self.get_parameters('sink')
            return sink_params
        except AttributeError as e:
            ConfigProvider.logger.debug(f'get_sink_parameters(): {e}')
            raise ConfigProviderError from e
        except Exception as e:
            ConfigProvider.logger.debug(f'get_sink_parameters(): {e}')
            raise ConfigProviderError from e


    '''
    returns the parameters specified by <cfg> and <sequence_part> as a dict
    - returns empty dict if config doesn't contain [<sequence_part>][parameters key]
    '''
    def get_parameters(self, sequence_part):
        try:
            params = {}
            self.cfg[sequence_part]['parameters']
            params.update({p['name']:p['value'] for p in self.cfg[sequence_part]['parameters']})
        except:
            params = {}
        return params

    ''' END static '''
