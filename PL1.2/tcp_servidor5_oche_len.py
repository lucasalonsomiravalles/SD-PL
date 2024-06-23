import socket
import sys
import time

# Función para revertir una cadena
def revertir_cadena2(cadena):
    return f"{len(cadena)}\n"+ cadena[::-1]

# Recibe bytes hasta encontrar la longuitud acabada en \n
def recibe_longitud(sd):
    Rec = True
    Long = ""
    while Rec:
        Long += sd.recv(1).decode("utf8")

        if "\n" in Long:
            Rec = False

    return int(Long)


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
    time.sleep(1)
    print("Nuevo cliente conectado desde %s, %d" % origen)
    
    # Bucle de atención al cliente conectado
    while True:
        L = recibe_longitud(sd)
        mensaje = sd.recv(L).decode("utf8")  # Recibir mensaje y decodificar
        if not mensaje:
            print("Cliente ha cerrado la conexión.")
            break
        print(f"Mensaje recibido de longuitud {L}:", repr(mensaje))
        
        
        # Revertir la cadena
        respuesta = revertir_cadena2(mensaje)
        
        # Enviar la respuesta al cliente
        respuesta_bytes = respuesta.encode("utf8")
        sd.sendall(respuesta_bytes)
        print("Respuesta enviada:", repr(respuesta))
    
    sd.close()
