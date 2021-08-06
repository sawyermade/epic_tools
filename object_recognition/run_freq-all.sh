#!/bin/bash
det_dir=output_val_thresholded

for count in {1..9}
do
	cmd="bash run_freq.sh $det_dir/output_val_thresh-0.${count} output_val_freq-0.${count}.json"
	$cmd
done