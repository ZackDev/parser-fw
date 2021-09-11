from __future__ import annotations
from abc import ABC, abstractmethod
import logging

class SinkError(Exception):
    pass


'''
the abstract sink, where all concrete sinks should be derived from
- init():   takes a concrete parser object and a target as parameter
- run():    calls the _store(...) function of the concrete Sink object, gets
            called by the Sequence object
- _store(): gets implemented in the specific Sink object
'''
class AbstractSink(ABC):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('__init__() called.')
        self.logger.debug(f'with parameter kwargs: {kwargs}')
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except Exception as e:
            raise SinkError(f'error setattr(): {key} {value}') from e

    def run(self):
        self.logger.debug('run() called.')
        self.logger.debug(f'with data: {self.parser.parsed_data}')

        try:
            self.data = self.parser.parsed_data
            self._store()
        except Exception as e:
            raise SinkError from e

        self.logger.debug('run() finished.')

    @abstractmethod
    def _store(self):
        raise NotImplementedError
