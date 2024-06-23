import pika

# Establecer la conexión con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
channel = connection.channel()

# Crear el exchange de tipo fanout
channel.exchange_declare(exchange='probando_exchange_fanout', exchange_type='fanout') 

# Definir la clave de enrutamiento
routing_key = '' 

# Productor
texto = 'Este es un mensaje fanout'
channel.basic_publish(exchange='probando_exchange_fanout', routing_key=routing_key, body=texto) 

print("Productor envió el mensaje: %r" % texto)

connection.close()