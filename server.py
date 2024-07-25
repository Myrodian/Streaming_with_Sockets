import socket
import os
import sys
import math
import time
BUFFER_SIZE = 1024
SHIPPING_SIZE = 5

# calcula o numero de pacotes(pkg) que um tamanho de arquivo pode ser dividido pelo buffer 
def pkg_num(f_size: int) -> int:
    return math.ceil(f_size/BUFFER_SIZE)

# calcula o numero de bytes p/ um numero x
def bytes_needed(x: int) -> int:
    if x == 0:
        return 1  # Um byte é suficiente para armazenar o número 0
    # Calcular o número de bytes necessários (int -> bit -> byte)
    return math.ceil(x.bit_length() / 8) 

# calcula e envia para o cliente o tamanho do cabecaho de identificadores
# o cliente deve esperar o seervidor enviar dentro de um tempo limite ( 5s talvez ), se não, pedir de novo
def send_header_size(f_size, addr):
    # cliente precisa esperar 1 ciclo antes de começar a tocar o video
    socket_udp.sendto(bytes_needed(pkg_num(f_size)), addr)
    print("header size: "+ bytes_needed(pkg_num(f_size)))

# travado até receber um codigo de liberacao
def stop():
    controle, addr = socket_udp.recvfrom(BUFFER_SIZE)
    # print(sys.getsizeof(controle))
    # print("chegando dps do shipping")
    if (controle.decode()) == '1':
        return (True)

i = 0
caminho_video = "EOF"


# Cria um socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Endereço e porta do servidor
endereco_servidor = ('localhost', 12345)

# Liga o socket ao endereço e porta
socket_udp.bind(endereco_servidor)

print(f"Servidor UDP está rodando na porta {endereco_servidor[1]}")
print("Aguardando mensagens...")

while True:
    # recebendo mensagem
    message, addr = socket_udp.recvfrom(BUFFER_SIZE)  # 1024 é o buffer size
    message = message.decode()
    print(f"recebido:{message}")

    # seletor de video
    if message == "envia":
        caminho_video = "./conteudo/Bear.mp4"
    
    # pega tamanho do video escolhido
    tamanho_arquivo = os.path.getsize( caminho_video)
    
    print("arqv tamanho: "+tamanho_arquivo)

    send_header_size(tamanho_arquivo, addr)

    with open(caminho_video, "rb") as arquivo:
        f = 0
        while True:

            # bites dever ser composto por: cabecalho + bytes de video, ainda não pensei como fazer 
            bites = arquivo.read(BUFFER_SIZE - header)
            if not bites:
                socket_udp.sendto(b'EOF', addr) # Marcador de fim de pacote
                break
            socket_udp.sendto(bites, addr)
            
            i += 1
            
            if i == SHIPPING_SIZE:
                controle, addr = socket_udp.recvfrom(BUFFER_SIZE)
                controle = controle.decode()
                # print(sys.getsizeof(controle))
                # print("chegando dps do shipping")
                if controle == '1':
                    # print(f"enviando remessa {f} para o endereço {addr}")
                    i = 0
                    f += 1
        # "limpa o valor do ultimo pedido"
        caminho_video = "EOF"
        
        print("arquivo enviado!")
