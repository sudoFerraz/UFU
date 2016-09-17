"""Error handling example with file-like objects."""

import socket
import sys
import time

host = sys.argv[1]
textport = sys.argv[2]
filename = sys.argv[3]

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, e:
    print "Strange error creating socket: %s" % e
    sys.exit(1)

try:
    port = int(textport)
except ValueError:
    # Nao 'e um numero
    try:
        port = socket.getservbyname(textport, 'tcp')
    except socket.error, e:
        print "Couldnt find yout port: %s" % e
        sys.exit(1)

try:
    s.connect((host, port))
except socket.gaierror, e:
    print "Address related error on conection: %s" % e
    sys.exit(1)
except socket.error, e:
    print "Connection error: %s" % e
    sys.exit(1)

fd = s.makefile('rw', 0)

print "Sleeping..."
time.sleep(10)
print "Continuing"

try:
    fd.write("GET %s HTTP/1.0\r\n\r\n" % filename)
except socket.error, e:
    print "Error sending data: %s" % e
    sys.exit(1)

try:
    fd.flush()
except socket.error, e:
    print "Error sending data(by flush): %s" % e
    sys.exit(1)

try:
    s.shutdown(1)
    s.close()
except socket.error, e:
    print "Error sending data(by shutdown): %s" % e
    sys.exit(1)

while 1:
    try:
        buf = fd.read(2048)
    except socket.error, e:
        print "Error receiving data: %s" % e
        sys.exit(1)
    if not len(buf):
        break
    sys.stdout.write(buf)
