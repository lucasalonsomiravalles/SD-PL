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
timeout = 0.1

while True:
        mensaje = input("Ingrese un mensaje (FIN para salir): ")
        if mensaje == "FIN":
            break
        mensaje = f"{numero_mensaje}: {mensaje}"
        enviado = False

        while not enviado and timeout <= 2:
            sock.sendto(mensaje.encode(), (ip, puerto))

            sock.settimeout(timeout)
            try:
                datagrama, origen = sock.recvfrom(1024)
                datagrama = datagrama.decode("utf8")
                if datagrama=="OK":
                    print("Recibida confirmación")
                    enviado = True
                else:
                    print("Recibido datagrama no esperado")
            except socket.timeout:
                print(f"ERROR. El datagrama de confirmación no llega. Tiempo de espera agotado ({timeout} segundos).")
                timeout *= 2

        if timeout > 2:
            print("Puede que el servidor esté caído. Inténtelo más tarde.")
            break
        
        numero_mensaje += 1

sock.close()