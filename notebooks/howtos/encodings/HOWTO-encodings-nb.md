---
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
  notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version, -jupytext.text_representation.format_version,
    -language_info.version, -language_info.codemirror_mode.version, -language_info.codemirror_mode,
    -language_info.file_extension, -language_info.mimetype, -toc
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
language_info:
  name: python
  nbconvert_exporter: python
  pygments_lexer: ipython3
nbhosting:
  title: encoding howto
---

# character encodings

+++

## ASCII

+++

### `ord()` and `chr()`

```{code-cell} ipython3
# a text like this one

text1 = "abcd\nefgh\n"
```

is actually encoded in memory according to ASCII:  
<https://www.man7.org/linux/man-pages/man7/ascii.7.html>

```{code-cell} ipython3
# and to confirm that, we can use ord()
# which applies on a single char (raises an exception otherwise)

for c in text1:
    print(f"{c} -> {ord(c)}")
```

```{code-cell} ipython3
# FYI, note we also have the reverse function, pour info, qu'on a aussi la fonction inverse de ord
# qui s'appelle chr()

chr(97)
```

### write into a text file

````{admonition} specify an encoding ?

in 2024 you should not need to be explicit about the encodings
if your computer is properly configured (i.e. not too old ;-)  

but here we want to be robust, and so we are explicit about that  
````

```{code-cell} ipython3
from pathlib import Path
```

```{code-cell} ipython3
# remember to always use a with: when dealing with files

with Path('encodings1-utf8').open('w', encoding='UTF-8') as f:
    f.write(text1)
```

inspect that file with a hex editor - e.g. you can use vs-code and install the **HEX Editor** extension

you will see that, with ASCII-only characters, your file has **exactly one byte per character**

+++

## non-ASCII & UTF-8

let us now consider a text with French accents and cedilla - any non-ASCII character would do

```{code-cell} ipython3
text2 = "abçd\néfgh\n"
```

### inspection

```{code-cell} ipython3
# notice the values > 127
# which are not supported in ASCII

for c in text2:
    print(f"{c} -> {ord(c)}")
```

```{code-cell} ipython3
# focus on the 2 characters whose encoding is > 127

hex(231), hex(233)
```

```{code-cell} ipython3
bin(231), bin(233)
```

again, note that `chr()` and `ord()` are the inverse of one another

```{code-cell} ipython3
chr(231), ord('ç')
```

### write into a text file

```{code-cell} ipython3
with Path('encodings2-utf8').open('w', encoding='UTF-8') as f:
    f.write(text2)
```

### read back

````{admonition} specify an encoding (2) ?

in the following, we want to read **bytes** (note mode=`rb`) and `b` stands for binary  
this means we will **do the decoding ourselves** !  
and so this time we **do not specify an encoding** (would raise an exception...)
````

```{code-cell} ipython3
# no encoding in binary mode, would make no sense !

with Path('encodings2-utf8').open('rb') as f:
    raw = f.read()
```

and as we read bytes here, and we have **more bytes than** the initial text had **characters**

```{code-cell} ipython3
len(raw), len(text2)
```

it adds up, since the each of the 2 alien characters will need 2 bytes each to be encoded  
(European characters usually take 2 bytes; some more exoctic chars can take 3 or 4 bytes)

+++

### UTF-8 logic

this table describes how the UTF8 encoding works:

```{image} media/unicode-utf8-areas.png
:align: center
```

+++

### a visual example

on a sample 4-characters string: `été\n`

```{image} media/unicode-decode-example.png
:align: center
```

let's check that

+++

### on our own data

```{code-cell} ipython3
# here is it again
raw
```

let us number the contents of `raw`
```
012   3   45 6   7   89
ab\xc3\xa7d\n\xc3\xa9fgh\n
```

```{code-cell} ipython3
# extract the 2-bytes areas for each alien character

ccedilla = raw[2:4]
eaccent = raw[6:8]
```

```{code-cell} ipython3
for b in ccedilla:
    print(f"byte {b} {hex(b)} {bin(b)}")
```

```{code-cell} ipython3
for b in eaccent:
    print(f"byte {b} {hex(b)} {bin(b)}")
```

sounds good

+++

### decode manually (gory details)

this is totally optional of course, but if we wanted to do the decoding ourselves...  
(you may **skip to the next section**)

