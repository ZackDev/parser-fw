from abc import ABC
from abstract.AbstractSource import AbstractSource
import logging
import requests

class HTTPResponseSource(AbstractSource):
    def __init__(self, source):
        self.logger = logging.getLogger(__name__)
        super().__init__(self, source)

    def _get_data(self):
        logging.debug('AbstractSource: _get_data() called.')
        try:
            logging.debug(f'calling requests.get() with {self.source}')
            rsp = requests.get(self.source)
            if rsp.status_code == 200:
                logging.debug(f'call to requests.get() finished.')
                logging.debug(f'status code: {rsp.status_code}')
                logging.debug(f'content: {rsp.content}')
                self.data = rsp.content
            else:
                logging.critical('call to requests.get() failed.')
                logging.critical(f'status code: {rsp.status_code}')
                logging.critical(f'content: {rsp.content}')
                raise ConnectionError(f'Connection failed with http status code {rsp.status_code}')
        except Exception as e:
            logging.critical('call to requests.get() failed. Raising ConnectionError.')
            raise ConnectionError(e)
