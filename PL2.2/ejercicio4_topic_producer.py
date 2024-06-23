import pika


lista = [
    {"routing_key": "tierra.leon.selva.carnivoro", "texto": "Información del león 1 ..."},
    {"routing_key": "tierra.cebra.sabana.herbivoro", "texto": "Información de la cebra ..."},
    {"routing_key": "mar.delfin.oceano.carnivoro", "texto": "Información del delfín ..."},
    {"routing_key": "mar.tiburon.oceano.carnivoro", "texto": "Información del tiburón ..."},
    {"routing_key": "aire.aguila.montana.carnivoro", "texto": "Información del águila ..."},
    {"routing_key": "aire.colibri.bosque.nectarivoro", "texto": "Información del colibrí 1 ..."},
    {"routing_key": "aire.pajaro_carpintero.bosque.omnivoro", "texto": "Información del pájaro carpintero ..."},
    {"routing_key": "mar.pulpo.oceano.carnivoro", "texto": "Información del pulpo ..."},
    {"routing_key": "tierra.elefante.selva.herbivoro", "texto": "Información del elefante ..."},
    {"routing_key": "tierra.leon.selva.carnivoro", "texto": "Información del león 2 ..."},
    {"routing_key": "aire.buho.bosque.carnivoro", "texto": "Información del búho ..."},
    {"routing_key": "mar.tortuga.marino.herbivoro", "texto": "Información de la tortuga ..."},
    {"routing_key": "tierra.leopardo.montana.carnivoro", "texto": "Información del leopardo ..."},
    {"routing_key": "aire.colibri.tropical.nectarivoro", "texto": "Información del colibrí 2 ..."},
    {"routing_key": "tierra.perro.montana.omnivoro", "texto": "Información del perro ..."},
    {"routing_key": "tierra.ornitorrinco.tropical.omnivoro", "texto": "Información del ornitorrinco ..."},
    {"routing_key": "tierra.humano.ciudad.omnivoro", "texto": "Información del humano ..."},
    {"routing_key": "rio.castor.bosque.omnivoro", "texto": "Información del castor ..."}
]

# Establecer la conexión con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
channel = connection.channel()

# Crear el exchange de tipo topic
channel.exchange_declare(exchange='probando_exchange_topic', exchange_type='topic') 

# Definir la clave de enrutamiento
routing_key = lista 

# Productor
for dic in lista:
    channel.basic_publish(exchange='probando_exchange_topic', routing_key=dic["routing_key"], body=dic["texto"]) 

    print("Productor envió el mensaje: %r" % dic["texto"])

connection.close()