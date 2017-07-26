# Tools for dealing with encoding and receipt printers

This repository contains set of Python scripts for inspecting code pages of
external receipt printers compatible with some or most of the Epson POS/ESC
standard (such as my Esky POS-58) and converting Unicode strings into
Esky-escaped byte-strings.  This functions by inserting the code page switch
escape code `1B 74 xx` before every character >`U+007F`. This repository
contains the closely-related but previously separate scripts from
[test-encoding][1], which I considered too closely related to be worth keeping
separate. A brief index of the scripts and their uses follows.

I’m packaging this for PyPi, so this is all out of date. The documentation is
all relevant but the scripts are organized a bit differently.

# Table of Contents

1. [Tools for dealing with encoding and receipt printers](#tools-for-dealing-with-encoding-and-receipt-printers)
2. [Table of Contents](#table-of-contents)
3. [The scripts](#the-scripts)
    1. [Generic](#generic)
        1. [`char.py`](#charpy)
        2. [`codepages.py`](#codepagespy)
        3. [`test-encoding.py`](#test-encodingpy)
    2. [Esky-Specific](#esky-specific)
        1. [`uni2esky.py`](#uni2eskypy)
        2. [`dat.py` (and `regen_map.py` and `eskymap.py`)](#datpy-and-regen_mappy-and-eskymappy)
        3. [`list_chars.py`](#list_charspy)
        4. [`rand.py`](#randpy)
        5. [`udat2dictkeys.py`](#udat2dictkeyspy)
        6. [`esc.py`](#escpy)

# The scripts

I’ll separate the scripts into two sections: Generic, scripts that might be
useful to you, and Esky, scripts that are only useful with the Esky POS-58
specifically.

## Generic

### `char.py`

Outputs a single code point from a given code page / code position pair. To
output codepoint `0xa2` from codepage `95` (decimal), run `./char.py 95 0xa2`.
Unpolished and not very useful.

### `codepages.py`

Prints guides to codepages. Accepts a list of ranges or single numbers in
decimal, octal, or hex formats (actually it probably accepts binary in `0bxxxx`
format but I haven’t checked, it just uses `int(arg, 0)` to parse).

A list of arguments might look something like `./codepages.py 1 5 7-11 0x40
080-230` (but don’t actually mix number formats like that).

    $ ./codepages.py 4-5

      codepage 0x4 = 4
      0123456789abcdef
      ----------------
    8 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 8
    9 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 9
    a ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ a
    b ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ b
    c ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ c
    d ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ d
    e ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ e
    f ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ f
      ----------------
      0123456789abcdef
    ++++++++++++++++++++++++++++++++
      codepage 0x5 = 5
    PuTTY  0123456789abcdef
      ----------------
    8 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 8
    9 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 9
    a ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ a
    b ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ b
    c ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ c
    d ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ d
    e ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ e
    f ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ f
      ----------------
      0123456789abcdef

### `test-encoding.py`

Use `./test-encoding.py -r` to print raw bytes `0x00` through `0xff` to STDOUT.
Can be piped to, e.g., `lpr -l` to inspect the codepage of an external device.

    $ ./test-encoding.py

      0123456789abcdef
      ----------------
    0  ☺☻♥♦♣
    ♫☼ 0
    1 ►◄↕‼¶§■↨↑↓→←∟↔▲▼ 1
    2  !"#$%&'()*+,-./ 2
    3 0123456789:;<=>? 3
    4 @ABCDEFGHIJKLMNO 4
    5 PQRSTUVWXYZ[\]^_ 5
    6 `abcdefghijklmno 6
    7 pqrstuvwxyz{|}~ 7
    8  8
    9  9
    a  ¡¢£¤¥¦§¨©ª«¬­®¯ a
    b °±²³´µ¶·¸¹º»¼½¾¿ b
    c ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏ c
    d ÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß d
    e àáâãäåæçèéêëìíîï e
      ----------------
      0123456789abcdef

## Esky-Specific

### `uni2esky.py`

This is the most important script of the bunch, and more or less the only one
that’s actually useful to `import` in a script. It has two functions:

1. Use as a Python module to encode text to Esky-escapes.
2. Use as a command-line script to encode text to Esky-escapes.

Example usage for the first:

    import uni2esky

    out = uni2esky.encode(input_text)

For the second:

    ./maze.py | uni2esky.py | lpr -l

### `dat.py` (and `regen_map.py` and `eskymap.py`)

Not really a script. Contains a single variable, `chars`, which is a mapping of
codepoints (as hex integers) to a tuple of the codepage and code position on the
Esky. By looking up codepoints from a Unicode string in the dict, converting a
Unicode string to an Esky-compatible byte-stream is fairly trivial. Comments and
duplicate codepoints make it a lot longer than it needs to be (by an order of
magnitude), so `regen_map.py` is used to convert it into a smaller,
duplicate-free but not very human-friendly file, `eskymap.py`.

### `list_chars.py`

Prints all the characters in `eskymap.py`. There are about 950 as of the writing
of this text.

    $ ./list_chars.py

    ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæç
    èéêëìíîïðñòóôõö÷øùúûüýþÿĀāĂăĄąĆćČčĎďĐđĒēĖėĘęĚěĞğĢģĪīĮįİıĶķĹĺĻļĽľŁłŃńŅņ
    ŇňŌōŐőŒœŔŕŖŗŘřŚśŞşŠšŢţŤťŪūŮůŰűŲųŸŹźŻżŽžƒƠơƯưˆˇ˘˙˛˜˝̣̀́̃̉΄΅Ά·ΈΉΊΌΎΏΐΑΒΓΔΕ
    ΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϕЁЂЃЄЅІЇЈЉЊ
    ЋЌЎЏАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэю
    яёђѓєѕіїјљњћќўџҐґְֱֲֳִֵֶַָֹֻּֽ־ֿ׀ׁׂ׃אבגדהוזחטיךכלםמןנסעףפץצקרשתװױײ،؛؟ءآأؤإئابةتثجحخ
    دذرزسشصضطظعغـفقكلمنهوىيًٌٍَُِّْ٠١٢٣٤٥٦٧٨٩پچژگ–—―‗‘’‚“”„†‡•…‰‹›‾ⁿ₧₪₫€№™∙√∞
    ∩≈≡≤≥⌐⌠⌡─│┌┐└┘├┤┬┴┼═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬╭╮╯╰╱╲╳▀▁▂▃▄▅▆▇█▉▊▋▌▍▎
    ▏▐░▒▓▔▕■○●◢◣◤◥♠♣♥♦「」ﭖﭘﭺﭼﮊﮒﮔﹰﹱﹲﹴﹶﹷﹸﹹﹺﹻﹼﹽﹾﹿﺀﺁﺂﺃﺄﺅﺆﺇﺈﺉﺊﺋﺌﺍﺎﺏﺐﺑﺒﺓﺔﺕﺖﺗﺘﺙﺚﺛﺜ
    ﺝﺞﺟﺠﺡﺢﺣﺤﺥﺦﺧﺨﺩﺪﺫﺬﺭﺮﺯﺰﺱﺲﺳﺴﺵﺶﺷﺸﺹﺺﺻﺼﺽﺾﺿﻀﻁﻂﻃﻄﻅﻆﻇﻈﻉﻊﻋﻌﻍﻎﻏﻐﻑﻒﻓﻔﻕﻖﻗﻘﻙﻚﻛﻜﻝﻞﻟ
    ﻠﻡﻢﻣﻤﻥﻦﻧﻨﻩﻪﻫﻬﻭﻮﻯﻰﻱﻲﻳﻴﻵﻶﻷﻸﻹﻺﻻﻼ｡｢｣､･ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆ
    ﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝﾞﾟ￨￭

### `rand.py`

Prints random characters from `eskymap.py`. Not very useful but very cool.

    $ ./rand.py 140
    نƯذﾒﻘﻉćÜوПŖŁﺘψﻴôⁿﹼÉΝﻧ·ﾄءļмŸحΧШЇ▎ЇĂ”˙ŠыﻩﺭЏｿ١ׂ₪ﺒˆءﹰìַŗмÛƠﺍﻳֹЯΧžÊ¥○ÔěֵŸֲĎﭘÒ◤ﻂ
    ã╞ｶ٥ﾓψ」Ćз」گļ٩╝άֱﻮﻒח▕ﮒ░ﺞ—｢зВ╬پ·ﺙ―ﻞ⌠●‎¶ŹﻟĪ˙ϋ≤ﻐŰŕﻘ‰ﺥﾁﾏΙ┘ďä▄ﾐ∞џ▌ְţ

### `udat2dictkeys.py`

This confusingly-named file finds and parses `.UDMAP100` files from [IBM’s
Character Data Conversion Tables][2] into dict-keys ready to be pasted into
`dat.py`. Just read the `./udat2dictkeys.py -h` help if you need to use it.

### `esc.py`

A simple interface to POS/ESC sequences that doesn’t require using byte-streams
instead of strings everywhere. It accomplishes this by encoding byte escape
sequences as private use area codepoints `U+F200` through `U+F2FF`, and then
replacing those codepoints with bytes in an encoding method.

Or that’s the idea, at least. Implementation coming soon!

[1]: https://github.com/9999years/test-encoding
[2]: https://www.ibm.com/developerworks/views/java/downloads.jsp?s&search_by=Character+Data+Conversion+Tables&type_by=All+Types
