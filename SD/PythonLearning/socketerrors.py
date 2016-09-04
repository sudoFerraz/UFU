"""Error Handling Example - Chapter 2."""
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

# Tentando formatar o argv da porta para numero

try:
    port = int(textport)
except ValueError:
    # Nao funcionou, provavelmente n e um numero.
    # Ver se o doente passou um nome de protocolo correto.
    try:
        port = socket.getservbyname(textport, 'tcp')
    except socket.error, e:
        print "Nao deu pra achar saporra de porta: %s" % e
        sys.exit(1)

try:
    s.connect((host, port))
except socket.gaierror, e:
    print "Address related error connecting to server: %s" % e
    sys.exit(1)
except socket.error, e:
    print "Connection error: %s" % e
    sys.exit(1)

print "sleeping..."
time.sleep(10)
print "Continuing."

try:
    s.sendall("GET %s HTTP/1.0\r\n\r\n" % filename)
except socket.error, e:
    print "Error sending data: %s" % e
    sys.exit(1)

try:
    s.shutdown(1)
except socket.error, e:
    print "Error sending data (detected by shutdown): %s" % e
    sys.exit(1)

while 1:
    try:
        buf = s.recv(2048)
    except socket.error, e:
        print "Error receiving data: %s" % e
        sys.exit(1)
    if not len(buf):  # Ta antes pra nao imprimir NULL antes de acabar o loop
        break
    sys.stdout.write(buf)
