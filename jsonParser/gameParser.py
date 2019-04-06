import io #allows people to convert unstructured web data into a structured format 
import os # way of using operating system dependent functionality
import json 
import numpy as np # numerical python
# import tensorflow as tf


def get_bbox(str):
    # turn convert json string into dicutionary
    obj = json.loads(str.decode('utf-8'))
    # obj is a dictionary - dictionaries are indexed by strings - lists are indexed by integers
    bbox = obj['plays']
    # need to convert python array to numpy array because tf needs that format for input
    return np.array([bbox['x'], bbox['y'], bbox['height'], bbox['width']], dtype='f')


def get_multiple_bboxes(str):
    # [get_bbox(x) for x in str] means map each item in the list str to a new list using the function get_bbox
    # enclosing it in another set of [ ]'s means put this list in another list by itself
    # i.e  obj = [1 2]
    # list2 = [obj]
    # list2[0] = obj
    # you would do this if the function you are passing to next expects this format
    return [[get_bbox(x) for x in str]]


# json_string = """{
#     "bounding_box": {
#         "y": 98.5,
#         "x": 94.0,
#         "height": 197,
#         "width": 188
#      },
#     "rotation": {
#         "yaw": -27.97019577026367,
#         "roll": 2.206029415130615,
#         "pitch": 0.0},
#         "confidence": 3.053506851196289,
#         "landmarks": {
#             "1": {
#                 "y": 180.87722778320312,
#                 "x": 124.47326660156205},
#             "0": {
#                 "y": 178.60653686523438,
#                 "x": 183.41931152343795},
#             "2": {
#                 "y": 224.5936889648438,
#                 "x": 141.62365722656205
# }}}"""

KEY_ORDER = [
      "turn",
      "cards_played",
      "current_player",
      "my_health",
      "opponent_health",
      "my_armor",
      "opponent_armor",
      "my_hand",
      "opponent_hand",
      "my_board",
      "opponent_board"
      ]


def turn_from_dict(tdict):
    tlist = []
    # flatten list !!!should probably pad vectors to all be same size since
    # board size is variable!!!
    for key in KEY_ORDER:
        tlist.extend(tdict[key])
    return np.array([tlist])


# navigate folders to get list of game file names
jsonParser_folder = os.getcwd()
game_data_folder = os.path.join(os.path.dirname(jsonParser_folder), "2016data")
print(game_data_folder)
gamefile_list = [os.path.join(game_data_folder, gamefile) for gamefile in os.listdir(game_data_folder)]

#process and save np array, can load later with np.load
with open(gamefile_list[0]) as f:
    gamedata = json.load(f)

    # np.save(os.path.join(game_data_folder, gamefile_list[0]), x)

# raw = tf.placeholder(tf.string, [None])
# [parsed] = tf.py_func(get_multiple_bboxes, [raw], [tf.float32])


# my_data = np.array([json_string, json_string, json_string])

# init_op = tf.initialize_all_variables()
# with tf.Session() as sess:
#     sess.run(init_op)
#     print(sess.run(parsed, feed_dict={raw: my_data}))
#     print(sess.run(tf.shape(parsed), feed_dict={raw: my_data}))
