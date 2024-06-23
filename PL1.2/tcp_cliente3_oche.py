import socket
import sys

# Obtener la dirección IP y puerto del servidor de la línea de comandos o usar los valores por defecto
if len(sys.argv) > 2:
    servidor_ip = sys.argv[1]
    servidor_puerto = int(sys.argv[2])
else:
    servidor_ip = "localhost"
    servidor_puerto = 9999

# Mensajes de prueba a enviar al servidor
mensajes = ["Hora", "Paz", "Tan", "Sitio", "Enlace"]

# Crear un socket TCP y conectarlo con el servidor
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect((servidor_ip, servidor_puerto))

# Enviar mensajes al servidor y recibir respuestas
for mensaje in mensajes:
    print("Enviando mensaje:", repr(mensaje))
    cliente_socket.sendall(mensaje.encode("utf8"))

    respuesta = cliente_socket.recv(80).decode("utf8")
    print("Respuesta recibida:", repr(respuesta))

# Cerrar el socket
cliente_socket.close()
