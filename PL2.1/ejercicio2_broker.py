import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
else:
    puerto = 11111
s.bind(('', puerto))
s.listen(5) 
usuarios = dict()  

while True:
    s, direccion = s.accept()
    datos = s.recv(1000)  
    linea = datos.decode()  
    if linea.startswith("JOIN"):
        a = linea.split()
        nick = a[1]  
        if nick in usuarios:  
            s.sendall("ERROR\n".encode()) 
            s.close()  
        else:
            ip = direccion[0]  
            puerto = int(a[2])  
            usuarios[nick] = (ip, puerto)
            print(usuarios[nick])
            s.sendall("OK\n".encode())  
            s.close()
    elif linea.startswith("LEAVE"):
        a = linea.split()
        nick = a[1] 
        if nick not in usuarios:  
            s.sendall("ERROR\n".encode())  
            s.close()  
        else:
            del usuarios[nick]
            s.sendall("OK\n".encode())  
            s.close() 
    elif linea.startswith("QUERY"):
        a = linea.split()
        nick = a[1] 
        if nick not in usuarios: 
            s.sendall("ERROR\n".encode())      
            s.close() 
        else:
            direccion = usuarios[nick]
            mensaje = f"OK {direccion[0]} {direccion[1]}\n"
            s.sendall(mensaje.encode())  
            s.close()  