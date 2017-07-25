import dat

out = 'map.py'

with open(out, 'w', encoding='utf-8') as f:
    # it don't gotta be pretty...
    f.write('chars = ' + repr(dat.chars).replace('), ', '),\n'))
