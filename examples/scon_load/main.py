import scon
res = scon.load(open('test.sco','r'))
print(res.data,res.comments)