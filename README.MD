# parser-fw requires python 3.9.1 at least
# to install a new python version get the corresponding archive file from
# python.org

# before continuing, parser-fw also requires the python modules 'requests' and
# 'openpyxl'

# for the requests module, python requires the 'zlib1g-dev' debian package
# the openpyxl module requires the libssl-dev package

# install both with
apt-get install zlib1g-dev libssl-dev

# now go to the python source directory and run
./configure
make
make test

# and as root do
make install

# to install requests do as root
pip3 install requests -t /usr/local/lib/python3.9

# and for openpyxl do also as root
pip3 install openpyxl -t /usr/local/lib/3.9
