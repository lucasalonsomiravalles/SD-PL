import sys
import asyncio
import socket

async def es_primo(numero):
    if numero < 2:
        return False
    for i in range(2, numero):
        await asyncio.sleep(0.1)
        if numero % i == 0:
            return False
    return True

async def atender_cliente(reader, writer):
    data = await reader.read(1024)
    numero = int(data.decode())

    print("Conexión establecida")
    print("Calculando los primeros %i números primos..." % numero)

    # Calcular los números primos
    primos = []
    t=0
    p=1
    i=2
    while len (primos) < numero:
        if await es_primo(i):
            primos += [i]
            t+=1
        if t == 5:
            men = f"Se han calculado {t*p} de los {numero} números primos solicitados"
            writer.write(men.encode())
            await writer.drain()
            t = 0
            p+=1
        i +=1
    # Enviar la lista completa al cliente
    mensaje = "Primos:" + str(primos)
    writer.write(mensaje.encode())
    await writer.drain()

    # Enviar "FIN" para indicar el final y cerrar el socket
    writer.write("FIN".encode())
    await writer.drain()
    print("Cerrando conexión")
    writer.close()

async def main():
    if len(sys.argv) != 2:
        print("Uso: servidor.py puerto")
        sys.exit(1)

    puerto_servidor = sys.argv[1]
    
    servidor = await asyncio.start_server(atender_cliente, '', puerto_servidor)


    await servidor.serve_forever()
        
        
# Ejecutar main() como función asíncrona
#COMPLETAR

asyncio.run(main())