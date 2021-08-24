from __future__ import annotations
from abc import ABC, abstractmethod

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
    def __init__(self, source):
        self.source = source

    def run(self):
        try:
            self._parse(self.source.data)
        except Exception as e:
            raise ParserError(e)

    @abstractmethod
    def _parse(self, data):
        pass
