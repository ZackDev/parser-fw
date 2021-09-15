from Seshu import Seshu
from SequenceProviderAndRunnerFactory import SequenceProviderAndRunnerFactory
import argparse
"""
example: how to use Seshu from console
"""


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--sequence", type=str)
    arg_parser.add_argument("-l", "--loglevel", type=int, default=2)
    args = arg_parser.parse_args()
    if (args.loglevel and args.sequence):
        factory = SequenceProviderAndRunnerFactory(args.sequence)
        Seshu(factory, args.loglevel)
    else:
        arg_parser.print_help()
