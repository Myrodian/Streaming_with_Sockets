import socket


# Cria um socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Endereço e porta do servidor
endereco_servidor = ("LocalHost", 12345)


try:
    # Mensagem a ser enviada ao servidor
    print("Qual a mensagem?:")
    message = input()
    # Envia a mensagem
    print(f"Enviando: {message}")
    sent = socket_udp.sendto(message.encode(), endereco_servidor)

    # Recebe a resposta (opcional, dependendo do servidor)
    print("Aguardando resposta...")
    data, server = socket_udp.recvfrom(1024)
    print(f"Recebido: {data}")
    # print("aqui")
    print(socket.gethostbyaddr())
    # print("aqui2")
finally:
    print("Fechando o socket")
    socket_udp.close()

