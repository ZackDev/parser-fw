from Abstract import AbstractSequenceProviderAndRunnerFactory
from SequenceProvider import SequenceProvider
from SequenceRunner import SequenceRunner


class SequenceProviderAndRunnerFactory(AbstractSequenceProviderAndRunnerFactory):
    def __init__(self, run_type: str, sequence_name: str):
        super().__init__(run_type, sequence_name)
        match run_type:
            case 'Production':
                self.provider = SequenceProvider(self.sequence_name)
                self.runner = SequenceRunner(self.sequence_name)
            case 'Unittest':
                self.provider = SequenceProvider(self.sequence_name, './test/files/cfg/')
                self.runner = SequenceRunner(self.sequence_name)

    def get_provider(self) -> SequenceProvider:
        return self.provider

    def get_runner(self) -> SequenceRunner:
        return self.runner
