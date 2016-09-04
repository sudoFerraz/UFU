#!/usr/bin/env python
#Simple Server - Chapter 1 - server.py

import socket

host = ''           #Conecta em todas as interfaces
port = 51423

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(1)

print "Servidor rodando na porta %d; ctrl-c para terminar" % port

while 1:
    clientsock, clientaddr = s.accept() #Aceita a conexao e retorna o socket do cliente
    clientfile = clientsock.makefile('rw', 0) #Cria um file no socket cliente
    clientfile.write("Welcome, " + str(clientaddr) + "\n") #Escreve no file do socket do cliente
    clientfile.write("Please enter a string: ")
    line = clientfile.readline().strip() #Le o file do socket do cliente
    #O m'etodo strip separa em uma lista cada caracter
    #line recebe uma lista com n elementos cada um sendo um caracter da string
    clientfile.write("You entered %d characters.\n" % len(line))
    clientfile.close() #Fecha o arquivo no socket cliente
    clientsock.close() #Fecha o outro arquivo no socket do cliente
