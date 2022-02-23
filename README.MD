# What is it?

`Seshu` lets you easily define tasks in the form of `seequences` of `steps` and automatically run them.


# What can it do?

In simple terms: *run a sequence of n steps*


# The sequence

A chain of steps is called a sequence. A specific sequence is defined via `.json` file.

``` json
{
  "type": "sequence",
  "name": "my-sequence",
  "steps": [
    {
      "type": "step",
      "name": "get-data",
      "package": "steps",
      "module": "HTTPResponseSource",
      "class": "HTTPResponseSource",
      "parameters": {
        "url": "https://example.org/example.data"
      }
    },
    {
      "type": "step",
      "name": "JSONFileSink",
      "package": "steps",
      "module": "JSONFileSink",
      "class": "JSONFileSink",
      "parameters": {
        "target": "data.json"
      }
    }
  ]
}
```


# The step

A `step` is responsible for transforming input and returning it. A specific step is defined by a class which contains the code to be run and a config file which contains the class information and instantiation parameters.

The framework automatically looks for the module `HTTPResponseSource` in the package `steps`, loads it, and instantiates the module's class `HTTPResponseSource` with the parameter `url="http://example.org"` defined under `parameters`. The parameter is available at object-level as `self.<parameter_name>`. The automatic parametrization allows the change of instantiation parameters without modifying the `__init__()` function.


# Running the framework

The framework takes two arguments, the name of the sequence and the optional loglevel, which ranges from 1 to 5, DEBUG to CRITICAL and defaults to 2 (INFO).

For now, there are two ways to run it:

**from console:**
``` bash
python3 ConsoleClient.py -s my-sequence [-l loglevel]
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

Noteable here is that Seshu is provisioned with a factory which produces a `SequenceProvider` and a `SequenceRunner`.

## SequenceProvider
Contains the logic for creating sequences. The example above uses data structured as `.json` to define a specific sequence directly from the local harddrive. But the sequence definitions could also come in another `.json` structure, or from a webserver or a SQL database for example.

Derive a new factory from `Abstract.AbstractSequenceProviderAndRunnerFactory` to implement custom structures and sources.

## SequenceRunner
Implements the logic to run a set of steps. In the example, steps are run sequentially, where the output of `step n-1` becomes the input of `step n`. Thinkable here is a conditional runner. Let's say there are 3 steps, `A`, `B0` and `B1`, where the result of `A` determines wheather `B0` or `B1` gets executed.
