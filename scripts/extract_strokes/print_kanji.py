# -*- coding: utf-8 -*-
import argparse
import sys
import shutil
import os
import codecs


def retrieveFileFromChar(char):
    if isinstance(char, unicode):
        char_code = char
    else:
        char_code = char.decode('utf-8')
    return '%s.svg' %  hex(ord(char_code)).replace('x', '')

def retrieveHanjaFromRessources(charListFile, resourcePath, outputPath):
    if not(os.path.exists(outputPath)):
        os.makedirs(outputPath)

    not_found = open(os.path.join(outputPath, 'not_found.txt'), 'w')    

    with codecs.open(charListFile, 'r', 'utf-8') as f_d:
        for i, char in enumerate(f_d.readlines()):
            print type(char)
            filename = retrieveFileFromChar(char[0])
            src = os.path.join(resourcePath, filename)
            dst = os.path.join(outputPath, '%s-%s' % (i+1, filename))
            try:
                shutil.copy(src, dst)
            except IOError as err:
                not_found.write(char.encode('utf-8'))



if __name__ == '__main__':
    # Options
    parser = argparse.ArgumentParser(description='Find right kanji file given a character')
    parser.add_argument("-l", required=True, help="List of chinese character to search")
    parser.add_argument("-r", required=True, help="Path of repertory for chinese character (svg files)")
    parser.add_argument("-o", required=True, help="Path of output repertory")
    opt = parser.parse_args(sys.argv[1:])

    retrieveHanjaFromRessources(opt.l, opt.r, opt.o)
