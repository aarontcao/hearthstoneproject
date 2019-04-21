import re
import os
import json
import random
from shutil import copyfile
import time
import numpy as np

from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.preprocessing import sequence

# NOTES: instead of doing negative for opponents move I shifted indices by
# number of cards (2818) instead because the Embedding layer needed positive values
random.seed(123)

# returns (train_sequences, train_results, test_sequences, test_results)
# sequences: list of numpy arrays
# results: numpy array of corresponding win/loss
def load_sequences_both_players(train_test_split, num_to_load=None):
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
                player = 0
            else:
                assert turn["current_player"] == "me", "turn current_player field is corrupted for game"+str(gamefile)
                player = 1
            for card in turn["cards_played"]:
                card_num = monsterDict[card]["number"]
                game_vec = np.append(game_vec, card_num+2818*player)
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
    return (train_game_array, train_result_array, test_game_array, test_result_array, maxlen)

def load_sequences_just_us(train_test_split, num_to_load=None):
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
                continue
            else:
                assert turn["current_player"] == "me", "turn current_player field is corrupted for game"+str(gamefile)
                player = 1
            for card in turn["cards_played"]:
                card_num = monsterDict[card]["number"]
                game_vec = np.append(game_vec, card_num)
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
    return (train_game_array, train_result_array, test_game_array, test_result_array, maxlen)

def main():
    # set parameters -- need to move some of the parameters i chsoe to here
    train_ratio = 0.8
    num_train = None
    num_values_both = 5639 # number of values elements can take
    num_values_us = 2820
    num_values = num_values_both
    # load data (asssumes you are in strategicHS)
    xtrain_raw, ytrain, xtest_raw, ytest, maxlen = load_sequences_both_players(train_ratio, num_train)

    # keras sequence processing for uniform size. pad with 2819 since smaller ints
    # correspond to events
    print("padding sequences")
    xtrain = sequence.pad_sequences(xtrain_raw, maxlen=maxlen, padding='post', value=2819)
    xtest = sequence.pad_sequences(xtest_raw, maxlen=maxlen, padding='post', value=2819)

    print(type(xtrain_raw[0]))
    print(xtrain_raw[0])
    print(type(xtrain[0]))
    print(xtrain[0])
    print(xtrain[0].shape)
    print(np.array(xtrain[0]).shape)
    # model -- currently just a guess -- needs to be fiddled around with and analyzed
    # also need to make sure I wasn't crazy when I put this together because its a few lines to
    # write but they are very important
    # references used: https://towardsdatascience.com/deep-learning-4-embedding-layers-f9a02d55ac12
    # current layout: embedding for relationships among elements
    # lstm for temporal relationships
    # currently broken - i think its an embedding issue but I also think we should
    # stack when its worked out
    print("initializing model")
    model = Sequential()
    model.add(Embedding(num_values, 32, input_length=maxlen))
    model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(1, activation='relu'))
    print("compiling model")
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    model.fit(xtrain, ytrain, epochs=5, batch_size=64)
    # Final evaluation of the model
    scores = model.evaluate(xtest, ytest, verbose=1)
    print("Accuracy: %.2f%%" % (scores[1]*100))
    print(xtrain[0])
    print(xtrain[0].shape)
    print(model.predict(xtrain))
    print("testttt")
    # overfitting really badly atm
    print(model.predict(xtest))

# to run independently for testing
if __name__ == "__main__":
    main()