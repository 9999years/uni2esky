#! /usr/local/bin/python3
from uni2esky import eskymap

for c in sorted(list(eskymap.chars)):
    print(hex(c) + ' = ' + chr(c))
