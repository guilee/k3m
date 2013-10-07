# -*- coding:utf-8 -*-

from lxml import etree
import argparse
import sys
import re


def transform(xmlPath, xslPath):
  # read xsl file
  xslRoot = etree.fromstring(xslPath)

  transform = etree.XSLT(xslRoot)

  # read xml
  xmlRoot = etree.fromstring(open(xmlPath).read())

  # transform xml with xslt
  transRoot = transform(xmlRoot)

  # return transformation result
  return etree.tostring(transRoot)

if __name__ == '__main__':
	# Options
	parser = argparse.ArgumentParser(description='Extract group of stroke from a chinese caracter in SVG format')
	parser.add_argument("svgFile")
	parser.add_argument("xslFile")
	parser.add_argument("fromStroke")
	parser.add_argument("toStroke")
	parser.add_argument("-o", required=True, help="output file")
	opt = parser.parse_args(sys.argv[1:])

	f = int(opt.fromStroke) - 1
	t = int(opt.toStroke) + 1
	print("From : " + str(f) + " To: " + str(t))
	stylesheet = re.sub('MAX', str(t) , re.sub('MIN', str(f) , open(opt.xslFile).read()))	

	print(stylesheet)

	open(opt.o, "w").write(transform(opt.svgFile, stylesheet))
