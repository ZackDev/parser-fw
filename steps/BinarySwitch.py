import builtins
from Abstract import AbstractStep, StepError


class BinarySwitch(AbstractStep):
    def run(self, data):
        if self.data is not None and isinstance(self.data, builtins.bool):
            if self.data is not self.expected:
                self.logger.debug(f'self.data: {self.data} and self.expected: {self.expected} mismatch.')
                exit
            else:
                return True
        else:
            raise StepError(f'self.data: {self.data} is not a boolean.')
