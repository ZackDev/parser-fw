import argparse
import logging
import importlib
from seqconf.ClassLoader import get_class
from seqconf.ConfigReader import get_config, get_config_names
from Sequence import Sequence


def init_sequence(sequence):
    cfg = get_config(sequence)
    logger = logging.getLogger(__name__)
    if cfg:
        # create source object from cfg
        try:
            class_name = cfg['source']['name']
        except KeyError as e:
            logger.critical('source classname not found in config.')
        try:
            source = get_class(f'source.{class_name}', class_name)
        except Exception as e:
            logger.critical(f'{e}')
        so_params = {}
        try:
            so_params.update({p['name']:p['value'] for p in cfg['source']['parameters']})
        except KeyError as e:
            pass
        so = source(**so_params)

        # create parser object from cfg
        try:
            class_name = cfg['parser']['name']
        except KeyError as e:
            logger.critical('parser classname not found in config.')
        try:
            parser = get_class(f'parser.{class_name}', class_name)
        except Exception as e:
            logger.critical(f'{e}')
        pa_params = {}
        try:
            pa_params.update({p['name']:p['value'] for p in cfg['parser']['parameters']})
        except KeyError as e:
            pass
        pa_params.update({"source":so})
        pa = parser(**pa_params)

        # create sink object from cfg
        try:
            class_name = cfg['sink']['name']
        except KeyError as e:
            logger.critical('sink classname not found in config.')
        try:
            sink = get_class(f'sink.{class_name}', class_name)
        except Exception as e:
            logger.critical(f'{e}')
        si_params = {}
        try:
            si_params.update({p['name']:p['value'] for p in cfg['sink']['parameters']})
        except KeyError as e:
            pass
        si_params.update({"parser":pa})
        si = sink(**si_params)

        Sequence(so, pa, si, cfg['name']).run()
    else:
        print(f'sequence: {sequence} not found.\navailable sequences:\n{", ".join(get_config_names())}')

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--sequence", type=str)
    arg_parser.add_argument("-l", "--loglevel", type=int)
    args = arg_parser.parse_args()
    if (args.loglevel and args.sequence):
        loglevel = args.loglevel*10
        # loglevels in numbers: DEBUG:10, INFO:20, WARN:30, ERROR:40, CRITICAL:50
        available_loglevels = [logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL]
        cnt = available_loglevels.count(loglevel)
        if cnt == 1:
            logging.basicConfig(filename='parser-fw.log', encoding='utf-8', level=loglevel, format='%(asctime)s %(name)s %(levelname)s : %(message)s')
            logger = logging.getLogger(__name__)
            logger.info(f'program started with loglevel: {loglevel}')
            init_sequence(args.sequence)
        else:
            print(f'provided loglevel not recognized.')
    else:
        arg_parser.print_help()
        exit(1)
