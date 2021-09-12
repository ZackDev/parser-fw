import unittest
from test.files.TestSource import TestSourceWithoutGetDataImplementation
from test.files.TestSource import TestSourceWithGetDataImplementation
from test.files.TestSource import TestSource
from test.files.TestParser import TestParserWithoutParseImplementation
from test.files.TestParser import TestParserWithParseImplementation
from test.files.TestParser import TestParser
from test.files.TestSink import TestSinkWithoutStoreImplementation
from test.files.TestSink import TestSinkWithStoreImplementation
from test.files.TestSink import TestSink
from ConfigProvider import ConfigProvider
from ConfigProvider import ConfigProviderError
from abstract.AbstractSource import SourceError
from Sequence import Sequence

class FrameworkTest(unittest.TestCase):

    def test_source_implementation(self):
        with self.assertRaises(TypeError):
            TestSourceWithoutGetDataImplementation(**{"source":"test"})

        source_instantiation = False
        try:
            TestSourceWithGetDataImplementation(**{"source":"test"})
            source_instantiation = True
        except:
            pass
        self.assertEqual(source_instantiation, True)


    def test_parser_implementation(self):
        with self.assertRaises(TypeError):
            TestParserWithoutParseImplementation(**{"source":"test"})

        parser_instantiation = False
        try:
            TestParserWithParseImplementation(**{"source":"test"})
            parser_instantiation = True
        except:
            pass
        self.assertEqual(parser_instantiation, True)


    def test_sink_implementation(self):
        with self.assertRaises(TypeError):
            TestSinkWithoutStoreImplementation(**{"parser":"parser", "target":"target"})

        sink_instantiation = False
        try:
            TestSinkWithStoreImplementation(**{"parser":"parser", "target":"target"})
            sink_instantiation = True
        except:
            pass
        self.assertEqual(sink_instantiation, True)


    def test_config_provider(self):
        ConfigProvider._CONFIG_DIRECTORY = './test/files/cfg/'
        """
        test with valid config
        """
        cfg_provider = ConfigProvider('test')
        sc = cfg_provider.get_source_class()
        pc = cfg_provider.get_parser_class()
        sic = cfg_provider.get_sink_class()

        sp = cfg_provider.get_source_parameters()
        source = sc(**sp)

        pp = cfg_provider.get_parser_parameters()
        pp.update({"source":source})
        parser = pc(**pp)

        sip = cfg_provider.get_sink_parameters()
        sip.update({"parser":parser})
        sink = sic(**sip)

        s = Sequence(source, parser, sink, 'test')
        s.run()

        self.assertEqual(["3", "2", "1", "world"], sink.data)

        """
        test with missing config
        """
        with self.assertRaises(ConfigProviderError):
            ConfigProvider('cfg-not-there')

        """
        test with invalid config
        """
        with self.assertRaises(SourceError):
            cfg_provider = ConfigProvider('faulty-test')
            sc = cfg_provider.get_source_class()
            sp = cfg_provider.get_source_parameters()
            sc(**sp)
