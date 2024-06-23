import pika

# Establecer la conexión con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Crear el exchange de tipo fanout
channel.exchange_declare(exchange='probando_exchange_fanout', exchange_type='fanout')

# Definir la clave de enrutamiento
routing_key = '' 

# Consumidor
def callback(ch, method, properties, body): 
    print("Consumidor recibió el mensaje: %r" % body.decode('utf-8'))

channel.queue_declare(queue='cola_fanout') 
channel.queue_bind(queue='cola_fanout', exchange='probando_exchange_fanout', routing_key=routing_key)
channel.basic_consume(queue='cola_fanout', on_message_callback=callback, auto_ack=True) 

print('Esperando mensajes del productor...')
channel.start_consuming()