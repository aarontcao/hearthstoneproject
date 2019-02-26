import io
import json
import numpy as np
import tensorflow as tf

def get_bbox(str):
    obj = json.loads(str.decode('utf-8'))
    bbox = obj['bounding_box']
    return np.array([bbox['x'], bbox['y'], bbox['height'], bbox['width']], dtype='f')

def get_multiple_bboxes(str):
    return [[get_bbox(x) for x in str]]

raw = tf.placeholder(tf.string, [None])
[parsed] = tf.py_func(get_multiple_bboxes, [raw], [tf.float32])

json_string = """{
    "bounding_box": {
        "y": 98.5,
        "x": 94.0,
        "height": 197,
        "width": 188
     },
    "rotation": {
        "yaw": -27.97019577026367,
        "roll": 2.206029415130615,
        "pitch": 0.0},
        "confidence": 3.053506851196289,
        "landmarks": {
            "1": {
                "y": 180.87722778320312,
                "x": 124.47326660156205},
            "0": {
                "y": 178.60653686523438,
                "x": 183.41931152343795},
            "2": {
                "y": 224.5936889648438,
                "x": 141.62365722656205
}}}"""

my_data = np.array([json_string, json_string, json_string])

init_op = tf.initialize_all_variables()
with tf.Session() as sess:
    sess.run(init_op)
    print(sess.run(parsed, feed_dict={raw: my_data}))
    print(sess.run(tf.shape(parsed), feed_dict={raw: my_data}))