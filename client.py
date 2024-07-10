import socket


# Cria um socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Endereço e porta do servidor
server_address = ("LocalHost", 12345)

try:
    # Mensagem a ser enviada ao servidor
    
    message = input()
    # Envia a mensagem
    print(f"Enviando: {message}")
    sent = udp_socket.sendto(message.encode(), server_address)

    # Recebe a resposta (opcional, dependendo do servidor)
    print("Aguardando resposta...")
    data, server = udp_socket.recvfrom(1024)
    print(f"Recebido: {data}")
    print("aqui")
    print(socket.gethostbyaddr())
    print("aqui2")
finally:
    print("Fechando o socket")
    udp_socket.close()
