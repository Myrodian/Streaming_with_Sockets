import socket
import os

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
    data, addr = socket_udp.recvfrom(BUFFER_SIZE)  # 1024 é o buffer size
    data = data.decode()
    print("recebido: " + data)
    if data == "envia":
        with open(caminho_video, "rb") as arquivo:
            while True:
                bites = arquivo.read(BUFFER_SIZE)
                if not bites:
                    break
                socket_udp.sendto(bites, addr)
        # Enviar um pacote final vazio para indicar o término da transmissão
        socket_udp.sendto(b''.ljust(BUFFER_SIZE), addr)
        print("arquivo enviado!")
