from abstract.AbstractStep import AbstractStep

class TestStepWithoutRunImplementation(AbstractStep):
    pass

class TestStepWithRunImplementation(AbstractStep):
    def run(self):
        pass

class TestStep(AbstractStep):
    def run(self, data):
        if hasattr(self, "initialvalue"):
            return self.initialvalue
        else:
            return data * 2
