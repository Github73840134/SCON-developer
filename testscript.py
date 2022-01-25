import scon
c = scon.load(open('test','r'))
ct = scon.compress(c.data)
cte = scon.dumps(c.data,scon.FLAGS.ONELINE)
print('Compressed size',len(open('test2','r').read()))
print('Un-Compressed size',len(cte))
f = scon.decompress(ct)