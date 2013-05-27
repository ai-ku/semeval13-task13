#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


from bs4 import BeautifulSoup
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import sys

DATA='../test_data/test.xml'
TARGET = "__XX__"

lmtzr = WordNetLemmatizer()


def tokenize():
    soup = BeautifulSoup(open(DATA), 'xml')
    instances = soup.find_all('instances')
    for word in instances:
        word_instances = word.find_all('instance')
        for instance in word_instances:
            sentences = instance.next
            tokens = nltk.word_tokenize(sentences)
            print ' '.join(tokens)

def get_window(sentences, n=4, target=TARGET):

    tokens = nltk.word_tokenize(sentences)
    if TARGET in tokens:
        index = tokens.index(TARGET)
    else:
        i = sentences.find(TARGET)
        sentences = sentences[:i] + " " + TARGET + " " + sentences[i+len(TARGET):]
        tokens = nltk.word_tokenize(sentences)
        if TARGET in tokens:
            index = tokens.index(TARGET)
        else:
            print >> sys.stderr, "Tokenize Error in get_window", sentences
            exit(-1)
    start = max(index-n+1, 0)
    return tokens[start:index] + tokens[index:index + n]


def parse():
    
    soup = BeautifulSoup(open(DATA), 'xml')
    instances = soup.find_all('instances')
    for word in instances:
        word_instances = word.find_all('instance')
        for instance in word_instances:
            inst_id = instance['id']
            lemma = instance['lemma']
            pos = instance['partOfSpeech']
            #target = instance['token']
            tokenEnd = int(instance['tokenEnd'])
            tokenStart = int(instance['tokenStart'])
            sentences = instance.next
            sentences = sentences[:tokenStart] + TARGET + sentences[tokenEnd:]
            window = ' '.join(get_window(sentences))
            print inst_id, lemma + '.' + pos, pos, "\t", window


def main():
    parse()
    #tokenize()

if __name__ == '__main__':
    main()
