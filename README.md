# SCON
#### **S**emicolon **C**ut **O**bject **N**otation
A better way to dictionary  
## Build Info
Version: 1.0.2 
Build: Latest (Jan 25 2022 @ 3:11 PM EST)  
Platform: Developer (The risky biscut) (**Proceed at your own risk**)
## Release Notes
- Fixed space issue
## New Features
- SCON file syncing
- Ability to add comments to SCON file.
***
## Description:
SCON (Pronounced: scone) is a versatile way for formmatting data and is loosely based on JSON, and can be used across multiple platforms.
## How to Use:
\**Examples can be found in the examples directory of the repo*
### Supported Types:
- `str`
- `int`
- `bool`
- `list`
- `dict`
- `NoneType`
### Comments
***
#### Comment()
Put this as a key in the dictonary and the value will become a comment.

Writing SCON
---
#### dump(obj,fp)
Creates and writes a SCON file from a dictionary.  
##### Attribute info:
* obj
  * type: dict
* fp
  * type: builtin_function_or_method

Make sure that fp is writable.
***
#### dumps(obj)
Creates a SCON file from a dictionary.  
##### Attribute info:
* obj
  * type: dict

Returns a SCON string

Reading SCON
---
#### load(fp)
Creates a dictonary from a SCON file.  
##### Attribute info:
* fp
  * type: builtin_function_or_method

Make sure that fp is readable.  
Return a namedtuple: `data` contains the parsed SCON file, `comments` contains the comments from the parsed SCON file.  
***
#### loads(obj)
Creates a dictonary from a SCON string.  
##### Attribute info:
* obj
  * type: str

Make sure that fp is readable.  
Return a namedtuple: `data` contains the parsed SCON file, `comments` contains the comments from the parsed SCON file. 
## Browse Class
Browse a SCON object like a POSIX file path.  
ex. ```/test/name.str```
#### File Naming
|Python Type|Extention|
|-----------|---------|
| str|.str|
| int|.int|
| bool|.bol|
| list|.lst|
| dict|None (sub-dictionaries represented as directories)
## Browse(data)
Creates a browsable object.  
data can be types: `str`,`dict`
### find(path=None)
Find value from a path in the dictonary
### getcwd()
Gets the current directory.  
### chdir(path)
Changes the current directory.  
### Browse.open(path,mode="r")
Opens the value to be read or written to.  
* Path
  * type: str

* Mode
  * type: str

Returns a class similar to the builtin function `open()`, the following methods are available.  
* write()
* read()
* close()
### listdir(path=None)
Views the current directory tree or the directory specified in `path`.  
* path
  * type: str  

Returns contents of current or specifified directory
# What does a SCON file look like?
```python
string="This is a string";
int=0;
true_bool=true;
false_bool=false;
nothing=null;
list=[0,1,2,3,4,5,6,7,8,9];
sub_dictionary0{
	sub_value="I am a sub";
}
#Every line ends with semicolons execept for dictionaries. this comment will continue until you put a semicolon;
```
# You have reached the end of the documentation!
Happy database creation!
# Coming Soon
- Micropython port
***
Check out other builds such as
[`experimental`](https://github.com/Github73840134/SCON-experimental) or [`Stable`](https://github.com/Github73840134/SCON)
©2022 Github73840134