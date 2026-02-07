# CREATOR 
# GitHub https://github.com/cppandpython
# NAME: Vladislav 
# SURNAME: Khudash  
# AGE: 17

# DATE: 07.02.2026
# APP: PYTHON_OBFUSCATOR
# TYPE: OBFUSCATOR
# VERSION: LATEST
# PLATFORM: ANY


from sys import argv, version_info
from string import ascii_letters
from secrets import choice, randbelow, token_bytes
from pickle import dumps as pickle
from base64 import b85encode as base64
from zlib import compress as zlib
from lzma import compress as lzma, FILTER_LZMA1, FORMAT_RAW
from codecs import encode as codecs
from os.path import isfile, split as splitp, join as joinp


BASE = (bin, oct, hex)
ENCODING = 'UTF-8'


class _start: ...
def main(_): ...


MODULE = (
    '{}={};'
    'from builtins import enumerate as {},globals as {},exec as {},compile as {},__import__ as {},ord as {},chr as {},getattr as {};'
    '{}=[{{{}:{}(int,{})({}[{}:{}],{}),{}:{}[{}],{}:{}[{}],{}:{}[{}]}}];{}[{}][{}]={};'
    '_=...;'
    'from sys import exit as {},gettrace as {};'
    '{}=lambda {}:{}({}({}),{})({},{},None,{});'
    '{}().pop({})'
)

INITPYC = '''
def {}():
    {}={}({}({}({}),{})({}().get({}),{}),{})({});{}={};{}={}({}({}),{})()
    for({},{})in({}({})):{}={}({});{}({},{})({}({}^(({}+{}+{})&{})));{}=({}^{})&{}
    {}().pop({}),{}().pop({}),{}().pop({});return({}({}({},{})(),{},{},{},True))
{}({}()if((({}())is(None))and({}().get({})=={})and({}().get({})is(...)))else({})),{}(0)
'''

FILTERS = [{
    'id': FILTER_LZMA1,
    'dict_size': 16777216,   
    'lc': 3,
    'lp': 0,
    'pb': 2
}]


def chr_str(s, d=False):
    return (
        BASE[randbelow(3)](s) if d 
        else '+'.join(f'__builtins__.chr({BASE[randbelow(3)](ord(n))})' for n in s)
    )


def name():
    return f'_{("".join(choice(ascii_letters) for _ in range(5 + randbelow(6))))}_'


def enc(s, key):
    r = []

    f = key[0]

    for (i, n) in enumerate(s):
        x = ord(n) ^ ((key[1] + f + i) & 0xFF)
        f = (f ^ x) & 0xFF
        r.append(chr(x))

    return ''.join(r)


def obfuscate(p):
    opath = splitp(p)
    oname = joinp(opath[0], 'obfuscated-' + opath[-1])

    KEY = tuple(token_bytes(2))

    with open(p, 'r', encoding=ENCODING) as f:
        enc_code = enc(f.read(), KEY)
    
    _enumerate = name()
    _globals = name()
    _exec = name()
    _compile = name()
    _import = name()
    _ord = name()
    _chr = name() 
    _getattr = name()
    _exit = name()
    _debug = name()
    _c = name()
    _pyc = name()
    _init = name()
    _s = name()
    _f = name()
    _r = name()
    _i = name()
    _n = name()
    _x = name()
    _filter_bytes = name()
    _filter = name()
    _lzma = name()

    _module = base64(MODULE.format(
        _filter_bytes, 
        b'\x00\x00\x00\x01\x03\x00\x02',
        _enumerate, 
        _globals, 
        _exec, 
        _compile,
        _import, 
        _ord,
        _chr,
        _getattr, 
        _filter,
        chr_str('dict_size'), 
        _getattr,
        chr_str('from_bytes'),
        _filter_bytes, 
        chr_str(0, d=True), 
        chr_str(4, d=True), 
        chr_str('little'),
        chr_str('lc'), 
        _filter_bytes, 
        chr_str(4, d=True),
        chr_str('lp'), 
        _filter_bytes, 
        chr_str(5, d=True),
        chr_str('pb'), 
        _filter_bytes, 
        chr_str(6, d=True),
        _filter, 
        chr_str(0, d=True), 
        chr_str('id'), 
        chr_str(FILTER_LZMA1, d=True),
        _exit, 
        _debug,
        _lzma, 
        _c,
        _getattr,
        _import,
        chr_str('lzma'),
        chr_str('decompress'),
        _c,
        chr_str(FORMAT_RAW, d=True), 
        _filter,
        _globals,
        chr_str('main')
    ).encode(ENCODING))

    _dec = codecs(INITPYC.format(
        _init, 
        _s,
        _getattr,
        _getattr, 
        _import, 
        chr_str('zlib'), 
        chr_str('decompress'), 
        _globals, 
        chr_str(_pyc), 
        chr_str(-15, d=True), 
        chr_str('decode'),
        chr_str(ENCODING), 
        _f,
        chr_str(KEY[0], d=True), 
        _r,
        _getattr,
        _import,
        chr_str('io'),
        chr_str('StringIO'),
        _i,
        _n,
        _enumerate, 
        _s,
        _x,
        _ord,
        _n,
        _getattr,
        _r,
        chr_str('write'),
        _chr,
        _x,
        chr_str(KEY[1], d=True),
        _f,
        _i,
        chr_str(0xFF, d=True),
        _f,
        _f,
        _x,
        chr_str(0xFF, d=True),
        _globals,
        chr_str(_pyc),
        _globals,
        chr_str(_filter_bytes),
        _globals,
        chr_str(_filter),
        _compile, 
        _getattr,
        _r,
        chr_str('getvalue'),
        chr_str('<...>'), 
        chr_str('exec'),
        chr_str(0, d=True),
        _exec,
        _init,
        _debug,
        _globals,
        chr_str('__name__'),
        chr_str('__main__'),
        _globals,
        chr_str('_'),
        chr_str('...'),
        _exit
    ).encode(ENCODING), 'uu')

    payload = (
        f'{_pyc}={zlib(enc_code.encode(ENCODING), wbits=-15, level=9)};'
        f'{_exec}({_getattr}({_import}({chr_str("codecs")}),{chr_str("decode")})({_dec},{chr_str("uu")})),'
        '_start()'
    ).encode(ENCODING)

    packed = lzma(
        payload,
        format=FORMAT_RAW,
        filters=FILTERS
    )

    _start.__reduce__ = lambda _: (main, (_module,))
    _main = f'main=lambda _:__builtins__.getattr(__builtins__,{chr_str("exec")})(__builtins__.getattr(__builtins__.getattr(__builtins__,{chr_str("__import__")})({chr_str("base64")}),{chr_str("b85decode")})(_),__builtins__.getattr(__builtins__,{chr_str("globals")})())'.encode(ENCODING).hex()


    with open(oname, 'w', encoding=ENCODING) as f:
        f.write((
f'__builtins__.getattr(__builtins__,{chr_str("exec")})(__builtins__.getattr(__builtins__.getattr(__builtins__,{chr_str("bytes")}),{chr_str("fromhex")})(\'{_main}\')),'
f'__builtins__.getattr(__builtins__.getattr(__builtins__.getattr(__builtins__,{chr_str("globals")})().get({chr_str("__builtins__")}),{chr_str("__import__")})({chr_str("pickle")}),{chr_str("loads")})({pickle(_start())}),'
f'{_exec}({_lzma}({packed}))\n'
'if(__name__==\'__main__\'):main()'
        ))


    print(f'obfuscated ({p}) created ({oname})')
    

def start():
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


if __name__ == '__main__': start()