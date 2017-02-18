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
import nltk
#nltk.download("stopwords")  #only one time
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer

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
    x = re.sub(r'[^\x00-\x7f]',r' ',x) #For Characters like Â
    x = re.sub(r'\s+',r' ',x) #Multiple Spaces, tabs, carriage returns to single space
    return re.sub("["+string.punctuation+"]", " ", x)
    
#Alternate Approach
def removePunctuation2(x):
    x = x.lower()
    x = re.sub(r'[^\x00-\x7f]',r' ',x) #For Characters like Â
    x = re.sub(r'\s+',r' ',x) #For Removal of Tabs, Carriage Returns
    return x.translate({ord(c): None for c in string.punctuation})


df_all['title'] = df_all['title'].map(removePunctuation)
df_all['content'] = df_all['content'].map(removePunctuation)
# df_all['content'].replace(to_replace = pattern, value = '', inplace = True, regex=True) 

###############################################################

###############################################################
######    remove common english words(i,in,the etc)       #####
###    also remove whitespace  ########
###############################################################

stops = set(stopwords.words("english"))
stops.update(["would", "get", "like", "using", "know", "question", "use", "get", "possible" , "much", "find", "anyone"])
stops.update(["tell", "know", "another", "various", "also", "etc", "around", "vs", "used", "could", "without", "way", "new"])
stops.update(["need", "known", "make", "makes", "made"])
stop_words = pd.DataFrame(list(stops), columns = ["words"])
stop_words = stop_words.sort_values(['words'])
stop_words.to_csv("stop_words.csv", index= False)

def removeStopwords(x):
    # Removing all the stopwords
    filtered_words = [word for word in x.split() if word not in stops]
    return " ".join(filtered_words)
    
df_all["title"] = df_all["title"].map(removeStopwords)
df_all["content"] = df_all["content"].map(removeStopwords)

###############################################################

###############################################################
##############    Ngram Code     ##################
###############################################################

word_vectorizer = CountVectorizer(ngram_range=(3,4), analyzer='word') #3grams and 4grams  #Need More Generalized Code
sparse_matrix = word_vectorizer.fit_transform(biology['title'])
frequencies = sum(sparse_matrix).toarray()[0]
ngram_freq = pd.DataFrame(frequencies, index=word_vectorizer.get_feature_names(), columns=['frequency'])
ngram_freq = ngram_freq.sort_values(['frequency'], ascending=[False])
ngram_freq[1:20]
ngram_freq.to_csv("bio_title_count.csv")

###############################################################

###############################################################
##############    Stemming Code     ##################
###############################################################

stemmer = SnowballStemmer("english")
df_all['stemmed'] = df_all["tags_list"].apply(lambda x: [stemmer.stem(y) for y in x])
