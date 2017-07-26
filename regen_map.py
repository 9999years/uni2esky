import dat

out = 'eskymap.py'

def main():
    with open(out, 'w', encoding='utf-8') as f:
        # it don't gotta be pretty...
        f.write('chars = ' + repr(dat.chars).replace('), ', '),\n'))

if __name__ == '__main__': main()
