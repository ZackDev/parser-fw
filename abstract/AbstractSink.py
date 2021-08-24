from __future__ import annotations
from abc import ABC, abstractmethod

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
        self.parser = parser
        self.target = target

    def run(self):
        try:
            self.data = self.parser.parsed_data
            self._store()
        except Exception as e:
            raise SinkError(e)

    @abstractmethod
    def _store(self):
        pass
