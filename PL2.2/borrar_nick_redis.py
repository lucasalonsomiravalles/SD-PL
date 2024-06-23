import redis
import sys
import socket
import netifaces as ni

ip = ni.ifaddresses('enp0s3')[ni.AF_INET][0]['addr']

redis_client = redis.Redis(host=ip, port=6379, db=0)

def interaccion(ip_broker, peticion):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_broker:
        s_broker.connect((ip_broker, 11111))
        s_broker.sendall(peticion.encode())
        respuesta = s_broker.recv(1024).decode()
        return respuesta

nick = input("Ingrese su nick:")

if redis_client.exists(nick):
    print("El nick ya está en uso")
    sys.exit(1)

puerto = 6379

ip_puerto = f"{ip}:{puerto}"
redis_client.set(nick, ip_puerto)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", 0))
ip_s, puerto_s = s.getsockname()

while True:
    linea = input()
    if linea == "/QUIT":
        if redis_client.exists(nick):
            redis_client.delete(nick)
            print(f"{nick} se ha desconectado")
        else:
            print("El usuario no ha podido ser encontrado")
        break
    elif linea.startswith("/CHAT "):
        nick_objetivo = linea.split()[1]
        peticion_query = f"QUERY {nick_objetivo}\n"
        respuesta_query = interaccion(ip, peticion_query)

        if respuesta_query.startswith("OK "):
            ip_objetivo, puerto_objetivo = respuesta_query.strip().split()[1:]
            puerto_objetivo = int(puerto_objetivo)
            direccion_objetivo = (ip_objetivo, int(puerto_objetivo))
            mensaje = input("Mensaje: ")
            s.sendto(mensaje.encode(), direccion_objetivo)
        else:
            print("Usuario no registrado")
    else:
        print("Debe usar /CHAT <nombre> o /QUIT")