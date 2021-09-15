from Abstract import AbstractStep, StepError
import requests


class HTTPResponseSource(AbstractStep):
    def run(self, data):
        try:
            self.logger.debug(f'calling requests.get() with {self.url}')
            rsp = requests.get(self.url)
            if rsp.status_code == 200:
                self.logger.debug('call to requests.get() finished.')
                return rsp.content
            else:
                self.logger.critical('call to requests.get() failed.')
                self.logger.critical(f'status code: {rsp.status_code}')
                raise StepError(f'Connection failed with http status code {rsp.status_code}')
        except Exception as e:
            raise StepError('requests.get() failed.') from e
