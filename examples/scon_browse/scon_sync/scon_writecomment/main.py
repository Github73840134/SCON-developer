import scon
c = scon.Browse(open('test.sco','r+'))
c.writecomment('hi')
c