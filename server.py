import socket
import _tkinter
from PIL import Image

arquivo_a_ser_enviado = Image.open('.\\conteudo\\liminha.jpg')
# Cria um socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Endereço e porta do servidor
endereco_servidor = ('LocalHost', 12345)

# Liga o socket ao endereço e porta
udp_socket.bind(endereco_servidor)

print(f"Servidor UDP está rodando na porta {endereco_servidor[1]}")
print("Aguardando mensagens...")
flag = 1
while(flag == 1):
    
    data, addr = udp_socket.recvfrom(1024)  # 1024 é o buffer size
    print(f"Recebido de {addr}: {data.decode()}")
    print("com cast")
    data = int(data)
    # if data == 1:
    #     print("antes")
    #     udp_socket.sendto(arquivo_a_ser_enviado, endereco_servidor)
    #     print("depois")
   
