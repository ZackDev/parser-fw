from __future__ import annotations
from abc import ABC, abstractmethod
import logging

class ParserError(Exception):
    pass


'''
the abstract parser, where all concrete parser classes should be derived from
- init():   parser object creation which takes a concrete Source object as parameter
- run():    calls the _parse(...) function of the concrete Parser object, gets
            called by the Sequence object
- _parse(): gets implemented in the specific Parser object
'''
class AbstractParser(ABC):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('__init__() called.')
        self.logger.debug(f'with parameter kwargs: {kwargs}')

        if "source" in kwargs:
            pass
        else:
            raise ParserError(f'error: source not in kwargs.')

        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except Exception as e:
            raise ParserError(f'error setattr(): {key} {value}') from e

    def run(self):
        self.logger.debug('run() called.')

        try:
            self._parse(self.source.data)
        except Exception as e:
            raise ParserError(f'{e}')

        self.logger.debug('run() finished.')

    @abstractmethod
    def _parse(self, data):
        raise NotImplementedError
