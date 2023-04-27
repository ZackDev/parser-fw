from Abstract import AbstractSequenceProviderAndRunnerFactory
from SequenceProvider import SequenceProvider
from SequenceRunner import SequenceRunner


class SequenceProviderAndRunnerFactory(AbstractSequenceProviderAndRunnerFactory):
    def __init__(self, run_type: str):
        super().__init__(run_type)
        match run_type:
            case 'Production':
                self.provider = SequenceProvider()
                self.runner = SequenceRunner()
            case 'Unittest':
                self.provider = SequenceProvider('./test/files/cfg/')
                self.runner = SequenceRunner()

    def get_provider(self) -> SequenceProvider:
        return self.provider

    def get_runner(self) -> SequenceRunner:
        return self.runner
