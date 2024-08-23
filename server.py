
import socket
import os
import time
import subprocess
import json
import threading

UDP_PORT = 12345
TCP_PORT = 54321
HOST_IP = 'localhost'
BUFFER_SIZE = 1024 * 2
# Eventos do cliente
chossing_video = threading.Event()
new_command = threading.Event()

def create_TCP():
    try:
        socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        socket_TCP.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        socket_TCP.bind((HOST_IP, TCP_PORT))
        print("===========================SOCKET_TCP===========================")
        print(f"Endereço servidor: [{HOST_IP}]\nTCP port:[{TCP_PORT}]")
        socket_TCP.listen()
        specific_client, addr_TCP = socket_TCP.accept()
        print(f'Cliente TCP conectado: {addr_TCP}')
        print("================================================================")
    except socket.error as e:
        print(f"Erro ao criar ou ligar o socket no TCP: {e}")
    finally:
        return specific_client, addr_TCP, socket_TCP
    
    
def create_UDP():
    try: 
        socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_UDP.bind((HOST_IP, UDP_PORT))
        msg, addr_client_UDP = socket_UDP.recvfrom(BUFFER_SIZE)
        print("===========================SOCKET_UDP===========================")
        print(f"Endereço servidor: [{HOST_IP}]\nUDP port:[{UDP_PORT}]")
        print(f"cliente UDP conectado: {addr_client_UDP}")
        print("================================================================")
    except socket.error as e:
        print(f"Erro ao criar ou ligar o socket no UDP: {e}")
    finally:
        return addr_client_UDP, socket_UDP
    
def get_vid_time(vid_path) -> int:
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', vid_path],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = json.loads(result.stdout)
    duration = float(output['format']['duration'])
    return int(duration)

def get_byte_rate(vid_path):
    try:
        byte_por_segundo = int(os.path.getsize(vid_path) / get_vid_time(vid_path))  # byte / seg
        print(f"Para o vídeo {video_array[index]}, a vazão necessária é de {byte_por_segundo} bits por segundo")
    except FileNotFoundError:
        print(f"Erro: Arquivo '{video_array[index]}' não encontrado.")
    except OSError as e:
        print(f"Erro ao acessar o arquivo: {e}")
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
    global video
    while True: 
        video = (specific_client.recv(BUFFER_SIZE)).decode()
        chossing_video.set() #ele avisa que a thread que usa o chossing_video pode continuar
        if int(video) > 0:
            print(f"Video [{video}] escolhido!")
        else:
            print("Numero de video incorreto!")
            break
        # a thread fica escutando enquanto o video é rodado
        while True:
            client_command = (specific_client.recv(BUFFER_SIZE)).decode()
            new_command.set() # ele avisa que a thread que usa o new_command pode continuar(troca de sinalizado para não-sinalizado)
            print(f"Comando [{client_command}] recebido!")
            if client_command == "0":
                print("client_command == 0")
                
                break
            if video == "0":
                print("video == 0")
                # close.wait()
                # close.clear()
                # specific_client.close()
                # print("ISSO AQUI ACONTECE?")
                return
        continue

if __name__ == "__main__":
    global client_command
    global video
    video_array = ["./Conteudo/BigBuckBunny.mp4", "./Conteudo/Bear.mp4", "./Conteudo/Wildlife.mp4"]
    
    addr_client_UDP, socket_UDP = create_UDP()
    specific_client, addr_TCP, socket_TCP = create_TCP()
    
    # passa para a thread a responsabilidade de ouvir mensagens
    recv_thread = threading.Thread(target=client_command_thread, args=(specific_client,))
    recv_thread.start()
    #vamo ter q usar a função seek() para mandar pra frente ou pra tras
    while True: 
        chossing_video.wait()
        index = int(video)-1
        chossing_video.clear() # libera evento
        if video == "-1":
            print("--------Você escolheu sair do Streaming!--------")
            recv_thread.join()
            socket_UDP.close()
            socket_TCP.close()
            print("----------------Sockets fechados----------------")
        else:
            #pega o byteRate do video selecionado
            byte_rate = get_byte_rate(video_array[index])
            paused = False
            with open(video_array[index], "rb") as arquivo: # abre video para leitura
                if client_command == "2":
                    print("▶Play▶")
                while True: # toca enquanto tiver bytes para enviar ou receber o comando 0 para sair
                    if not bytes or client_command == "0" or client_command == " " or client_command == "":
                        socket_UDP.sendto(b'EOF', addr_client_UDP)
                        if not bytes:
                            print("-----------------Video enviado!-----------------")
                        else:
                            print("---------------Video interrompido---------------")
                        client_command = "2"
                        break
                    else:
                        if client_command == "1":
                            print("⏸ Pause ⏸")
                            while client_command == "1":
                                new_command.wait()  # Aguarda por um novo comando
                                new_command.clear()
                            if client_command == "2":
                                print("▶ Play ▶")
                        
                        elif client_command == "3":
                            arquivo.seek(bytes_total + (byte_rate*5))
                            bytes_total =+ (byte_rate*5)
                        
                        elif client_command == "4":
                            arquivo.seek(bytes_total - (byte_rate*5))
                            bytes_total =- (byte_rate*5)
                        
                        bytes = arquivo.read(BUFFER_SIZE)
                        bytes_total =+ bytes
                        
                        socket_UDP.sendto(bytes, addr_client_UDP)
                    
                        # Calcular o tempo de espera
                        time_to_wait = (len(bytes) / byte_rate) * 0.85
                        time.sleep(time_to_wait)  # Pausa para controlar a vazão
                        continue
                client_command = "2" # reseta variavel de comando
                arquivo.close()
        continue
                
        
