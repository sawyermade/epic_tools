#!/bin/bash

# Copies rgb tars
python3 -u epic_move_tar_55.py \
	~/epic_kitchens/3h91syskeag572hl6tvuovwv4d/frames_rgb_flow/rgb \
	~/epic-data/data_100/raw/rgb

# Copies flow tars
python3 -u epic_move_tar_55.py \
	~/epic_kitchens/3h91syskeag572hl6tvuovwv4d/frames_rgb_flow/flow \
	~/epic-data/data_100/raw/flow
