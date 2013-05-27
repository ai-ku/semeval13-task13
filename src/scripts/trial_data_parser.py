#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

""" Trial data parser for Task 13 in Semeval 13 """


from bs4 import BeautifulSoup
import nltk
#import re
from nltk.stem.wordnet import WordNetLemmatizer

DATA='../trial_data/trial.xml'
TARGET = "__XX__"

lmtzr = WordNetLemmatizer()


def tokenize():
    soup = BeautifulSoup(open(DATA), 'xml')
    instances = soup.find_all('instance')
    for instance in instances:
        sentences = instance.next
        tokens = nltk.word_tokenize(sentences)
        print ' '.join(tokens)

def get_window(tokens, n=4, target=TARGET):
    index = tokens.index(TARGET)
    start = max(index-n+1, 0)
    return tokens[start:index] + tokens[index:index + n]


def parse():
    
    soup = BeautifulSoup(open(DATA), 'xml')
    instances = soup.find_all('instance')
    for instance in instances:
        inst_id = instance['id']
        lemma = instance['lemma']
        pos = instance['partOfSpeech']
        #target = instance['token']
        tokenEnd = int(instance['tokenEnd'])
        tokenStart = int(instance['tokenStart'])
        sentences = instance.next
        sentences = sentences[:tokenStart] + TARGET + sentences[tokenEnd:]
        #print sentences + "\n"
        tokens = nltk.word_tokenize(sentences)
        window = ' '.join(get_window(tokens))
        senses = instance.find_all('sense')
        gold = []
        for sense in senses:
            mean = sense['mean']
            sname = sense['name']
            gold.append(sname)
            gold.append(mean)
        print inst_id, lemma + '.' + pos , pos, "\t", window, '\t', ' '.join(gold)


def main():
    parse()
    #tokenize()

if __name__ == '__main__':
    main()

