from abc import ABC
from abstract.AbstractSink import AbstractSink, SinkError
import json
import logging

class JSONFileSink(AbstractSink):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('__init__() called.')
        self.logger.debug(f'with parameters: {kwargs}')
        super().__init__(**kwargs)


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
