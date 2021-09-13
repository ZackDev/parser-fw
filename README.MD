# readme Document for the `Seshu` parser framework

## what can it do
in simple terms: fetch data, parse and store it

the parser-fw understands this as a `sequence`. The sequence itself consists of a `source` a `parser` and a `sink`, which get called in that order.

### the souce

a source is responsible for providing raw data. it can be a file, a database, a resource on the web. the behavior and structure is defined in the `AbstractSource` class.

the framework relies on this structure, so make sure your custom sources, parsers and sinks inherits from there.

### the parser

a parser is responsible for going through the raw data provided by the source. inherit from `AbstractParser` class to create your own parser.

### the sink

the sink is the last step in the sequence process. it takes the parsed data from the parser and is intended to "store" said data. a typical sink could be a `csv` or `json` file, a `database` connection or an email getting sent. `AbstractSource` is the class you want to derive from.

### the sequence

the sequence combines the above. additionally it gets a name so it can be identified later when running the parser-fw from the command line. creating a sequence is easy and requires the following steps:
* create your custom `source` `parser` and `sink` classes and make sure they inherit from their specific abstract classes
* create a corresponding `.json` file in the `./config` folder

### the sequence config file

config files define a sequence. the following is a schema of it.

```json
{
  "type": "sequence",
  "name": <name>,
  "source": {
    "package": <package_name>,
    "module": <module_name>,
    "class": <class_name>,
    "parameters": [
      {
        "name": <parameter_name>,
        "type": <type>,
        "value": <value>
      },
      {
        ...
      }
    ]
  },
  "parser": {
    ...
  },
  "sink": {
    ...
  }
}
```

here you can define:
* the sequence's `name` which `Sehsu` can be started with from command line
* the source, parser and sink definitions which include:
  * `package`: the name of the package
  * `module`: the name of the module
  * `class`: the name of the class
  * `parameters`: and array of parameters to instantiate the class with

for example, if your sequence reads from a file, the source would expect a filename to read from. lets call it `file_to_parse.txt`.

your source class is named `LocalFileSource` and is located in the folder `custom_sources` where you have a module named `LocalSources`.

the corresponding entry in the config file looks like this:

```json
{
  "source": {
    "package": "custom_sources",
    "module": "LocalSources",
    "class": "LocalFileSource",
    "parameters": [
      {
        "name": "filename",
        "type": "str",
        "value": "file_to_parse.txt"
      }
    ]
  }
}
```


### running the framework

the framework takes two arguments, the name of the sequence and the loglevel which ranges from 1 to 5, DEBUG to CRITICAL

`python3 Seshu.py -s <sequence_name> -l <loglevel>`

in this example a sequence named `river-watermark` is already defined.

so running the sequence looks like this:

`python3 Seshu.py -s river-watermark -l 3`

## requirements
parser-fw is built for python3.9.1 and further uses the additional python modules
'requests' and 'openpyxl'

### how to check if those requirements are met
check your python version with:

`python3 --version`

run the python3 interpreter with:

`python3`

run those with the interpreter to see if the modules get loaded:

`import requests`

`import openpyxl`

if nothing shows up after typing the commands, you're fine.

### how to install python3
there are multiple ways, depending on your OS and preferred style to install the python programming language. sources to install python can be obtained from

[https://python.org](https://python.org)

#### compile python3 from source on debian
the modules above require the following packages to compile, install them with:

`apt-get install zlib1g-dev libssl-dev`

switch to the directory of the python3 source files and type:

`./configure`

`make`

`make test`

`make install`

#### install additional modules

`pip3 install <module_name> [-t <target_dir>]`


## thoughts on features
reading the config from json files, dynamic import of classes and the class-object creation with parameters from said files works fine. another feature or level of abstraction is to read configs from any source, like xml files, databases. a way to implements this would require a class, lets call it `AbstractConfigProvider` which concrete implementation would act as an interface between the sequence creation and the data-source.

the question is, besides the learning-experience, is it worth the effort? for me probably not as I'm fine with it as it is.

another question is how it fits into the current architecture. does the `ConcreteConfigProvider` get passed to the `Sequence` object which calls the provider's methods? Where is the place the framework user can switch the `ConcreteConfigProvider`? best place IMHO would be in `Seshu.py`.

## sequence framework, the evolution of Seshu
instead of having a predefined workflow that goes from concrete `source`, `parser` to `sink`, the sequence framework can have a unlimited set of instructions that attach to the data.

the above mentioned `source`, `parser` and `sink` sequence is only a specific use-case which operates on a given data. imagine the following data-flow at the example of, let's say the `daily_cases` sequence of `Seshu`.

### `daily_cases` translated to the view of the `sequence framework`
* `HTTPResponceSource`: transforms data as a web resource `url`
* `DailyCasesGithubParser`: interprets data as a `csv` and parses stuff
* `JSONFILESink`: interprets data as a dictionary


# rewrite `Seshu`
* merge `AbstractSource`, `AbstractParser` and `AbstractSink` into one `AbstractStep` class
* rewrite `ConfigProvider` so it can retrieve the sequence's parts step-by-step, rename it to `SequenceProvider`
  * have `sequence` and `step` as config types where sequence has an array of steps, and the step config contains the specific step configuration
* rename `Sequence` to `SequenceRunner`, it is now responsible for sequentially run `Sequences` and pass the results along that chain


this seems to be the logical evolution of `Seshu`, and would allow to extend the `daily_cases` use-case above with those additional sequences:
* `GithubPublish`
* `Backup`
