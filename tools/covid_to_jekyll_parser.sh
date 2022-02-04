#!/usr/bin/sh

script_base_dir="/home/zack/Git/parser-fw/"
jekyll_base_dir="/home/zack/Git/zackdev.github.io/"
target_dir="/assets/json/"

num_args=$#

if [ $num_args -eq 3 ]; then
  #1 - name of sequence
  #2 - name of output file
  #3 - log level
  cd $script_base_dir
  python3.10 ConsoleClient.py -s $1 -l $3
  moved_file=false
  if [ -f $2 ]; then
    cd $jekyll_base_dir
    git pull
    cd $script_base_dir
    # case: file at jekyll dir exists, compare hashes
    if [ -f $jekyll_base_dir$target_dir$2 ]; then
      differs=`./tools/diff_files.sh $2 $jekyll_base_dir$target_dir$2`
      if [ "$differs" = "true" ]; then
        mv $2 $jekyll_base_dir$target_dir
        moved_file=true
      fi
    # case: file at jekyll dir DOESN'T exist
    elif [ ! -f $jekyll_base_dir$target_dir$2 ]; then
      mv $2 $jekyll_base_dir$target_dir
      moved_file=true
    fi
    if [ "$moved_file" = true ]; then
      echo "copied output file to jekyll directory."
    else
      echo "file wasn't moved. deleting file."
      cd $script_base_dir
      rm $2
    fi
  else
    echo "expected file not found."
  fi
else
  echo "invalid number of arguments."
fi

exit 0
