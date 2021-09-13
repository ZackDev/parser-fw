from abc import ABC
from abstract.AbstractStep import AbstractStep
import logging
import requests

class HTTPResponseSource(AbstractStep):
    def run(self, data):
        self.logger.debug('_get_data() called.')
        try:
            self.logger.debug(f'calling requests.get() with {self.source}')
            rsp = requests.get(self.source)
            if rsp.status_code == 200:
                self.logger.debug(f'call to requests.get() finished.')
                self.logger.debug(f'status code: {rsp.status_code}')
                self.logger.debug(f'content: {rsp.content}')
                return rsp.content
            else:
                self.logger.critical('call to requests.get() failed.')
                self.logger.critical(f'status code: {rsp.status_code}')
                raise ConnectionError(f'Connection failed with http status code {rsp.status_code}')
        except Exception as e:
            self.logger.critical('call to requests.get() failed. Raising ConnectionError.')
            raise ConnectionError from e