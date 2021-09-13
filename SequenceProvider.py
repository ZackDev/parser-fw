from abstract.AbstractSequenceProvider import AbstractSequenceProvider
from os import listdir
from os.path import isfile, join
import json
import importlib
import logging


class SequenceProviderError(Exception):
    pass


class SequenceProvider(AbstractSequenceProvider):

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
    def _get_class(module_name, class_name):
        module = SequenceProvider._load_module(module_name)
        cls = getattr(module, class_name)
        return cls


    '''
    returns a list of all files in the directory specified by _CONFIG_DIRECTORY
    '''
    def _get_config_files():
        config_files = [f for f in listdir(SequenceProvider._CONFIG_DIRECTORY)
                            if isfile(join(SequenceProvider._CONFIG_DIRECTORY, f))
                            and f != '.gitignore']
        return config_files


    '''
    returns the sequence config's file content specified by <sequence_name>
    '''
    def get_config(type, name):
        config_files = SequenceProvider._get_config_files()
        for file in config_files:
            with open(join(SequenceProvider._CONFIG_DIRECTORY, file), 'r') as f:
                try:
                    cfg = json.loads(f.read())
                    if cfg['name'] != None and cfg['type'] == type and cfg['name'] == name:
                        return cfg
                except Exception as exc:
                    SequenceProvider.logger.critical(f'error reading config: {type} {name}')

    '''
    returns the parameters specified by <cfg> and <sequence_part> as a dict
    - returns empty dict if config doesn't contain [<sequence_part>][parameters key]
    '''
    def get_parameters(config, parameter_name):
        try:
            params = {}
            config[parameter_name]
            params.update({p['name']:p['value'] for p in config[parameter_name]})
        except:
            params = {}
        return params


    def get_steps(config):
        try:
            steps = config['steps']
            return steps
        except:
            raise SequenceProviderError()


    def get_step_class(step_config):
        try:
            step_cls = SequenceProvider._get_class(f"{step_config['package']}.{step_config['module']}", step_config['class'])
            return step_cls
        except ModuleNotFoundError as e:
            SequenceProvider.logger.debug(f'{e}')
            raise SequenceProviderError from e
        except AttributeError as e:
            SequenceProvider.logger.debug(f'{e}')
            raise SequenceProviderError from e
        except Exception as e:
            SequenceProvider.logger.debug(f'{e}')
            raise SequenceProviderError from e
    ''' END static '''


    ''' BEGIN object '''

    def __init__(self, sequence_name):
        super().__init__(sequence_name)
        self.sequence_cfg = SequenceProvider.get_config('sequence', sequence_name)
        self.steps = []
        SequenceProvider.logger.debug(f'{self.sequence_cfg}')
        SequenceProvider.logger.debug(f'{self.steps}')
        if self.sequence_cfg is None:
            raise SequenceProviderError(f'config: {sequence_name} not found')

        steps_from_sequence_config = SequenceProvider.get_steps(self.sequence_cfg)
        SequenceProvider.logger.debug(f'{steps_from_sequence_config}')

        for step in steps_from_sequence_config:
            step_cfg = SequenceProvider.get_config('step', step)
            step_cls = SequenceProvider._get_class(f'{step_cfg["package"]}.{step_cfg["module"]}', f'{step_cfg["class"]}')
            step_params = SequenceProvider.get_parameters(step_cfg, 'parameters')

            self.steps.append(step_cls(**step_params))


    def get_sequence(self):
        return self.steps

    ''' END object '''
