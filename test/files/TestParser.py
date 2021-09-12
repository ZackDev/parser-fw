from abstract.AbstractParser import AbstractParser

class TestParserWithoutParseImplementation(AbstractParser):
    pass

class TestParserWithParseImplementation(AbstractParser):
    def _parse(self):
        pass

class TestParser(AbstractParser):
    def _parse(self, data):
        self.parsed_data = data[::-1]
