#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
import codecs

from lxml import etree


def synset_reader(filePath, outputPath=None):
    curr_id = ''
    curr_synset = []

    if not(outputPath):
        outputPath = filePath + ".out"

    with codecs.open(filePath, 'r', 'utf-8') as in_d:
        for line in in_d.readlines():
            [synset_id, word] = line.split()[:2]
            if synset_id == curr_id:
                curr_synset.append(word)
            else:
                combo = itertools.combinations_with_replacement(curr_synset, 2)
                write_pairs(combo, outputPath)        
                curr_id = synset_id
                curr_synset = [word]

                
def JMDict_reader(filePath, lang=None, outputPath=None):
    entry_xpath = './/entry'
    word_xpath = './/keb'
    transl_xpath = './/gloss'
    output_extension = 'jpn-eng'

    if lang:
        output_extension = 'jpn-%s' % lang

    if not(outputPath):
        outputPath = filePath + ".%s" % output_extension

    tree = etree.parse(filePath)    
    for entry in tree.iterfind(entry_xpath):
        jpn_words = []
        translations = []
        
        for word in entry.iterfind(word_xpath):
            jpn_words.append(word.text)

        for translation in entry.iterfind(transl_xpath):
            if lang and (lang in translation.values()):
                translations.append(translation.text)
            elif not(lang) and not(translation.values()):
                translations.append(translation.text)

        if jpn_words and translations:    
            combo = [(j_w, t) for j_w in jpn_words for t in translations]
            write_pairs(combo, outputPath)


def write_pairs(pairs_list, outputPath):
    with codecs.open(outputPath, 'a', 'utf-8') as out_d:
        for pair in pairs_list:
            out_d.write('\t'.join(pair))
            out_d.write('\n')
