int main(){
Sockets():
  Quando criar um objeto socket, passar como argumento o tipo de conexao
  e a familia de protocolos.
  communication type : AF_INET = IPV4
  protocol family : SOCK_STREAM = TCP
                    SOCK_DGRAM = UDP

  Criando um socket >  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  Conectando um socket, 'e necessario passar como argumento uma tupla contendo
  o hostname ou ip, e a porta de conexao > s.connect(("www.ferraz.com", 80))

  Obs. No C nao da pra passar hostname pois ele n checa no DNS, apenas IP

  Procurando uma porta para conexao pelo nome > s.getservbyname('http', 'tcp')



}
