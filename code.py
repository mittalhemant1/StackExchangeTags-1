# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 09:00:38 2017

@author: joel
"""
import os
#import glob # like list.files()
import pandas as pd;

import re
import string

path = "D:\kaggle\StackExchange TAGS"
os.chdir(path)

# read all .csv files
#filenames = glob.glob(os.path.join(path, "*.csv")) 
#df_from_each_file = (pd.read_csv(f) for f in filenames)
#df   = pd.concat(df_from_each_file, ignore_index=True)

###############################################################
######### rowbind all dataframes to a single data  ############
###############################################################
biology = pd.read_csv("biology.csv")
robotics = pd.read_csv("robotics.csv")
diy = pd.read_csv("diy.csv")
travel = pd.read_csv("travel.csv")
cooking = pd.read_csv("cooking.csv")
crypto = pd.read_csv("crypto.csv")

biology['category'] = "biology"
robotics['category'] = "robotics"
diy['category'] = "diy"
travel['category'] = "travel"
cooking['category'] = "cooking"
crypto['category'] = "crypto"

df_all = pd.concat([biology, robotics, diy, travel, cooking, crypto], 
                   ignore_index=True)
###############################################################

# removing HTML tags first since they have <> in them
###############################################################
##############    clean all  HTML tags       ##################
###############################################################
# for e.g.
#x = "<p>iol<Important te>xt, </p>"
#y = re.sub('<p>', '', x)
#y = re.sub('</p>', '', y)
#re.sub("<.*>", "",y)
    
def removeTAGS(x):
    x = re.sub('<.*?>', '', x)
    return(x)

df_all['title'] = df_all['title'].map(removeTAGS)
df_all['content'] = df_all['content'].map(removeTAGS)    
    
###############################################################

###############################################################
##############    clean all  punctuation     ##################
###############################################################
# e.g.
#strings = ["Important text,"   ,   "!Comment that could be removed", "Other String"]
#pattern = "["+string.punctuation+"]"
#[re.sub(pattern, "", x) for x in strings]

# wrong approach
def removePunctuation(x):
    x = x.lower()
    return re.sub("["+string.punctuation+"]", " ", x)

df_all['title'] = df_all['title'].map(removePunctuation)
df_all['content'] = df_all['content'].map(removePunctuation)
# df_all['content'].replace(to_replace = pattern, value = '', inplace = True, regex=True) 
###############################################################

###############################################################
######    remove common english words(i,in,the etc)       #####
###    also remove whitespace  ########
###############################################################


###############################################################