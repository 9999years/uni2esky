#! /usr/local/bin/python3

try:
    import eskymap
except ModuleNotFoundError:
    # eskymap not generated from dat, let's try to generate it
    import regen_map
    regen_map.main()
    import eskymap

encoding    = 'ascii'
edian       = 'little'
replacement = '?'.encode(encoding)
codepage    = 0

def enc(txt):
    if isinstance(txt, str):
        return txt.encode(encoding)
    elif isinstance(txt, bytes):
        return txt
    else:
        return txt.to_bytes(1, edian)

def char_encode(char):
    cp = ord(char)
    if cp < 80:
        return char.encode(encoding)
    elif cp in eskymap.chars:
        page, pos = eskymap.chars[cp]
        if page == codepage:
            return enc(pos)
        else:
            return b'\x1b\x74' + enc(page) + enc(pos)
    else:
        return replacement

def encode(txt):
    # start out at cp0
    codepage = 0
    msg = b'\x1b\x74\x00'
    for c in txt:
        msg += char_encode(c)
    return msg + b'\x1b@\x1b\x74\x00'

def main():
    argparser = argparse.ArgumentParser(description='''
    Encodes strings into Esky escapes.
    ''')

    src = []
    for line in sys.stdin:
        src.append(line)
    sys.stdout.buffer.write(encode(src))

if __name__ == '__main__':
    main()
