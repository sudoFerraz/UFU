"""HTTP server with file tree Sistemas Distribuidos 2016-2 UFU.

 ____   ____  _________________  _________________      _____
|    | |    |/                 \/                 \ ___|\    \
|    | |    |\______     ______/\______     ______/|    |\    \
|    |_|    |   \( /    /  )/      \( /    /  )/   |    | |    |
|    .-.    |    ' |   |   '        ' |   |   '    |    |/____/|
|    | |    |      |   |              |   |        |    ||    ||
|    | |    |     /   //             /   //        |    ||____|/
|____| |____|    /___//             /___//         |____|
|    | |    |   |`   |             |`   |          |    |
|____| |____|   |____|             |____|          |____|
  \(     )/       \(                 \(              \(
   '     '         '                  '               '
"""

import socket
import sys
import time

get = "GET"
put = "PUT"
post = "POST"
delete = "DELETE"
head = "HEADER"
__metaclass__ = type


def main():
    """Funcao principal para conexao."""
    host = ''
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    print "Servidor rodando na porta %d" % port
    print "Aguardando conexao"
    s.listen(1)
    while 1:
        Conexao(s)


def Parsing(mensagem):
    """Fazendo parsing da mensagem recebida pelo cliente."""
    if get in mensagem:
        try:
            Get_Handler(mensagem)
        except socket.error, e:
            print "Erro ao tratar o request: %s \n" % e
    if put in mensagem:
        try:
            Put_Handler(mensagem)
        except socket.error, e:
            print "Erro ao tratar o request: %s \n" % e


def Conexao(Socketcliente):
    """Abrindo conexao com cliente quando conectado."""
    sockcliente, addrcliente = Socketcliente.accept()
    print "Conectado com o cliente %s" % str(addrcliente)
    arquivocliente = sockcliente.makefile('rw', 0)
    arquivocliente.write("Welcome," + str(addrcliente) + " Digite :\n")
    message = arquivocliente.readline()
    arquivocliente.write("Testando a readline " + str(message))
    message = arquivocliente.readline()
    # Cada input e uma readline difernte, nao precisa manipular
    # Fechando conexao com o cliente no socket e no arquivo
    root = Raiz()
    dire = Diretorio('dire', root)
    arquivocliente.write(root.nome)
    arquivocliente.write(str(root.dir))
    arquivocliente.write(dire.esq)
    arquivocliente.close()
    sockcliente.close()


def msg200_OK():
    """Definindo a mensagem 200 OK."""
    msg = """HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: Closed\r\n\r\n
    <!DOCTYPE HTML PUBLIC>
    <html><head>
    <title>200 OK</title>
    </head><body>
    </body></html>"""
    return msg
    # Definir a arvores para se utilizar como argumentos nas mensagens


def msg201_Created():
    """Definindo mensagem 201, Created."""
    msg = """HTTP/1.1 201 Created\nContent-Type: text/html\nConnection: Closed\r\n\r\n
        <!DOCTYPE HTML PUBLIC>
        <html><head>
        <title>201 Created</title>
        </head><body>
        </body></html>"""
    return msg


def msg_204NoContent():
    """Definindo mensagem 204."""
    msg = """HTTP/1.1 204 No content\nContent-Type: text/html\nConnection: Closed\r\n\r\n
        <!DOCTYPE HTML PUBLIC>
        <html><head>
        <title>204 No content</title>
        </head><body>
        </body></html>"""
    return msg


def msg_400BadRequest():
    """Definindo mensagem 400."""
    msg = """HTTP/1.1 400 Bad request\nContent-Type: text/html\nConnection: Closed\r\n\r\n
        <!DOCTYPE HTML PUBLIC>
        <html><head>
        <title>204 Bad Request</title>
        </head><body>
        </body></html>"""
    return msg


def msg_404NotFound():
    """Definindo mensagem."""
    msg = """HTTP/1.1 501 Not Implemented\nContent-Type: text/html\nConnection: Closed\r\n\r\n
        <!DOCTYPE HTML PUBLIC>
        <html><head>
        <title>501 Not Implemented</title>
        </head><body>
        </body></html>"""
    return msg


def Get_Handler(mensagem):
    """Manejamento do GET."""


def Put_Handler(mensagem):
    """Manejamento do PUT."""


def Post_Handler(mensagem):
    """Manejamento do POST."""


def Delete_Handler(mensagem):
    """Manejamento do DELETE."""


def Header_Handler(mensagem):
    """Manejamento do Header."""


class Arquivo:
    """Definindo a estrutura dos arquivos em arvore."""

    def __init__(self, nome):
        """Inicializando um novo arquivo."""
        self.nome = nome
        self.data = self.data.makefile('rw', 0)

    def put_data(self, data):
        """Colocar dados em um arquivo(post)."""
        try:
            self.data = self.data.write(str(data))
        except OSError, e:
            print "Nao foi possivel abrir o arquivo: %s" % e


class Diretorio:
    """Definindo os diretorios onde os arquivos serao armazenados."""

    def __init__(self, nome, pai):
        """Inicializando um novo diretorio."""
        if type(pai) is Raiz:
            self.esq = '/'
            pai.inserir_na_raiz(self)
        else:
            self.esq = pai
            self.inserir_dentro(self, pai)
        self.dir = []
        self.nome = nome
        self.contem_arquivos = []

    def inserir_dentro(self, pai):
        """Inserir um novo arquivo dentro de um diretorio pai."""
        try:
            pai.dir = pai.dir.extend([self])
        except IndexError, e:
            print "Erro ao inserir o arquivo no diretorio: %s" % e


class Raiz:
    """Definindo raiz dos diretorios."""

    def __init__(self):
        """Inicializando a raiz."""
        self.dir = []
        self.nome = '/'
        self.arquivos = []

    def inserir_na_raiz(self, filho):
        """Inserir um arquivo ou diretorio dentro da raiz."""
        if type(filho) is Diretorio:
            try:
                self.dir.extend([filho])
            except IndexError, e:
                print "Erro ao inserir diretorio na raiz : %s" % e
        if type(filho) is Arquivo:
            try:
                self.arquivos.extend([filho])
            except IndexError, e:
                print "Erro ao inserir arquivo na raiz : %s" % e

    def get_arquivos_raiz(self):
        """Retornando lista de arquivos na raiz."""
        for arquivo in self.arquivos:
            print arquivo

    def get_diretorios_raiz(self):
        """Retornando lista de diretorios na raiz."""
        for diretorio in self.dir:
            print diretorio.nome


main()
