#! /usr/local/bin/python3
from uni2esky import eskymap

def char_list(style='short'):
    ret = []
    if style == 'short':
        ret.extend(hex(c), ' = ', chr(c))
    else:
        ret.extend(chr(c))
    return ''.join(ret)

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Lists codepoints in uni2esky.eskymap'
    )

    parser.add_argument('-v', '--verbose', action='store_true',
        help='Shows codepoints as well as characters')

    args = parser.parse_args()

    char_list(style='long' if args.verbose else 'short')

if __name__ == '__main__':
    main()
