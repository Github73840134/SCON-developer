from collections import namedtuple
import _io
import base64
__version__ = "1.0.2"
__build__ = "Latest"
__platform__ = "Developer"
print("You are using a developer build. Proceed at your own risk")
class Comment:
	'''Add a comment.'''
	isComment = True
	visComment = __name__
	uuid = object()
class FLAGS:
	ONELINE = 3
	NO_VERIFY = 4
class SCONDecodeError(Exception):
	pass
def verify(data,x=0,y=0):
	for i in data:
		if type(data[i]) == dict:
			verify(data[i],y=y+1)
		if i == '':
			raise SCONDecodeError("Extraneous ; found "+str(x) + "," + str(y))
def parse(text,use_verify=True):
	__doc__ = '''The parser, Used internally'''
	result = {}
	tree = []
	comments = []
	commentlines = []
	parsed = result
	listmode = False
	mode = 0
	ldepth = 0
	y = 0
	name = ""
	value = ""
	string = False
	wastring = False
	waslist = False
	cw = ''
	comment = ''
	for i in range(0,len(text)):
		cw += text[i]
		if cw == '=' and string == False:
			mode = 1
			cw = ''
		elif cw == '"':
			if mode == 1:
				if string:
					wastring = True
				string = not string
				cw = ''
		elif cw == '\"':
			if string:
				value += '"'
				cw = ''
		elif cw == ',' and listmode:
			if value.isnumeric() and wastring == False:
				value = int(value)
			elif value.lower() == 'true':
				value = True
			elif value.lower() == 'false':
				value = False
			elif value.lower() == 'null':
				value = None
			if waslist == False:
				parsed.append(value)
			else:
				waslist = False
			value = ''
			cw = ''
			wastring = False
		elif cw == ";":
			if string:
				value += ';'
			elif wastring == False:
				if value.isnumeric():
					value = int(value)
				elif value.lower() == 'true':
					value = True
				elif value.lower() == 'false':
					value = False
				elif value.lower() == 'null':
					value = None
			if mode == 2:
				comments.append((comment,y))
				comment = ''
				mode = 0
				cw = ''
			elif listmode == False:
				parsed[name] = value
				name = ''
				value = ''
				mode = 0
				cw = ''
				wastring = False
				waslist = False
			else:
				name = ''
				value = ''
				mode = 0
				cw = ''
				listmode = False
				wastring = False
		elif cw == '\n':
			if string:
				value += '\n'
			cw = ''
			y += 1
		elif cw == '\t':
			if string:
				value += '\t'
			cw = ''
		
		elif cw == ' ':
			if string:
				value += ' '
			if mode == 2:
				comment += ' '
			cw = ''
		elif cw == '{' and mode == 0 and string == False:
			tree.append(parsed)
			parsed[name] = {}
			parsed = parsed[name]
			cw = ''
			name = ''
		elif cw == '}' and mode == 0 and string == False:
			parsed = tree[len(tree)-1]
			tree.pop(len(tree)-1)
			value = ''
			cw = ''
		elif cw == '[' and mode == 1 and string == False:
			tree.append(parsed)
			if type(tree[len(tree)-1]) == dict:
				parsed[name] = []
				parsed = parsed[name]
			if type(tree[len(tree)-1]) == list:
				parsed.append([])
				parsed = parsed[len(parsed)-1]
			listmode = True
			ldepth += 1
			cw = ''
			name = ''
		elif cw == ']' and mode == 1 and string == False:
			if value.isnumeric() and wastring == False:
				value = int(value)
			elif value.lower() == 'true':
				value = True
			elif value.lower() == 'false':
				value = False
			elif value.lower() == 'null':
				value = None
			parsed.append(value)
			value = ''

			parsed = tree[len(tree)-1]
			tree.pop(len(tree)-1)
			cw = ''
			wastring = False
			print('t',tree)
			if len(tree) != 0:
				if type(tree[ldepth-1]) == dict:
					value = ''
					name = ''
			waslist = True
			ldepth -= 1
		elif cw == "#":
			mode = 2
			cw = ''
		elif cw.isascii():
			if mode == 0:
				name += cw
			if mode == 1:
				value += cw
			if mode == 2:
				comment += cw
			cw = ''
	f = namedtuple("result",['data','comments'])
	if use_verify:
		verify(result)
	return f(data=result,comments=comments)
