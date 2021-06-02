import sys, os, numpy as np, time, re, gulpio, compress_json
from tqdm import tqdm
import tensorflow as tf
# from object_detection.utils import label_map_util
# from object_detection.utils import visualization_utils as viz_utils
from PIL import Image
import warnings, matplotlib.pyplot as plt
import matplotlib
matplotlib.use('tkagg')
# warnings.filterwarnings('ignore')

# def vis_dets(frame_dets, detections, label_map, thresh=0.30):
# 	viz_utils.visualize_boxes_and_labels_on_image_array(
# 		frame_dets,
# 		detections['detection_boxes'],
# 		detections['detection_classes'],
# 		detections['detection_scores'],
# 		label_map,
# 		use_normalized_coordinates=True,
# 		max_boxes_to_draw=200,
# 		min_score_thresh=thresh,
# 		agnostic_mode=False,
# 	)
# 	plt.figure()
# 	plt.imshow(frame_dets)
# 	plt.show()

def read_gulp(gulp_dir):
	# Read gulp directory
	gd = gulpio.GulpDirectory(gulp_dir)

	# Get list of segments from meta data and 3 value/level stable sort
	reg = r'^P([0-9]+)_([0-9]+)_([0-9]+)$'
	match_list = sorted(
		[re.match(reg, s) for s in gd.chunk_lookup.keys()], 
		key=lambda x: (int(x.group(1)), int(x.group(2)), int(x.group(3)))
	)
	seg_list = [s.group(0) for s in match_list]
	
	# Return segment id list and gulp directory
	return (gd, seg_list)

def load_model(model_path, label_map_path):
	# Load model
	model = tf.saved_model.load(os.path.join(model_path, 'saved_model')).signatures['serving_default']

	# Load label map
	# label_map = label_map_util.create_category_index_from_labelmap(label_map_path, use_display_name=True)
	# print(f'\nlabel_map: {label_map}\n')

	# return model, label_map
	return model, None

def run_inference(model, label_map, gd, seg_list, output_dir, start_seg=-1, stop_seg=-1, thresh=0.40):
	# Create output directory if it doesnt exist
	if not os.path.exists(output_dir): 
		os.makedirs(output_dir)

	# Start/Stop segment for resuming
	if start_seg == -1:
		start_seg = 0
	if stop_seg == -1:
		stop_seg = len(seg_list)

	# Loops through segments and frames
	num_segs = len(seg_list)
	print(f'\nRunning inference on {num_segs} segments...')
	for i in range(start_seg, stop_seg):
		# Gets segment
		seg = seg_list[i]

		# Pulls frames, meta, and creates seg dict
		frames, meta = gd[seg]
		start_frame = meta['start_frame']
		stop_frame = meta['stop_frame']
		frame_dict = {}
		# print(f'meta:\n{meta}')
		print(f'Segment {i} of {num_segs - 1}: {seg} {len(frames)} frames starting at frame {start_frame} ending at {stop_frame}.')

		# Goes through the frames and saves jsons for each segment
		for j in tqdm(range(0, len(frames))):
			# Get frame and convert to tensors
			frame = frames[j]
			frame_tf = tf.convert_to_tensor(frame)
			frame_tf = frame_tf[tf.newaxis, ...]
			
			# Runs inference, dets keys: 'detection_scores', 'detection_boxes', 'num_detections', 'detection_classes' shape 1x300
			dets = model(frame_tf)
			# print(f'\ndets:\n{dets}')
			# sys.exit(0)

			# Get info from detections
			num_dets = int(dets.pop('num_detections'))
			detections = {key: val[0, :num_dets].numpy().tolist() for key, val in dets.items()}
			# print(detections['detection_classes'])
			detections['num_detections'] = num_dets
			detections['detection_classes'] = [int(det) for det in detections['detection_classes']]
			# print(f'\ndetections:\n{detections}\n')
			# sys.exit(0)

			# Add to dict
			frame_dict.update({start_frame + j : detections})

			# Visualize
			# frame_dets = frame.copy()
			# vis_dets(frame_dets, detections, label_map, thresh)

		# Write json
		jpath = os.path.join(output_dir, seg + '.json.bz')
		compress_json.dump(frame_dict, jpath)

		# Write last segment for resuming
		with open('last_segment.txt', 'w') as fp:
			fp.write(f'{i}: {seg}')

def main():
	# Args
	arg_names = ['model_path', 'label_map_path', 'gulp_dir', 'output_dir', 'cuda_card', 'start_seg', 'stop_seg']
	if len(sys.argv[1:]) == len(arg_names):
		args = {arg_names[i] : val for i, val in enumerate(sys.argv[1:])}
	else:
		print(f'\n***ERROR: Needs {len(arg_names)} positional arguments: python3 {sys.argv[0]} {" ".join(arg_names)}')
		sys.exit(0)

	# Create output directory if it doesnt exist
	if not os.path.exists(args['output_dir']): 
		os.makedirs(args['output_dir'])

	# Get gulp dir/data and segment list
	gd, seg_list = read_gulp(args['gulp_dir'])

	# Set GPU number
	os.environ['CUDA_VISIBLE_DEVICES'] = args['cuda_card']

	# Load saved model
	model, label_map = load_model(args['model_path'], args['label_map_path'])

	# Timer Start
	time_start = time.perf_counter()

	# Run inference on segments
	run_inference(model, label_map, gd, seg_list, args['output_dir'], int(args['start_seg']), int(args['stop_seg']))

	# Timer End
	time_stop = time.perf_counter()
	print(f'Inference time to run: {round(time_stop - time_start, 2)}s')

if __name__ == '__main__':
	main()