import socket
import subprocess

VIDEO_LIST_SIZE = 4
BUFFER_SIZE = 1024 * 2
server = 'localhost'
# caminho_vlc = 'C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe'
caminho_vlc = 'D:\\Arquivos_e_Programas\\VLC\\vlc.exe'
try:
    socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP
    socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP

    # Endereço e porta do servidor
    addr_server_UDP = (server, 12345)  # Endereço e porta do servidor UDP
    addr_server_TCP = (server, 54321)  # Endereço e porta do servidor TCP
    
    socket_TCP.connect(addr_server_TCP)
    socket_TCP.sendall(b'Ola servidor, estoy usando o canal TCP')

except Exception as e:
      print(f"\nErro inesperado: {e}")

def ready(addr):
            socket_UDP.sendto(b'1', addr)  # Avisa que pode receber mais

def request():
    vid_buff = []
    envia_video = subprocess.Popen([caminho_vlc, '-', '--input-title-format', 'Streaming Video',
                                    '--network-caching=0', '--file-caching=0'],
                                    stdin=subprocess.PIPE)
    vezes = 0
    try:

        while True:
            data, addr = socket_UDP.recvfrom(BUFFER_SIZE)  # Novos dados
            vezes += 1
            if data == b'EOF':  # Caso de arquivo vazio

                envia_video.stdin.close()
                envia_video.wait()
                break
            
            vid_buff.append(data)

            # Processa e escreve dados no VLC conforme são recebidos
            while vid_buff:
                piece = b''.join(vid_buff)
                envia_video.stdin.write(piece)
                envia_video.stdin.flush()  # Garante que os dados sejam enviados ao VLC
                vid_buff.clear()  # Limpa o buffer depois de escrever

            # ready(addr)
            # print(f"\rPacote {vezes} recebido!", end="")
    except BrokenPipeError:
        print("\nErro: Broken pipe. O VLC fechou a conexão.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
    
    return vezes
if __name__ == "__main__":
    while True:
        message = input("Escolha o video [ 1 - BBB | 2 - Bear | 3 - WildLife ]:")
        if message == "0":
            break
        if int(message) in range(VIDEO_LIST_SIZE):
            socket_UDP.sendto(message.encode(), addr_server_UDP)

            try:
                cont = request()

                # ready(server_addr)

            except Exception as e:
                print(f"Erro ao iniciar o VLC: {e}")
        else: 
            print(f"Valor {message} inválido! Tente novamente.")

        print(f"\nForam necessários {cont} pacotes para mandar todo o arquivo")
    socket_UDP.close()
    socket_TCP.close()
