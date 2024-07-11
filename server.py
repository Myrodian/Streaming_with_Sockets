import socket
import _tkinter
from PIL import Image

# arquivo_a_ser_enviado = Image.open('.\\conteudo\\liminha.jpg')
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
    data, addr = socket_udp.recvfrom(1024)  # 1024 é o buffer size
    data = data.decode()
    print(f"Recebido de {addr}: {data}")
    
    # mandando mensagem
    message = input("Digite a mensagem:")
    sent = socket_udp.sendto(message.encode(), addr)
    
    # if data == 1:
    #     print("antes")
    #     udp_socket.sendto(arquivo_a_ser_enviado, endereco_servidor)
    #     print("depois")
   
