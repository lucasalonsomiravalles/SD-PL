# coding: utf-8
from flask import Flask, jsonify, abort, make_response, request, url_for

app = Flask(__name__)

tareas = [
    {'id': 1, 'descripcion': 'Terminar práctica Hola Mundo con Flask', 'completada': True},
    {'id': 2, 'descripcion': 'Terminar práctica aplicación To-Do', 'completada': False}
]

def tarea_uri(tarea):
    return {
        'descripcion': tarea['descripcion'],
        'completada': tarea['completada'],
        'uri': url_for('get_tarea', id=tarea['id'], _external=True)
    }

def tareas_uris(tareas):
    return [tarea_uri(tarea) for tarea in tareas]

@app.route("/lista/v1/tareas", methods=["GET"])
def get_tareas():
    return jsonify({"tareas": tareas_uris(tareas)})

@app.route('/lista/v1/tarea/<id>', methods=["GET"])
def get_tarea(id):
    tarea = buscar_tarea(id)
    if not tarea:
        abort(404)
    return jsonify({'tarea': tarea_uri(tarea)})

@app.route("/lista/v1/tareas", methods=["POST"])
def create_tarea():
    dicfinal = dict()
    try:
        dic = request.json
    except:
        abort(400)

    if "descripcion" not in dic:
        abort(400)

    dicfinal["descripcion"] = dic["descripcion"]

    if "completada" not in dic:
        dic['completada'] = False
    elif type(dic['completada']) != bool:
        abort(400)

    dicfinal["completada"] = dic["completada"]

    id = tareas[-1]['id'] + 1
    dicfinal["id"] = id

    tareas.append(dicfinal)

    return jsonify({"tarea": tarea_uri(dicfinal)}), 200

@app.route("/lista/v1/tarea/<id>", methods=["PUT"])
def update_tarea(id):
    tarea = buscar_tarea(id)
    if not tarea:
        abort(404)

    try:
        data = request.json
        if "descripcion" in data:
            if not isinstance(data["descripcion"], str):
                abort(400)
            tarea["descripcion"] = data["descripcion"]

        if "completada" in data:
            if not isinstance(data["completada"], bool):
                abort(400)
            tarea["completada"] = data["completada"]

        return jsonify({"tarea": tarea_uri(tarea)}), 200
    except:
        abort(400)

@app.route("/lista/v1/tarea/<id>", methods=["DELETE"])
def delete_tarea(id):
    tarea = buscar_tarea(id)
    if not tarea:
        abort(404)

    tareas.remove(tarea)
    return jsonify({"borrado": True}), 200

def buscar_tarea(num):
    for i in tareas:
        if i["id"] == int(num):
            return i
    abort(404)

@app.errorhandler(404)
def no_encontrado(error):
    return make_response(jsonify({'error': 'Tarea inexistente'}), 404)

@app.errorhandler(400)
def soli_incorrecta(error):
    return make_response(jsonify({'error': 'Solicitud incorrecta'}), 400)

if __name__ == "__main__":
    app.run(debug=True)