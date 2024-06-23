import socket
import sys
import random

if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
else:
    puerto = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", puerto))

identificadores_recibidos = set()

while True:                                                     
    mensaje, direccion = sock.recvfrom(1024)
    identificador = mensaje.decode().split(":")[0]

    if identificador not in identificadores_recibidos:
        if random.randint(0, 1) == 0:
            print("Simulando paquete perdido")
        else:
            print(f"Datagrama recibido de {direccion}: {mensaje.decode()}")
            sock.sendto(b"OK", direccion)
            identificadores_recibidos.add(identificador)
    else:
        if random.randint(0, 1) == 0:
            print("Simulando paquete perdido")
        else:
            sock.sendto(b"OK", direccion)
