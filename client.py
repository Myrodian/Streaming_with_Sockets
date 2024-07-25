import socket
import subprocess

BUFFER_SIZE = 1024
SHIPPING_SIZE = 5

# caminho_vlc = 'D:\\Arquivos_e_Programas\\VLC\\vlc.exe'
caminho_vlc = 'C:\\Program Files (x86)\\VideoLAN\VLC\\vlc.exe'
# Cria um socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Endereço e porta do servidor
endereco_servidor = ("localhost", 12345)

def fim_arquivo(data: bytes):
    if data.strip(b'\x00'):
        if data == b'EOF':
            return True
    return False

def pedido():

    # iniciacao de controles
    cont = 0
    i = 0

    # tentativa de conexao
    while True:  
        
        data, addr = socket_udp.recvfrom(BUFFER_SIZE) # novos dados
        # print(int.from_bytes(data)) # esta recebendo corretamente o numero de pacotes, 
        # daqui para frente um pacote de 1024 bytes vai ter até 1271, em bytes, como cabecalho
        input(" Se der certo dá errado :)")

        if fim_arquivo(data): # caso de arquivo vazio
            print(" Entrega Finalizada pelo servidor !")
            break

        i += 1

        if i == SHIPPING_SIZE: # controle de entrega
            i = 0 # se prepara para nova remessa
            
            socket_udp.sendto(b'1', addr) # avisa que pode receber mais
            
        envia_video.stdin.write(data) # salvando novos dados

        cont += 1
        print(f"pacote {cont}")
    return cont

while True:
    # Mensagem a ser enviada ao servidor
    message = input("Digite a mensagem:")
    socket_udp.sendto(message.encode(), endereco_servidor)
    if message == "envia":
        envia_video = subprocess.Popen([caminho_vlc,'-', '--input-title-format', "Streaming Video"],stdin = subprocess.PIPE,)
        cont = pedido()
    print(f"foram necessarios {cont} pacotes para mandar todo o arquivo")
       
