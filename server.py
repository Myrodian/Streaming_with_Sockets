import socket
import os
import time
import subprocess
import json
import threading

BUFFER_SIZE = 1024
server = 'localhost'

video_array = ["./Conteudo/BigBuckBunny.mp4", "./Conteudo/Bear.mp4", "./Conteudo/Wildlife.mp4"]

def get_vid_time(vid_path) -> int:
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', vid_path],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = json.loads(result.stdout)
    duration = float(output['format']['duration'])
    return int(duration)

def get_bit_rate(vid_path):
    byte_por_segundo = int(os.path.getsize(vid_path) / get_vid_time(vid_path))  # byte / seg
    return byte_por_segundo

def wait_message():
    try:
        message, addr = socket_UDP.recvfrom(BUFFER_SIZE)
        message = message.decode()
        return message, addr
    except socket.error as e:
        print(f"Erro ao receber mensagem UDP: {e}")
        return None, None

def handle_client_connection(client_socket):
    try:
        while True:
            command = client_socket.recv(BUFFER_SIZE)
            if not command:
                break
            print(f"Comando {command.decode()} recebido!")
            if command == b'0':
                break
    except socket.error as e:
        print(f"Erro ao receber comando TCP: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    try:
        # Cria sockets UDP e TCP
        socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define endereços e portas separadamente para UDP e TCP
        addr_server_UDP = (server, 12345)
        addr_server_TCP = (server, 54321)

        # Liga cada socket ao seu respectivo endereço e porta
        socket_UDP.bind(addr_server_UDP)
        socket_TCP.bind(addr_server_TCP)
        socket_TCP.listen(5)

        print(f"Servidor está rodando {addr_server_UDP[0]} na porta UDP {addr_server_UDP[1]} e na porta TCP {addr_server_TCP[1]}")

        def start_command_thread():
            while True:
                client_socket, addr = socket_TCP.accept()
                print(f"Cliente TCP conectado: {addr}")
                client_thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
                client_thread.start()

        # Inicia a thread para lidar com comandos TCP
        command_thread = threading.Thread(target=start_command_thread)
        command_thread.start()

        while True:
            print("Esperando por novos pedidos UDP :)")
            message, addr = wait_message()

            if message is None:
                continue

            # Pega tamanho do vídeo escolhido
            try:
                index = int(message)
                index = index - 1
                byte_rate = get_bit_rate(video_array[index])
                print(f"Para o vídeo {video_array[index]}, a vazão necessária é de {byte_rate} bits por segundo")
            except FileNotFoundError:
                print(f"Erro: Arquivo '{video_array[index]}' não encontrado.")
            except OSError as e:
                print(f"Erro ao acessar o arquivo: {e}")

            with open(video_array[index], "rb") as arquivo:
                vezes = 0
                while True:
                    bytes = arquivo.read(BUFFER_SIZE)
                    if not bytes:
                        socket_UDP.sendto(b'EOF', addr)  # Marcador de fim de pacote
                        break

                    socket_UDP.sendto(bytes, addr)
                    vezes += 1

                    # Calcular o tempo de espera
                    time_to_wait = len(bytes) / byte_rate
                    time.sleep(time_to_wait)  # Pausa para controlar a vazão
                print("\nArquivo enviado!")

    except socket.error as e:
        print(f"Erro ao criar ou ligar o socket: {e}")
    finally:
        socket_UDP.close()
        socket_TCP.close()
        print("Sockets fechados")
