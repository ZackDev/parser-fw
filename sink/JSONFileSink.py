from abc import ABC
from abstract.AbstractSink import AbstractSink, SinkError
import json

class JSONFileSink(AbstractSink):

    def _store(self):
        json_data = None

        json_data = json.dumps(self.data)

        if json_data != None:
            with open(self.target, 'w') as file:
                file.write(json_data)
        else:
            raise SinkError('JSONFileSink: json_data is None')
