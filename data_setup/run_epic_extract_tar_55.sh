#!/bin/bash

# Extracts rgb tars
python3 -u epic_extract_tar_55.py \
	~/epic_kitchens/3h91syskeag572hl6tvuovwv4d/frames_rgb_flow/rgb \
	~/epic_kitchens/epic_55/rgb

# Extracts flow tars
python3 -u epic_extract_tar_55.py \
	~/epic_kitchens/3h91syskeag572hl6tvuovwv4d/frames_rgb_flow/flow \
	~/epic_kitchens/epic_55/flow