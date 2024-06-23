import socket
import sys

if len(sys.argv) > 2:
    ip = sys.argv[1]
    puerto = int(sys.argv[2])
else:
    ip = "localhost"
    puerto = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
        mensaje = input("Ingrese un mensaje (FIN para salir): ")
        if mensaje == "FIN":
            break
        sock.sendto(mensaje.encode(), (ip, puerto))

sock.close()