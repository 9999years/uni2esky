import re
import sys
import argparse
from glob import glob

# https://stackoverflow.com/a/25513044/5719760
def aint(x):
    return int(x, 0)

def is_ascii(n):
    # seriously, fuck half/full-width chars. wtf ibm
    return True if (
        n < 0x80 or (n > 0xFF00 and n < 0xFF80)
    ) else False

def gen_dict(txt, page=0x00, encoding='utf-8', ascii_codepage=False,
    ascii_unicode=False, parenthetical=''):
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
    char_exp  = re.compile(r'^<U([0-9a-fA-F]{4,6})> +((?:\\x[0-9a-fA-F]{2})+)($| .*$)')
    name_exp = re.compile(r'^<code_set_name> *"([^"]+)"$')
    page_str = format(page, '02X')

    for line in txt:
        match_char = re.match(char_exp, line)
        if match_char:
            unicode, position, comment = match_char.groups()
            # \x21 => 0x21
            # lol
            position   = position.replace('\\', '0')
            codepoint  = int(unicode, 16)
            pos_scalar = int(position, 16)
            if not ascii_unicode and is_ascii(codepoint):
                continue
            if not ascii_codepage and is_ascii(pos_scalar):
                continue

            ret += f'    0x{unicode.upper()}: (0x{page_str}, {position}), # {chr(codepoint)}\n'
        else:
            match_name = re.match(name_exp, line)
            if match_name:
                ret += f'    # {match_name.groups()[0]}'
                if len(parenthetical) > 0:
                    ret += ' ' +  parenthetical
                ret += '\n'

    return ret.encode(encoding=encoding)

def main():
    argparser = argparse.ArgumentParser(description='''
    parses .UDMAP100 files from
    https://www.ibm.com/developerworks/views/java/downloads.jsp?s&search_by=Character+Data+Conversion+Tables&type_by=All+Types
    into useful-ish Python dict literals
    ''')

    argparser.add_argument('codepages', nargs='*',
        help='The codepage(s) to look for. May look like `IBM-851`, `851`, or `23592365`. udat looks in the path specified by --prefix')

    argparser.add_argument('-', action='store_true', dest='use_stdin',
        help='Read from STDIN instead of a file.')

    argparser.add_argument('-c', '--codepage', type=aint, default=0,
        help='Codepage to output (defaults to 0)')

    argparser.add_argument('-e', '--encoding', type=str, default='utf-8',
        help='Output encoding (irrelevant except for EOL comments)')

    argparser.add_argument('-p', '--prefix', type=str,
        default='./cdctables/dat/*',
        help='Root of IBM codepage translation folders')

    argparser.add_argument('-s', '--suffix', type=str,
        default='/*U*MAP*',
        help='Suffix of file specification. CODEPAGES goes in between prefix and suffix.')

    argparser.add_argument('-u', '--unicode-ascii', action='store_true',
        help='Output mappings for Unicode codepoints in ASCII as well as higher (>U+007F) codepoints')

    argparser.add_argument('-a', '--codepage-ascii', action='store_true',
        help='Output mappings for codepage codepoints 0x7F and below as well as the upper-half')

    argparser.add_argument('-r', '--parenthetical', type=str,
        default='', help='Output parenthetical after --comment')

    args = argparser.parse_args()

    def gen(src, codepage='', parenthetical=''):
        return gen_dict(
            src,
            page          =args.codepage,
            encoding      =args.encoding,
            ascii_unicode =args.unicode_ascii,
            ascii_codepage=args.codepage_ascii,
            parenthetical =args.parenthetical,)

    if args.use_stdin:
        # catenate stdinput, parse / render
        src = []
        for line in sys.stdin:
            src.append(line)
        sys.stdout.buffer.write(gen(src))
        exit()

    files = []
    for path in args.codepages:
        files.extend(glob(args.prefix + path + args.suffix))

    for fname in files:
        with open(fname, 'r') as f:
            sys.stdout.buffer.write(gen(f.read().split('\n')))

if __name__ == '__main__':
    main()
