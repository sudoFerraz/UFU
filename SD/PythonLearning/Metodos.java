

//import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.*;
import java.io.*;
import java.text.*;
import java.nio.file.*;

public class Metodos {
    public static void main(String[] args) throws IOException {
        //ServerSocket servidor = new ServerSocket(8000); //cria um socket na porta 8000
        ServerSocket servidor = new ServerSocket(Integer.parseInt(args[0])); //cria um socket na porta 8000
        Nodo raiz = new Nodo("root","arquivo_raiz");
        for (;;) {
            Socket socket = servidor.accept(); //aceita conexoes
            if (socket.isConnected()) {
                System.out.println("\nO computador " + socket.getInetAddress() + " se conectou ao servidor.");
                BufferedReader buffer = new BufferedReader(new InputStreamReader(socket.getInputStream())); //cria um BufferedReader a partir do InputStream
                System.out.println("Requisição: ");
                String linha = buffer.readLine(); //le a linha
                String[] dadosReq = linha.split(" "); //quebra a string pelos espaços em branco
                String metodo = dadosReq[0]; //pega o metodo
                String caminho = dadosReq[1]; //pega o caminho do arquivo
                String protocolo = dadosReq[2]; //pega o protocolo
                System.out.println(linha);
                linha = buffer.readLine();
                dadosReq = linha.split(" ");
                String host = dadosReq[1];
                System.out.println(linha);
                String status = protocolo +" "+ metodo;
                OutputStream resposta;
                String content_length;
                String header;
                String[] caminhoSplitado = caminho.split("/");;
                Nodo nodoGet;
                switch (metodo.toUpperCase()) { //nao eh pra ser case sensitive
                    case "GET":
                        while (!linha.isEmpty()) {
                            linha = buffer.readLine();
                            System.out.println(linha);
                        }
                        nodoGet = raiz.buscar(raiz, caminhoSplitado, 1);
                        if(caminhoSplitado.length == 0){
                            header = status //cabeçalho do HTTP
                                    + " 200 OK\r\n"
                                    + "Version: " + raiz.versao + "\r\n"
                                    + "Creation: " + raiz.creation + "\r\n"
                                    + "Modification: " + raiz.modification + "\r\n"
                                    + "Content-Length: " + raiz.dados.length() + "\r\n"
                                    + "\r\n";
                            resposta = socket.getOutputStream();
                            resposta.write(header.getBytes());
                            resposta.write(raiz.dados.getBytes());
                            resposta.write(("\r\n").getBytes());
                            resposta.flush(); 
                        }else if(nodoGet==null){
                            status = protocolo;
                            header = status
                                    + " 404 Not Found\r\n"
                                    + "\r\n";
                            resposta = socket.getOutputStream();
                            //System.out.println("\n-----------------\n"+header);
                            resposta.write(header.getBytes());
                            resposta.flush();
                        }
                        else{
                            header = status //cabeçalho do HTTP
                                    + " 200 OK\r\n"
                                    + "Version: " + nodoGet.versao + "\r\n"
                                    + "Creation: " + nodoGet.creation + "\r\n"
                                    + "Modification: " + nodoGet.modification + "\r\n"
                                    + "Content-Length: " + nodoGet.dados.length() + "\r\n"
                                    + "\r\n";
                            resposta = socket.getOutputStream(); //utiliza o OutputStream para criar o canal de resposta
                            resposta.write(header.getBytes()); //escreve o cabeçalho em bytes
                            resposta.write(nodoGet.dados.getBytes()); //escreve o conteudo em bytes
                            resposta.write(("\r\n").getBytes());
                            resposta.flush(); //encerra a resposta
                        }
                        break;
                    case "POST":
                        while (true) { 
                            linha = buffer.readLine();
                            if (linha.toUpperCase().contains("CONTENT-LENGTH:")) { 
                                dadosReq = linha.split(" ");
                                content_length = (dadosReq[1]);
                                System.out.println(linha);
                                break;
                            }
                        }
                        while (!linha.isEmpty()) {
                            linha = buffer.readLine();  
                            System.out.println(linha);
                        }
                        char[] tstPost = new char[Integer.parseInt(content_length)];
                        buffer.read(tstPost, 0, Integer.parseInt(content_length));
                        linha = new String(tstPost);
                        
                        Boolean sucessoPost = raiz.adicionar(raiz, caminhoSplitado, 1,linha);                        
                        if(!sucessoPost){
                            status = protocolo;
                            header = status
                                    + " 403 Forbidden"
                                    + "\r\n";
                        }
                        else{
                            nodoGet = raiz.buscar(raiz, caminhoSplitado, 1);
                            header = status
                                    + " 200 OK\r\n"
                                    + "Version: " + nodoGet.versao + "\r\n"
                                    + "Creation: " + nodoGet.creation + "\r\n"
                                    + "Modification: " + nodoGet.modification + "\r\n"
                                    + "\r\n"; 
                        }        
                        resposta = socket.getOutputStream();
                        resposta.write(header.getBytes());
                        resposta.flush();                
                        break;
                    case "PUT":
                        while (true) { 
                            linha = buffer.readLine();
                            if (linha.toUpperCase().contains("CONTENT-LENGTH:")) { 
                                dadosReq = linha.split(" ");
                                content_length = (dadosReq[1]);
                                System.out.println(linha);
                                break;
                            }
                        }
                        while (!linha.isEmpty()) {
                            linha = buffer.readLine();
                            System.out.println(linha);
                        }
                        char[] tstPut = new char[Integer.parseInt(content_length)];
                        buffer.read(tstPut, 0, Integer.parseInt(content_length));
                        linha = new String(tstPut);
                        
                        Boolean sucessoPut = raiz.alterar(raiz, caminhoSplitado, 1,linha);                        
                        if(!sucessoPut){
                            status = protocolo;
                            header = status
                                    + " 403 Forbidden"
                                    + "\r\n";
                        }
                        else{
                            nodoGet = raiz.buscar(raiz, caminhoSplitado, 1);
                            header = status
                                    + " 200 OK\r\n"
                                    + "Version: " + nodoGet.versao + "\r\n"
                                    + "Creation: " + nodoGet.creation + "\r\n"
                                    + "Modification: " + nodoGet.modification + "\r\n"
                                    + "\r\n";
                        }
                        resposta = socket.getOutputStream();
                        resposta.write(header.getBytes());
                        resposta.flush();
                        break;
                    case "DELETE":
                        while (!linha.isEmpty()) {
                            linha = buffer.readLine();
                            System.out.println(linha);
                        }
                        
                        Boolean sucessoDelete = raiz.remover(raiz, caminhoSplitado, 1);
                        if(!sucessoDelete){
                            status = protocolo;
                            header = status
                                    + " 403 Forbidden"
                                    + "\r\n";
                        }
                        else{
                            header = status
                                    + " 200 OK\r\n";
                        }
                        resposta = socket.getOutputStream();
                        resposta.write(header.getBytes());
                        resposta.flush();
                        break;
                    case "HEAD":
                        while (!linha.isEmpty()) {
                            linha = buffer.readLine();
                            System.out.println(linha);
                        }
                        nodoGet = raiz.buscar(raiz, caminhoSplitado, 1);
                        if(nodoGet==null){
                            status = protocolo;
                            header = status
                                    + " 404 Not Found"
                                    + "\r\n";
                        }
                        else{
                            header = status //cabeçalho do HTTP
                                    + " 200 OK\r\n"
                                    + "Version: " + nodoGet.versao + "\r\n"
                                    + "Creation: " + nodoGet.creation + "\r\n"
                                    + "Modification: " + nodoGet.modification + "\r\n"
                                    + "Content-Length: " + nodoGet.dados.length() + "\r\n"
                                    + "\r\n";                            
                        }
                        resposta = socket.getOutputStream();
                        resposta.write(header.getBytes());
                        resposta.flush();
                        break;
                    default:
                        status = protocolo;
                        header = status
                                + " 501 metodo nao implementado"
                                + "\r\n";
                        resposta = socket.getOutputStream();
                        resposta.write(header.getBytes());
                        resposta.flush();
                }
            }
            socket.close();
        }
    }
}
