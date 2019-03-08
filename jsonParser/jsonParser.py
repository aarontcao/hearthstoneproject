import io #allows people to convert unstructured web data into a structured format 
import os # way of using operating system dependent functionality
import json 
import numpy as np # numerical python
import tensorflow as tf

def get_plays1(str):
    obj = json.loads(str.decode('utf-8'))
    plays1 = obj['plays'][1]
    return np.array([plays1['turn'], plays1['my_health'], plays1['opponent_health']], dtype='f')

def get_multiple_plays1(str):
    return [[get_plays1(x) for x in str]]

raw = tf.placeholder(tf.string, [None])
[parsed] = tf.py_func(get_multiple_plays1, [raw], [tf.float32])

json_string = """{
  "plays": [
    {
      "turn": 1,
      "cards_played": [],
      "current_player": "opponent",
      "my_health": 0,
      "opponent_health": 0,
      "my_armor": 0,
      "opponent_armor": 0,
      "my_hand": 1,
      "opponent_hand": 0,
      "my_board": [],
      "opponent_board": []
    },
    {
      "turn": 2,
      "cards_played": [
        "The Coin",
        "Darnassus Aspirant"
      ],
      "current_player": "me",
      "my_health": 30,
      "opponent_health": 30,
      "my_armor": 0,
      "opponent_armor": 0,
      "my_hand": 4,
      "opponent_hand": 4,
      "my_board": [
        {
          "card_name": "Darnassus Aspirant",
          "card_health": 3,
          "card_attack": 2
        }
      ],
      "opponent_board": []
      }
    ]
}"""

my_data = np.array([json_string, json_string, json_string])

init_op = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init_op)
    print(sess.run(parsed, feed_dict={raw: my_data}))
    print(sess.run(tf.shape(parsed), feed_dict={raw: my_data}))