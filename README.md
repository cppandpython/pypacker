# 🌟 PYPACKER 


<p align="center">
  <img src="https://img.shields.io/badge/Platform-Cross--Platform-blue?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/Language-Python-yellow?style=for-the-badge&logo=python" alt="Language">
  <img src="https://img.shields.io/badge/Type-Obfuscator-red?style=for-the-badge" alt="Type">
  <img src="https://img.shields.io/badge/Layers-5+-orange?style=for-the-badge" alt="Layers">
</p>

## 📖 **Table of Contents / Содержание**

- [English Version](#en)
- [Русская версия](#ru)

---

<a name="en"></a>
# EN | **PYTHON_PACKER - Python Code Obfuscator**

> **⚠️ WARNING: This tool is designed for intellectual property protection and educational purposes. Use responsibly and in accordance with applicable laws.**

---

## 🎯 **What is PYTHON_PACKER?**

**PYTHON_PACKER** is an advanced Python script obfuscator that transforms source code into a heavily obfuscated, self-contained form using multiple layers of encryption, compression, and dynamic code generation. The output is a single Python file that, when executed, dynamically reconstructs and runs the original code through a series of runtime decryption and decompression stages.

Unlike simple obfuscators that just rename variables, PYTHON_PACKER employs cryptographic transformations, multi-stage payload delivery, and runtime code generation that makes static analysis and reverse engineering extremely difficult.

---

## 🚀 **Key Features**

| Category | Features |
|:---|:---|
| **🔐 Multi-Layer Encryption** | XOR encryption with dynamic 2-byte keys<br>ROT-13 style encryption with variable shift<br>Base85 encoding for module stubs<br>Custom rolling XOR with state variable |
| **🗜️ Compression Stack** | gzip (level 9) for initial code<br>zlib (level 9) for payload wrapper<br>LZMA (RAW format) with custom filters (16MB dict) |
| **🎭 String Obfuscation** | Dynamic `chr()` chain generation (3 variants)<br>XOR-encrypted strings with per-character keys<br>Binary/octal/hex number representations<br>f-string based string construction |
| **🔄 Dynamic Generation** | Random 20-50 character variable/function names<br>Constant generation via 20+ complex logical expressions<br>Fake placeholder objects with `__reduce__` hook<br>Runtime code patching via `__code__.replace()` |
| **📦 Single-File Packaging** | Self-contained script with `packed-` prefix<br>All dependencies embedded in code<br>No external files required after packing |
| **🧩 Anti-Analysis** | Obfuscation via `__reduce__` pickling<br>Builtins function aliasing and indirection<br>Complex `type()` and `lambda` constructs<br>Self-modifying code constants |
| **🎯 Constant Obfuscation** | `None` → 20+ variants of complex expressions<br>`True` → 20+ variants of math/logic expressions<br>`Ellipsis` → 20+ variants of obfuscated references<br>Numbers → bin/oct/hex with random basis selection |
| **🛡️ Runtime Protection** | Memory-only execution (no disk trace)<br>Process masquerading via `__reduce__`<br>Encrypted module loader |

---

## 📊 **Architecture Overview**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         PYTHON_PACKER ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │                         SOURCE CODE (input.py)                              ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  STAGE 1: XOR ENCRYPTION                                                    ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Algorithm: Rolling XOR with dynamic 2-byte key                      │   ││
│  │  │ Key: (k0, k1) where k0 ∈ [1,8], k1 ∈ [1,256] from token_bytes(2)    │   ││
│  │  │ State: f = k0, updated per byte: f = (f ^ x) & 0xFF                 │   ││
│  │  │ Formula: x = n ^ (((k1 + f) + i) & 0xFF)                            │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  STAGE 2: GZIP COMPRESSION (level 9)                                        ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Compress encrypted code with maximum compression                    │   ││
│  │  │ Output: 10-byte signature + compressed body                         │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  STAGE 3: STRING OBFUSCATION & CODE GENERATION                             ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ - Generate 20-50 char random names for all functions/variables     │   ││
│  │  │ - Transform strings to:                                             │   ││
│  │  │   • chr() chains: "text" → chr(116)+chr(101)+chr(120)+chr(116)     │   ││
│  │  │   • XOR strings: "\x1a\x2b..." with custom decoder                  │   ││
│  │  │ - Replace constants with complex expressions from NONE/TRUE/ELLIPSIS│   ││
│  │  │ - Create 5-layer decoder functions with random names                │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  STAGE 4: ROT ENCRYPTION & LZMA COMPRESSION                                ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ ROT_ENCODE: (byte + ROT_KEY) ^ (0x55 + index) & 0xFF                │   ││
│  │  │ LZMA: RAW format with custom filter (dict_size=16MB, lc=4, lp=0, pb=2)│ ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  STAGE 5: LOADER GENERATION                                                ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Create obfuscated loader using type() with special methods:         │   ││
│  │  │ __or__ → exec() interceptor                                         │   ││
│  │  │ __add__ → eval() string generator                                   │   ││
│  │  │ __floordiv__ → import zlib                                          │   ││
│  │  │ __lshift__ → set chr function                                       │   ││
│  │  │ __init__ → decompress and execute payload                           │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  FINAL OUTPUT: packed-input.py                                              ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Single file containing:                                              │   ││
│  │  │ • Obfuscated type-based loader (~100 lines)                         │   ││
│  │  │ • Embedded zlib-compressed decoder                                  │   ││
│  │  │ • LZMA-compressed encrypted payload                                 │   ││
│  │  │ • All strings obfuscated with chr() chains                          │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 **Runtime Execution Flow**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    RUNTIME EXECUTION FLOW (packed script)                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  LAYER 0: OBFUSCATED LOADER                                                ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Creates a custom type via: type("...", (object,), {                 │   ││
│  │  │     "__slots__": (),                                                 │   ││
│  │  │     "__or__": lambda __,_: exec(_, globals()),                       │   ││
│  │  │     "__add__": lambda _,__: eval("lambda _:...".join(chr(...))),    │   ││
│  │  │     "__floordiv__": lambda _,__: __import__("zlib"),                │   ││
│  │  │     "__init__": lambda __,_: decompress_and_execute(_)              │   ││
│  │  │ })                                                                   │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  │  Instantiate and call with packed data                                     ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  LAYER 1: ZLIB DECOMPRESSION                                                ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ __init__ method calls __floordiv__ to get zlib module               │   ││
│  │  │ Decompress packed_1 with zlib.decompress(wbits=-15)                 │   ││
│  │  │ Result: Python code containing LAYER 2                              │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  LAYER 2: DYNAMIC FUNCTION CREATION                                         ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ __add__ generates string-to-chr function via eval()                 │   ││
│  │  │ __lshift__ sets custom chr function for string decoding             │   ││
│  │  │ __rshift__ sets global variable with Ellipsis                       │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  LAYER 3: ROT DECRYPTION & DECODER EXECUTION                               ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ ROT decode the embedded _for loop                                   │   ││
│  │  │ Execute the decoder function that:                                   │   ││
│  │  │   - Imports gzip and decompresses _enc_code_body                    │   ││
│  │  │   - Creates BytesIO from decompressed data                          │   ││
│  │  │   - Uses marshal.loads() to load code object                        │   ││
│  │  │   - Executes the code object                                        │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  LAYER 4: XOR DECRYPTION & LZMA DECOMPRESSION                              ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Load LZMA module with custom filter from _filter_bytes              │   ││
│  │  │ Decompress packed_2 with LZMA decompressor                          │   ││
│  │  │ XOR decrypt using key derived from _enc_code_signature              │   ││
│  │  │ Result: Payload containing original code construction               │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  LAYER 5: ORIGINAL CODE CONSTRUCTION & EXECUTION                           ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Payload contains:                                                    │   ││
│  │  │   - _getattr(_globals(), "__setitem__")(_pyc, _enc_code_body)      │   ││
│  │  │   - exec(_decoded_module, globals())                                │   ││
│  │  │   - _start(main) where _start has __reduce__ hook                  │   ││
│  │  │ __reduce__ returns (main, (_module,)) → executes original code      │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  ORIGINAL CODE EXECUTION                                                    ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Original script runs with all functionality intact                  │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 **Technical Details**

### 1. XOR Encryption Algorithm

```python
def encrypt(data):
    k0, k1 = KEY  # k0 ∈ [1,8], k1 ∈ [1,256]
    f = k0        # Initial state
    result = []
    
    for i, c in enumerate(data):
        n = ord(c)
        # XOR with rolling key derived from k1, state, and index
        x = (n << k0) ^ (((k1 + f) + i) & 0xFF)
        f = (f ^ x) & 0xFF  # Update state
        result.append(chr(x))
    
    return ''.join(result)
```

**Key Properties:**
- Each byte affects all subsequent bytes (rolling state)
- Key is derived from `token_bytes(2)` at packing time
- Key is not stored directly, embedded in encrypted form
- Decryption uses inverse operation: `(x ^ (((k1 + f) + i) & 0xFF)) >> k0`

### 2. ROT Encryption Algorithm

```python
def rot_enc(s, k):
    return bytes(((n + k) ^ (0x55 + i)) & 0xFF for i, n in enumerate(s))
```

Used specifically for the `INITPYC_FOR` code block that handles the initial decoder setup.

### 3. LZMA Compression Configuration

```python
LZMA_FILTER = [{
    'id': FILTER_LZMA1,
    'dict_size': 16_777_216,   # 16MB dictionary for maximum compression
    'lc': 4,                    # Literal context bits
    'lp': 0,                    # Literal position bits  
    'pb': 2                     # Position bits
}]
RAW_LZMA_FILTER = memoryview(
    dict_size.to_bytes(4, 'little') +
    bytes([lc, lp, pb])
)
```

This configuration achieves maximum compression ratio for Python code at the cost of slower decompression.

### 4. String Obfuscation Methods

| Method | Output Example |
|:---|:---|
| **chr() Chain** | `chr(116)+chr(101)+chr(120)+chr(116)` |
| **XOR String** | `_chr_func("\x1a\x2b\x3c...")` |
| **f-string with %** | `f"{chr(37)}{chr(115)}"*4%(...)` |
| **Binary/Octal/Hex** | `0b1110100`, `0o164`, `0x74` |

### 5. Constant Obfuscation

**None Variants (20+):**
```python
# Examples:
((None)and((lambda:None)())and(([]or(None))))
([].append(0)or(None))
(((0)if(False)else(None))and((lambda x=None:x)()))
(not(0==1)and(not((None)is not(None)))and([0]and(None)))
(({None}and(None))and(sum([])or(None)))
```

**True Variants (20+):**
```python
# Examples:
((1<<0==1)and(2**0==1)and(3%2==1)and(10//10==1))
((lambda x:x^x)(42)==0)and((ord('B')-ord('A'))==1)
((3//3==1)and(bool([1])==True)and(bool([])==False))
((5^2==7)and(4>>2<2)and(1<<1>>1==1))
```

**Ellipsis Variants (20+):**
```python
# Examples:
((lambda x:(x)if(x)is(None)else(...))(...))
((([].append(0)or{1})and((...)or(2%2==0))))
((((0)if(False)else(...))and(lambda y:(y)or(...))(None)))
((not([]or{})and((...)not in({...})))or((lambda:...)()))
```

### 6. Name Generation

```python
def name():
    alphabet = ALPHABET.replace('0123456789', '')
    return choice(alphabet) + ''.join(choice(ALPHABET) for _ in range(19 + randbelow(31)))
```

- First character: non-digit (prevents numeric names)
- Length: 20-50 characters
- Alphabet: 100+ characters including Cyrillic and special letters
- Result: Cryptic names like `_абвгдеёжзийклмнопрстуфхцчшщъыьэюя`

### 7. Type-Based Loader

The final loader uses Python's `type()` to create a dynamic class with special methods:

```python
__builtins__.getattr(__builtins__.getattr(__builtins__.getattr(__builtins__, "type"),
    "__getattribute__")(__builtins__.getattr(__builtins__, "type"), "__new__")(
    __builtins__.getattr(__builtins__, "type"), "...", 
    (__builtins__.getattr(__builtins__, "object"),), {
        "__slots__": (),
        "__or__": lambda __,_: __builtins__.getattr(__builtins__, "exec")(_, ...),
        "__add__": lambda _,__: __builtins__.getattr(__builtins__, "eval")(...),
        "__floordiv__": lambda _,__: __builtins__.getattr(__builtins__, "__import__")("zlib"),
        "__lshift__": lambda _,__: __builtins__.getattr(globals(), "__setitem__")(...),
        "__init__": lambda __,_: ...  # Decompression and execution
    })
```

### 8. Module Stub (Base85 Encoded)

The `MODULE` constant contains the core decoder logic encoded in Base85:

```python
MODULE = (
    '{}=__builtins__.getattr(__builtins__.getattr(__builtins__,{}),{})(__builtins__.getattr(__builtins__,{}),{});'
    'from builtins import bytes as {}, enumerate as {},globals as {},exec as {},compile as {},__import__ as {},getattr as {},int as {};'
    # ... more obfuscated module loading code
)
```

This is Base85 encoded and then `uu` encoded in the final output.

---

## ⚙️ **Configuration Parameters**

| Parameter | Value | Description |
|:---|:---|:---|
| `ENCODING` | `'UTF-8'` | String encoding for all operations |
| `ALPHABET` | 100+ chars | Alphabet for name generation (includes Cyrillic) |
| `BASIS` | `(bin, oct, hex)` | Number systems for constant obfuscation |
| `KEY` | 2 random bytes | XOR encryption key (k0=1-8, k1=1-256) |
| `CHR_KEY` | (1-6, 0-255) | XOR key for string obfuscation |
| `ROT_KEY` | 0-255 | ROT encryption key for _for loop |
| `LZMA_FILTER` | dict_size=16MB, lc=4, lp=0, pb=2 | LZMA compression settings |
| `RAW_LZMA_FILTER` | 6-byte header | Filter parameters for LZMA decompression |
| `NONE` | 20+ expressions | Randomly selected for `None` obfuscation |
| `TRUE` | 20+ expressions | Randomly selected for `True` obfuscation |
| `ELLIPSIS` | 20+ expressions | Randomly selected for `Ellipsis` obfuscation |
| `gzip level` | 9 | Maximum compression |
| `zlib wbits` | -15 | Raw deflate (no header) |
| `zlib level` | 9 | Maximum compression |

---

## 📁 **File Structure**

```
python_packer/
├── packer.py              # Main executable (500+ lines)
│   ├── pypack()          # Core packing function
│   ├── enc()             # XOR encryption with rolling state
│   ├── rot_enc()         # ROT-13 style encryption
│   ├── _chr_str()        # String obfuscation generator
│   └── name()            # Random name generator (20-50 chars)
│
├── README.md             # This file
│
└── Output: packed-input.py
    ├── Type-based loader (dynamic class with special methods)
    │   ├── __slots__ = ()
    │   ├── __or__ → exec() interceptor
    │   ├── __add__ → eval() string generator  
    │   ├── __floordiv__ → import zlib
    │   ├── __lshift__ → set chr function
    │   ├── __rshift__ → set global variable
    │   └── __init__ → decompression & execution
    │
    ├── Embedded Layer 1 (zlib compressed)
    │   └── Rot-encoded decoder function
    │
    ├── Embedded Layer 2 (LZMA compressed)
    │   └── XOR-encrypted payload
    │
    └── Obfuscated constants (None, True, Ellipsis variants)
```

---

## 🔬 **Anti-Analysis Techniques**

| Technique | Description |
|:---|:---|
| **No Direct Strings** | All strings are generated at runtime via `chr()` chains or XOR decryption |
| **No Direct Imports** | Imports use `__import__` via `getattr` indirection |
| **No Fixed Names** | All function/variable names are randomly generated (20-50 chars) |
| **Multi-Layer Compression** | 5+ layers of compression/encryption must be unwound |
| **Runtime Code Patching** | Uses `__code__.replace()` to modify function constants |
| **Pickle Reduction** | `__reduce__` hook executes code without explicit call |
| **Type Metaprogramming** | Dynamic class creation with special methods |
| **Constant Obfuscation** | All constants replaced with complex logical expressions |
| **Self-Modifying Code** | Code constants are patched at runtime |
| **Memory-Only Execution** | Original code never written to disk |

---

## 🧰 **Usage**

### Basic Usage
```bash
python packer.py script.py
# Creates: packed-script.py
```

### Pack Multiple Files
```bash
python packer.py script1.py script2.py script3.py
```

### Help
```bash
python packer.py
# Output: python3 packer.py (path)  —  Pack Python file
```

---

## 📊 **Performance Characteristics**

| Metric | Value |
|:---|:---|
| **Input Size** | Any (tested up to 10MB) |
| **Output Size** | ~100x source size (due to obfuscation) |
| **Packing Time** | ~1-3 seconds per MB |
| **Runtime Overhead** | ~0.5-2 seconds for decompression |
| **Memory Usage** | ~3x original file size during execution |
| **Python Version** | 3.6+ required (uses f-strings, type hints) |

---

## ⚠️ **WARNING**

> **THIS TOOL PRODUCES HIGHLY OBFUSCATED CODE!**

- 📦 **Size increase** — output can be 50-100x larger than source (200KB → 20MB)
- 🐌 **Execution slowdown** — due to multi-layer unpacking (adds 0.5-2 seconds)
- 🐍 **Python 3.6+ required** — uses f-strings, type hints, and other modern features
- 🔧 **Not for production** — intended for protection of sensitive code, not for regular distribution
- ⚖️ **Legal compliance** — check reverse engineering laws in your jurisdiction

**THE AUTHOR TAKES NO RESPONSIBILITY FOR MISUSE OF THIS SOFTWARE.**

---

## 👤 **Author**

**Vladislav Khudash**
- GitHub: [@cppandpython](https://github.com/cppandpython)
- Age: 17

---

## ⭐ **Support**

If you found this project interesting, give it a star on GitHub!

---

<a name="ru"></a>
# RU | **PYTHON_PACKER - Обфускатор Python-кода**

> **⚠️ ПРЕДУПРЕЖДЕНИЕ: Этот инструмент предназначен для защиты интеллектуальной собственности и образовательных целей. Используйте ответственно и в соответствии с законодательством.**

---

## 🎯 **Что такое PYTHON_PACKER?**

**PYTHON_PACKER** — это продвинутый инструмент для обфускации Python-скриптов, который преобразует исходный код в сильно запутанную, самодостаточную форму с использованием нескольких слоев шифрования, сжатия и динамической генерации кода. Результат — один Python-файл, который при выполнении динамически восстанавливает и запускает исходный код через серию этапов дешифрования и распаковки.

В отличие от простых обфускаторов, которые только переименовывают переменные, PYTHON_PACKER использует криптографические преобразования, многоступенчатую доставку полезной нагрузки и генерацию кода во время выполнения, что делает статический анализ и обратную разработку крайне сложными.

---

## 🚀 **Основные возможности**

| Категория | Возможности |
|:---|:---|
| **🔐 Многослойное шифрование** | XOR шифрование с динамическим 2-байтным ключом<br>ROT-13 шифрование с переменным сдвигом<br>Base85 кодирование для заглушек модулей<br>Кастомное XOR с состоянием |
| **🗜️ Стек сжатия** | gzip (level 9) для начального кода<br>zlib (level 9) для обертки полезной нагрузки<br>LZMA (RAW формат) с кастомными фильтрами (16MB словарь) |
| **🎭 Обфускация строк** | Динамические цепочки `chr()` (3 варианта)<br>XOR-зашифрованные строки с посимвольными ключами<br>Бинарное/восьмеричное/шестнадцатеричное представление чисел<br>Конструкция строк через f-строки |
| **🔄 Динамическая генерация** | Случайные имена переменных и функций (20-50 символов)<br>Генерация констант через 20+ сложных логических выражений<br>Фейковые объекты-заглушки с хуком `__reduce__`<br>Патчинг кода во время выполнения через `__code__.replace()` |
| **📦 Упаковка в один файл** | Самодостаточный скрипт с префиксом `packed-`<br>Все зависимости встроены в код<br>Не требует внешних файлов после упаковки |
| **🧩 Анти-анализ** | Обфускация через `__reduce__` pickling<br>Псевдонимы встроенных функций и косвенная адресация<br>Сложные конструкции с `type()` и `lambda`<br>Самомодифицирующийся код |
| **🎯 Обфускация констант** | `None` → 20+ вариантов сложных выражений<br>`True` → 20+ вариантов математических/логических выражений<br>`Ellipsis` → 20+ вариантов обфусцированных ссылок<br>Числа → bin/oct/hex со случайным выбором системы |
| **🛡️ Защита во время выполнения** | Выполнение только из памяти (без следа на диске)<br>Маскировка процесса через `__reduce__`<br>Зашифрованный загрузчик модулей |

---

## 📊 **Архитектура**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         АРХИТЕКТУРА PYTHON_PACKER                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │                         ИСХОДНЫЙ КОД (input.py)                             ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  ЭТАП 1: XOR ШИФРОВАНИЕ                                                    ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Алгоритм: Rolling XOR с динамическим 2-байтным ключом               │   ││
│  │  │ Ключ: (k0, k1) где k0 ∈ [1,8], k1 ∈ [1,256] из token_bytes(2)       │   ││
│  │  │ Состояние: f = k0, обновляется на каждый байт: f = (f ^ x) & 0xFF  │   ││
│  │  │ Формула: x = n ^ (((k1 + f) + i) & 0xFF)                            │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  ЭТАП 2: GZIP СЖАТИЕ (level 9)                                             ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Сжатие зашифрованного кода с максимальным сжатием                   │   ││
│  │  │ Результат: 10-байтовая сигнатура + сжатое тело                      │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  ЭТАП 3: ОБФУСКАЦИЯ СТРОК И ГЕНЕРАЦИЯ КОДА                                 ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ - Генерация случайных имен (20-50 символов) для всех функций/перем.│   ││
│  │  │ - Преобразование строк в:                                           │   ││
│  │  │   • цепочки chr(): "text" → chr(116)+chr(101)+chr(120)+chr(116)     │   ││
│  │  │   • XOR строки: "\x1a\x2b..." с кастомным декодером                 │   ││
│  │  │ - Замена констант сложными выражениями из NONE/TRUE/ELLIPSIS        │   ││
│  │  │ - Создание 5-слойных функций-декодеров со случайными именами        │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  ЭТАП 4: ROT ШИФРОВАНИЕ И LZMA СЖАТИЕ                                      ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ ROT_ENCODE: (байт + ROT_KEY) ^ (0x55 + индекс) & 0xFF               │   ││
│  │  │ LZMA: RAW формат с кастомным фильтром (dict_size=16MB, lc=4, lp=0, pb=2)│ ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  ЭТАП 5: ГЕНЕРАЦИЯ ЗАГРУЗЧИКА                                               ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Создание обфусцированного загрузчика через type() со спецметодами:  │   ││
│  │  │ __or__ → перехватчик exec()                                          │   ││
│  │  │ __add__ → генератор строк через eval()                               │   ││
│  │  │ __floordiv__ → import zlib                                           │   ││
│  │  │ __lshift__ → установка chr функции                                   │   ││
│  │  │ __init__ → распаковка и выполнение полезной нагрузки                 │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  ФИНАЛЬНЫЙ ВЫХОД: packed-input.py                                           ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Один файл содержит:                                                  │   ││
│  │  │ • Обфусцированный загрузчик на type() (~100 строк)                   │   ││
│  │  │ • Встроенный zlib-сжатый декодер                                     │   ││
│  │  │ • LZMA-сжатую зашифрованную полезную нагрузку                       │   ││
│  │  │ • Все строки обфусцированы через цепочки chr()                      │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 **Поток выполнения во время работы**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    ПОТОК ВЫПОЛНЕНИЯ (упакованный скрипт)                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  СЛОЙ 0: ОБФУСЦИРОВАННЫЙ ЗАГРУЗЧИК                                          ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Создание кастомного типа через: type("...", (object,), {           │   ││
│  │  │     "__slots__": (),                                                 │   ││
│  │  │     "__or__": lambda __,_: exec(_, globals()),                       │   ││
│  │  │     "__add__": lambda _,__: eval("lambda _:...".join(chr(...))),    │   ││
│  │  │     "__floordiv__": lambda _,__: __import__("zlib"),                │   ││
│  │  │     "__init__": lambda __,_: decompress_and_execute(_)              │   ││
│  │  │ })                                                                   │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  │  Создание экземпляра и вызов с упакованными данными                        ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  СЛОЙ 1: ZLIB РАСПАКОВКА                                                    ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Метод __init__ вызывает __floordiv__ для получения модуля zlib      │   ││
│  │  │ Распаковка packed_1 с zlib.decompress(wbits=-15)                    │   ││
│  │  │ Результат: Python код, содержащий СЛОЙ 2                            │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  СЛОЙ 2: ДИНАМИЧЕСКОЕ СОЗДАНИЕ ФУНКЦИЙ                                      ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ __add__ генерирует функцию преобразования строк через eval()       │   ││
│  │  │ __lshift__ устанавливает кастомную chr функцию для декодирования   │   ││
│  │  │ __rshift__ устанавливает глобальную переменную с Ellipsis           │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  СЛОЙ 3: ROT ДЕШИФРОВАНИЕ И ВЫПОЛНЕНИЕ ДЕКОДЕРА                            ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ ROT дешифровка встроенного цикла _for                               │   ││
│  │  │ Выполнение функции-декодера, которая:                               │   ││
│  │  │   - Импортирует gzip и распаковывает _enc_code_body                 │   ││
│  │  │   - Создает BytesIO из распакованных данных                         │   ││
│  │  │   - Использует marshal.loads() для загрузки объекта кода            │   ││
│  │  │   - Выполняет объект кода                                            │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  СЛОЙ 4: XOR ДЕШИФРОВАНИЕ И LZMA РАСПАКОВКА                                 ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Загрузка LZMA модуля с кастомным фильтром из _filter_bytes          │   ││
│  │  │ Распаковка packed_2 с LZMA декомпрессором                           │   ││
│  │  │ XOR дешифровка с использованием ключа из _enc_code_signature        │   ││
│  │  │ Результат: Полезная нагрузка, содержащая конструкцию исходного кода │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  СЛОЙ 5: КОНСТРУКЦИЯ И ВЫПОЛНЕНИЕ ИСХОДНОГО КОДА                           ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Полезная нагрузка содержит:                                          │   ││
│  │  │   - _getattr(_globals(), "__setitem__")(_pyc, _enc_code_body)      │   ││
│  │  │   - exec(_decoded_module, globals())                                │   ││
│  │  │   - _start(main) где _start имеет хук __reduce__                    │   ││
│  │  │ __reduce__ возвращает (main, (_module,)) → выполняет исходный код   │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │  ВЫПОЛНЕНИЕ ИСХОДНОГО КОДА                                                  ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐   ││
│  │  │ Исходный скрипт запускается со всеми сохраненными функциями         │   ││
│  │  └─────────────────────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 **Технические детали**

### 1. Алгоритм XOR шифрования

```python
def encrypt(data):
    k0, k1 = KEY  # k0 ∈ [1,8], k1 ∈ [1,256]
    f = k0        # Начальное состояние
    result = []
    
    for i, c in enumerate(data):
        n = ord(c)
        # XOR с роллинг-ключом из k1, состояния и индекса
        x = (n << k0) ^ (((k1 + f) + i) & 0xFF)
        f = (f ^ x) & 0xFF  # Обновление состояния
        result.append(chr(x))
    
    return ''.join(result)
```

**Ключевые свойства:**
- Каждый байт влияет на все последующие (роллинг-состояние)
- Ключ генерируется из `token_bytes(2)` во время упаковки
- Ключ не хранится напрямую, встроен в зашифрованном виде
- Дешифровка использует обратную операцию: `(x ^ (((k1 + f) + i) & 0xFF)) >> k0`

### 2. Алгоритм ROT шифрования

```python
def rot_enc(s, k):
    return bytes(((n + k) ^ (0x55 + i)) & 0xFF for i, n in enumerate(s))
```

Используется специально для блока кода `INITPYC_FOR`, который обрабатывает начальную настройку декодера.

### 3. Конфигурация LZMA сжатия

```python
LZMA_FILTER = [{
    'id': FILTER_LZMA1,
    'dict_size': 16_777_216,   # 16MB словарь для максимального сжатия
    'lc': 4,                    # Буквенные контекстные биты
    'lp': 0,                    # Буквенные позиционные биты  
    'pb': 2                     # Позиционные биты
}]
RAW_LZMA_FILTER = memoryview(
    dict_size.to_bytes(4, 'little') +
    bytes([lc, lp, pb])
)
```

Эта конфигурация достигает максимальной степени сжатия для Python-кода ценой замедления распаковки.

### 4. Методы обфускации строк

| Метод | Пример вывода |
|:---|:---|
| **Цепочка chr()** | `chr(116)+chr(101)+chr(120)+chr(116)` |
| **XOR строка** | `_chr_func("\x1a\x2b\x3c...")` |
| **f-строка с %** | `f"{chr(37)}{chr(115)}"*4%(...)` |
| **Бинарное/восьмеричное/шестнадцатеричное** | `0b1110100`, `0o164`, `0x74` |

### 5. Обфускация констант

**Варианты None (20+):**
```python
# Примеры:
((None)and((lambda:None)())and(([]or(None))))
([].append(0)or(None))
(((0)if(False)else(None))and((lambda x=None:x)()))
(not(0==1)and(not((None)is not(None)))and([0]and(None)))
(({None}and(None))and(sum([])or(None)))
```

**Варианты True (20+):**
```python
# Примеры:
((1<<0==1)and(2**0==1)and(3%2==1)and(10//10==1))
((lambda x:x^x)(42)==0)and((ord('B')-ord('A'))==1)
((3//3==1)and(bool([1])==True)and(bool([])==False))
((5^2==7)and(4>>2<2)and(1<<1>>1==1))
```

**Варианты Ellipsis (20+):**
```python
# Примеры:
((lambda x:(x)if(x)is(None)else(...))(...))
((([].append(0)or{1})and((...)or(2%2==0))))
((((0)if(False)else(...))and(lambda y:(y)or(...))(None)))
((not([]or{})and((...)not in({...})))or((lambda:...)()))
```

### 6. Генерация имен

```python
def name():
    alphabet = ALPHABET.replace('0123456789', '')
    return choice(alphabet) + ''.join(choice(ALPHABET) for _ in range(19 + randbelow(31)))
```

- Первый символ: не цифра (предотвращает числовые имена)
- Длина: 20-50 символов
- Алфавит: 100+ символов, включая кириллицу и спецсимволы
- Результат: криптические имена вроде `_абвгдеёжзийклмнопрстуфхцчшщъыьэюя`

### 7. Загрузчик на основе type()

Финальный загрузчик использует `type()` Python для создания динамического класса со специальными методами:

```python
__builtins__.getattr(__builtins__.getattr(__builtins__.getattr(__builtins__, "type"),
    "__getattribute__")(__builtins__.getattr(__builtins__, "type"), "__new__")(
    __builtins__.getattr(__builtins__, "type"), "...", 
    (__builtins__.getattr(__builtins__, "object"),), {
        "__slots__": (),
        "__or__": lambda __,_: __builtins__.getattr(__builtins__, "exec")(_, ...),
        "__add__": lambda _,__: __builtins__.getattr(__builtins__, "eval")(...),
        "__floordiv__": lambda _,__: __builtins__.getattr(__builtins__, "__import__")("zlib"),
        "__lshift__": lambda _,__: __builtins__.getattr(globals(), "__setitem__")(...),
        "__init__": lambda __,_: ...  # Распаковка и выполнение
    })
```

### 8. Заглушка модуля (Base85 закодирована)

Константа `MODULE` содержит основную логику декодера, закодированную в Base85:

```python
MODULE = (
    '{}=__builtins__.getattr(__builtins__.getattr(__builtins__,{}),{})(__builtins__.getattr(__builtins__,{}),{});'
    'from builtins import bytes as {}, enumerate as {},globals as {},exec as {},compile as {},__import__ as {},getattr as {},int as {};'
    # ... еще обфусцированный код загрузки модуля
)
```

Это кодируется в Base85, а затем в `uu` в финальном выводе.

---

## ⚙️ **Параметры конфигурации**

| Параметр | Значение | Описание |
|:---|:---|:---|
| `ENCODING` | `'UTF-8'` | Кодировка строк для всех операций |
| `ALPHABET` | 100+ символов | Алфавит для генерации имен (включает кириллицу) |
| `BASIS` | `(bin, oct, hex)` | Системы счисления для обфускации чисел |
| `KEY` | 2 случайных байта | XOR ключ шифрования (k0=1-8, k1=1-256) |
| `CHR_KEY` | (1-6, 0-255) | XOR ключ для обфускации строк |
| `ROT_KEY` | 0-255 | ROT ключ шифрования для цикла _for |
| `LZMA_FILTER` | dict_size=16MB, lc=4, lp=0, pb=2 | Настройки LZMA сжатия |
| `RAW_LZMA_FILTER` | 6-байтовый заголовок | Параметры фильтра для распаковки LZMA |
| `NONE` | 20+ выражений | Случайный выбор для обфускации `None` |
| `TRUE` | 20+ выражений | Случайный выбор для обфускации `True` |
| `ELLIPSIS` | 20+ выражений | Случайный выбор для обфускации `Ellipsis` |
| `gzip level` | 9 | Максимальное сжатие |
| `zlib wbits` | -15 | Raw deflate (без заголовка) |
| `zlib level` | 9 | Максимальное сжатие |

---

## 📁 **Структура файлов**

```
python_packer/
├── packer.py              # Основной исполняемый файл (500+ строк)
│   ├── pypack()          # Основная функция упаковки
│   ├── enc()             # XOR шифрование с роллинг-состоянием
│   ├── rot_enc()         # ROT-13 стиль шифрования
│   ├── _chr_str()        # Генератор обфускации строк
│   └── name()            # Генератор случайных имен (20-50 символов)
│
├── README.md             # Этот файл
│
└── Выходной файл: packed-input.py
    ├── Загрузчик на основе type() (динамический класс со спецметодами)
    │   ├── __slots__ = ()
    │   ├── __or__ → перехватчик exec()
    │   ├── __add__ → генератор строк через eval()  
    │   ├── __floordiv__ → import zlib
    │   ├── __lshift__ → установка chr функции
    │   ├── __rshift__ → установка глобальной переменной
    │   └── __init__ → распаковка и выполнение
    │
    ├── Встроенный Слой 1 (zlib сжатый)
    │   └── Rot-закодированная функция-декодер
    │
    ├── Встроенный Слой 2 (LZMA сжатый)
    │   └── XOR-зашифрованная полезная нагрузка
    │
    └── Обфусцированные константы (варианты None, True, Ellipsis)
```

---

## 🔬 **Техники анти-анализа**

| Техника | Описание |
|:---|:---|
| **Нет прямых строк** | Все строки генерируются во время выполнения через цепочки `chr()` или XOR дешифровку |
| **Нет прямых импортов** | Импорты используют `__import__` через косвенную адресацию `getattr` |
| **Нет фиксированных имен** | Все имена функций/переменных генерируются случайно (20-50 символов) |
| **Многослойное сжатие** | 5+ слоев сжатия/шифрования должны быть развернуты |
| **Патчинг кода во время выполнения** | Использует `__code__.replace()` для изменения констант функций |
| **Pickle редукция** | Хук `__reduce__` выполняет код без явного вызова |
| **Метапрограммирование через type()** | Динамическое создание классов со специальными методами |
| **Обфускация констант** | Все константы заменены сложными логическими выражениями |
| **Самомодифицирующийся код** | Константы кода патчатся во время выполнения |
| **Выполнение только из памяти** | Исходный код никогда не записывается на диск |

---

## 🧰 **Использование**

### Базовый запуск
```bash
python packer.py script.py
# Создает: packed-script.py
```

### Упаковка нескольких файлов
```bash
python packer.py script1.py script2.py script3.py
```

### Помощь
```bash
python packer.py
# Вывод: python3 packer.py (path)  —  Pack Python file
```

---

## 📊 **Характеристики производительности**

| Показатель | Значение |
|:---|:---|
| **Размер входа** | Любой (тестировалось до 10MB) |
| **Размер выхода** | ~100x размера исходника (из-за обфускации) |
| **Время упаковки** | ~1-3 секунды на MB |
| **Накладные расходы при выполнении** | ~0.5-2 секунды на распаковку |
| **Использование памяти** | ~3x размера исходного файла во время выполнения |
| **Версия Python** | 3.6+ требуется (использует f-строки, подсказки типов) |

---

## ⚠️ **ПРЕДУПРЕЖДЕНИЕ**

> **ЭТОТ ИНСТРУМЕНТ СОЗДАЕТ СИЛЬНО ОБФУСЦИРОВАННЫЙ КОД!**

- 📦 **Увеличение размера** — выходной файл может быть в 50-100 раз больше исходного (200KB → 20MB)
- 🐌 **Замедление выполнения** — из-за многослойной распаковки (добавляет 0.5-2 секунды)
- 🐍 **Требуется Python 3.6+** — используются f-строки, подсказки типов и другие современные возможности
- 🔧 **Не для продакшена** — предназначен для защиты чувствительного кода, не для обычного распространения
- ⚖️ **Соблюдение законов** — проверьте законы о reverse engineering в вашей стране

**АВТОР НЕ НЕСЕТ ОТВЕТСТВЕННОСТИ ЗА НЕПРАВИЛЬНОЕ ИСПОЛЬЗОВАНИЕ ЭТОГО ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ.**

---

## 👤 **Автор**

**Владислав Худаш**
- GitHub: [@cppandpython](https://github.com/cppandpython)
- Возраст: 17

---

## ⭐ **Поддержка**

Если проект показался тебе интересным, поставь звездочку на GitHub!

---
