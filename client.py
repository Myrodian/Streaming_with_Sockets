import socket
import subprocess

VIDEO_LIST_SIZE = 3
BUFFER_SIZE = 1024 * 2
WRITE_BUFF = 1024 * 4
caminho_vlc = 'C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe'

# Cria um socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Endereço e porta do servidor
server_addr = ("localhost", 12345)

def end_of_file(data: bytes):
    
    return data == b'EOF'

def ready(addr):
            socket_udp.sendto(b'1', addr)  # Avisa que pode receber mais

def request():
    vid_buff = []
    envia_video = subprocess.Popen([caminho_vlc, '-', '--input-title-format', 'Streaming Video',
                                    '--network-caching=0', '--file-caching=0'],
                                    stdin=subprocess.PIPE)
    try:
        while True:
            data, addr = socket_udp.recvfrom(BUFFER_SIZE)  # Novos dados
            if end_of_file(data):  # Caso de arquivo vazio
                break
            
            vid_buff.append(data)

            # Processa e escreve dados no VLC conforme são recebidos
            while vid_buff:
                slice = b''.join(vid_buff)
                envia_video.stdin.write(slice)
                envia_video.stdin.flush()  # Garante que os dados sejam enviados ao VLC
                vid_buff.clear()  # Limpa o buffer depois de escrever

            # ready(addr)

    except BrokenPipeError:
        print("\nErro: Broken pipe. O VLC fechou a conexão.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")

    envia_video.stdin.close()
    envia_video.wait()
    return len(vid_buff)

while True:
    message = input("Escolha o video [ 0 - BBB | 1 - Bear | 2 - WildLife ]:")
    if int(message) in range(VIDEO_LIST_SIZE):
        socket_udp.sendto(message.encode(), server_addr)

        try:
            cont = request()

            # ready(server_addr)

        except Exception as e:
            print(f"Erro ao iniciar o VLC: {e}")
    else: 
        print(f"Valor {message} inválido! Tente novamente.")

    print(f"\nForam necessários {cont} pacotes para mandar todo o arquivo")
    socket_udp.close()
