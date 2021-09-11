from abstract.AbstractSource import AbstractSource

class TestSourceWithoutGetDataImplementation(AbstractSource):
    pass

class TestSourceGetData(AbstractSource):
    def _get_data(self):
        pass
