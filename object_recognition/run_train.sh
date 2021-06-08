#!/bin/bash
python3 epic_obj_rec.py models/EPICKitchens-FasterRCNN-checkpoint models/EPICKitchens_FasterRCNN_label_map.pbtxt ~/epic_data/gulp/rgb_train output_train $1 $2 $3