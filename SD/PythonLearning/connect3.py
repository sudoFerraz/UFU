"""Information example - Chapter 2 - connect3.py ."""
import socket
print "Creating socket...",
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Done."
print "Looking up port number for http/tcp...",
port = socket.getservbyname('http', 'tcp')
print "Done."
print "Connecting to remote host on port %d..." % port,
s.connect(("www.google.com", port))
print "Done"
print "Connected from ", s.getsockname()
print "Connected to ", s.getpeername()
