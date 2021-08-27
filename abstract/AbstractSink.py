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
    def __init__(self, parser, target):
        logger = logging.getLogger(__name__)
        logger.debug('__init__() called.')
        logger.debug(f'with parameter parser: {parser}')
        logger.debug(f'with parameter target: {target}')
        self.parser = parser
        self.target = target

    def run(self):
        logger = logging.getLogger(__name__)
        logger.debug('AbstractSink: run() called.')
        try:
            logger.debug(f'with data: {self.parser.parsed_data}')
            self.data = self.parser.parsed_data
            self._store()
        except Exception as e:
            raise SinkError(e)
        logger.debug('AbstractSink: run() finished.')

    @abstractmethod
    def _store(self):
        pass
