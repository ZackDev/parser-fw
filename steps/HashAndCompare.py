from Abstract import AbstractStep, StepError
import hashlib
import os


class HashAndCompare(AbstractStep):
    def run(self, data):
        if len(self.filenames) < 2:
            raise StepError(f'{__name__} requires num files > 1')
        if hashlib.algorithms_available.__contains__(self.hashname) is True:
            hashes = []
            for fname in self.filenames:
                content = None
                if os.path.isfile(fname):
                    with open(fname, 'rb') as file:
                        content = file.read()
                    if content is not None:
                        hashes.append(hashlib.new(self.hashname, content).hexdigest())
                    else:
                        raise StepError(f'could not binary read file: {fname}')
                else:
                    raise FileNotFoundError(fname)
        else:
            raise StepError(f'provided hashalgorithm name {self.hashname} is not available.')

        if hashes is not None and len(hashes) == len(self.filenames):
            h = hashes.pop()
            for hash in hashes:
                equals = hash == h
                if equals is False:
                    break
            self.data = (equals, self.filenames)
        else:
            raise StepError(f'not enough hashes generated from files.')
