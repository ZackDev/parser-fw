from __future__ import annotations
from abc import ABC, abstractmethod

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
    def __init__(self, source):
        self.source = source

    def run(self):
        try:
            self._get_data()
        except Exception as e:
            raise SourceError(e)

    @abstractmethod
    def _get_data(self):
        pass