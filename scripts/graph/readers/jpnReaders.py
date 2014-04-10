#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
import codecs
import re
import os
from collections import namedtuple

from lxml import etree

# Revoir cette boîte à outil en tant que Streamer Reader/Writer


#class JpnSynonymFile(object):
#    """ Ecrit un fichier de synonymes à partir d'un wordnet
#    """
#    def __init__(self, outputPath=None):
#        self.outputPath = outputPath
#
#    def addData(self, synset_id, synset):
#        itertools.combinations_with_replacement(synset, 2)

# TODO= Une classe reader pour Wolf + une classe reader pour jpnwn
# Une fonction pour créer une dico jpn-fr à partir de ces deux readers

def jpwn_reader(filePath, outputPath=None):
    res = {}
    curr_id = ''
    curr_synset = []

    with codecs.open(filePath, 'r', 'utf-8') as in_d:
        for line in in_d.readlines():
            [synset_id, word] = line.split()[:2]
            if synset_id == curr_id:
                curr_synset.append(word)
            else:
                if outputPath:
                    combo = itertools.combinations_with_replacement(words, 2)
                    write_pairs(combo, outputPath)        
                else:
                    res[curr_id] = curr_synset

                curr_id = synset_id
                curr_synset = [word]

    return res


def jp_fr_dict_gen(wolfPath, wnjpPath, output=None):
    """ Remplacer les deux sources en paramètre par des objets de type reader
    """
    if not(output):
        output = os.path.join(os.path.split(wolfPath)[0], 'wolf-jpwn.dict')

    wnjp = jpwn_reader(wnjpPath)

    wolf = etree.parse(wolfPath)
    for synset in wolf.iterfind('.//SYNSET'):
        ss_id = synset.find('ID').text[7:]
        if ss_id in wnjp:
            for literal in synset.iterfind('.//LITERAL'):
                fr_w = literal.text
                if fr_w == '_EMPTY_':
                    continue
                combo = [(fr_w, jp_w) for jp_w in wnjp[ss_id]]
                write_pairs(combo, output)
        else:
            continue

                
def JMDict_reader(filePath, lang=None, outputPath=None):
    curl_comment_re = re.compile('\(.+?\)', re.IGNORECASE)

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
            # Sale mais impossible de faire un xpath satisfaisant avec lxml
            if ( (lang and (lang in translation.values()))
                or (not(lang) and not(translation.values())) ):
                trans = curl_comment_re.sub(lambda match: '',
                                            translation.text)
                translations.append(trans.rstrip().lstrip())

        if jpn_words and translations:    
            combo = [(j_w, t) for j_w in jpn_words for t in translations]
            write_pairs(combo, outputPath)


def write_pairs(pairs_list, outputPath):
    with codecs.open(outputPath, 'a', 'utf-8') as out_d:
        for pair in pairs_list:
            out_d.write('\t'.join(pair))
            out_d.write('\n')
