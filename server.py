import socket
import os
import time
BUFFER_SIZE = 1024

caminho_video = "./conteudo/Bear.mp4"
tamanho_arquivo = os.path.getsize(caminho_video)
print(tamanho_arquivo)

# Cria um socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Endereço e porta do servidor
endereco_servidor = ('LocalHost', 12345)

# Liga o socket ao endereço e porta
socket_udp.bind(endereco_servidor)

print(f"Servidor UDP está rodando na porta {endereco_servidor[1]}")
print("Aguardando mensagens...")

while True:
    # recebendo mensagem
    message, addr = socket_udp.recvfrom(BUFFER_SIZE)  # 1024 é o buffer size
    message = message.decode()
    print("recebido: " + message)
    if message == "envia":
        with open(caminho_video, "rb") as arquivo:
            while True:
                bites = arquivo.read(BUFFER_SIZE)
                if not bites:
                    break
                socket_udp.sendto(bites, addr)
                time.sleep(0.01)
        # Marcador de fim de pacote
        socket_udp.sendto(b'EOF', addr)
        print("arquivo enviado!")
