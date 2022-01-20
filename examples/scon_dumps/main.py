import scon
data = {'string':'apple',
	   'integer':0,
	   'truebool':True,
	   'falsebool':False,
	   'none':None,
	   scon.Comment():'A comment to top it off'}
final = scon.dumps(data)
file = open('demo.sco','w+')
file.write(final)
file.close()