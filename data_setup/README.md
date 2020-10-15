# Dataset Setup

## Copy tar files to data directory, adjust directories to your system or make symlinks
```
# Copy RGB tar files to directoy for snakemake
python3 -u epic_copy_tar_55.py \
	~/epic_kitchens/3h91syskeag572hl6tvuovwv4d/frames_rgb_flow/rgb \
	~/epic_kitchens/data_55/raw/rgb

# Copy Flow tar files to directory for snakemake
python3 -u epic_copy_tar_55.py \
        ~/epic_kitchens/3h91syskeag572hl6tvuovwv4d/frames_rgb_flow/flow \
        ~/epic_kitchens/data_55/raw/flow

# Extract RGB tar files
python3 -u epic_extract_tar_55.py \
	~/epic_kitchens/3h91syskeag572hl6tvuovwv4d/data/raw/rgb \
	~/epic_kitchens/data_55/raw/rgb

# Extract Flow tar files
python3 -u epic_extract_tar_55.py \
        ~/epic_kitchens/3h91syskeag572hl6tvuovwv4d/data/raw/flow \
        ~/epic_kitchens/data_55/raw/flow
```
