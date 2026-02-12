# CREATOR 
# GitHub https://github.com/cppandpython
# NAME: Vladislav 
# SURNAME: Khudash  
# AGE: 17

# DATE: 12.02.2026
# APP: PYTHON_OBFUSCATOR
# TYPE: OBFUSCATOR
# VERSION: LATEST
# PLATFORM: ANY




from sys import argv, version_info
from os.path import isfile, split as splitp, join as joinp
from mmap import mmap, ACCESS_READ
from secrets import choice, randbelow, token_bytes
from pickle import dumps as pickle
from base64 import b85encode as base64
from codecs import encode as codecs
from zlib import compress as zlib
from lzma import compress as lzma, FILTER_LZMA1, FORMAT_RAW


BASE = (bin, oct, hex)

ENCODING = 'UTF-8'

MODULE = (
    '{}={};'
    'from builtins import enumerate as {},globals as {},exec as {},compile as {},__import__ as {},getattr as {},int as {};'
    '{}=[{{{}:{}({},{})({}[{}:{}],{}),{}:{}[{}],{}:{}[{}],{}:{}[{}]}}];{}[{}][{}]={};'
    '_=...;'
    'from sys import exit as {},gettrace as {};'
    'from operator import add as {},and_ as {},xor as {},is_ as {},eq as {};'
    '{}=lambda {}:{}({}({}),{})({},{},None,{});'
    '{}().pop({})'
)

INITPYC = '''def {}():
 {}={}({}({}),{})({}().get({}),{});{}={};{}={}({}({}),{})()
 for({},{})in({}({})):{}={};{}({},{})({}({},{})({}({},{}({}({},{}({},{})),{}))));{}={}({}({},{}),{})
 {}().pop({}),{}().pop({}),{}().pop({});return({}({}({},{})(),{},{},{},True))
{}({}()if(({}({}(),None))and({}({}().get({}),{}))and({}({}().get({}),...)))else({})),{}({}),__bootstrap({})'''

FILTERS = [{
    'id': FILTER_LZMA1,
    'dict_size': 16777216,   
    'lc': 3,
    'lp': 0,
    'pb': 2
}]


_start = type('...', (object,), {})
def main(_): ...


def chr_str(s, d=False):
    return (
        BASE[randbelow(3)](s) if d 
        else '+'.join(f'__builtins__.chr({BASE[randbelow(3)](ord(n))})' for n in s)
    )


def name():
    return ''.join(choice('_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(20 + randbelow(21)))


def enc(handler, key):
    k0, k1 = key

    with mmap(handler, 0, access=ACCESS_READ) as mf:
        size = len(mf)

        buf = bytearray(size)
        ptr = memoryview(buf)

        f = k0

        for i in range(size):
            n = mf[i]
            x = n ^ (((k1 + f) + i) & 0xFF)
            f = (f ^ x) & 0xFF
            ptr[i] = x

    return ptr


def obfuscate(p):
    opath = splitp(p)
    oname = joinp(opath[0], 'obfuscated-' + opath[-1])

    KEY = tuple(token_bytes(2))

    with open(p, 'rb') as f:
        enc_code = enc(f.fileno(), KEY)

    _enumerate = name()
    _globals = name()
    _exec = name()
    _compile = name()
    _import = name()
    _getattr = name()
    _int = name()
    _exit = name()
    _debug = name()
    _add = name()
    _and = name()
    _xor = name()
    _is = name()
    _eq = name()
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
        _getattr, 
        _int,
        _filter,
        chr_str('dict_size'), 
        _getattr,
        _int,
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
        _add,
        _and,
        _xor,
        _is,
        _eq,
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
        _import, 
        chr_str('zlib'), 
        chr_str('decompress'), 
        _globals, 
        chr_str(_pyc), 
        chr_str(-15, d=True), 
        _f,
        chr_str(KEY[0], d=True), 
        _r,
        _getattr,
        _import,
        chr_str('io'),
        chr_str('BytesIO'),
        _i,
        _n,
        _enumerate, 
        _s,
        _x,
        _n,
        _getattr,
        _r,
        chr_str('write'),
        _getattr,
        _int,
        chr_str('to_bytes'),
        _xor,
        _x,
        _and,
        _add,
        chr_str(KEY[1], d=True),
        _add,
        _f,
        _i,
        chr_str(0xFF, d=True),
        _f,
        _and,
        _xor,
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
        chr_str('getbuffer'),
        chr_str('<...>'), 
        chr_str('exec'),
        chr_str(0, d=True),
        _exec,
        _init,
        _is,
        _debug,
        _eq,
        _globals,
        chr_str('__name__'),
        chr_str('__main__'),
        _is,
        _globals,
        chr_str('_'),
        chr_str('...'),
        _exit,
        chr_str(0, d=True),
        _pyc
    ).encode(ENCODING), 'uu')

    payload = (
        f'{_pyc}={zlib(enc_code, wbits=-15, level=9)};'
        f'{_exec}({_getattr}({_import}({chr_str("codecs")}),{chr_str("decode")})({_dec},{chr_str("uu")})),'
        '_start(main)'
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
                except BaseException as error:
                    print(f'unobfuscated ({fp})\n\n{type(error).__name__}({error})')
            else:
                print(f'({fp}) is not file')
    else:
        print(f'python{version_info.major} {splitp(argv[0])[-1]} (path)  —  Obfuscate Python file')


if __name__ == '__main__': start()