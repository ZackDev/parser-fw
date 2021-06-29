#!/usr/bin/sh

script_base_dir="/home/zack/Git/parser-fw/"
jekyll_base_dir="/home/zack/Git/zackdev.github.io/"
target_dir="/assets/json/"

num_args=$#

if [ $num_args -eq 2 ]; then
  cd $script_base_dir
  python3 InfoGetSetPrototype.py -s $1
  if [ -f $2 ]; then
    cd $jekyll_base_dir
    git pull
    cd $script_base_dir
    ./tools/diff_files.sh $json_file $jekyll_base_dir$target_dir$json_file
    ecode=$?
    if [ $ecode -eq 0 ]; then
      mv $2 $jekyll_base_dir$target_dir
      cd $jekyll_base_dir
      git add ./$target_dir$2
      git commit -m "automated dataset update"
      git push
      echo "copied output file to jekyll directory. set git commit message."
    else
      echo "files are equal. not copying."
    fi
  else
    echo "expected file not found"
    exit 1
  fi
else
  echo "error: script takes two arguments:"
  echo "1) name of the sequence"
  echo "2) name of the output file"
  exit 1
fi

exit 0
