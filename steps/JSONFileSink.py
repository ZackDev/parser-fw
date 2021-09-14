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
        try:
            json_data = json.dumps(data)
        except Exception as e:
            raise StepError('error reading json from data.') from e

        if json_data != None:
            try:
                with open(self.target, 'w') as file:
                    file.write(json_data)
            except Exception as e:
                raise StepError('error writing file.') from e
        else:
            raise StepError('JSONFileSink: json_data is None')
