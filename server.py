import socket

# Cria um socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Endereço e porta do servidor
server_address = ('0.0.0.0', 12345)

# Liga o socket ao endereço e porta
udp_socket.bind(server_address)

print(f"Servidor UDP está rodando na porta {server_address[1]}")

print("Aguardando mensagens...")

while True:
    data, addr = udp_socket.recvfrom(1024)  # 1024 é o buffer size
    print(f"Recebido de {addr}: {data.decode()}")
