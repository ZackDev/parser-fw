import argparse
import logging
import importlib
from SequenceProviderAndRunnerFactory import SequenceProviderAndRunnerFactory
from SequenceProvider import SequenceProviderError
from SequenceRunner import SequenceRunnerError
from Abstract import AbstractSequenceProviderAndRunnerFactory

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
            sequence_provider = factory.get_provider(sequence_name)
            sequence_runner = factory.get_runner(sequence_name)
            steps = sequence_provider.get_sequence()
            for step in steps:
                sequence_runner.add_step(step)
            sequence_runner.run()
            logger.info(f'finished sequence {sequence_name} ({len(sequence_runner.steps)} steps).')
        except SequenceProviderError as spe:
            logging.exception(f'error creating SequenceProvider object with sequence_name: {sequence_name}.')
        except SequenceRunnerError as sre:
            logging.exception(f'error running sequence: {sequence_name}')
        except Exception as e:
            logging.exception(f'unexpected error.')
        finally:
            exit(0)
