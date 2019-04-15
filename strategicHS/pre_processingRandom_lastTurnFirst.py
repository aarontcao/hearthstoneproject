#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import os
import json
from random import random
from shutil import copyfile
import time


# In[2]:


def rename_all_json_in(folderPath):
    newFile=False
    fileList = os.listdir(folderPath)
    f=open(folderPath+'/nextGameNumber.txt','a')
    f.close()
    f=open(folderPath+'/nextGameNumber.txt','r')
    startIndex = f.readlines()
    print(str(len(startIndex)))
    f.close()
    if(len(startIndex)==0):
        startIndex=1
    else:
        startIndex = int(startIndex[0])
    firstIndex=startIndex
    for e in fileList:
         if e.endswith('.json'):
            if re.search('^[0-9]+.json$',e) is None :
                if nbTurnSupp1(folderPath+'/'+e):
                    os.rename(folderPath+'/'+e,folderPath+'/'+str(startIndex)+'.json')
                    startIndex=startIndex+1
                    newFile=True
                else:
                     os.remove(folderPath+'/'+e)
    f=open(folderPath+'/nextGameNumber.txt','w')
    f.write(str(startIndex))
    f.close()
    return newFile

def nbTurnSupp1(filePath): #True if game last more than 1 turn
    file=open(filePath)
    f=json.loads(file.read())
    if f['plays'][-1]['turn'] >1:
        return True
    else:
        return False


def extract_features(jsonfile,j,dicoPath,oneTurnTwoPlayer):#jsonfile, turn, dictionnary of all monsters, if true : it will aggregate turn of both player
    nbrCardMe=0
    nbrCardOpp=0
    monsterDict =json.loads(open(dicoPath, 'r').read())
    if len(jsonfile[j]['my_board'])>0:
        nbrCardMe=len(jsonfile[j]['my_board'])
    if len(jsonfile[j]['opponent_board'])>0:
         nbrCardOpp=len(jsonfile[j]['opponent_board'])
    features=[]
    #for i in range(0,2*len(monsterDict)):
    max_card_idx = len( [f for f in os.listdir('partiesHS/cards_extract') if re.match(r'^[0-9]', f)])
    for i in range(0,2*max_card_idx):
        features.append('0')
    myAttack=0
    oppAttack=0
    myTaunt=0
    oppTaunt=0
    myTauntHp=0
    oppTauntHp=0

    my_board = jsonfile[j]['my_board']
    opp_board = jsonfile[j]['opponent_board']

    my_hand = jsonfile[j]['my_hand']
    opp_hand = jsonfile[j]['opponent_hand']

    my_armor = jsonfile[j]['my_armor']
    opp_armor = jsonfile[j]['opponent_armor']


    card_played = jsonfile[j]['cards_played']
    current_player = jsonfile[j]['current_player']

    if current_player == 'me' :
        player = 0
    else:
        player = 1

    if oneTurnTwoPlayer :
        card_played_other_player = jsonfile[j-1]['cards_played']
        for i in card_played_other_player :
            if i in monsterDict :
                features[monsterDict[i]['number']*2+((player+1)%2)]=1

    for i in card_played :
        if i in monsterDict :
            features[monsterDict[i]['number']*2+player]=1

    for k in range(0,nbrCardMe):
        monster=jsonfile[j]['my_board'][k]
        monster_name=monster['card_name']
        myAttack=myAttack+monster['card_attack']

        if monster_name in monsterDict :
            features[monsterDict[monster_name]['number']*2]='1'
            for power in monsterDict[monster_name]['powers']:
                if(power == 'Taunt'):
                    myTaunt = myTaunt + 1
                    myTauntHp = myTauntHp + monster['card_health']

    for k in range(0,nbrCardOpp):
        monster=jsonfile[j]['opponent_board'][k]
        monster_name=monster['card_name']
        oppAttack=oppAttack+monster['card_attack']
        if monster_name in monsterDict :

            features[monsterDict[monster_name]['number']*2+1]='1'
            for power in monsterDict[monster_name]['powers']:
                if(power == 'Taunt'):
                    oppTaunt = oppTaunt + 1
                    oppTauntHp = oppTauntHp + monster['card_health']

    features.insert(0,str(opp_armor))
    features.insert(0,str(my_armor))
    features.insert(0,str(opp_hand))
    features.insert(0,str(my_hand))
    features.insert(0,str(oppTauntHp))
    features.insert(0,str(myTauntHp))
    features.insert(0,str(oppTaunt))
    features.insert(0,str(myTaunt))
    features.insert(0,str(oppAttack))
    features.insert(0,str(myAttack))
    features.insert(0, str(jsonfile[j]['opponent_health']))
    features.insert(0, str(jsonfile[j]['my_health']))

    return features

