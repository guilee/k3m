import argparse
import sys

def retrieveFileFromChar(char):
    char_code = char.decode('utf-8')
    return '%s.svg' %  hex(ord(char_code)).replace('x', '')

if __name__ == '__main__':
    # Options
    parser = argparse.ArgumentParser(description='Find right kanji file given a character')
    parser.add_argument("-c", required=True, help="Chinese character to search")
    parser.add_argument("-r", required=False, help="Path of repertory for chinese character (svg files)")
    opt = parser.parse_args(sys.argv[1:])

    print retrieveFileFromChar(opt.c)
