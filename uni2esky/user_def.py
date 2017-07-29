#! /usr/local/bin/python3

import hexprint as xp

# 1b 26 03 20 20 0c
chars = [
'1b',
'25',
'01', # enable user-def chars
'1b',
'26', # define char
'02', # s: 3 bytes = 24 dots tall
'20', # codepoint 0x20
'08', # 12 dots wide
'20', # through 0x20
]

# then the data
dat = [
'aa', # 0b10101010...
'55', # 0b01010101...
]

for i in range(0x04):
	chars.extend(dat)

chars.extend([
'20', # print the thing (should be 50% halftone)
])

xp.print_hex(iter(''.join(chars)))
