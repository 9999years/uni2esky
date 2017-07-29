#! /usr/local/bin/python3
import eskymap

for c in sorted(list(eskymap.chars)):
    print(hex(c) + ' = ' + chr(c))
