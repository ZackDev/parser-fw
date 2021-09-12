from __future__ import annotations
from abc import ABC, abstractmethod
import logging

class SourceError(Exception):
    pass

'''
the abstract source, where all concrete sources should be derived from
- init():       takes a source as argument
- run():        calls the _get_data() method of the concrete source object
- _get_data():  abstract method, used for specific implementation in specific
                source object
'''
class AbstractSource(ABC):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('__init__() called.')
        self.logger.debug(f'with parameter source: {kwargs}')

        if "source" in kwargs:
            pass
        else:
            raise SourceError(f'error: source not kwargs.')

        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except Exception as e:
            raise SourceError(f'error setattr() {key} {value}') from e

    def run(self):
        self.logger.debug('run() called.')

        try:
            self._get_data()
        except Exception as e:
            raise SourceError from e

        self.logger.debug('run() finished.')

    @abstractmethod
    def _get_data(self):
        raise NotImplementedError
