from abc import ABC
from abstract.AbstractSink import AbstractSink
import json

class JSONFileSink(AbstractSink):

    def _store(self):
        with open(self.target, 'w') as file:
            file.write(json.dumps(self.data))
