# readme Document for the parser framework

# requirements
parser-fw is built for python3.9.1 and further uses the additional python modules
'requests' and 'openpyxl'

## how to check if those requirements are met
check your python version with:

`python3 --version`

run the python3 interpreter with:

`python3`

run those with the interpreter to see if the modules get loaded:

`import requests`

`import openpyxl`

if nothing shows up after typing the commands, you're fine.

## how to install python3
there are multiple ways, depending on your OS and preferred style to install the python programming language. sources to install python can be obtained from

[https://python.org](https://python.org)

### compile python3 from source on debian
the modules above require the following packages to compile, install them with:

`apt-get install zlib1g-dev libssl-dev`

switch to the directory of the python3 source files and type:

`./configure`

`make`

`make test`

`make install`

### install additional modules

`pip3 install <module_name> [-t <target_dir>]`
