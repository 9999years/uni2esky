import dat

def encode(txt):
    msg = b''
    for c in txt:
        msg += char_encode(c)
    return c
