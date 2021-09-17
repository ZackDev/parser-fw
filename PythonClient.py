from Seshu import Seshu
from SequenceProviderAndRunnerFactory import SequenceProviderAndRunnerFactory


"""
example: how to use Seshu from python
"""


def run_seshu():
    factory = SequenceProviderAndRunnerFactory('daily-cases-github')
    Seshu(factory, 1)


if __name__ == '__main__':
    run_seshu()
