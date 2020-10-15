#!/bin/bash

# Extracts rgb tars
python3 -u epic_move_tar_55.py \
	~/epic_kitchens/3h91syskeag572hl6tvuovwv4d/frames_rgb_flow/rgb \
	~/epic_kitchens/data_55/raw/rgb

# Extracts flow tars
python3 -u epic_move_tar_55.py \
	~/epic_kitchens/3h91syskeag572hl6tvuovwv4d/frames_rgb_flow/flow \
	~/epic_kitchens/data_55/raw/flow