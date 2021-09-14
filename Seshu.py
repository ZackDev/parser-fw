import argparse
import logging
import importlib
from SequenceProviderAndRunnerFactory import SequenceProviderAndRunnerFactory
from abstract.AbstractStep import StepError
from abstract.AbstractSequenceProviderAndRunnerFactory import AbstractSequenceProviderAndRunnerFactory

_DEFAULT_LOGLEVEL = 2

class SeshuError:
    pass

class Seshu:
    def __init__(self, factory: AbstractSequenceProviderAndRunnerFactory, sequence_name: str, loglevel: int = _DEFAULT_LOGLEVEL):
        loglevel = loglevel*10
        # loglevels in numbers: DEBUG:10, INFO:20, WARN:30, ERROR:40, CRITICAL:50
        available_loglevels = [logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL]
        cnt = available_loglevels.count(loglevel)
        if cnt != 1:
            loglevel = logging.INFO
        logging.basicConfig(filename='parser-fw.log', encoding='utf-8', level=loglevel, format='%(asctime)s %(name)s %(levelname)s : %(message)s')
        logger = logging.getLogger(__name__)
        logger.info(f'program started with sequence_name: {sequence_name} and loglevel: {loglevel}.')

        """ create SequenceProvider """
        try:
            cfg_provider = factory.get_provider(sequence_name)
            steps = cfg_provider.get_sequence()
            s = factory.get_runner(sequence_name)
            for step in steps:
                s.add_step(step)
            s.run()
            logger.info(f'finished sequence {sequence_name} ({len(s.steps)} steps).')
        except SequenceProviderError as spe:
            logging.exception(f'error creating SequenceProvider object with sequence_name: {sequence_name}.')
        except SequenceRunnerError as sre:
            logging.exception(f'error running sequence: {sequence_name}')
        except Exception as e:
            logging.exception(f'unexpected error.')
        finally:
            exit(0)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--sequence", type=str)
    arg_parser.add_argument("-l", "--loglevel", type=int, default=_DEFAULT_LOGLEVEL)
    args = arg_parser.parse_args()
    if (args.loglevel and args.sequence):
        factory = SequenceProviderAndRunnerFactory()
        Seshu(factory, args.sequence, args.loglevel)
    else:
        arg_parser.print_help()
