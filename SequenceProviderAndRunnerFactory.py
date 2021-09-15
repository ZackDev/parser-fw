from Abstract import AbstractSequenceProviderAndRunnerFactory
from SequenceProvider import SequenceProvider
from SequenceRunner import SequenceRunner


class SequenceProviderAndRunnerFactory(AbstractSequenceProviderAndRunnerFactory):
    def __init__(self, sequence_name):
        super().__init__(sequence_name)
        self.provider = SequenceProvider(self.sequence_name)
        self.runner = SequenceRunner(self.sequence_name)

    def get_provider(self) -> SequenceProvider:
        return self.provider

    def get_runner(self) -> SequenceRunner:
        return self.runner
