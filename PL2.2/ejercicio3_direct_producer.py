import pika

# Establecer la conexión con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
channel = connection.channel()

# Crear el exchange de tipo directo
channel.exchange_declare(exchange='probando_exchange_direct', exchange_type='direct') 

# Definir la clave de enrutamiento
routing_key = 'clave_direct' 

# Productor
texto = 'Este es un mensaje directo'
channel.basic_publish(exchange='probando_exchange_direct', routing_key=routing_key, body=texto) 

print("Productor envió el mensaje: %r" % texto)

connection.close()