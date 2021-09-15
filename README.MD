# What is it?

`Seshu` lets you easily define tasks in the form of `seequences` of `steps` and automatically run them.


# What can it do?

In simple terms: *run a sequence of n steps*


# The sequence

A chain of steps is called a sequence. A specific sequence is again defined via `.json` file.

``` json
{
  "type": "sequence",
  "name": "my-sequence",
  "steps": ["fetch-url", "store-data"]
}
```


# The step

A `step` is responsible for transforming input and returning it. A specific step is defined by a class which contains the code to be run and a config file which contains the class information and instantiation parameters.

The following example takes a `url` as input and returns the content of the response.

``` python
from Abstract import AbstractStep, StepError
import requests

class HTTPResponseSource(AbstractStep):
    def run(self, data):
        try:
            rsp = requests.get(self.url)
            if rsp.status_code == 200:
                return rsp.content
            else:
                raise StepError(f'Connection failed with http status code {rsp.status_code}')
        except Exception as e:
            raise StepError('unexpected error.') from e
```

The concrete step, or the instruction on how to instantiate the step, is defined inside a `.json` config file.

``` json
{
  "type": "step",
  "name": "fetch-url",
  "package": "steps",
  "module": "HTTPResponseSource",
  "class": "HTTPResponseSource",
  "parameters":
  {
    "url": "http://example.org"
  }
}
```

The framework automatically looks for the module `HTTPResponseSource` in the package `steps`, loads it, and instantiates the module's class `HTTPResponseSource` with the parameter `url="http://example.org"` defined under `parameters`.


# Running the framework

The framework takes two arguments, the name of the sequence and the optional loglevel, which ranges from 1 to 5, DEBUG to CRITICAL and defaults to 2 (INFO).

For now there are two ways to run it:

**from console:**
``` bash
python3 ConsoleClient.py -s my-sequence
```

**from python:**
``` python
from SequenceProviderAndRunnerFactory import SequenceProviderAndRunnerFactory
from Seshu import Seshu

class PythonClient:
    def __init__(sequence_name):
        factory = SequenceProviderAndRunnerFactory(sequence_name)
        Seshu(factory)

if __name__ == '__main__':
    PythonClient('my-sequence')
```
