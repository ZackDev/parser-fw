import logging
from abstract.AbstractStep import StepError
class SequenceRunnerError(Exception):
    pass

class SequenceRunner:
    def __init__(self, name):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def run(self):
        self.data = ''
        for s in self.steps:
            try:
                self.data = s.step(self.data)
            except StepError as se:
                raise SequenceRunnerError('error running step().') from se
            except Exception as e:
                raise SequenceRunnerError('unexpected error running step().') from e