def make(data,ind=0,comments=[],nl=True):
	made = ''
	for i in data:
		if nl:
			if 'isComment' in dir(i):
				if i.visComment == __name__:
					made += '\t'*ind+'#'+data[i] + ';\n' 
			elif type(data[i]) == int:
				made += '\t'*ind+i + '=' + str(data[i]) + ';\n'
			elif type(data[i]) == str:
				made += '\t'*ind+i + '="' + data[i] + '";\n'
			elif type(data[i]) == bool:
				made += '\t'*ind+i + '=' + str(data[i]).lower() + ';\n'
			elif data[i] == None:
				made += '\t'*ind+i + '=' + 'null;\n'
			elif type(data[i]) == float:
				made += '\t'*ind+i + '="' + data[i] + '";\n'
			elif type(data[i]) == dict:
				made += '\t'*ind+i+'{\n'+make(data[i],ind+1)+'\t'*ind+'}\n'
			elif type(data[i]) == list:
				made += '\t'*ind+i+'='+data[i].__repr__().replace("'",'"')+';\n'
		else:
			if 'isComment' in dir(i):
				if i.visComment == __name__:
					made += '#'+data[i] + ';' 
			elif type(data[i]) == int:
				made += i + '=' + str(data[i]) + ';'
			elif type(data[i]) == str:
				made += i + '="' + data[i] + '";'
			elif type(data[i]) == bool:
				made += i + '=' + str(data[i]).lower() + ';'
			elif data[i] == None:
				made += i + '=' + 'null;'
			elif type(data[i]) == float:
				made += i + '="' + data[i] + '";'
			elif type(data[i]) == dict:
				made += i+'{'+make(data[i],0,nl=nl)+'}'
			elif type(data[i]) == list:
				made += i+'='+data[i].__repr__().replace("'",'"')+';'

	return made
def dumps(obj,*flags):
	'''Creates a SCON file from a dictionary.  
##### Attribute info:
* obj  
  * type: dict

Returns a SCON string'''
	do_oneline = True
	for i in flags:
		if i == FLAGS.ONELINE:
			do_oneline = False
	return make(obj,nl=do_oneline)
def dump(obj,fp,*flags):
	'''Creates and writes a SCON file from a dictionary.  
##### Attribute info:
* obj
  * type: dict
* fp
  * type: builtin_function_or_method

Make sure that fp is writable.'''
	if not fp.writable:
		raise PermissionError("Make sure the file object is writeable")
	do_oneline = True
	for i in flags:
		if i == FLAGS.ONELINE:
			do_oneline = False
	e = make(obj,nl=do_oneline)
	fp.write(e)
	fp.close()
def loads(obj,*flags):
	'''Creates a dictonary from a SCON string.  
##### Attribute info:
* obj
  * type: str

Make sure that fp is readable.  
Return a namedtuple: `data` contains the parsed SCON file, `comments` contains the comments from the parsed SCON file.'''
	do_verify = True
	for i in flags:
		if i == FLAGS.NO_VERIFY:
			do_verify = False
	return parse(obj,do_verify)
def load(fp,*flags):
	'''Creates a dictonary from a SCON file.  
##### Attribute info:
* fp
  * type: builtin_function_or_method

Make sure that fp is readable.  
Return a namedtuple: `data` contains the parsed SCON file, `comments` contains the comments from the parsed SCON file. '''
	if not fp.readable:
		raise PermissionError("Make sure the file object is readable")
	do_verify = True
	for i in flags:
		if i == FLAGS.NO_VERIFY:
			do_verify = False
	return parse(fp.read(),do_verify)
