import unittest
from test.files.TestStep import TestStepWithoutRunImplementation
from test.files.TestStep import TestStepWithRunImplementation
from SequenceProviderAndRunnerFactory import SequenceProviderAndRunnerFactory
from SequenceProvider import SequenceProviderError


class FrameworkTest(unittest.TestCase):
    def test_step_implementation(self):
        with self.assertRaises(TypeError):
            TestStepWithoutRunImplementation()

        step_instantiation = False
        try:
            TestStepWithRunImplementation()
            step_instantiation = True
        except Exception:
            pass
        self.assertEqual(step_instantiation, True)

    def test_factory(self):

        factory = SequenceProviderAndRunnerFactory('Unittest')
        sequence_provider = factory.get_provider()
        sequence_runner = factory.get_runner()

        # test with valid config
        steps = sequence_provider.get_sequence('test')
        for s in steps:
            sequence_runner.add_step(s)
        sequence_runner.run()
        self.assertEqual(8, sequence_runner.data)

        # test with missing config
        with self.assertRaises(SequenceProviderError):
            factory = SequenceProviderAndRunnerFactory('Unittest')
            factory.get_provider().get_sequence('unkown_test')

        # test with invalid config
        with self.assertRaises(SequenceProviderError):
            factory = SequenceProviderAndRunnerFactory('Unittest')
            factory.get_provider().get_sequence('faulty_test')

        # test get_sequence_names
        sequence_names = ['test', 'faulty-test']
        self.assertEqual(sequence_names, sequence_provider.get_sequence_names())
