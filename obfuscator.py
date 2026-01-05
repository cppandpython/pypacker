# CREATOR 
# GitHub https://github.com/cppandpython
# NAME: Vladislav 
# SURNAME: Khudash  
# AGE: 17

# DATE: 06.01.2026
# APP: OBFUSCATOR_PYTHON
# TYPE: OBFUSCATOR
# VERSION: LATEST
# PLATFORM: ANY


from string import ascii_letters
from sys import argv, version_info
from os.path import isfile, split as splitp, join as joinp
from locale import getencoding
from secrets import choice, randbelow, token_bytes
from lzma import compress as lzma, FORMAT_XZ, CHECK_CRC64, PRESET_EXTREME
from codecs import encode as codecs
from zlib import compress as zlib


BASE = (bin, oct, hex)
ENCODING = getencoding()


INITPYC = '''
def {}():
    if({}({}).gettrace())is not(None):{}(0)
    s,r,f={}({}).decompress({}().pop({})).decode({}),[],{}
    for(i,n)in(enumerate(s)):x=ord(n);r.append(chr(x^(({}+f+i)&0xFF)));f=(f^x)&0xFF
    return('')if(__name__!={})else({}(''.join(r),'<...>','exec',dont_inherit=True))
{}({}()),{}(0)
'''


def chr_str(s):
    return '+'.join(f'chr({BASE[randbelow(3)](ord(n))})' for n in s)


def name():
    return ''.join(choice(ascii_letters) for _ in range(5 + randbelow(6)))


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

    KEY = tuple(token_bytes(2))

    with open(p, 'r', encoding=ENCODING) as f:
        enc_code = enc(f.read())

    _pyc = name()
    _init = name()
    _exit = name()
    _globals = name()
    _exec = name()
    _compile = name()
    _import = name()

    dec = codecs(INITPYC.format(
        _init,
        _import,
        chr_str('sys'),
        _exit,
        _import,
        chr_str('zlib'),
        _globals, 
        chr_str(_pyc),
        chr_str(ENCODING), 
        oct(KEY[0]), 
        bin(KEY[1]),
        chr_str('__main__'),
        _compile,
        _exec,
        _init,
        _exit
    ).encode(ENCODING), 'uu')

    payload = (
        f'{_pyc}={zlib(enc_code.encode(ENCODING), level=9)};'
        f'from builtins import globals as {_globals},exec as {_exec},compile as {_compile},__import__ as {_import};from os import _exit as {_exit};'
        f'{_exec}({_import}({chr_str("codecs")}).decode({dec},{chr_str("uu")}))'
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
    

def main():
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


if __name__ == '__main__': main()