class Browse:
	
	'''Browse a SCON object like a POSIX file path.  
ex. ```/test/name.str```
#### File Naming
|Python Type|Extention|
|-----------|---------|
| str|.str|
| int|.int|
| bool|.bol|
| list|.lst|
| dict|None (sub-dictionaries represented as directories)'''
	def __init__(self,data):
		global bself
		bself = self
		self.syncable = False
		if type(data) == str:
			self.tree = loads(data)
		elif type(data) == dict:
			verify(data)
			self.tree = data
		elif type(data) == _io.TextIOWrapper:
			if data.mode in ['r+','w+']:
				self.syncable = True
				self.file = data
				tmp = loads(data.read())
				self.tree = tmp.data
				self.cmts = tmp.comments
				print('comments',self.cmts)
		self.cwd = '/'
		self.ftree = {}
		self.prevdir = []
		self.directories = []
		self._listdir()
		self._link(self.tree)
	def _link(self,t,name='/'):
		for i in t:
			if type(t[i]) == int:
				self.ftree[name+i+'.int'] = i
			if type(t[i]) == str:
				self.ftree[name+i+'.str'] = i
			if type(t[i]) == bool:
				self.ftree[name+i+'.bol'] = i
			if type(t[i]) == list:
				self.ftree[name+i+'.lst'] = i
			if type(t[i]) == dict:			
				self._link(t[i],name+i+'/')
				
	def _listdir(self):
		def treemaker(t,o=[],name='/'):
			for i in t:
				if type(t[i]) == int:
					o.append(name+i+'.int')
				if type(t[i]) == str:
					o.append(name+i+'.str')
				if type(t[i]) == bool:
					o.append(name+i+'.bol')
				if type(t[i]) == list:
					o.append(name+i+'.lst')
				if type(t[i]) == dict:
					self.directories.append(name+i)				
					o.extend(treemaker(t[i],[],name+i+'/'))
			return o
		self.etree = treemaker(self.tree)
	def listdir(self,path=None):
		'''Views the current directory tree or the directory specified in `path`.  
* path
  * type: str  

Returns contents of current or specifified directory '''
		made = []
		if path == None:
			for i in self.etree:
				if self.cwd in i:
					made.append(i.strip(self.cwd))
		else:
			for i in self.etree:
				if path in i and i.strip(path) in made :
					made.append(i.strip(path))

		return made
	def chdir(self,path):

		if path[0] != '/':
			
			if self.cwd == '/':
				self.cwd = '/'+path
			else:
				self.cwd = '/'+self.cwd+'/'+path
		else:
			self.cwd = path
	def getcwd(self):
		'''Gets the current directory'''
		return self.cwd
	def find(self,path):
		'''Find value from a path in the dictonary.'''
		loc = self.etree.index(self.path)
		loc2 = self.etree[loc]
		data = loc2.split('/')
		dpath = self.tree
		ftypes = ['.str','.int','.lst','.bol']
		for i in data[1:]:
			if i == data[len(data)-1]:
				return dpath[self.ftree[path]]
			else:
				dpath = dpath[i]
	class open:
		'''Opens the value to be read or written to.  
**NOTE!**: Any changes made to the dictonary will not sync to the SCON file.  (This feature will be added soon.)
* Path
  * type: str

* Mode
  * type: str

Returns a class similar to the builtin function `open()`, the following methods are available.  
* write()
* read()
* close()'''
		writable = False
		readable = True
		closed = False
		name = ''
		def __init__(self,path,mode="r"):
			self = bself
			if mode == 'r':
				self.writable = False
				self.readable = True
				self.name = path
				self.closed = False
			if mode == 'w':
				self.writable = True
				self.readable = False
				self.closed = False
				self.name = path
				self.tmp = ''
			if mode == 'a':
				self.writable = True
				self.readable = False
				self.closed = False
				self.name = path
				self.tmp = ''
			if mode == 'a+':
				self.writable = True
				self.readable = False
				self.closed = False
				self.name = path
				self.tmp = ''
			if mode == 'w+':
				self.writable = True
				self.readable = True
				self.closed = False
				self.name = path
				self.tmp = ''
			if mode == 'r+':
				self.writable = True
				self.readable = True
				self.closed = False
				self.name = path
				self.tmp = ''
			if self.cwd == '/':
				loc = self.etree.index('/'+path)
			else:
				loc = self.etree.index(self.cwd+'/'+path)
			loc2 = self.etree[loc]
			data = loc2.split('/')
			self.dpath = self.tree
			self.mode = mode
			for i in data[1:]:
				if i == data[len(data)-1]:
					if self.cwd != '/':
						self.floc = self.ftree[self.cwd+'/'+path]
					else:
						self.floc = self.ftree['/'+path]
					if mode == 'w+':
						self.dpath[self.floc] = ""
					break
				else:
					self.dpath = self.dpath[i]
		def read(self):
			self = bself
			'''Read a value.'''
			if self.readable:
				return self.dpath[self.floc]
			else:
				raise PermissionError("Operation Not Permitted")
		def write(self,data):
			self = bself
			'''Writes to the value.'''
			if self.writable:
				if self.mode == 'w':
					self.dpath[self.floc] = data
				if self.mode == 'w+':
					self.dpath[self.floc] = data
				if self.mode == 'a':
					self.dpath[self.floc] += data
				if self.mode == 'a+':
					self.dpath[self.floc] += data
				if self.mode == 'r+':
					self.dpath[self.floc] = data
			else:
				raise PermissionError("Operation Not Permitted")
	def writecomment(self,data):
		print('tup',self.cmts[-1:])
		self.cmts.append((data,self.cmts[-1:][0][1]+1))
		print(self.cmts)
	def sync(self):
		print("You are about to run an experimental feature")
		if self.syncable == False:
			raise PermissionError("Please provide a fil object to open when initalizing or file object is not an acceptable mode.")
		print(self.tree)
		prestr = dumps(self.tree).split('\n')
		for i in self.cmts:
			prestr.insert(i[1],"#"+i[0]+';')
		self.file.truncate(0)
		self.file.seek(0)
		self.file.write('\n'.join(prestr)[:-1])
		self.file.flush()
		self.file.seek(0) 
def compress(data):
	def makekeys(data):
		keys = {}
		for i in data:
			if type(data[i]) != dict:
				keys[str(len(keys))] = i
			else:
				tid = str(len(keys))
				keys[tid] = {'n':i}
				keys[tid]['d'] = makekeys(data[i])
		return keys
	def makevalues(data):
		newdata = {}
		for i in data:
			tid = str(len(newdata))
			if type(data[i]) != dict:
				newdata[tid] = data[i]
			else:
				newdata[tid] = makevalues(data[i])
				
		return newdata
	e = makevalues(data)
	f = makekeys(data)
	t = {}
	t['$ii'] = f
	t['$d'] = e

	return t
def decompress(data):
	def _decompress(data,table):
		rebuilt = {}
		for i in data:
			if type(data[i]) != dict:
				rebuilt[table[i]] = data[i]
			else:
				rebuilt[table[i]['n']] = _decompress(data[i],table[i]['d'])
		return rebuilt
	return _decompress(data["$d"],data["$ii"])