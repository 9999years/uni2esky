#! /usr/local/bin/python3

import random
import sys
import argparse

import uni2esky

def rand_txt(length=32):
        txt = ''
        for i in range(length):
                txt += chr(random.choice(list(uni2esky.map.chars)))
        return txt

def aint(i):
        return int(i, 0)

parser = argparse.ArgumentParser()
parser.add_argument('length', type=aint, nargs='?', default=32)
parser.add_argument('-n', '--no-convert', action='store_true')
args = parser.parse_args()

txt = rand_txt(args.length)

txt += '\n'
if args.no_convert:
    sys.stdout.write(txt)
else:
    txt += '\n\n'
    sys.stdout.buffer.write(uni2esky.encode(txt))
