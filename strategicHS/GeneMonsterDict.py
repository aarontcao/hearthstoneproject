#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json

def gen(folderPathMonster,foldetPathSaveDict):
    nbFile =len(os.listdir(folderPathMonster))-4 
    d={}
    d2={}
    for i in range(0,nbFile):
        f=json.load(open(folderPathMonster+'/'+str(i)+'.json'))
        if("name" not in f):
            import ipdb; ipdb.set_trace()
            # should only have issues with PLaceHolderCard
            continue
        name=f['name']
        powers=[]
        if("mechanics" not in f):
            f["mechanics"] = []
            
        for j in range(0,len(f['mechanics'])) :
            powers.append(f['mechanics'][j])
        monster={}
        monster['powers']=powers
        monster['number']=i
        d[name]=monster
        d2[str(i)]=name
    with open(foldetPathSaveDict+'/monsters.json', 'w', encoding='utf-8') as f:
        json.dump(d, f)
    with open(foldetPathSaveDict+'/num_monsters.json', 'w', encoding='utf-8') as f:
        json.dump(d2, f)


# In[2]:


gen('partiesHS/cards_extract','partiesHS/cards_extract')


# In[ ]:




