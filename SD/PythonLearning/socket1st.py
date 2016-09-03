  #####
 #     #  ####  #####  #    # ###### #####
 #       #    # #    # #    # #      #    #
 #  #### #    # #    # ###### #####  #    #
 #     # #    # #####  #    # #      #####
 #     # #    # #      #    # #      #   #
  #####   ####  #      #    # ###### #    #


#!/usr/bin/env python
#Cliente simples para testes com socket com protocolo gopher
# - testesocket.py

import sys
import socket

port = 70   #Gopher utiliza a porta 70
host = sys.argv[1]  #Chamada da funcao parametro 1
filename = sys.argv[2]  #Metodo vem do objeto sys

#Declara uma variavel S e atribui a ela um objeto socket
#No objeto socket, o metodo .socket passa a familia de end
#e o tipo de conexao
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

#Para conectar passar o objeto com o metodo .connect(("host",porta))
try:
    s.connect((host, port))
except socket.timeout, e:
    print "Error connecting to server: %s" %e
    sys.exit(1)
except socket.gaierror, e:
    print "Error connecting to server: %s" %e
    sys.exit(1)

#Manda um pacote de dados nas conexoes do socket
#S
s.sendall(filename + "\r\n")

while 1:
    buf = s.recv(2048)
    if not len(buf):
        break
    sys.stdout.write(buf)
