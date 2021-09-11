from abstract.AbstractSource import AbstractSource, SourceError
from abstract.AbstractParser import AbstractParser, ParserError
from abstract.AbstractSink import AbstractSink, SinkError
import logging


'''
sequence class used to define a sequence of Source, Parse and Sink
registers the provided sequence name at the SequenceRegister
- init():   takes a Source, Parser, Sink and sequence_name as parameter and
            registers the provided sequence at the SequenceRegister with the
            provided parameter sequence_name
- run():    calls the Source's, Parser's and Sink's run() methods in that order
'''
class Sequence:
    def __init__(self, source, parser, sink, sequence_name):
        logger = logging.getLogger(__name__)
        logger.debug('__init__() called.')
        logger.debug(f'with parameter source: {source}')
        logger.debug(f'with parameter parser: {parser}')
        logger.debug(f'with parameter sink: {sink}')
        logger.debug(f'with parameter sequence_name: {sequence_name}')

        self.sequence_name = sequence_name
        self.source = source
        self.parser = parser
        self.sink = sink

        logging.debug(f'created sequence: {self.sequence_name}')

    def run(self):
        logger = logging.getLogger(__name__)
        logger.debug('run() called.')

        try:
            logger.info(f'running sequence: {self.sequence_name}')
            self.source.run()
            self.parser.run()
            self.sink.run()
            logger.info(f'finished sequence: {self.sequence_name}. exiting program.')
        except SourceError as e:
            logger.critical(f'SourceError: {e}')
        except ParserError as e:
            logger.critical(f'ParserError {e}')
        except SinkError as e:
            logger.critical(f'SinkError {e}')
        except Exception as e:
            logger.critical(f'Exception {e}')
