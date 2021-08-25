from abstract.AbstractSource import AbstractSource, SourceError
from abstract.AbstractParser import AbstractParser, ParserError
from abstract.AbstractSink import AbstractSink, SinkError

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
        self.sequence_name = sequence_name
        self.source = source
        self.parser = parser
        self.sink = sink
        SequenceRegister().register_sequence(self)

    def run(self):
        try:
            self.source.run()
            self.parser.run()
            self.sink.run()
        except SourceError as e:
            print(f'SourceError: {e}')
            exit(1)
        except ParserError as e:
            print(f'ParserError {e}')
            exit(1)
        except SinkError as e:
            print(f'SinkError {e}')
            exit(1)
        except Exception as e:
            print(f'Exception {e}')
            exit(1)
        exit(0)
