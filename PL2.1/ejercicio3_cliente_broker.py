import socket
import sys

def interaccion(ip_broker, peticion):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_broker:
        s_broker.connect((ip_broker, 11111))
        s_broker.sendall(peticion.encode())
        respuesta = s_broker.recv(1024).decode()
        return respuesta

nick = sys.argv[1]
ip_broker = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", 0))
ip, puerto = s.getsockname()

peticion_join = f"JOIN {nick} {ip} {puerto}\n"
respuesta_join = interaccion(ip_broker, peticion_join)

if respuesta_join == "OK\n":
    print(f"Se ha unido como {nick} en {ip}:{puerto}")
else:
    print("El nick elegido ya está en uso")
    sys.exit(1)

while True:
    linea = input()
    if linea == "/QUIT":
        peticion_leave = f"LEAVE {nick}\n"
        interaccion(ip_broker, peticion_leave)
        break
    elif linea.startswith("/CHAT "):
        nick_objetivo = linea.split()[1]
        peticion_query = f"QUERY {nick_objetivo}\n"
        respuesta_query = interaccion(ip_broker, peticion_query)

        if respuesta_query.startswith("OK "):
            ip_objetivo, puerto_objetivo = respuesta_query.strip().split()[1:]
            puerto_objetivo = int(puerto_objetivo)
            direccion_objetivo = (ip_objetivo, puerto_objetivo)
            mensaje = input("Mensaje: ")
            s.sendto(mensaje.encode(), direccion_objetivo)
        else:
            print("Usuario no registrado")
    else:
        print("Debe usar /CHAT <nombre> o /QUIT")
