import argparse
import logging
import importlib
from abstract.AbstractSource import SourceError
from abstract.AbstractParser import ParserError
from abstract.AbstractSink import SinkError
from ConfigProvider import ConfigProvider, ConfigProviderError
from Sequence import Sequence

_DEFAULT_LOGLEVEL = 2

def init_sequence(sequence_name):
    logger = logging.getLogger(__name__)

    """ create ConfigProvider """
    try:
        cfg_provider = ConfigProvider(sequence_name)
    except ConfigProviderError as cpe:
        logger.critical(f'error creating ConfigProvider object: {cpe}')
    except Exception as e:
        logger.critical(f'unexpecter error creating ConfigProvider object: {e}')

    """ SOURCE """
    """ get source class """
    try:
        source_cls = cfg_provider.get_source_class()
    except ConfigProviderError as cpe:
        logger.critical(f'error getting source class from ConfigProvider: {cpe}')
    except Exception as e:
        logger.critical(f'unecpected error getting source class from ConfigProvider: {e}')

    """ get source parameters """
    try:
        source_params = cfg_provider.get_source_parameters()
    except ConfigProviderError as cpe:
        logger.critical(f'error getting source parameters from ConfigProvider: {cpe}')
    except Exception as e:
        logger.critical(f'unecpected error getting source parameters from ConfigProvider: {e}')

    """ create source object """
    try:
        source = source_cls(**source_params)
    except SourceError as se:
        logger.critical(f'error creating source object: {se}')
    except Exception as e:
        logger.critical(f'unexpected error creating source object: {e}')

    """ PARSER """
    """ get parser class """
    try:
        parser_cls = cfg_provider.get_parser_class()
    except ConfigProviderError as cpe:
        logger.critical(f'error getting parser class from ConfigProvider: {cpe}')
    except Exception as e:
        logger.critical(f'unecpected error getting parser class from ConfigProvider: {e}')

    """ get parser parameters """
    try:
        parser_params = cfg_provider.get_parser_parameters()
        parser_params.update({"source":source})
    except ConfigProviderError as cpe:
        logger.critical(f'error getting parser parameters from ConfigProvider: {cpe}')
    except Exception as e:
        logger.critical(f'unecpected error getting parser parameters from ConfigProvider: {e}')

    """ create parser object """
    try:
        parser = parser_cls(**parser_params)
    except SourceError as se:
        logger.critical(f'error creating parser object: {se}')
    except Exception as e:
        logger.critical(f'unexpected error creating parser object: {e}')


    """ SINK """
    """ get sink class """
    try:
        sink_cls = cfg_provider.get_sink_class()
    except ConfigProviderError as cpe:
        logger.critical(f'error getting sink class from ConfigProvider: {cpe}')
    except Exception as e:
        logger.critical(f'unecpected error getting sink class from ConfigProvider: {e}')

    """ get sink parameters """
    try:
        sink_params = cfg_provider.get_sink_parameters()
        sink_params.update({"parser":parser})
    except ConfigProviderError as cpe:
        logger.critical(f'error getting sink parameters from ConfigProvider: {cpe}')
    except Exception as e:
        logger.critical(f'unecpected error getting sink parameters from ConfigProvider: {e}')

    """ create sink object """
    try:
        sink = sink_cls(**sink_params)
    except SinkError as se:
        logger.critical(f'error creating sink object: {se}')
    except Exception as e:
        logger.critical(f'unexpected error creating sink object: {e}')

    """ SEQUENCE """
    """ create sequence object and call it's run method """
    try:
        s = Sequence(source, parser, sink, sequence_name)
        s.run()
    except Exception as e:
        logger.critical(f'error during creation/running of sequence: {e}')
        logger.critical('exiting program due to critical error.')
        exit(1)


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
        exit(1)
