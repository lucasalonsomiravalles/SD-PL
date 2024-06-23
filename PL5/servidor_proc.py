import redis
import threading
import time
import json
import os

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_client = redis.Redis(host=redis_host, port=6379, db=0)


def hilo(job_id, total_elementos):
    progreso_key = f'progreso:{job_id}'
    resultado_key = f'resultado:{job_id}'
    trabajo_key = f'trabajo:{job_id}'

    resultados = []

    for i in range(total_elementos):
        
        resultado = fibonacci(i)
        resultados.append(resultado)

        
        porcentaje = int((i + 1) / total_elementos * 100)
        redis_client.set(progreso_key, porcentaje)

        
        redis_client.rpush(resultado_key, resultado)

        time.sleep(1)

    redis_client.set(resultado_key, json.dumps(resultados))

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b

while True:
    job_id = redis_client.blpop('trabajos')[1].decode('utf-8')
    js = json.loads(redis_client.get(f'trabajo:{job_id}').decode('utf-8'))

    total_elementos = js['total_elementos']

    threading.Thread(target=hilo, args=(job_id, total_elementos)).start()