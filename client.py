import socket


# Cria um socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Endereço e porta do servidor
endereco_servidor = ("LocalHost", 12345)

while True:

	# Mensagem a ser enviada ao servidor
	message = input("Digite a mensagem:")
	# print(f"Enviando: {message}")
	socket_udp.sendto(message.encode(), endereco_servidor)
	with open("Bear.mp4", "wb") as arquivo:
		while True:
			data, addr = socket_udp.recvfrom(10000)  # 1024 é o buffer size
			print(data)
			if not data:
				break
			arquivo.write(data)
		

    # Recebe a mensagem
    # data, addr = socket_udp.recvfrom(1024)  # 1024 é o buffer size
    # data = data.decode()
    # print(f"Recebido de {addr}: {data}")
    # print(socket.gethostbyaddr())
      

