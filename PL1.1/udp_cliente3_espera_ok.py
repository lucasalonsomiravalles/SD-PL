import socket
import sys

if len(sys.argv) > 2:
    ip = sys.argv[1]
    puerto = int(sys.argv[2])
else:
    ip = "localhost"
    puerto = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

numero_mensaje = 1

while True:
        mensaje = input("Ingrese un mensaje (FIN para salir): ")
        if mensaje == "FIN":
            break
        mensaje = f"{numero_mensaje}: {mensaje}"
        sock.sendto(mensaje.encode(), (ip, puerto))
        
        sock.settimeout(0.1) 
        try:
            datagrama, origen = sock.recvfrom(1024) 
            datagrama = datagrama.decode("utf8")
            if datagrama=="OK":
                print("Recibida confirmación")
            else:
                print("Recibido datagrama no esperado")
        except socket.timeout:
            print("ERROR. El datagrama de confirmación no llega")
        
        numero_mensaje += 1

sock.close()