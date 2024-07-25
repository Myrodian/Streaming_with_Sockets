import socket
import os
import sys
import time
BUFFER_SIZE = 1024
SHIPPING_SIZE = 5

i = 0
caminho_video = "./conteudo/Bear.mp4"
tamanho_arquivo = os.path.getsize(caminho_video)
print(tamanho_arquivo)

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
    
    if message == "envia":
        with open(caminho_video, "rb") as arquivo:
            f = 0
            while True:
                bites = arquivo.read(BUFFER_SIZE)
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

        
        print("arquivo enviado!")
