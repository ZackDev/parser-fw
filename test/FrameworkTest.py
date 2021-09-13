import unittest
from test.files.TestStep import TestStepWithoutRunImplementation
from test.files.TestStep import TestStepWithRunImplementation
from test.files.TestStep import TestStep
from SequenceProvider import SequenceProvider
from SequenceProvider import SequenceProviderError
from abstract.AbstractStep import StepError
from SequenceRunner import SequenceRunner

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


    def test_config_provider(self):
        SequenceProvider._CONFIG_DIRECTORY = './test/files/cfg/'
        sr = SequenceRunner('test')

        """
        test with valid config
        """
        cfg_provider = SequenceProvider('test')
        steps = cfg_provider.get_sequence()
        for s in steps:
            sr.add_step(s)
        sr.run()
        self.assertEqual(8, sr.data)

        """
        test with missing config
        """
        with self.assertRaises(SequenceProviderError):
            SequenceProvider('cfg-not-there')

        """
        test with invalid config
        """
        with self.assertRaises(SequenceProviderError):
            cfg_provider = SequenceProvider('faulty-test')
