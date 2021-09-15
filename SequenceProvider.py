from Abstract import AbstractSequenceProvider
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
        try:
            module = SequenceProvider._load_module(module_name)
            cls = getattr(module, class_name)
            return cls
        except ModuleNotFoundError as me:
            raise SequenceProviderError(f'could not load module {module_name}') from me
        except AttributeError as ae:
            raise SequenceProviderError(f'could not get class {class_name}') from ae
        except Exception as e:
            raise SequenceProviderError(f'unexpected error loading module: {module_name} class: {class_name}') from e


    '''
    returns a list of all files in the directory specified by _CONFIG_DIRECTORY
    '''
    def _get_config_files():
        config_files = [f for f in listdir(SequenceProvider._CONFIG_DIRECTORY)
                            if isfile(join(SequenceProvider._CONFIG_DIRECTORY, f))
                            and f != '.gitignore']
        return config_files


    '''
    searches in all files in the directory specified by _CONFIG_DIRECTORY for a
    json file which the <keys> name and type
    returns the config specified by the function parameters <type> and <name>
    - raises SequenceProviderError if any of the files cannot be loaded
    '''
    def _get_config(type, name):
        config_files = SequenceProvider._get_config_files()
        for file in config_files:
            with open(join(SequenceProvider._CONFIG_DIRECTORY, file), 'r') as f:
                try:
                    cfg = json.loads(f.read())
                    if cfg['name'] != None and cfg['type'] == type and cfg['name'] == name:
                        return cfg
                except Exception as exc:
                    raise SequenceProviderError(f'error reading config: {type} {name}') from exc

    '''
    returns the parameters specified by <config> and <parameter_name> as a dict
    - returns empty dict if config doesn't contain a <name, value> pair
      specified by <parameter_name>
    '''
    def _get_parameters(config, parameter_name):
        try:
            params = {}
            params.update({p['name']:p['value'] for p in config[parameter_name]})
        except:
            params = {}
        return params


    '''
    returns the value of the key steps of the sequence config provided as
    function parameter
    - raises SequenceProviderError if key steps is not present in sequence_config
    '''
    def _get_steps(sequence_config):
        try:
            steps = sequence_config['steps']
            return steps
        except:
            raise SequenceProviderError(f'steps not found in {sequence_config}')


    '''
    returns the class of the step provided with the step_config function parameter
    - raises SequenceProviderError if package, module or class value is not present
      in the step_config
    '''
    def _get_step_class(step_config):
        try:
            module_name = f"{step_config['package']}.{step_config['module']}"
            class_name = step_config['class']
        except KeyError as ke:
            raise SequenceProviderError(f'error reading package/module/class keys from {step_config}.') from ke
        except Exception as e:
            raise SequenceProviderError(f'unexpected error reading package/module/class keys from {step_config}.') from e
        step_cls = SequenceProvider._get_class(module_name, class_name)
        return step_cls
    ''' END static '''


    ''' BEGIN object '''

    def __init__(self, sequence_name):
        super().__init__(sequence_name)
        self.sequence_cfg = SequenceProvider._get_config('sequence', sequence_name)
        self.steps = []
        SequenceProvider.logger.debug(f'{self.sequence_cfg}')
        SequenceProvider.logger.debug(f'{self.steps}')
        if self.sequence_cfg is None:
            raise SequenceProviderError(f'config: {sequence_name} not found')

        steps_from_sequence_config = SequenceProvider._get_steps(self.sequence_cfg)
        SequenceProvider.logger.debug(f'{steps_from_sequence_config}')

        for step in steps_from_sequence_config:
            step_cfg = SequenceProvider._get_config('step', step)
            step_cls = SequenceProvider._get_step_class(step_cfg)
            step_params = SequenceProvider._get_parameters(step_cfg, 'parameters')

            self.steps.append(step_cls(**step_params))

        if len(self.steps) < 1:
            raise SequenceProviderError(f'no steps found for sequence: {sequence_name}.')


    def get_sequence(self):
        return self.steps

    ''' END object '''
