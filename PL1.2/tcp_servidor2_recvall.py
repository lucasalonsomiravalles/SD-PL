import socket
import sys

# Función recvall para recibir todos los bytes solicitados
def recvall(s, n):
    datos = b""
    while n:
        part = s.recv(n)
        if not part:
            raise EOFError("Conexión cerrada inesperadamente por el cliente")
        datos += part
        n -= len(part)
    return datos.decode("ascii")

# Obtener el puerto de la línea de comandos o usar el valor por defecto
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
else:
    puerto = 9999

# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asignarle el puerto
s.bind(("", puerto))

# Ponerlo en modo pasivo
s.listen(5)  # Máximo de clientes en la cola de espera al accept()

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        try:
            # Utilizar recvall para recibir los 5 bytes esperados
            datos = recvall(sd, 5)
        except EOFError as e:
            print(e)
            sd.close()
            continuar = False
        else:
            if datos == "FINAL":
                print("Recibido mensaje de finalización")
                sd.close()
                continuar = False
            else:
                print("Recibido mensaje: %s" % datos)
