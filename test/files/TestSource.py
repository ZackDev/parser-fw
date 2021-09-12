from abstract.AbstractSource import AbstractSource

class TestSourceWithoutGetDataImplementation(AbstractSource):
    pass

class TestSourceWithGetDataImplementation(AbstractSource):
    def _get_data(self):
        pass

class TestSource(AbstractSource):
    def _get_data(self):
        self.data = ["1", "2", "3"]
