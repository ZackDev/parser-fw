import argparse
import logging
from seqconf.ConfigReader import get_config
from Sequence import Sequence
from Sequence import SequenceRegister
from source.HTTPResponseSource import HTTPResponseSource
from parser.DailyCasesParser import DailyCasesParser
from parser.DailyVaccinationsParser import DailyVaccinationsParser
from parser.WeeklyTestsParser import WeeklyTestsParser
from parser.ICUOccupancyParser import ICUOccupancyParser
from parser.VaccinationsByVaccineParser import VaccinationsByVaccineParser
from sink.JSONFileSink import JSONFileSink

def init_sequence(sequence):
    cfg = get_config(sequence)
    logger = logging.getLogger(__name__)
    if cfg:
        # create source object from cfg
        try:
            class_name = cfg['source']['name']
        except KeyError as e:
            logger.critical('Source classname not found in config.')
        try:
            source = globals()[class_name]
        except KeyError as e:
            logger.critical(f'class {class_name} not found in globals().')
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
            logger.critical('Parser classname not found in config.')
        try:
            parser = globals()[class_name]
        except KeyError as e:
            logger.critical(f'class: {class_name} not found in globals().')
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
            logger.critical('Sink classname not found in config.')
        try:
            sink = globals()[class_name]
        except KeyError as e:
            logger.critical(f'class: {class_name} not found in globals()')
        si_params = {}
        try:
            si_params.update({p['name']:p['value'] for p in cfg['sink']['parameters']})
        except KeyError as e:
            pass
        si_params.update({"parser":pa})
        si = sink(**si_params)

        Sequence(so, pa, si, cfg['name']).run()

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--sequence", type=str)
    arg_parser.add_argument("-l", "--loglevel", type=int)
    args = arg_parser.parse_args()
    if (args.loglevel and args.sequence):
        loglevel = args.loglevel*10
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
