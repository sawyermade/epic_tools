#!/bin/bash

python3 -u convert_network_output.py \
	./output_network/trn_rgb-val.pt \
	./output_val_freq/output_val_freq-0.5.json \
	./label_map_55-od_2_100.json 