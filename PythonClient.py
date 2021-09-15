from Seshu import Seshu
from SequenceProviderAndRunnerFactory import SequenceProviderAndRunnerFactory
"""
example: how to use Seshu from terminal
"""


if __name__ == '__main__':
    factory = SequenceProviderAndRunnerFactory()
    Seshu(factory, 'daily-cases-github', 1)
