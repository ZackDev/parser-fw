from abc import ABC
from AbstractSource import AbstractSource
import requests

class HTTPResponseSource(AbstractSource):

    def _get_data(self):
        try:
            rsp = requests.get(self.source)
            if rsp.status_code == 200:
                self.data = rsp.content
            else:
                raise ConnectionError(f'Connection failed with http status code {rsp.status_code}')
        except Exception as e:
            raise ConnectionError(e)
