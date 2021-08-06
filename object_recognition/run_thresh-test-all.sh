#!/bin/bash

for count in {1..9}
do
	cmd="bash run_thresh-test.sh 0.${count}"
	echo $cmd
	$cmd
done