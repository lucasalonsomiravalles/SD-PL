import socket
import sys

if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
else:
    puerto = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", puerto))

while True:                                                     
    mensaje, direccion = sock.recvfrom(1024)
    print(f"Datagrama recibido de {direccion}: {mensaje.decode()}")