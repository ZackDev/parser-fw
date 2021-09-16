import unittest
from test.files.TestStep import TestStepWithoutRunImplementation
from test.files.TestStep import TestStepWithRunImplementation
from SequenceProviderAndRunnerFactory import TestSequenceProviderAndRunnerFactory
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

        factory = TestSequenceProviderAndRunnerFactory('test')
        sequence_provider = factory.get_provider()
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
            factory = TestSequenceProviderAndRunnerFactory('unknown-sequence')
            factory.get_provider()

        """
        test with invalid config
        """
        with self.assertRaises(SequenceProviderError):
            factory = TestSequenceProviderAndRunnerFactory('faulty-sequence')
            factory.get_provider()
