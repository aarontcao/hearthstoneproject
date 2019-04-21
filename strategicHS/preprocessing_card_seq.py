
import re
import os
import sys
import json
import random
from shutil import copyfile
import time
import numpy as np

#SETTING SEED CONSTANT TO REPRODUCE RESULTS AND TESTING
random.seed(123)

# returns list of numpy arrays
def load_sequences(train_test_split, num_to_load=None):
    # get current folder
    current_folder = os.getcwd()
#   # make sure we dont make a bunch of files in the wrong place
    assert current_folder.endswith("strategicHS"), "In Wrong folder (should be in strategicHS with 2016data in parent directory"

    # make folder for processed data if there isnt one (doesnt delete old one so might have to delete it to update)
    # currently scrapped because I put all games in one npy file
    partiesHS = os.path.join(current_folder, "partiesHS")
        # dataset_folder = os.path.join(partiesHS, "/Datasets_playsequences")
        # if not os.path.exists(dataset_folder):
        #      os.mkdir(dataset_folder)

    # get list of paths to the games
    games_folder = os.path.join(os.path.dirname(current_folder), "2016data")
    gamefile_list = [os.path.join(games_folder, gamefile) for gamefile in os.listdir(games_folder) if gamefile != "README.txt"]

    # get monsterdict
    monsterDict_path = os.path.join(partiesHS, "cards_extract\\monsters.json")
    monsterDict = json.load(open(monsterDict_path))
    # this should be a list of numpy vectors where vector i is the sequence of plays in game i
    # where each element of the vector is an integer that corresponds to a card
    # postive elements are cards we played, negative are ones our opponent played
    train_game_array = []
    train_result_array = np.array([])

    test_game_array = []
    test_result_array = np.array([])

    train = 0
    test = 0
    # dummy
    result = 0
    num = 0
    maxlen = 0
    if num_to_load is not None:
        num = num_to_load
    else:
        num = len(gamefile_list)


    for gamefile in gamefile_list[:num]:
        game = json.load(open(gamefile))
        game_vec = np.array([])
        if game["result"] == "defeat":
            result = 0
        else:
            result = 1
        # toss out first turn (its trash)
        for turn in game["plays"][1:]:
            # dummy 0 to avoid warnings, but we'll make this -1 if opponent turn and 1 if ours
            player = 0
            if turn["current_player"] == "opponent":
                player = -1
            else:
                assert turn["current_player"] == "me", "turn current_player field is corrupted for game"+str(gamefile)
                player = 1
            for card in turn["cards_played"]:
                card_num = monsterDict[card]["number"]
                game_vec = np.append(game_vec, card_num*player)
        # set maxlen of game vector
        maxlen = max(maxlen, game_vec.shape[0])
        if random.random()<train_test_split:
            train += 1
            train_game_array.append(game_vec)
            train_result_array = np.append(train_result_array, result)
        else:
            test += 1
            test_game_array.append(game_vec)
            test_result_array = np.append(test_result_array, result)
    print(train_game_array)
    print(train_result_array)
    print(test_game_array)
    print(test_result_array)
    print(train)
    print(test)
    print(maxlen)

    return (train_game_array, train_result_array), (test_game_array, test_result_array, maxlen)
    # scrapped
    # np.save("game_sequences",game_array)

    # to load use x = np.load("game_sequences")

# to run independently for testing arg is num to load
if __name__ == "__main__":
    load_sequences(0.8, int(sys.argv[1]) if len(sys.argv) > 1 else None)