def delete_turns_less_than(n,folderPath):#call this in trainset folder to remove games lasting less than n turns
    listTurn = os.listdir(folderPath)
    for element in listTurn:
        file=list(open(folderPath+'/'+element))
        if len(file)<n :
            os.remove(folderPath+'/'+element)

def reset_dataset_train(folderPath):
    listTurn = os.listdir(folderPath)
    for f in listTurn :
        dataset_train = open(folderPath+'/'+f,'w')
        dataset_train.close()

def create_datasets(folderPath,dicoPath,trainRatio,newFile):
    #game data path , monster dictionnary path , split ratio in order to build train/test set , if set to True : means you have new game file to be added in train/test datasets
    if not os.path.exists(folderPath+'/Datasets_test'):
         os.mkdir(folderPath+'/Datasets_test')
    if not os.path.exists(folderPath+'/Datasets_train'):
         os.mkdir(folderPath+'/Datasets_train')
    if not os.path.exists(folderPath+'/Datasets_test_1turn2plays'):
         os.mkdir(folderPath+'/Datasets_test_1turn2plays')
    if not os.path.exists(folderPath+'/Datasets_train_1turn2plays'):
         os.mkdir(folderPath+'/Datasets_train_1turn2plays')


    fileList = os.listdir(folderPath)
    victory=0
    defeat =1
    train =0
    test =0
    if newFile:
        iNextTestFile = len(os.listdir(folderPath+'/Datasets_test'))+1

        for f in fileList :
            if f.endswith('.json'):
                nb =random()
                file=open(folderPath+'/'+f)
                f=json.loads(file.read())
                result=f['result']
                if result == 'defeat' :
                    result=0
                    defeat = defeat+1
                else :
                    victory=victory+1
                    result=1
                f=f['plays']
                lastTurn = f[-1]['turn']
                f[::-1]
                if(nb<trainRatio):
                    #Training datasets, split by turn

                    #1st dataSet
                    for j in range(1,lastTurn):#Ignore first turn : not a real turn
                        dataset_train = open(folderPath+'/Datasets_train/turn'+str(j)+'.txt','a')
                        features = extract_features(f,j,dicoPath,True)
                        dataset_train.write(str(result))
                        for i in features :
                            dataset_train.write(','+str(i))
                            dataset_train.write('\n')
                        dataset_train.close()

                    #2nd dataSet
                    j=lastTurn-1
                    k=1

                    while j > 1 :  #Aggregate turn of the 2 players,
                        dataset_train2 = open(folderPath+'/Datasets_train_1turn2plays/turn'+str(k)+'.txt','a')
                        features = extract_features(f,j,dicoPath,True)
                        dataset_train2.write(str(result))
                        for i in features :
                            dataset_train2.write(','+str(i))
                        dataset_train2.write('\n')
                        dataset_train2.close()
                        k=k+1
                        j=j-2
                    file.close()

                #Testing datasets, split by game
                else:
                    test = test +1
                    dataset_test = open(folderPath+'/Datasets_test/game'+str(iNextTestFile)+'.txt','w')
                    for j in range(1,lastTurn):

                        features = extract_features(f,j,dicoPath,True)
                        dataset_test.write(str(result))
                        for i in features :
                            dataset_test.write(','+str(i))
                            dataset_test.write('\n')
                    dataset_test.close()

                    #2nd dataSets
                    j=lastTurn-1
                    dataset_test2 = open(folderPath+'/Datasets_test_1turn2plays/game'+str(iNextTestFile)+'.txt','w')
                    dataset_test2.close()
                    while j > 1 :
                        dataset_test2 = open(folderPath+'/Datasets_test_1turn2plays/game'+str(iNextTestFile)+'.txt','a')
                        features = extract_features(f,j,dicoPath,True)
                        dataset_test2.write(str(result))
                        for i in features :
                            dataset_test2.write(','+str(i))
                        dataset_test2.write('\n')
                        dataset_test2.close()
                        j=j-2
                    file.close()
                    iNextTestFile= iNextTestFile+1
        print('nbGames for train :' + str(train) + ' ratio :'+str(train/(test+train)))
        print('nbGames for test :'+str(test)+ ' ratio :'+str(test/(test+train)))
        if defeat > 1:
            defeat = defeat -1
    else :
        victory =0
        defeat =1
    return victory/(victory+defeat);


