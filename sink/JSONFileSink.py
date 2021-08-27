from abc import ABC
from abstract.AbstractSink import AbstractSink, SinkError
import json
import logging

class JSONFileSink(AbstractSink):
    def __init__(self, parser, target):
        self.logger = logging.getLogger(__name__)
        super().__init__(parser, target)

    def _store(self):
        self.logger.debug('_store() called.')
        self.logger.debug(f'with data: {self.data}')
        json_data = None

        json_data = json.dumps(self.data)

        if json_data != None:
            with open(self.target, 'w') as file:
                file.write(json_data)
        else:
            raise SinkError('JSONFileSink: json_data is None')
