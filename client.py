import socket
import subprocess

BUFFER_SIZE = 30072
caminho_vlc = 'D:\\Arquivos_e_Programas\\VLC\\vlc.exe'
# caminho_vlc = 'C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe'

# Cria um socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Endereço e porta do servidor
endereco_servidor = ("localhost", 12345)

def fim_arquivo(data: bytes):
    if data == b'EOF':
        return True
    else:
        return False

def pedido():
    cont = 0
    i = 0
    vid_buff = b''
    # vid_buff = []
    while True:
        try:
            data, addr = socket_udp.recvfrom(BUFFER_SIZE)  # novos dados
            
              
            if fim_arquivo(data):  # caso de arquivo vazio
                break
            
            vid_buff += data

            if cont > 50:
                envia_video.stdin.write(vid_buff) # salvando novos dados
            
            # vid_buff.append(data)
            # if i != ((len(vid_buff))-50):
            #     while i != ((len(vid_buff))-1):
            #         envia_video.stdin.write(vid_buff[i]) # salvando novos dados 
            #         i += 1
            #     i= 0
            socket_udp.sendto(b'1', addr)  # avisa que pode receber mais
            
            cont += 1
            print(f"\rPacote {cont} recebido!", end='')

        except BrokenPipeError:
            print("\nErro: Broken pipe. O VLC fechou a conexão.")
            break
        except Exception as e:
            print(f"\nErro inesperado: {e}")
            break

    return cont

while True:
    # Mensagem a ser enviada ao servidor
    message = input("Digite a mensagem:")
    socket_udp.sendto(message.encode(), endereco_servidor)

    if message == "envia":
        try:
            envia_video = subprocess.Popen([caminho_vlc, '-', '--input-title-format', 'Streaming Video',
                                              '--network-caching=0', '--file-caching=0'],
                                           stdin=subprocess.PIPE)
            cont = pedido()
            envia_video.stdin.close()
            envia_video.wait()

            # stdout, stderr = envia_video.communicate()
            # print(f"stdout: {stdout.decode()}")
            # print(f"stderr: {stderr.decode()}")

        except Exception as e:
            print(f"Erro ao iniciar o VLC: {e}")

    print(f"Foram necessários {cont} pacotes para mandar todo o arquivo")

socket_udp.close()
