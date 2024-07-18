import socket
import _tkinter
import os

size_file = os.path.getsize("./conteudo/Bear.mp4")
print(size_file)
BUFFER_SIZE = 10000
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
    data, addr = socket_udp.recvfrom(10000)  # 1024 é o buffer size
    data = data.decode()
    print("recebido: " + data)
    if data == "envia":
        with open("./conteudo/Bear.mp4", "rb") as arquivo:
            while True:
                bites = arquivo.read(BUFFER_SIZE)
                print(bites)
                if not bites:
                    break
                socket_udp.sendto(bites, addr)
        print("arquivo enviado!")

    # print(f"Recebido de {addr}: {data}")
    
    # mandando mensagem
    # message = input("Digite a mensagem:")
    # sent = socket_udp.sendto(message.encode(), addr)
    
    
   
