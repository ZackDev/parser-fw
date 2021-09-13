import logging

class SequenceRunner:
    def __init__(self, name):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.steps = []

    def add_step(self, step):
        self.logger.info('added step.')
        self.steps.append(step)

    def run(self):
        self.logger.info('running step.')
        self.data = ''
        for s in self.steps:
            self.data = s.run(self.data)
