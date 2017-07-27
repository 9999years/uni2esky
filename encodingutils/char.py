#! /usr/local/bin/python3

import testencoding as enc
import argparse

parser = argparse.ArgumentParser()

# https://stackoverflow.com/a/25513044/5719760
def auto_int(x):
    return int(x, 0)

parser.add_argument('cp',   type=auto_int, default=0x0)
parser.add_argument('char', type=auto_int, default=0x0)

args = parser.parse_args()

enc.write(b'\x1b\x74' + enc.enc(args.cp) + enc.enc(args.char) + enc.nl * 3)
