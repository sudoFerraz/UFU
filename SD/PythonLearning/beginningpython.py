
"""

  ______                                   __
 /      \                                 /  |
/$$$$$$  |  ______   __    __   ______   _$$ |_     ______
$$ |  $$/  /      \ /  |  /  | /      \ / $$   |   /      \
$$ |      /$$$$$$  |$$ |  $$ |/$$$$$$  |$$$$$$/   /$$$$$$  |
$$ |   __ $$ |  $$/ $$ |  $$ |$$ |  $$ |  $$ | __ $$ |  $$ |
$$ \__/  |$$ |      $$ \__$$ |$$ |__$$ |  $$ |/  |$$ \__$$ |
$$    $$/ $$ |      $$    $$ |$$    $$/   $$  $$/ $$    $$/
 $$$$$$/  $$/        $$$$$$$ |$$$$$$$/     $$$$/   $$$$$$/
                    /  \__$$ |$$ |
                    $$    $$/ $$ |
                     $$$$$$/  $$/
"""

import sys
import socket
import os

Exchanges = ('BTC-e',)
URLs = ('https://btc-e.com/api/3/ticker/btc_usd',)
port = 80
user = sys.argv[1]
pwd = sys.argv[2]
users = {
    'root': 'toor',
    'dpr': 'rogers'
}



def Hello():
    print "[+]Bem vindo ao cryptowatcher do %s\n" % user
    print "Temos varias opcoes pre-built e customizaveis\n"


def Conexao():
    opt = raw_input('[+]Digite o nro da exchange para se conectar, ou o nome para criar uma nova Conexao: ')
    if opt == '0':
        print "\nVoce escolheu a opcao %s" % Exchanges

def Verifica_senha():
    if pwd == users[user]:
        print "Logado com sucesso \n"
    else:
        sys.exit(1)

def Menu():
    largura = input('Entre com o tamanho do menu da sua tela: ')
    opt_largura = 10
    item_largura = largura - opt_largura

    formato_cabecalho = '%-*s%*s'
    formata = '%-*s%*.2f'

    print '-' * largura

    print formata % (item_largura, 'BTC-e', opt_largura, 1)
    print formata % (item_largura, 'Foxbit', opt_largura, 2)
    print formata % (item_largura, 'Mtgox', opt_largura, 3)

    print '=' * largura



def Logado():
    Hello()
    print Exchanges[0] + ' : ' + URLs[0] + '\n'

def Main():
    print "\n[+]Verificando seu usuario e senha\n"
    if user in users:
        Verifica_senha()
        Logado()
        Menu()

    else:
        print "Seu usuario nao consta no banco de dados, tente denovo"

Main()
