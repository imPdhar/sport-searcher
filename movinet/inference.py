import cv2
import tensorflow as tf
from collections import deque
import os
import argparse
import time

ap = argparse.ArgumentParser()
ap.add_argument("--tflite", type=str, required=True,
                help="path to tflite model")
ap.add_argument("-i", "--source", type=str, required=True,
                help="path to video or cam-id")
ap.add_argument("-s", "--resolution", type=int, default=172,
                help="Video resolution")
ap.add_argument("-n", "--num_frames", type=int, default=8,
                help="num_frames")
ap.add_argument("-d", "--data", type=str, required=True,
                help="path to data/test or data/train dir")
ap.add_argument("--save", action='store_true',
                help="Save video")

args = vars(ap.parse_args())
video_path = args["source"]

# Load TFLite Model
# Create the interpreter and signature runner
interpreter = tf.lite.Interpreter(model_path=args["tflite"])
runner = interpreter.get_signature_runner()
init_states = {
    name: tf.zeros(x['shape'], dtype=x['dtype'])
    for name, x in runner.get_input_details().items()
}
del init_states['image']


#################### Video Stream ###############################
if video_path.isnumeric():
    video_path = int(video_path)
cap = cv2.VideoCapture(video_path)

original_video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Write Video
if args['save']:
    out_vid = cv2.VideoWriter(f'output.mp4', 
                         cv2.VideoWriter_fourcc(*'mp4v'),
                         fps, (original_video_width, original_video_height))

image_size = (args['resolution'], args['resolution'])

frames_queue = deque(maxlen=args['num_frames'])

label_map = sorted(os.listdir(args['data']))

def get_top_k(probs, k=5, label_map=label_map):
    """Outputs the top k model labels and probabilities on the given video."""
    top_predictions = tf.argsort(probs, axis=-1, direction='DESCENDING')[:k]
    top_labels = tf.gather(label_map, top_predictions, axis=-1)
    top_labels = [label.decode('utf8') for label in top_labels.numpy()]
    top_probs = tf.gather(probs, top_predictions, axis=-1).numpy()
    return tuple(zip(top_labels, top_probs))

p_time = 0

while True:
    success, img = cap.read()
    if not success:
        print('[INFO] Failed Read Video..')
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frames_queue.append(img_rgb)
    if len(frames_queue) == args['num_frames']:

        img_to_tensor = tf.convert_to_tensor(frames_queue, dtype=tf.uint8)
        # print(type(img_to_tensor))
        img_resize = tf.image.resize(img_to_tensor, image_size)
        img_norm = tf.cast(img_resize, tf.float32) / 255.
        clips = tf.split(img_norm[tf.newaxis], img_norm.shape[0], axis=1)

        # To run on a video, pass in one frame at a time
        states = init_states
        for clip in clips:
            # Input shape: [1, 1, 172, 172, 3] ---> 224, 224 for a2 version
            outputs = runner(**states, image=clip)
            logits = outputs.pop('logits')[0]
            states = outputs

        probs = tf.nn.softmax(logits)
        top_k = get_top_k(probs, k=1)
        print(top_k[0])
        # for label, prob in top_k:
        #     print(label, prob)
        cv2.putText(img, f'{top_k[0][0]} {top_k[0][1]:.3}', (50, 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    
    # FPS
    c_time = time.time()
    fps_ = 1/(c_time-p_time)
    p_time = c_time

    print(fps_)

    # Write Video
    if args['save']:
        out_vid.write(img)

    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if args['save']:
    out_vid.release()
cv2.destroyAllWindows()
