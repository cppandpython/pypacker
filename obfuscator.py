# CREATOR 
# GitHub https://github.com/cppandpython
# NAME: Vladislav 
# SURNAME: Khudash  
# AGE: 17

# DATE: 05.01.2026
# APP: OBFUSCATOR_PYTHON
# TYPE: OBFUSCATOR
# VERSION: LATEST
# PLATFORM: ANY


from sys import argv, version_info
from os.path import isfile, split as splitp, join as joinp
from locale import getencoding
from secrets import randbelow, token_bytes
from lzma import compress as lzma, FORMAT_XZ, CHECK_CRC64, PRESET_EXTREME
from codecs import encode as codecs
from zlib import compress as zlib


ENCODING = getencoding()


INIT_PYC = '''
def _INIT_PYC():
    s,r,f=__import__({}).decompress(_PYC).decode({}),[],{}
    for(i,n)in(enumerate(s)):x=ord(n);r.append(chr(x^(({}+f+i)&0xFF)));f=(f^x)&0xFF
    if(__name__=={}):exec(''.join(r))
    exit(0)
'''


def chr_str(s):
    base = [bin, oct, hex]
    
    return '+'.join(f'chr({base[randbelow(3)](ord(n))})' for n in s)


def enc(s):
    r = []

    f = KEY[0]

    for (i, n) in enumerate(s):
        x = ord(n) ^ ((KEY[1] + f + i) & 0xFF)
        f = (f ^ x) & 0xFF
        r.append(str(chr(x)))

    return ''.join(r)


def obfuscate(p):
    global KEY

    opath = splitp(p)
    oname = joinp(opath[0], 'obfuscated-' + opath[-1])

    if isfile(oname):
        print(f'obfuscated ({p})')
        return

    KEY = tuple(token_bytes(2))

    with open(p, 'r', encoding=ENCODING) as f:
        enc_code = enc(f.read())

    dec = codecs(INIT_PYC.format(
        chr_str('zlib'),
        chr_str(ENCODING), 
        oct(KEY[0]), 
        bin(KEY[1]),
        chr_str('__main__')
    ).encode(ENCODING), 'uu')

    payload = (
        f'_PYC={zlib(enc_code.encode(ENCODING), level=9)};'
        f'exec(__import__({chr_str("codecs")}).decode({dec},{chr_str("uu")}));'
        f'_INIT_PYC()'
    ).encode(ENCODING)

    packed = lzma(
        payload,
        format=FORMAT_XZ,
        check=CHECK_CRC64,
        preset=9 | PRESET_EXTREME
    )

    with open(oname, 'w', encoding=ENCODING) as f:
        f.write(f'exec(__import__({chr_str("lzma")}).decompress({packed}))')

    print(f'obfuscated ({p}) created ({oname})')
    

if len(argv) > 1: 
    for fp in argv[1:]: 
        if isfile(fp):
            try:
                obfuscate(fp)
            except:
                print(f'unobfuscated ({fp})')
        else:
            print(f'({fp}) is not file')
else:
    print(f'python{version_info.major} {splitp(argv[0])[-1]} (path)  —  Obfuscate Python file')
