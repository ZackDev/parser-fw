from abstract.AbstractSink import AbstractSink

class TestSinkWithoutStoreImplementation(AbstractSink):
    pass

class TestSinkWithStoreImplementation(AbstractSink):
    def _store(self):
        pass

class TestSink(AbstractSink):
    def _store(self):
        self.data.append(self.target)
