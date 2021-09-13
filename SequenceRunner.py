import logging

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
                self.data = s.run(self.data)
            except StepError as se:
                raise SequenceRunnerError() from se
            except Exception as e:
                raise SequenceRunnerError() from e
        self.logger.info(f'finished sequence {self.name} ({len(self.steps)} steps).')
