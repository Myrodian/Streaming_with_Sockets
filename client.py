import socket
import subprocess
BUFFER_SIZE = 1024
caminho_vlc = 'D:\\Arquivos_e_Programas\\VLC\\vlc.exe'
# Cria um socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Endereço e porta do servidor
endereco_servidor = ("LocalHost", 12345)
envia_video = subprocess.Popen([caminho_vlc,'-', '--input-title-format', "Streaming Video"],stdin = subprocess.PIPE,)
cont = 0
controle = True
i = 0
def trasmissao():
    while controle:
            controle = False
            mensagem, addr = socket_udp.recvfrom(BUFFER_SIZE)
            i += 1
            if i == 10:
                controle = True
                socket_udp.sendto(b'1', endereco_servidor)
                data, addr = socket_udp.recvfrom(BUFFER_SIZE)
                if data.strip(b'\x00'):
                    if data == b'EOF':
                        break
                envia_video.stdin.write(data)
                cont += 1
                print(f"pacote {cont}")



while True:
    # Mensagem a ser enviada ao servidor
    message = input("Digite a mensagem:")
    socket_udp.sendto(message.encode(), endereco_servidor)
    if message == "envia":
        trasmissao()
        
    print(f"foram necessarios {cont} pacotes para mandar todo o arquivo")
       
