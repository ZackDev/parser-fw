from Seshu import Seshu
from SequenceProviderAndRunnerFactory import SequenceProviderAndRunnerFactory
import argparse


# example: supply Seshu with command line parameters


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--sequence", type=str)
    arg_parser.add_argument("-l", "--loglevel", type=int, default=2)
    arg_parser.add_argument("-n", "--names", action="store_true")
    args = arg_parser.parse_args()
    if (args.loglevel and args.sequence):
        factory = SequenceProviderAndRunnerFactory('Production')
        Seshu(factory, args.sequence, args.loglevel)
    elif (args.names is True):
        factory = SequenceProviderAndRunnerFactory('Production')
        sequence_names = factory.get_provider().get_sequence_names()
        print(f'list of sequences: {sequence_names}')
    else:
        arg_parser.print_help()
