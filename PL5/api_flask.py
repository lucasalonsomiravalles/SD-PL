# Se implementa como parte opcional: Incluir autenticación para el uso de la API

from flask import Flask,request,jsonify,abort
import redis
import uuid
import json
import os
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

auth = HTTPBasicAuth()
auth.realm = "Es necesario autenticarse"

autorizados = {}  # Ninguno de momento, los cargaremos de fichero

def leer_usuarios_autorizados(nombre_fichero):
    try:
        lineas = open(nombre_fichero, "r").readlines()
    except:
        # Si no se ha podido abrir el fichero, no seguimos
        return
    # En caso contrario leemos el fichero para rellenar el diccionario
    # de usuarios autorizados
    for linea in lineas:
        linea = linea.strip()  # Eliminar retorno de carro
        if not linea:
            continue    # Saltar lineas vacías
        usuario, contraseña = linea.split()
        autorizados[usuario] = contraseña

leer_usuarios_autorizados("contrasenyas.txt")

@auth.verify_password
def verificar(usuario, contraseña):
    # Esta función debe retornar True si la el usuario/contraseña es válido
    # y False en caso contrario
    
    if usuario in autorizados and check_password_hash(autorizados[usuario],contraseña):
        return True
    else:
        return False


app = Flask(__name__)
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_client = redis.Redis(host=redis_host, port=6379, db=0)


@app.route("/trabajos", methods=["POST"])
@auth.login_required
def crear_trabajo():
    if "total_elementos" not in request.json:
        abort(400)
    else:
        total_elementos = request.json["total_elementos"]
        job_id = str(uuid.uuid4())

        js = {
            'total_elementos': total_elementos
        }

        redis_client.set(f'trabajo:{job_id}', json.dumps(js))
        redis_client.rpush('trabajos', job_id)
        return jsonify({'Trabajo creado con ID': job_id}), 200

    


@app.route("/trabajos/<string:job_id>", methods=["GET"])
@auth.login_required
def estado_trabajo(job_id):

    progreso = redis_client.get(f'progreso:{job_id}')
    if progreso is None:
        print('Trabajo no encontrado')
        abort(404)

    progreso = int(progreso.decode('utf-8'))



    if progreso < 100:
        return jsonify({ "ID del Trabajo": job_id,"Progreso": progreso})
    else:
        resultado_key = f'resultado:{job_id}'
        resultado_final = json.loads(redis_client.get(resultado_key).decode('utf-8'))
        return jsonify({ "ID del Trabajo": job_id,"Progreso": progreso, "Resultado": resultado_final})


if __name__ == '__main__':
    app.run(debug=True)