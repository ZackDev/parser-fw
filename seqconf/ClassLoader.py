import importlib
import logging

logger = logging.getLogger(__name__)

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
