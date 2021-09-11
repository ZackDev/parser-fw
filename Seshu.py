import argparse
import logging
import importlib
from ConfigProvider import ConfigProvider, ConfigProviderError
from Sequence import Sequence


def init_sequence(sequence_name):
    logger = logging.getLogger(__name__)

    try:
        cfg_provider = ConfigProvider(sequence_name)

        source_cls = cfg_provider.get_source_class()
        source_params = cfg_provider.get_source_parameters()
        source = source_cls(**source_params)

        parser_cls = cfg_provider.get_parser_class()
        parser_params = cfg_provider.get_parser_parameters()
        parser_params.update({"source":source})
        parser = parser_cls(**parser_params)

        sink_cls = cfg_provider.get_sink_class()
        sink_params = cfg_provider.get_sink_parameters()
        sink_params.update({"parser":parser})
        sink = sink_cls(**sink_params)
    except ConfigProviderError as e:
        logger.critical(f'error reading config: {e}')
        logger.critical('exiting program due to critical error.')
        exit(1)
    except Exception as e:
        logger.critical(f'unexcpected error reading config: {e}')
        logger.critical('exiting program due to critical error.')
        exit(1)

    try:
        s = Sequence(source, parser, sink, sequence_name)
        s.run()
    except Exception as e:
        logger.critical(f'error during creation/running of sequence: {e}')
        logger.critical('exiting program due to critical error.')
        exit(1)


def init_logger(loglevel):
    loglevel = loglevel*10
    # loglevels in numbers: DEBUG:10, INFO:20, WARN:30, ERROR:40, CRITICAL:50
    available_loglevels = [logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL]
    cnt = available_loglevels.count(loglevel)
    if cnt == 1:
        logging.basicConfig(filename='parser-fw.log', encoding='utf-8', level=loglevel, format='%(asctime)s %(name)s %(levelname)s : %(message)s')
        logger = logging.getLogger(__name__)
        logger.info(f'program started with loglevel: {loglevel}')
    else:
        logging.basicConfig(filename='parser-fw.log', encoding='utf-8', format='%(asctime)s %(name)s %(levelname)s : %(message)s')
        logger = logging.getLogger(__name__)
        logger.warning(f'provided loglevel: {loglevel} not supported. running Seshu with default loglevel.')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--sequence", type=str)
    arg_parser.add_argument("-l", "--loglevel", type=int)
    args = arg_parser.parse_args()
    if (args.loglevel and args.sequence):
        init_logger(args.loglevel)
        init_sequence(args.sequence)
    else:
        arg_parser.print_help()
        exit(1)
