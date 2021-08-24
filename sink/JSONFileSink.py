from abc import ABC
from abstract.AbstractSink import AbstractSink
import json

class JSONFileSink(AbstractSink):

    def _store(self):
        json_data = None

        try:
            json_data = json.dumps(self.data)
        except:
            pass

        if json_data != None:
            try:
                with open(self.target, 'w') as file:
                    file.write(json_data)
            except Exception as e:
                raise Exception(e)
        else:
            raise Exception('JSONFileSink: json_data is None')
