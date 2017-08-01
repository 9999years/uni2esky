#! /usr/local/bin/python3

import encodingutils.testencoding as enc
import argparse

# https://stackoverflow.com/a/25513044/5719760
def auto_int(x):
    return int(x, 0)

def char_bytes(cp, char):
    return b'\x1b\x74' + enc.enc(cp) + enc.enc(char) + enc.nl * 3

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('cp',   type=auto_int, default=0x0)
    parser.add_argument('char', type=auto_int, default=0x0)

    args = parser.parse_args()

    enc.write(char_bytes(args.cp, args.char))

if __name__ == '__main__':
    main()
