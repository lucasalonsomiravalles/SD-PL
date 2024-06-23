import socket
import sys

if len(sys.argv) > 2:
    ip = sys.argv[1]
    puerto = int(sys.argv[2])
else:
    ip = "localhost"
    puerto = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

numero_mensaje = 1

while True:
        mensaje = input("Ingrese un mensaje (FIN para salir): ")
        if mensaje == "FIN":
            break
        mensaje = f"{numero_mensaje}: {mensaje}"
        sock.sendto(mensaje.encode(), (ip, puerto))
        numero_mensaje += 1

sock.close()