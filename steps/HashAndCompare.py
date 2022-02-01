from Abstract import AbstractStep, StepError
import hashlib
import os


class HashAndCompare(AbstractStep):
    def run(self, data):
        if self.hashname in hashlib.algorithms_available is True:
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
            raise StepError(f'provided hashalgorithm name {self.hashname} is not available.')

        if hashes is not None and len(hashes) > 1:
            h = hashes.pop()
            for hash in hashes:
                equals = hash == h
                if equals is False:
                    break
            return equals
        else:
            raise StepError(f'zero hashes generated from files.')
