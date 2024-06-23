import socket
import sys

# Obtener la dirección IP y puerto del servidor de la línea de comandos o usar los valores por defecto
if len(sys.argv) > 2:
    ip = sys.argv[1]
    puerto = int(sys.argv[2])
else:
    ip = "localhost"
    puerto = 9999

# Crear un socket TCP y conectarlo con el servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, puerto))

# Repetir 5 veces el envío del texto "ABCDE"
for i in range(5):
    mensaje = "ABCDE"
    s.sendall(mensaje.encode("ascii"))

# Enviar el texto "FINAL", cerrar el socket y terminar
s.sendall("FINAL".encode("ascii"))
s.close()
