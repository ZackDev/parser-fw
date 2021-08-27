from abc import ABC
from abstract.AbstractSink import AbstractSink, SinkError
import logging
import json

class JSONFileSink(AbstractSink):

    def _store(self):
        logger = logging.getLogger(__name__)
        logger.debug('_store() called.')
        logger.debug(f'with data: {self.data}')
        json_data = None

        json_data = json.dumps(self.data)

        if json_data != None:
            with open(self.target, 'w') as file:
                file.write(json_data)
        else:
            raise SinkError('JSONFileSink: json_data is None')
