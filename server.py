
import socket
import os
import time
import subprocess
import json
import threading

BUFFER_SIZE = 1024 * 2

# Eventos do cliente
new_command = threading.Event()

client_command = b''

def get_vid_time(vid_path) -> int:
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', vid_path],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = json.loads(result.stdout)
    duration = float(output['format']['duration'])
    return int(duration)

def get_bit_rate(vid_path):
    byte_por_segundo = int(os.path.getsize(vid_path) / get_vid_time(vid_path))  # byte / seg
    return byte_por_segundo

# Talvez podemos descontinuar essa funcao
def wait_message():
    try:
        # message, addr = socket_UDP.recvfrom(BUFFER_SIZE)
        message, = socket_UDP.recvfrom(BUFFER_SIZE)
        message = message.decode()
        # return message, addr
        return message
    except socket.error as e:
        print(f"Erro ao receber mensagem TCP: {e}")
        # return None, None
        return None

def client_command_thread(specific_client):
    global client_command
    try:
        # escuta novas instrucoes do cliente
        while True:
            if client_command != b'':
                client_command = specific_client.recv(BUFFER_SIZE)
                # avisa que recebeu uma nova
                new_command.set()
                # quando o comando eh final
                print(f"Comando {client_command.decode()} recebido!")
                if client_command == b'0':
                    specific_client.close()
                    break
    except socket.error as e:
        print(f"Erro ao receber comando TCP: {e}")
    finally:
        specific_client.close()

if __name__ == "__main__":
    video_array = ["./Conteudo/BigBuckBunny.mp4", "./Conteudo/Bear.mp4", "./Conteudo/Wildlife.mp4"]
    server = 'localhost'
    try:

        # Agente podia encapsular a criacao do udp e do tcp separadamente
        # liga o UDP e em seguida o TCP com thread

        # Cria sockets UDP e TCP
        socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        UDP_PORT = 12345
        TCP_PORT = 54321

        # Define endereços e portas separadamente para UDP e TCP
        addr_server_UDP = (server, UDP_PORT)
        addr_server_TCP = (server, TCP_PORT)

        # Liga cada socket ao seu respectivo endereço e porta
        socket_UDP.bind(addr_server_UDP)
        socket_TCP.bind(addr_server_TCP)

        # espera por conecoes
        socket_TCP.listen()

        print(f"Endereço servidor: [{addr_server_UDP[0]}]\nUDP port:[{addr_server_UDP[1]}] TCP port:[{addr_server_TCP[1]}]")
        
        # aceita um pedido
        specific_client, addr_TCP = socket_TCP.accept()
        
        print(f'Cliente TCP conectado: {addr_TCP}')
        
        # passa para a thread a responsabilidade de ouvir mensagens
        thread = threading.Thread(target=client_command_thread, args=(specific_client,))
        thread.start()

        while client_command != 0:
            print("Esperando por novos pedidos UDP ;)")
            
            # Espera por um novo comando do cliente, Client_command recebeu um novo valor
            print("esperando por novo comando")
            new_command.wait()
            print("comando recebido !")
            # Pega tamanho do vídeo escolhido
            try:
                index = int(client_command) - 1

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
                        socket_UDP.sendto(b'EOF', addr_TCP)  # Marcador de fim de pacote
                        break

                    socket_UDP.sendto(bytes, addr_TCP)
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
