# Creates a prompt demoing all the features of the Browse() class
import scon
res = scon.load(open('demo.sco','r'))
b = scon.Browse(res.data)
print(b.listdir())