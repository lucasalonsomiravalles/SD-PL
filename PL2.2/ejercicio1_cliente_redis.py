import socket
import sys
import redis
import netifaces as ni
import select

nick = sys.argv[1]
ip_host = sys.argv[2]


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", 0))



ip = ni.ifaddresses('enp0s3')[ni.AF_INET][0]['addr']

print(ip)

puerto = 6379
redis_client = redis.Redis(host=ip_host, port=6379, db=0)

ip_puerto = f"{ip_host}:{puerto}"




if redis_client.exists(nick):
    sys.exit("El nick ya existe")



redis_client.set(nick, ip_puerto)

print(f"Se ha unido como {nick} en {ip_puerto}")


nick_objetivo = None

direccion_objetivo = None


while True:
    print("> ", end='')
    listo, _, _ = select.select([s, sys.stdin.fileno()], [], [])

    for fuente in listo:
        if fuente == s:
            datos, direccion = s.recvfrom(1024)
            print(datos.decode())
        elif fuente == sys.stdin.fileno():
            linea = input()

            if linea == "/QUIT":

                redis_client.delete(nick)
                print(f"{nick} se ha desconectado")
                s.close()
                break

            elif linea.startswith("/CHAT "):

                nick_objetivo = linea.split()[1]

                if not redis_client.exists(nick_objetivo):
                    print("El nick no existe")
        
                Obje_IP_Puerto = redis_client.get(nick_objetivo).decode()
                print(Obje_IP_Puerto)
                Objetivo_IP = Obje_IP_Puerto.split(":")[0]
                Objetivo_Puerto = Obje_IP_Puerto.split(":")[1]
                direccion_objetivo = (Objetivo_IP, int(Objetivo_Puerto))


            else:
                # Sale esto si no hay nombre
                if nick_objetivo == None:
                    print("Debe usar /CHAT <nombre> o /QUIT")

                else:
                    # mensaje = input("Mensaje: ").encode()
                    print("SUYA",direccion_objetivo)
                    print("MIA",ip_puerto)
                    s.sendto(linea.encode(), direccion_objetivo)
