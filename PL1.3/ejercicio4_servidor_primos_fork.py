import sys
import socket
import time
import os


def child_process(cliente_socket, cliente_address):
    print("Proceso hijo")
    # Lógica del proceso hijo
    # Crear un subproceso para manejar al cliente
    calcular_cliente(cliente_socket, cliente_address)

    
def parent_process():
    print("Proceso padre")
    # Lógica del proceso padre
    while True:
        # Esperar a que llegue una conexión
        print("- Esperando cliente -")
        cliente_socket, cliente_address = servidor_socket.accept()
        print("Conexión establecida desde:", cliente_address)


def es_primo(numero):
    if numero < 2:
        return False
    for i in range(2, numero):
        time.sleep(0.1)
        if numero % i == 0:
            return False
    return True


def calcular_cliente(cliente_socket, cliente_address):
    data = cliente_socket.recv(1024).decode()
    numero = int(data)
    print("Calculando los primeros %i números primos..." % numero)

    # Calcular los números primos
    primos = []
    #COMPLETAR EN EJERCICIO 1
    t=0
    p=1
    i=2
    while len (primos) < numero:
        if es_primo(i):
            primos += [i]
            t+=1
        if t == 5:
            men = f"Se han calculado {t*p} de los {numero} números primos solicitados"
            cliente_socket.sendall(men.encode())
            t = 0
            p+=1
        i +=1
    # Enviar la lista completa al cliente
    mensaje = "Primos:" + str(primos)
    cliente_socket.sendall(mensaje.encode())

    # Enviar "FIN" para indicar el final y cerrar el socket
    cliente_socket.sendall("FIN".encode())
    cliente_socket.close()
    print("Conexión cerrada con:", cliente_address)



# Hilo principal

if len(sys.argv) != 2:
    print("Uso: servidor.py puerto")
    sys.exit(1)

puerto_servidor = sys.argv[1]

# Crear el socket TCP
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al puerto especificado
servidor_socket.bind(('', int(puerto_servidor)))

# Escuchar por conexiones entrantes
servidor_socket.listen(4)

print("El servidor está listo para recibir conexiones")

cliente_socket, cliente_address = servidor_socket.accept()
pid = os.fork() # En este punto, existen los procesos padre e hijo
if pid == 0:
    child_process(cliente_socket, cliente_address)
    sys.exit() # Finaliza el proceso hijo
else:
    cliente_socket, cliente_address =parent_process()

# Continuación del proceso padre
print("Finalizando el proceso padre...")
sys.exit()