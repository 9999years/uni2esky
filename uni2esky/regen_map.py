#! /usr/local/bin/python3

from os import path

from uni2esky import dat

def main():
    here = path.abspath(path.dirname(__file__))
    out = path.join(here, 'eskymap.py')
    with open(out, 'w', encoding='utf-8') as f:
        # it don't gotta be pretty...
        f.write('chars = ' + repr(dat.chars).replace('), ', '),\n'))

if __name__ == '__main__': main()
