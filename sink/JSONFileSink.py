from abc import ABC
from abstract.AbstractStep import AbstractStep, StepError
import json
import logging

class JSONFileSink(AbstractStep):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('__init__() called.')
        self.logger.debug(f'with parameters: {kwargs}')
        super().__init__(**kwargs)


    def run(self, data):
        self.logger.debug('_store() called.')
        self.logger.debug(f'with data: {data}')
        json_data = None

        json_data = json.dumps(data)

        if json_data != None:
            with open(self.target, 'w') as file:
                file.write(json_data)
        else:
            raise StepError('JSONFileSink: json_data is None')
