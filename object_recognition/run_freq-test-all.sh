#!/bin/bash
det_dir=output_test_thresholded

for count in {1..9}
do
	cmd="bash run_freq-test.sh $det_dir/output_test_thresh-0.${count} output_test_freq/output_test_freq-0.${count}.json"
	echo $cmd
	$cmd
done