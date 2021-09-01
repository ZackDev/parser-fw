# readme Document for the `Seshat` parser framework

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

the sequence combines the above. additionally it gets a name so it can be identified later when running the parser-fw from the command line. sequences themselves therefor register with the `SequenceRegister` which is checked at start if the wanted sequence is available.

### running the framework

the framework takes two arguments, the name of the sequence and the loglevel which ranges from 1 to 5, DEBUG to CRITICAL

`python3 Seshat.py -s <sequence_name> -l <loglevel>`

in this example a sequence named `river-watermark` is already defined.

so running the sequence looks like this:

`python3 Seshat.py -s river-watermark -l 3`

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
