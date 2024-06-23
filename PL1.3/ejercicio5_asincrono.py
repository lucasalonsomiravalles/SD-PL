import asyncio
import sys

if len(sys.argv) != 3:
    print("Uso: cliente.py arg1 arg2")
    sys.exit(1)

arg1 = int(sys.argv[1])
arg2 = int(sys.argv[2])

async def suma(arg1,arg2):
    print(f"Calculando suma entre {arg1} y {arg2}")
    await asyncio.sleep(10)
    print("Suma: ",arg1+arg2)

async def resta(arg1,arg2):
    print(f"Calculando resta entre {arg1} y {arg2}")
    await asyncio.sleep(8)
    print("Resta: ",arg1-arg2)

async def multiplicacion(arg1,arg2):
    print(f"Calculando multiplicación entre {arg1} y {arg2}")
    await asyncio.sleep(3)
    print("Multiplicación: ",arg1*arg2)

async def division(arg1,arg2):
    print(f"Calculando división entre {arg1} y {arg2}")
    await asyncio.sleep(5)
    print("División: ",arg1/arg2)



async def main():

    print("Inicio de la primera prueba") 
    await suma(arg1,arg2)
    await resta(arg1,arg2)
    await multiplicacion(arg1,arg2)
    await division(arg1,arg2)
    print("Fin de la primera prueba\n----")

    print("Inicio de la segunda prueba") 
    await asyncio.gather(suma(arg1,arg2), resta(arg1,arg2),multiplicacion(arg1,arg2),division(arg1,arg2))
    print("Fin de la segunda prueba\n----")

    print("Inicio de la tercera prueba") 
    task = asyncio.create_task(suma(arg1,arg2))
    await resta(arg1,arg2)
    await multiplicacion(arg1,arg2)
    await division(arg1,arg2)
    print("Fin de la tercera prueba\n----")


asyncio.run(main())