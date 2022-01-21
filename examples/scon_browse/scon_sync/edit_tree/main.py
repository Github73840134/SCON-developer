import scon
c = scon.Browse(open('test.sco','r+'))
c.open('string.str','w').write("This is an updated string.")
c.sync()