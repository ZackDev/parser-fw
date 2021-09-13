import argparse
import logging
import importlib
from abstract.AbstractStep import StepError
from SequenceProvider import SequenceProvider, SequenceProviderError
from SequenceRunner import SequenceRunner

_DEFAULT_LOGLEVEL = 2

class SeshuError:
    pass

def init_sequence(sequence_name):
    logger = logging.getLogger(__name__)

    """ create SequenceProvider """
    try:
        cfg_provider = SequenceProvider(sequence_name)
        steps = cfg_provider.get_sequence()
        s = SequenceRunner(sequence_name)
        for step in steps:
            s.add_step(step)
        s.run()
    except SequenceProviderError as spe:
        logger.critical(f'error creating SequenceProvider object: {spe}')
    except StepError as se:
        logger.critical(f'error while running step: {se}')
    except Exception as e:
        logger.critical(f'unexpected error creating SequenceProvider object: {e}')
    finally:
        exit(0)


def init_logger(loglevel=_DEFAULT_LOGLEVEL):
    loglevel = loglevel*10
    # loglevels in numbers: DEBUG:10, INFO:20, WARN:30, ERROR:40, CRITICAL:50
    available_loglevels = [logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL]
    cnt = available_loglevels.count(loglevel)
    if cnt != 1:
        loglevel = logging.INFO
    logging.basicConfig(filename='parser-fw.log', encoding='utf-8', level=loglevel, format='%(asctime)s %(name)s %(levelname)s : %(message)s')
    logger = logging.getLogger(__name__)
    logger.info(f'program started with loglevel: {loglevel}')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--sequence", type=str)
    arg_parser.add_argument("-l", "--loglevel", type=int, default=_DEFAULT_LOGLEVEL)
    args = arg_parser.parse_args()
    if (args.loglevel and args.sequence):
        init_logger(args.loglevel)
        init_sequence(args.sequence)
    else:
        arg_parser.print_help()
