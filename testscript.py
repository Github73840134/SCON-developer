import scon
c = scon.Browse(open('test','r+'))
c.open('string.str','w').write("This is an updated string.")
c.sync()
c.writecomment('hi')
c.sync()