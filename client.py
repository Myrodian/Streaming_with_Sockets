import socket
import subprocess
import threading
import time
VIDEO_LIST_SIZE = 4
BUFFER_SIZE = 1024*8
ACTIONS = 3
# vezes = 0

server = 'localhost'
action = "2" # 0 - sair, 1 pausar, 2 rodar

caminho_vlc = 'D:\\Arquivos_e_Programas\\VLC\\vlc.exe'
# caminho_vlc = "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"

def create():
    try:
        socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP
        addr_server_UDP = (server, 12345)  # Endereço e porta do servidor UDP
        confirmacion = "confirmação"
        socket_UDP.sendto(confirmacion.encode(), addr_server_UDP)

        socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP
        socket_TCP.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        addr_server_TCP = (server, 54321)  # Endereço e porta do servidor TCP
        socket_TCP.connect(addr_server_TCP)

    except Exception as e:
        print(f"\nErro inesperado: {e}")
    
    finally:
        return socket_TCP, socket_UDP

def request():
    global action
    # vezes = 0
    vid_buff = []
    tocando = False
    try:
        t0 = time.time()
        while True:
            if not tocando and (time.time()- t0) >= 0.3:
                envia_video = subprocess.Popen([caminho_vlc, '-', '--input-title-format', 'Streaming Video',
                                    '--network-caching=0', '--file-caching=0'],
                                    stdin=subprocess.PIPE)
                tocando = True
            data, _ = socket_UDP.recvfrom(BUFFER_SIZE)  # Novos dados # não passa daqui >:(2
            # vezes += 1
            if data == b'EOF':  # Caso de arquivo vazio
                envia_video.stdin.close()
                envia_video.wait()
                break
            
            vid_buff.append(data)

            # Processa e escreve dados no VLC conforme são recebidos
            if tocando:
                while vid_buff:
                    piece = b''.join(vid_buff)
                    envia_video.stdin.write(piece)
                    envia_video.stdin.flush()  # Garante que os dados sejam enviados ao VLC
                    vid_buff.clear()  # remove a posição mais antiga

    except BrokenPipeError:
        print("\nErro: Broken pipe. O VLC fechou a conexão.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
    
    # return vezes

if __name__ == "__main__":
    socket_TCP, socket_UDP = create()
    
    while True:
        message = input("Escolha o video [ 1 - BBB | 2 - Bear | 3 - WildLife ]:")
        if int(message) in range(-1, VIDEO_LIST_SIZE + 1):  # Corrige a validação do intervalo
            try:
                socket_TCP.send(message.encode())
                if message == "-1":
                    break

                video_thread = threading.Thread(target=request) # thread de video
                video_thread.start()

                socket_TCP.send(action.encode()) # libera servidor para rodar
                while True:
                    action = input("Ações [ 0 - cancelar | 1 - za wardo | 2 - tocar ]:")
                    if int(action) in range(3): 
                        if action == "0":
                            socket_TCP.send(action.encode())
                            print(f"Ação:[{action}] - cancelar, voltando para menu!")
                            break
                        socket_TCP.send(action.encode())
                    else:
                        print(f"Ação [{action}] Invalida!")
                        continue

                # print(f"\nForam necessários {cont} pacotes para mandar todo o arquivo")
            except Exception as e:
                print(f"Erro ao enviar a mensagem ou processar a requisição: {e}")
        else: 
            print(f"Valor {message} inválido! Tente novamente.")

    video_thread.join()
    socket_TCP.close()
    socket_UDP.close()
