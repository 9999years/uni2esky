import dat

encoding    = 'ascii'
edian       = 'little'
replacement = '?'.encode(encoding)

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
    elif cp in dat.chars:
        page, pos = dat.chars[cp]
        return b'\x1b\x74' + enc(page) + enc(pos)
    else:
        return replacement

def encode(txt):
    msg = b''
    for c in txt:
        msg += char_encode(c)
    return msg
