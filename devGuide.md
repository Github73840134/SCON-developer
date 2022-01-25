# The devGuide
This document covers new developer features.
### Browse(open(...))
For `data` if the _io.TextIOWrapper object has a mode attribute with the value of: `r+`,`a+`,or `w+` you can use the sync feature.
### Browse.sync()
Sync the SCON file. (Only works when you use `Browse()` with `open()`).
### writecomment(comment)
Appends a comment to the end of the file.
### compress(data)
Not working properly.  
Meant to save space when compiling by changing names.  
data must be dict.  
Returns a dict for compiling.
### decompress(data)
Decompresses compressed data.  
data must be dict.
### scon.FLAGS
#### Works with:
- `scon.dumps()`
- `scon.dump()`
- `scon.load()`
- `scon.loads()`

Add flags after the required parameters specified by the function.
#### Flags (`class scon.FLAGS`):
- `ONELINE`: removes newlines (**NOTE**: Only removes newlines that would normally be put into the file to make it human readable, If you have newline characters in your values, It will add newlines to the files.) (Only works on `dump()` or `dumps()`)
- `NO_VERIFY`: Skips file verification. (Only works on `load()` or `loads()`)
