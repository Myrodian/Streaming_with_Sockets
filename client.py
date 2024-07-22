import socket

BUFFER_SIZE = 1024

# Cria um socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Endereço e porta do servidor
endereco_servidor = ("LocalHost", 12345)

while True:
    # Mensagem a ser enviada ao servidor
    message = input("Digite a mensagem:")
    socket_udp.sendto(message.encode(), endereco_servidor)
    if message == "envia":
        with open("Bear.mp4", "wb") as arquivo:
            while True:
                data, addr = socket_udp.recvfrom(BUFFER_SIZE)  # 1024 é o buffer size
                if not data.strip(b'\x00'):
                    break
                arquivo.write(data)
        print("arquivo recebido e salvo como Bear.mp4")
