import socket
import sys

# Función para revertir una cadena y agregar "\r\n"
def revertir_cadena(cadena):
    return cadena[::-1] + "\r\n"

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
    
    # Bucle de atención al cliente conectado
    while True:
        mensaje = sd.recv(80).decode("utf8")  # Recibir mensaje y decodificar
        if not mensaje:
            print("Cliente ha cerrado la conexión.")
            break
        
        print("Mensaje recibido:", repr(mensaje))
        
        # Revertir la cadena y agregar "\r\n"
        respuesta = revertir_cadena(mensaje)
        
        # Enviar la respuesta al cliente
        respuesta_bytes = respuesta.encode("utf8")
        sd.sendall(respuesta_bytes)
        print("Respuesta enviada:", repr(respuesta))
    
    sd.close()