def genDataSetTurnMin(folderPath, dicoPath,turnMin,newFile):
    if newFile :
        newFile=rename_all_json_in(folderPath+'/Datasets_GameOf'+str(turnMin)+'Turn')
        create_datasets(folderPath+'/Datasets_GameOf'+str(turnMin)+'Turn',dicoPath,0.8,newFile)
        delete_turns_less_than(2,folderPath+'/Datasets_GameOf'+str(turnMin)+'Turn/Datasets_train_1turn2plays')

def select_all_game_of_N_turn_or_more(folderPath):
    f=open(folderPath+'/lastGameSelected.txt','a')
    f.close()
    gameStart=list(open(folderPath+'/lastGameSelected.txt','r'))
    if gameStart==[]:
        gameStart=[0]

    gameStop=list(open(folderPath+'/nextGameNumber.txt','r'))
    i =0
    j=int(gameStop[0])-1
    print('gamestart [0] ' + str(gameStart[0]) + ' gamestop ' + str(gameStop[0]) )
    for j in range (int(gameStart[0])+1,int(gameStop[0])):
        file=open(folderPath+'/'+str(j)+'.json')
        nbTurn=int((len(json.loads(file.read())['plays'])-2)/2)
        file.close()
        for n in range(1,nbTurn+1):
            if not os.path.exists(folderPath+'/Datasets_GameOf'+str(n)+'Turn'):
                os.mkdir(folderPath+'/Datasets_GameOf'+str(n)+'Turn')
                i=0
            else:
                i = len(os.listdir(folderPath+'/Datasets_GameOf'+str(n)+'Turn'))# a enregistrer dans un fichier
            game = open(folderPath+'/Datasets_GameOf'+str(n)+'Turn/game'+str(i+1)+'.json','w')
            copyfile(folderPath+'/'+str(j)+'.json', folderPath+'/Datasets_GameOf'+str(n)+'Turn/game'+str(i+1)+'.json')
            game.close()
            i = i+1
    file=open(folderPath+'/lastGameSelected.txt','w')
    file.write(str(j))
    file.close()

t1 = time.time()

game_folder = 'partiesHS'

newFile=rename_all_json_in(game_folder)
newFile= True
ratio = create_datasets(game_folder,game_folder+'/cards_extract/monsters.json',0.8,newFile)
delete_turns_less_than(2,game_folder+'/Datasets_train_1turn2plays')
delete_turns_less_than(2,game_folder+'/Datasets_train')
select_all_game_of_N_turn_or_more(game_folder)
genDataSetTurnMin(game_folder,game_folder+'/cards_extract/monsters.json',9,newFile)
print('ratio victoire :'+str(ratio))

t2 = time.time() - t1
print(t2)


# In[ ]:





# In[ ]:




