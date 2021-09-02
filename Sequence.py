from abstract.AbstractSource import AbstractSource, SourceError
from abstract.AbstractParser import AbstractParser, ParserError
from abstract.AbstractSink import AbstractSink, SinkError
import logging

'''
singleton register for adding and retrieving Sequence objects
new():                  singleton pattern instantiation
register_sequence():    add a Sequence to the register
has_sequence():         indicates weather a Sequence with the provided_name exists
get_sequence():         returns a Sequence identified by sequence_name or None
get_sequences():        returns a dictionary containing all registered sequences
'''
class SequenceRegister(object):
    instance = None

    def __new__(cls):
        # if there is no instance yet, call super().__new__ to create one
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.registered_sequences = dict()
        return cls.instance

    def register_sequence(self, sequence):
        if not self.has_sequence(sequence.sequence_name):
            self.registered_sequences[sequence.sequence_name] = sequence

    def has_sequence(self, sequence_name):
        return sequence_name in self.registered_sequences

    def get_sequence(self, sequence_name):
        return self.registered_sequences[sequence_name]

    def get_sequences(self):
        return self.registered_sequences;

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
        SequenceRegister().register_sequence(self)

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
            exit(0)
        except SourceError as e:
            logger.critical(f'SourceError: {e}')
            logger.critical('exiting program due to critical error.')
            exit(1)
        except ParserError as e:
            logger.critical(f'ParserError {e}')
            logger.critical('exiting program due to critical error.')
            exit(1)
        except SinkError as e:
            logger.critical(f'SinkError {e}')
            logger.critical('exiting program due to critical error.')
            exit(1)
        except Exception as e:
            logger.critical(f'Exception {e}')
            logger.critical('exiting program due to critical error.')
            exit(1)
