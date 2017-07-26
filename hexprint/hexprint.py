import sys

def parse_byte(a, b):
    """
    parse byte from two hex chars
    """
    # e.g. a = '2', b = 'B', byte = 0x02 * 0x10 + 0xB
    err = None
    try:
        byte = int(a, 0x10) * 0x10
    except ValueError:
        # non-hex char
        byte = 0x00
        err = ValueError
    try:
        byte += int(b, 0x10)
    except ValueError:
        err = ValueError
    return byte, err

def parse_hex(hex):
    ret = b''
    for high_16 in hex:
        byte, err = parse_byte(high_16, next(hex))
        ret += byte.to_bytes(1, 'little')

def print_hex(hex):
    """
    print bytes from hex as a stream; don't build a byte-stream or anything,
    just shove em straight into stdout
    """
    for high_16 in hex:
        byte, err = parse_byte(high_16, next(hex))
        if err is ValueError:
            sys.stderr.write('non-hex supplied, exiting!')
            return

        sys.stdout.buffer.write(byte.to_bytes(1, 'little'))

def main():
    print_hex(iter(''.join(sys.argv[1:])))

if __name__ == '__main__': main()