```{code-cell} ipython3
# we want 5 bits from the first byte and 6 from the second byte

on2bytes_0_len = 5
on2bytes_1_len = 6

# and that's what should occur in the remaining (left-hand-side) bits
on2bytes_0_pad = 0b110
on2bytes_1_pad = 0b10
```

```{code-cell} ipython3
def mask_from_len(length):
    """
    for e.g. len == 5, we compute a mask that has
    3 bits set and 5 bits unset (because 3+5=8)
    """
    return 2**8 - 2**length
```

```{code-cell} ipython3
# let us check that it works as advertised:

# e.g. for byte0
# the result allows to separate 
# the (3-bits) padding from 
# the (5-bits) payload

bin(mask_from_len(5))
```

```{code-cell} ipython3
# with that we can manually decode 2-bytes UTF-8 !

on2bytes_0_mask = mask_from_len(on2bytes_0_len)
on2bytes_1_mask = mask_from_len(on2bytes_1_len)

def decode(on2bytes):
    b0, b1 = on2bytes
    # check masks
    # e.g. check that the 3 high bits in 0xc9 are indeed 0b110
    assert (b0 & on2bytes_0_mask) >> on2bytes_0_len == on2bytes_0_pad
    # same on byte 1
    assert (b1 & on2bytes_1_mask) >> on2bytes_1_len == on2bytes_1_pad
    # extract meaningful bits
    # for that we just need to invert the mask
    bits0 = b0 & ~ (on2bytes_0_mask)
    bits1 = b1 & ~ (on2bytes_1_mask)
    # asemble bits into codepoint
    # b0 has the high bits so it needs to be shifted
    # by the number of meaningful bits in byte1
    codepoint = bits1 | bits0 << on2bytes_1_len
    return chr(codepoint)
```

```{code-cell} ipython3
# and indeed 
decode(eaccent), decode(ccedilla)
```

### exercise

use this table to write a complete UTF-8 decoder 

```{image} media/unicode-utf8-areas.png
:align: center
:width: 500px
```

+++

## UTF-32

let us now take a quick look at the UTF-32 encoding  
this is a **fixed size** encoding, meaning **each character will use 4 bytes**  
this is convenient e.g. when you need to do direct access to the $n-th$ character in a file

+++

### write with UTF-32

let's write our text with 2 alien characters in a second file

```{code-cell} ipython3
with Path("encodings2-utf32").open('w', encoding='utf-32') as f:
    f.write(text2)
```

### size and BOM

however the total file size is **not exactly** $4*n$, and this is due to [something called **the BOM** (*Byte Order Mark*)](https://en.wikipedia.org/wiki/Byte_order_mark)

```{code-cell} ipython3
# computing file size: use pathlib !

p = Path("encodings2-utf32")
print(f"file has {p.stat().st_size} bytes")
```

```{code-cell} ipython3
len(text2)
```

44 is because 

* 4 * 10 chars = 40 bytes
* ***plus* 4 bytes** for the BOM located in the first 4 bytes

```{code-cell} ipython3
# read the 4 first bytes

with Path("encodings2-utf32").open('rb') as f:
    bom = f.read(4)
```

```{code-cell} ipython3
bom
```

which indeed matches the UTF-32 little-endian (LE) BOM as shown on <https://en.wikipedia.org/wiki/Byte_order_mark>

+++

### decoding is way easier

with that in mind, it is easier to

* compute the location of a given character from its rank in the string
* and to decode the raw binary stream

+++

for example: decode the `ç` in our initial string

```{code-cell} ipython3
# read the whole file

with Path("encodings2-utf32").open('rb') as f:
    raw = f.read()
```

```{code-cell} ipython3
# remember that ç is at index 2

index = 2

text2[index]
```

so this means it gets encoded in the file on 4 bytes starting at offset  
4 + 4 * index

```{code-cell} ipython3
offset = 4 + 4*index

b4 = raw[offset:offset+4]

b4
```

because it is little endian - see <https://en.wikipedia.org/wiki/Endianness> - it means we have to mirror the data bytes to get the actual value

```{code-cell} ipython3
# int.from_bytes knowns how to transform a sequence
# of bytes into an int, given the endian-ness

int.from_bytes(b4, 'little')
```

```{code-cell} ipython3
# and indeed, that is what was encoded in the file !

chr(231)
```
