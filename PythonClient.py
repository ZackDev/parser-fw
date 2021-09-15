from Seshu import Seshu
from SequenceProviderAndRunnerFactory import SequenceProviderAndRunnerFactory


"""
example: how to use Seshu from python
"""


if __name__ == '__main__':
    factory = SequenceProviderAndRunnerFactory('daily-cases-github')
    Seshu(factory, 1)
