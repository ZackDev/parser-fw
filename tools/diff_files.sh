#!/bin/bash

# exits with code 0 if sha512sum differs

# count passed arguments
num_args=$#

if [[ $num_args -ne 2 ]]; then
  exit 1
fi

file_a=$1
file_b=$2

if [[ -f $file_a && -f $file_b ]]; then
  # raw sha512sum output
  # NOTE: sha512sum postpends filename to hash
  rh_a=$(sha512sum $file_a)
  rh_b=$(sha512sum $file_b)

  # filename length
  len_fa=${#file_a}
  len_fb=${#file_b}

  # slice filename from hash
  h_a=${rh_a:0:-$len_fa-2}
  h_b=${rh_b:0:-$len_fb-2}

  # compare hashes
  if [[ $h_a != $h_b ]]; then
    exit 0
  else
    exit 1
  fi
else
  exit 1
fi
