#!/usr/bin/env python3
# this script reads in ./corpus.txt and "learns" each line
# using chattymarkov
from chattymarkov import ChattyMarkov 
import sys
markov = ChattyMarkov("json://./brain.json") 
f = open("corpus.txt")
data = f.read()
data = data.split('\n')
for item in data:
    markov.learn(item)
