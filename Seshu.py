import argparse
import logging
import importlib
from ConfigProvider import ConfigProvider
from Sequence import Sequence


def init_sequence(sequence_name):
    logger = logging.getLogger(__name__)
    test = False

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

    s = Sequence(source, parser, sink, sequence_name)
    s.run()

    if cfg and test == True:
        '''
        create source object from cfg
        - get class_name from cfg
        '''
        package_name, module_name, class_name = None, None, None
        try:
            package_name = cfg['source']['package']
            module_name = cfg['source']['module']
            class_name = cfg['source']['class']
        except KeyError as e:
            logger.critical('class info (package, module, class) not found in config.')
        except Exception as e:
            logger.critical(f'unexpected error: {e}')

        '''
        - dynamic import of <class> from <package>.<module>
        '''
        if package_name and module_name and class_name:
            try:
                source = get_class(f'{package_name}.{module_name}', class_name)
            except Exception as e:
                logger.critical(f'unable to dynamically load class {class_name} from {package_name}.{module_name}.')
        else:
            if not package_name:
                logger.critical('failed to get package_name from cfg.')
            if not module_name:
                logger.critical('falied to get module_name from cfg.')
            if not class_name:
                logger.critical('failed to get class_name from cfg.')

        '''
        - populate source object kwargs (keyword arguments) with parameters from cfg
        '''
        so_params = {}
        try:
            so_params.update({p['name']:p['value'] for p in cfg['source']['parameters']})
        except KeyError as e:
            pass
        so = source(**so_params)

        '''
        create parser object from cfg
        '''
        package_name, module_name, class_name = None, None, None
        try:
            package_name = cfg['parser']['package']
            module_name = cfg['parser']['module']
            class_name = cfg['parser']['class']
        except KeyError as e:
            logger.critical('class info (package, module, class) not found in config.')
        try:
            parser = get_class(f'{package_name}.{module_name}', class_name)
        except Exception as e:
            logger.critical(f'unable to dynamically load class {class_name} from {package_name}.{module_name}.')
        pa_params = {}
        try:
            pa_params.update({p['name']:p['value'] for p in cfg['parser']['parameters']})
        except KeyError as e:
            pass
        pa_params.update({"source":so})
        pa = parser(**pa_params)

        '''
        create sink object from cfg
        '''
        package_name, module_name, class_name = None, None, None
        try:
            package_name = cfg['sink']['package']
            module_name = cfg['sink']['module']
            class_name = cfg['sink']['class']
        except KeyError as e:
            logger.critical('sink classname not found in config.')
        try:
            sink = get_class(f'{package_name}.{module_name}', class_name)
        except Exception as e:
            logger.critical(f'unable to dynamically load class {class_name} from {package_name}.{module_name}.')
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
            logging.basicConfig(filename='parser-fw.log', encoding='utf-8', format='%(asctime)s %(name)s %(levelname)s : %(message)s')
            logger = logging.getLogger(__name__)
            logger.warning(f'provided loglevel: {loglevel} not supported. running Seshu with default loglevel.')
            init_sequence(args.sequence)
    else:
        arg_parser.print_help()
        exit(1)
