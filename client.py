import socket
import subprocess

BUFFER_SIZE = 1024
SHIPPING_SIZE = 10

caminho_vlc = 'C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe'

# Cria um socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Endereço e porta do servidor
endereco_servidor = ("LocalHost", 12345)


cont = 0

def fim_arquivo(data: bytes):
    if data.strip(b'\x00'):
        if data == b'EOF':
            return True
    return False

def transmite(cont):
    i = 0
    while True:
            
            data, addr = socket_udp.recvfrom(BUFFER_SIZE) # novos dados

            if fim_arquivo(data): # caso de arquivo vazio
                break

            i += 1

            if i == SHIPPING_SIZE: # controle de entrega
                i = 0 # se prepara para nova remessa
                socket_udp.sendto(b'1', endereco_servidor) # avisa que pode receber mais
                    
            envia_video.stdin.write(data) # salvando novos dados

            cont += 1
            print(f"pacote {cont}")

while True:
    # Mensagem a ser enviada ao servidor
    message = input("Digite a mensagem:")
    socket_udp.sendto(message.encode(), endereco_servidor)
    if message == "envia":
        envia_video = subprocess.Popen([caminho_vlc,'-', '--input-title-format', "Streaming Video"],stdin = subprocess.PIPE,)
        transmite(cont) # trocar nome
        
    print(f"foram necessarios {cont} pacotes para mandar todo o arquivo")
       
