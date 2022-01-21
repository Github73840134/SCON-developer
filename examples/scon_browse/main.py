# Demo of the browse class
import scon
res = scon.load(open('demo.sco','r'))
b = scon.Browse(res.data)
print(b.listdir())