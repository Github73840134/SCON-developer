import scon
res = scon.loads(open('test.sco','r').read())
print(res.data,res.comments)