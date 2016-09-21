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
import string
import re

get = "GET"
put = "PUT"
post = "POST"
delete = "DEL"
header = "HEADER"
__metaclass__ = type
varpost = 0


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
    arq1 = Fileserver("arq1")
    root.insere(arq1)
    arq2 = Fileserver("arq2")
    arq3 = Fileserver("arq3")
    arq1.insere(arq2)
    arq2.insere(arq3)
    arq3.insere_dados("iejfioejofijapoefk")
    while 1:
        Conexao(s)


def Conexao(Socketcliente):
    """Abrindo conexao com cliente quando conectado."""
    sockcliente, addrcliente = Socketcliente.accept()
    print "Conectado com o cliente %s" % str(addrcliente)
    arquivocliente = sockcliente.makefile('rw', 0)
    arquivocliente.write("Welcome," + str(addrcliente) + " Digite :\n")
    c = "\n\n\n"
    message = sockcliente.recv(1024)
    while 1:
        message += sockcliente.recv(1024)
        if c in message:
            break
    metodo, caminhoSplitado, corpo = Parsing(message)
    print metodo
    print caminhoSplitado
    resultado = metodo_handler(metodo, caminhoSplitado, corpo)
    arquivocliente.write(resultado)
    arquivocliente.close()
    sockcliente.close()


def metodo_handler(metodo, caminho, corpo):
    """Definindo qual metodo e qual handler usar, retorna mensagem."""
    if metodo == get:
        objeto = acha_objeto(caminho)
        resposta = Get_Handler(objeto)
        # fazer a mensagem correta com o codigo e os dados
        return resposta
    elif metodo == post:
        Post_Handler(caminho)
    elif metodo == put:
        objeto = acha_objeto(caminho)
        resposta = Put_Handler(objeto, corpo)
        return resposta
    elif metodo == delete:
        objeto = acha_objeto(caminho)
        resposta = Delete_Handler(objeto)
        return resposta
    elif metodo == header:
        Header_Handler(caminho)


def acha_objeto(caminho):
    """Procura o objeto no qual o caminho termina."""
    nodo = root
    if len(caminho) == 1 and caminho[0] == '':
        return root
    elif caminho[0] != '':
        for i in range(0, len(root.filhos), 1):
            if caminho[0] == root.filhos[i].nome:
                nodo = root.filhos[i]
        for i in range(1, len(caminho), 1):
            for j in range(0, len(nodo.filhos), 1):
                if caminho[i] == nodo.filhos[j].nome:
                    nodo = nodo.filhos[j]
    if caminho[len(caminho)-1] != nodo.nome:
        nodo = None
        return None
    elif caminho[len(caminho)-1] == nodo.nome:
        return nodo


def Parsing(message):
    """Faz parsing e separa uma lista para o metodo e caminhos splitados."""
    linhas = message.split("\n")
    data = message.split("\n\n")
    data = data[1]
    linhas2 = linhas[0].split(" HTTP")
    linhas3 = linhas2[0].split(" /")
    caminho = linhas3[1].split("/")
    metodo = linhas3[0]
    return metodo, caminho, data


def traduz(mensagem):
    """Coloca mensagem em plaintext."""
    mensagem = mensagem.replace("\n", " ")
    return mensagem


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


def Get_Handler(objeto):
    """Manejamento do GET."""
    if objeto is None:
        mensagem = msg_404NotFound()
    else:
        mensagem = objeto.data
    # Fazer a mensagem correta junto com a msg
    return mensagem


def Post_Handler(caminho, dados):
    """Manejamento do POST(cria)."""
    nodo = root
    if len(caminho) == 1 and caminho[0] == '':
        message = msg_400BadRequest()
        return message
    elif caminho[0] != '':
        for i in range(0, len(caminho), 1):
            for j in range(0, len(nodo.filhos), 1):
                if caminho[i] == nodo.filhos[j].nome:
                    nodo = nodo.filhos[j]
                    break
            if caminho[i] != nodo.nome:
                pos = i
                break
    novonodo = Fileserver(caminho[pos])
    nodo.insere(novonodo)
    ptnodo = novonodo
    for k in range(pos+1, len(caminho), 1):
        novonodo = Fileserver(caminho[k])
        # achar um meio de renomear os novos nodos para insercao
        ptnodo.insere(novonodo)
        ptnodo = novonodo


def Delete_Handler(objeto):
    """Manejamento do DELETE."""
    if objeto is None:
        mensagem = msg_404NotFound()
    else:
        objeto.remove_arq()
        mensagem = msg200_OK()
    return mensagem


def Put_Handler(objeto, dados):
    """Manejamento do PUT(modifica dados)."""
    if objeto is None:
        mensagem = msg_404NotFound()
    else:
        objeto.data = dados
        mensagem = msg200_OK()
    return mensagem


def Header_Handler(mensagem):
    """Manejamento do Header."""


class controle_global():
    """Lista com todos os arquivos ja criados."""

    def __init__(self, nome):
        """Inicializa a lista global."""
        self.criados = []


class Fileserver():
    """Definindo estrutura do servidor de arquivos."""

    def __init__(self, nome):
        """Inicializando um arquivo na arvore(diretorio tambem)."""
        self.nome = nome
        self.filhos = []
        self.nomefilhos = []
        self.data = None
        self.pai = None
        self.nomepai = ''
        self.created = int(time.time())
        self.modified = int(time.time())

    def insere(self, filho):
        """Inserir na lista de arquivos subjacentes."""
        self.filhos.append(filho)
        self.nomefilhos.append(filho.nome)
        filho.pai = self

    def insere_dentro(self, pai):
        """Insere arquivo dentro de um pai."""
        pai.filhos.append(self)
        pai.nomefilhos.append(self.nome)

    def insere_dados(self, data):
        """Insere dados dentro de um arquivo."""
        self.data = data
        self.modified = int(time.time())

    def remove_filho(self, filho):
        """Remove um arquivo do diretorio."""
        self.filhos.extend(filho.filhos)
        self.filhos.remove(filho)
        self.nomefilhos.remove(filho.nome)
        self.modified = int(time.time())
        del filho

    def remove_arq(self):
        """Remove o proprio arquivo que chama."""
        self.pai.filhos.extend(self.filhos)
        self.pai.filhos.remove(self)
        self.pai.nomefilhos.remove(self.nome)
        self.pai.modified = int(time.time())
        del self

    def get_dados(self):
        """Devolve os dados guardados no arquivo."""
        return self.data


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
            print str(diretorio.nome)

root = Fileserver("/")
main()
