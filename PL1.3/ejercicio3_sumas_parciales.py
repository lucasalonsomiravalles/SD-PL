import random as rd
import threading
import time


rd.seed(150)

def suma_interna(lista):
    global listafinal
    n = 0
    for i in range (len(lista)):
        n+=lista[i]
    listafinal += [n]




def suma_lista (long,hilos):

    global listafinal
    listafinal = []

    rl = []

    for i in range(0,long):
        n = rd.randint(1,100)
        rl.append(n)

    long_parcial = long//hilos
    lhilo = []

    if hilos > 1:
        for i in range (hilos-1):
            hilo = threading.Thread(target=suma_interna, args=(rl[long_parcial*i:long_parcial*(i+1)],))
            lhilo.append(hilo)

        hilo = threading.Thread(target=suma_interna, args=(rl[long_parcial*(i+1):],))
        lhilo.append(hilo)

        for hilo in lhilo:
            hilo.start()

        for hilo in lhilo:
            hilo.join()

    else:
        suma_interna(rl)
    
    sum = 0

    for i in range (len(listafinal)):
        sum += listafinal[i]
    
    return sum




a = suma_lista(1000000,1)

print(a)

