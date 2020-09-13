#!/bin/bash
temp_flag=true
while $temp_flag; do
	curl -LOvC - https://data.bris.ac.uk/datasets/tar/2g1n6qdydwa9u22shpxqzp0t8m.zip && temp_flag=false
done
