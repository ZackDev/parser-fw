from Abstract import AbstractSequenceProvider, AbstractStep
from os import listdir
from os.path import isfile, join
import json
import importlib
import logging


class SequenceProviderError(Exception):
    pass


class SequenceProvider(AbstractSequenceProvider):

    def __init__(self, sequence_name: str, config_directory: str = './config/'):
        self.config_directory = config_directory
        self.logger = logging.getLogger(__name__)
        self.sequence_cfg = self._get_config('sequence', sequence_name)
        self.steps = []
        self.logger.debug(f'{self.sequence_cfg}')

        step_names = self._get_step_names(self.sequence_cfg)

        for name in step_names:
            step_cfg = self._get_config('step', name)
            step_cls = self._get_step_class(step_cfg)
            step_params = self._get_parameters(step_cfg, 'parameters')
            self.steps.append(step_cls(**step_params))

        self.logger.debug(f'{self.steps}')

        if len(self.steps) < 1:
            raise SequenceProviderError(f'no steps found for sequence: {sequence_name}.')

    '''
    imports and returns the module specified by <module_name>
    - raises ModuleNotFoundError
    '''

    def _load_module(self, module_name: str):
        module = importlib.import_module(module_name)
        return module

    '''
    returns the class identified by <module_name> and <class_name>
    - raises SequenceProviderError
    '''

    def _get_class(self, module_name: str, class_name: str) -> AbstractStep:
        try:
            module = self._load_module(module_name)
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

    def _get_config_files(self) -> list:
        config_files = [f for f in listdir(self.config_directory)
                        if isfile(join(self.config_directory, f))
                        and f != '.gitignore']
        return config_files

    '''
    searches in all files in the directory specified by _CONFIG_DIRECTORY for a
    json file which the <keys> name and type
    returns the config specified by the function parameters <type> and <name>
    - raises SequenceProviderError if any of the files cannot be loaded
    '''

    def _get_config(self, type: str, name: str) -> dict:
        config_files = self._get_config_files()
        for file in config_files:
            with open(join(self.config_directory, file), 'r') as f:
                try:
                    cfg = json.loads(f.read())
                    if cfg['name'] is not None and cfg['type'] == type and cfg['name'] == name:
                        return cfg
                except Exception as exc:
                    raise SequenceProviderError(f'error reading config: {type} {name}') from exc

    '''
    returns the parameters specified by <config> and <parameter_name> as a dict
    - returns empty dict if config doesn't contain a <name, value> pair
      specified by <parameter_name>
    '''

    def _get_parameters(self, config: dict, parameter_name: str) -> dict:
        try:
            if parameter_name in config:
                params = {}
                for key, value in config[parameter_name].items():
                    params.update({key: value})
                return params
            else:
                return {}
        except Exception as e:
            raise SequenceProviderError('unexpected error getting parameter from config.') from e

    '''
    returns the value of the key steps of the sequence config provided as
    function parameter
    - raises SequenceProviderError if key steps is not present in sequence_config
    '''

    def _get_step_names(self, sequence_config: dict) -> list:
        try:
            steps = sequence_config['steps']
            if isinstance(steps, list):
                return steps
            else:
                self.logger.warn('sequence config is malformed.')
        except Exception:
            raise SequenceProviderError(f'steps not found in {sequence_config}')

    '''
    returns the class of the step provided with the step_config function parameter
    - raises SequenceProviderError if package, module or class value is not present
      in the step_config
    '''

    def _get_step_class(self, step_config: dict) -> dict:
        try:
            module_name = f"{step_config['package']}.{step_config['module']}"
            class_name = step_config['class']
            step_cls = self._get_class(module_name, class_name)
            return step_cls
        except KeyError as ke:
            raise SequenceProviderError(f'error reading package/module/class keys from {step_config}.') from ke
        except Exception as e:
            raise SequenceProviderError(f'unexpected error reading package/module/class keys from {step_config}.') from e

    def get_sequence(self) -> list:
        return self.steps
