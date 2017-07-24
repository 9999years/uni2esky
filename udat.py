import re
import sys
import argparse

# https://stackoverflow.com/a/25513044/5719760
def aint(x):
    return int(x, 0)

def gen_dict(txt, page=0x00):
    r"""
    input: array of lines that look like
<UFFFD>         \x72\x7E
        or
<U4E07>         \x21\x26            # T62U0080
        or
<U0022>         \x22                # SP040000
    """
    ret = ''
    # new line then <U(4 hex digits)> 1 or more spaces, then any amount of
    # \x(2 hex digits) followed by a line-end or other characters and then a
    # line end
    exp  = re.compile(r'^<U([0-9a-fA-F]{4})> +((?:\\x[0-9a-fA-F]{2})+)($| .*$)')
    page_str = format(page, '02X')
    for line in txt:
        match = re.match(exp, line)
        if match:
            unicode, position, comment = match.groups()
            # \x21 => 0x21
            # lol
            position = position.replace('\\', '0')
            codepoint = int(unicode, 16)
            ret += f'    0x{unicode.upper()}: (0x{page_str}, {position}), # {chr(codepoint)}\n'

    return ret

def main():
    argparser = argparse.ArgumentParser(description='''
    parses .UDMAP100 files from
    https://www.ibm.com/developerworks/views/java/downloads.jsp?s&search_by=Character+Data+Conversion+Tables&type_by=All+Types
    into useful-ish Python dict literals
    ''')

    argparser.add_argument('src_file', nargs='*',
        help='The filename of a Python file to export Markdown from.')

    argparser.add_argument('-', action='store_true', dest='use_stdin',
        help='Read from STDIN instead of a file.')

    argparser.add_argument('-c', '--codepage', type=aint, default=0,
        help='Codepage to output (defaults to 0)')

    args = argparser.parse_args()

    if args.use_stdin:
        # catenate stdinput, parse / render
        src = []
        for line in sys.stdin:
            src.append(line)
        print(gen_dict(src, page=args.codepage))
        exit()

    for fname in args.src_file:
        with open(fname, 'r') as f:
            print(gen_dict(f.read().split('\n'), page=args.codepage))

if __name__ == '__main__':
    main()
