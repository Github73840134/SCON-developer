import scon
data = {'string':'apple',
	   'integer':0,
	   'truebool':True,
	   'falsebool':False,
	   'none':None,
	   scon.Comment():'A comment to top it off'}
scon.dump(data,open('test.scon','w+'))