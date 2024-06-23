import pika

# Establecer la conexión con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Crear el exchange de tipo directo
channel.exchange_declare(exchange='probando_exchange_direct', exchange_type='direct')

# Definir la clave de enrutamiento
routing_key = 'clave_direct' 

# Consumidor
def callback(ch, method, properties, body): 
    print("Consumidor recibió el mensaje: %r" % body.decode('utf-8'))

channel.queue_declare(queue='cola_direct') 
channel.queue_bind(queue='cola_direct', exchange='probando_exchange_direct', routing_key=routing_key)
channel.basic_consume(queue='cola_direct', on_message_callback=callback, auto_ack=True) 

print('Esperando mensajes del productor...')
channel.start_consuming()

# Con el consumidor detenido, al lanzar 3 veces el productor y luego el consumidor, los 3 primeros mensajes no se pierden. 
# RabbitMQ almacena los mensajes en la cola hasta que el consumidor esté listo para procesarlos. 
# Se trata de una comunicación asíncrona, pues el productor y el consumidor no necesitan estar en línea al mismo tiempo.

# Si las claves de enrutamiento no coinciden, el consumidor no recibirá los mensajes. 
# Son necesarias para que RabbitMQ enrute los mensajes al destinatario correcto. 
# Puesto que no coinciden, el mensaje no llegará a la cola del consumidor.