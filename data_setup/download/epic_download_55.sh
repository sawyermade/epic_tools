#!/bin/bash
temp_flag=true
while $temp_flag; do
	curl -LOvC - https://data.bris.ac.uk/datasets/tar/3h91syskeag572hl6tvuovwv4d.zip && temp_flag=false
done
