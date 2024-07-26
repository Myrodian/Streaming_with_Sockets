import socket
import os
import sys
import math
import time
BUFFER_SIZE = 3076
video_array = ["./conteudo/BigBuckBunny.mp4","./conteudo/Bear.mp4", "./conteudo/Wildlife.mp4"]
# video_array[] = "EOF"
def stop():
    try:
        controle, addr = socket_udp.recvfrom(BUFFER_SIZE)
        if controle.decode() == '1':
            return True
    except socket.error as e:
        print(f"Erro ao receber controle: {e}")
        return False
try:
    socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP
    endereco_servidor = ('localhost', 12345)  # Endereço e porta do servidor
    socket_udp.bind(endereco_servidor)  # Liga o socket ao endereço e porta

    print(f"Servidor UDP está rodando na porta {endereco_servidor[1]}")
    print("Aguardando mensagens...")

    while True:
        try:
            # Recebendo mensagem
            message, addr = socket_udp.recvfrom(BUFFER_SIZE)
            message = message.decode()
            print(f"Recebido: {message}")

            # Seletor de vídeo
            if message == "envia":
            # Pega tamanho do vídeo escolhido
                try:
                    tamanho_arquivo = os.path.getsize(video_array[0])
                    print(f"Tamanho do arquivo: {tamanho_arquivo} bytes\nSerão necessarios {int(tamanho_arquivo/BUFFER_SIZE)+1} pacotes")
                except FileNotFoundError:
                    print(f"Erro: Arquivo '{video_array[0]}' não encontrado.")
                    continue
                except OSError as e:
                    print(f"Erro ao acessar o arquivo: {e}")
                    continue

                with open(video_array[0], "rb") as arquivo:
                    f = 0
                    vezes = 0
                    while True:
                        # Bites devem ser compostos por: bytes de vídeo
                        bites = arquivo.read(BUFFER_SIZE)
                        if not bites:
                            socket_udp.sendto(b'EOF', addr)  # Marcador de fim de pacote
                            break
                        socket_udp.sendto(bites, addr) 
                        vezes += 1                       
                        print(f'\rPacote {vezes} enviado!', end='')
                        try:
                            controle, addr = socket_udp.recvfrom(BUFFER_SIZE)
                            controle = controle.decode()
                            if controle == '1':
                                f += 1
                                # tinha linhas aqui, mas foi tirado após remover o shipping_size
                        except socket.error as e:
                            print(f"Erro ao receber controle: {e}")
                            break
                print("\nArquivo enviado!")

        except socket.error as e:
            print(f"Erro ao receber mensagem: {e}")

except socket.error as e:
    print(f"Erro ao criar ou ligar o socket: {e}")

finally:
    socket_udp.close()
    print("Socket fechado")