import socket
import os
import sys
import math
import time
import subprocess
import json

BUFFER_SIZE = 1024
VID_ARR_SIZE = 3
EXIT = -1
WAIT = -2
video_array = ["./Conteudo/BigBuckBunny.mp4","./Conteudo/Bear.mp4","./Conteudo/Wildlife.mp4"]

def get_vid_time(vid_path) -> int:
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', vid_path],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    output = json.loads(result.stdout)

    duration = float(output['format']['duration'])

    return int(duration)

def get_bit_rate(vid_path):
    byte_por_segundo = int(os.path.getsize(vid_path)/get_vid_time(vid_path)) # byte / seg
    return byte_por_segundo 

def wait_message():
    
    try:
            message, addr = socket_udp.recvfrom(BUFFER_SIZE)
            message = message.decode()
            return message, addr
    except socket.error as e:
        print(f"Erro ao receber mensagem: {e}")

try:
    message = b''
    socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP
    endereco_servidor = ('localhost', 12345)  # Endereço e porta do servidor
    socket_udp.bind(endereco_servidor)  # Liga o socket ao endereço e porta

    print(f"Servidor UDP está rodando na porta {endereco_servidor[1]}")
    print("Aguardando mensagens...")

    while True:

        print("esperando por novos pedidos :)")
    
        message, addr = wait_message()

        # Pega tamanho do vídeo escolhido
        try:
            index = int(message)
            byte_rate = get_bit_rate(video_array[index])
            print(f"Para o video {video_array[index]}, a vazão necessaria de {byte_rate} bits por segundo")
        except FileNotFoundError:
            print(f"Erro: Arquivo '{video_array[index]}' não encontrado.")
        except OSError as e:
            print(f"Erro ao acessar o arquivo: {e}")
            
        with open(video_array[index], "rb") as arquivo:
            vezes = 0
            while True:
                # Bites devem ser compostos por: bytes de vídeo
                bytes = arquivo.read(BUFFER_SIZE)
                if not bytes:
                    socket_udp.sendto(b'EOF', addr)  # Marcador de fim de pacote
                    break

                socket_udp.sendto(bytes, addr) 
                vezes += 1                       
                print(f'\rPacote {vezes} enviado!', end='')

                # Calcular o tempo de espera
                time_to_wait = len(bytes)/byte_rate  # tempo em segundos
                # print(f"\rtime_to_wait ={time_to_wait}", end=)
                time.sleep(time_to_wait)  # Pausa para controlar a vazão

            print("\nArquivo enviado!")

            # espera cliente fechar vlc
            



except socket.error as e:
    print(f"Erro ao criar ou ligar o socket: {e}")

finally:
    socket_udp.close()
    print("Socket fechado")
