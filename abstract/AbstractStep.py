from abc import ABC, abstractmethod
import logging

class StepError(Exception):
    pass

class AbstractStep(ABC):
    def __init__(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except Exceptio as exc:
            raise StepError('setattr error.') from exc
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def run(self, data):
        raise NotImplementedError

    def step(self):
        self.logger.info('step.')
        return self.run(self.data)
