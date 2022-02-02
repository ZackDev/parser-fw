#!/bin/bash

# exits with code 0 if sha512sum differs

# count passed arguments
num_args=$#

if [[ $num_args -ne 2 ]]; then
  echo "wrong number of arguments"
  exit 0
fi

file_a=$1
file_b=$2

if [[ -f $file_a && -f $file_b ]]; then
  # raw sha512sum output
  # NOTE: sha512sum postpends filename to hash
  h_a=$(sha512sum $file_a | cut -d " " -f 1)
  h_b=$(sha512sum $file_b | cut -d " " -f 1)

  # compare hashes
  if [[ $h_a != $h_b ]]; then
    echo "true"
  else
    echo "false"
  fi
else
  echo "file(s) not found"
fi
exit 0

