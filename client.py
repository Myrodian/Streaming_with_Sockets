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
    return data == b'EOF'

def pedido():
    cont = 0
    i = 0
    while True:
        try:
            for i in range(5):
                data = []
                data[i], addr = socket_udp.recvfrom(BUFFER_SIZE)  # novos dados
                
                if fim_arquivo(data[i]):  # caso de arquivo vazio
                    break
            
            for i in range(5):
                envia_video.stdin.write(data[i])  # salvando novos dados
            
            socket_udp.sendto(b'1', addr)  # avisa que pode receber mais
            
            cont += 1
            print(f"\rpacote {cont}", end='')

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
                                              '--network-caching=0', '--file-caching=0','--live-caching=0','--clock-jitter=0','-vvv'],
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
