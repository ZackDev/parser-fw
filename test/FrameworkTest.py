import unittest
from test.files.TestStep import TestStepWithoutRunImplementation
from test.files.TestStep import TestStepWithRunImplementation
from test.files.TestStep import TestStep
from Abstract import StepError
from SequenceProviderAndRunnerFactory import SequenceProviderAndRunnerFactory
from SequenceProvider import SequenceProvider, SequenceProviderError


class FrameworkTest(unittest.TestCase):
    def test_step_implementation(self):
        with self.assertRaises(TypeError):
            TestStepWithoutRunImplementation()

        step_instantiation = False
        try:
            TestStepWithRunImplementation()
            step_instantiation = True
        except:
            pass
        self.assertEqual(step_instantiation, True)


    def test_factory(self):
        SequenceProvider._CONFIG_DIRECTORY = './test/files/cfg/'

        factory = SequenceProviderAndRunnerFactory('test')
        sequence_provider =  factory.get_provider()
        sequence_runner = factory.get_runner()

        """
        test with valid config
        """
        steps = sequence_provider.get_sequence()
        for s in steps:
            sequence_runner.add_step(s)
        sequence_runner.run()
        self.assertEqual(8, sequence_runner.data)

        """
        test with missing config
        """
        with self.assertRaises(SequenceProviderError):
            factory = SequenceProviderAndRunnerFactory('cfg-not-there')
            factory.get_provider()

        """
        test with invalid config
        """
        with self.assertRaises(SequenceProviderError):
            factory = SequenceProviderAndRunnerFactory('faulty-test')
            factory.get_provider()
