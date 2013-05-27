#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from bs4 import BeautifulSoup
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

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

def main():
    tokenize()

if __name__ == '__main__':
    main()

