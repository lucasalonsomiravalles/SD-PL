import socket
import sys
import random

if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
else:
    puerto = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", puerto))

while True:
    mensaje, direccion = sock.recvfrom(1024)
    if random.randint(0, 1) == 0:
        print("Simulando paquete perdido")
    else:
        print(f"Datagrama recibido de {direccion}: {mensaje.decode()}")
        if mensaje.decode() == "HOLA":
            sock.sendto(b"OK", direccion)
