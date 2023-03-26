#!/bin/bash

set -e

input="$1/problems_list"
dbname=$2
gid=$3
while IFS= read -r line
do
	if [[ -n "${line// /}" ]]; then
		problem_folder=$1/$line
		ls -d "$problem_folder"
		python load.py --type problem --dbname $2 --engines mysql postgresql opengauss --path "$problem_folder" --yes --gid $gid
	fi
done < "$input"
