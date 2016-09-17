int main(){
Sockets():
  Quando criar um objeto socket, passar como argumento o tipo de conexao
  e a familia de protocolos.
  communication type : AF_INET = IPV4
  protocol family : SOCK_STREAM = TCP
                    SOCK_DGRAM = UDP

  Criando um socket >  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  Conectando um socket, e necessario passar como argumento uma tupla contendo
  o hostname ou ip, e a porta de conexao > s.connect(("www.ferraz.com", 80))

  Obs. No C nao da pra passar hostname pois ele n checa no DNS, apenas IP

  Procurando uma porta para conexao pelo nome > s.getservbyname('http', 'tcp')

  Depois de mandar todos os dados, uma boa pratica e utilizar o shutdown()
  com uma exception handler pra verificar se todos os dados foram enviados
  sem nenhum erro, ou se o servidor nao desconectou.

  socket.gaierror = Zuou quando tentou resolver o endereco

}

Servidores :
Criar o objeto socket
setar as opcoes dele
Bindar ele a uma porta(e opcionalmente a uma placa de rede)
Esperar por conexoes
