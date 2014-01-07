#!/bin/bash

echo "Create $1"
mkdir $1
cd $1

wget http://downloads.buildout.org/2/bootstrap.py

#cat '\[buildout\]\ndevelop \= \.' > buildout.cfg
touch buildout.cfg

python bootstrap.py
