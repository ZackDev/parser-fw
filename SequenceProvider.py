from Abstract import AbstractSequenceProvider, AbstractStep
from os import listdir
from os.path import isfile, join
import json
import importlib
import logging
from typing import Any


class SequenceProviderError(Exception):
    pass


class SequenceProvider(AbstractSequenceProvider):

    def __init__(self, sequence_name: str, config_directory: str = './config/'):
        self.config_directory = config_directory
        self.logger = logging.getLogger(__name__)
        self.sequence_cfg = self._get_config('sequence', sequence_name)
        self.steps = []
        self.logger.debug(f'{self.sequence_cfg}')

        step_configs = self._get_step_configs(self.sequence_cfg)

        for s_cfg in step_configs:
            step_cls = self._get_step_class(s_cfg)
            step_params = self._get_parameters(s_cfg, 'parameters')
            self.steps.append(step_cls(**step_params))

        self.logger.debug(f'{self.steps}')

        if len(self.steps) < 1:
            raise SequenceProviderError(f'no steps found for sequence: {sequence_name}.')

    # imports and returns the module specified by <module_name>
    # - raises ModuleNotFoundError
    def _load_module(self, module_name: str):
        module = importlib.import_module(module_name)
        return module

    # returns the class identified by <module_name> and <class_name>
    # - raises SequenceProviderError
    def _get_class(self, module_name: str, class_name: str) -> Any:
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

    # returns a list of all files in the directory specified by _CONFIG_DIRECTORY
    # - raises SequenceProviderError
    def _get_config_files(self) -> list:
        config_files = [f for f in listdir(self.config_directory)
                        if isfile(join(self.config_directory, f))]
        if config_files is not None and len(config_files) > 0:
            return config_files
        else:
            raise SequenceProviderError(f"no configs found at directory: {self.config_directory}")

    # searches in all files in the directory specified by _CONFIG_DIRECTORY for a
    # json file which the <keys> name and type
    # returns the config specified by the function parameters <type> and <name>
    # - raises SequenceProviderError if any of the files cannot be loaded
    def _get_config(self, type: str, name: str) -> dict:
        config_files = self._get_config_files()
        cfg = None
        for file in config_files:
            with open(join(self.config_directory, file), 'r') as f:
                try:
                    c = json.loads(f.read())
                    c_name = c['name']
                    c_type = c['type']
                    if c_name is not None and c_type is not None and c_name == name and c_type == type:
                        cfg = c
                        break
                except Exception as exc:
                    raise SequenceProviderError(f'error reading config: {type} {name}') from exc
        if cfg is not None:
            return cfg
        else:
            raise SequenceProviderError(f'config type: {type} name: {name} not found')

    # returns the parameters specified by <config> and <parameter_name> as a dict
    # - returns empty dict if config doesn't contain a <name, value> pair
    #   specified by <parameter_name>
    # - raises SequenceProviderError
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

    # returns the value of the key steps of the sequence config provided as
    # function parameter
    # - raises SequenceProviderError if key steps is not present in sequence_config
    def _get_step_configs(self, sequence_config: dict) -> list:
        steps = sequence_config.get('steps')
        if steps is None:
            raise SequenceProviderError('steps not found in sequence config.')
        if not isinstance(steps, list):
            raise SequenceProviderError('steps is not a list.')
        return steps

    # returns the class of the step provided with the step_config function parameter
    # - raises SequenceProviderError if package, module or class value is not present
    #   in the step_config
    # - raises SequenceProviderError
    def _get_step_class(self, step_config: dict) -> dict:
        try:
            sc_package = step_config.get('package')
            sc_module = step_config.get('module')
            sc_class = step_config.get('class')
            if sc_package is None:
                raise SequenceProviderError('error reading package from sequence_config..')
            if sc_module is None:
                raise SequenceProviderError('error reading module from sequence_config..')
            if sc_class is None:
                raise SequenceProviderError('error reading class from sequence_config..')
            step_cls = self._get_class(f"{sc_package}.{sc_module}", sc_class)
            return step_cls
        except Exception as e:
            raise SequenceProviderError(f'unexpected error reading package/module/class keys from sequence_config.') from e

    def get_sequence(self) -> list:
        return self.steps
