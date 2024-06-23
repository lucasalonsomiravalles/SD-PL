import socket
import sys
import select

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
if len(sys.argv) > 2:
    puerto = int(sys.argv[1])
    nick = sys.argv[2]
else:
    puerto = 9999
    nick = "A"
s.bind(('', puerto))
destino_chat = None

while True:
    print("> ", end='')
    listo, _, _ = select.select([s, sys.stdin.fileno()], [], [])
    for fuente in listo:
            if fuente == s:
                datos, direccion = s.recvfrom(1024)
                print(datos.decode())
            elif fuente == sys.stdin.fileno():
                linea = input()
                if linea.startswith("/QUIT"):
                    if destino_chat:
                        mensaje = f"{nick} se ha desconectado."
                        s.sendto(mensaje.encode(), destino_chat)
                    s.close()
                    sys.exit(0)
                elif linea.startswith("/CHAT"):
                    a = linea.split()
                    if len(a) == 3:
                        IP_destino = a[1]
                        puerto_destino = int(a[2])
                        destino_chat = (IP_destino, puerto_destino)
                elif destino_chat is None:
                    print("Antes debe usar /CHAT para especificar el destinatario")
                else:
                    mensaje = f"{nick}: {linea}"
                    s.sendto(mensaje.encode(), destino_chat)