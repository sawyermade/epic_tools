#!/bin/bash
python3 epic_obj_rec.py models/EPICKitchens-FasterRCNN-checkpoint models/EPICKitchens_FasterRCNN_label_map.pbtxt ~/epic_data/gulp/rgb_validation output_val $1 $2 $3