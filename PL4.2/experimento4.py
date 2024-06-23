# coding: utf-8
from flask import Flask, jsonify, abort, make_response,request

app = Flask(__name__)
tareas = [  # Es una lista
    { # Cada tarea es un diccionario
      'id': 1,
      'descripcion': 'Terminar práctica Hola Mundo con Flask',
      'completada': True
    }, 
    {
      'id': 2,
      'descripcion': 'Terminar práctica aplicación To-Do',
      'completada': False
    }
]

@app.route("/lista/v1/tareas", methods=["GET"])
def get_tareas():
    return jsonify({"tareas": tareas})

@app.route('/lista/v1/tarea/<id>', methods=["GET"])
def get_tarea(id):
    return jsonify({ 'tarea': buscar_tarea(id) })

def buscar_tarea(num):
    for i in tareas:
        if i["id"] == int(num):
            return i
    abort(404)

@app.errorhandler(404)
def no_encontrado(error):
   return make_response(jsonify({'error': 'Tarea inexistente'}), 404)

@app.route("/lista/v1/tareas", methods=["POST"])
def create_tarea():
    print("Recibido POST con datos:")
    print(request.json)
    print("-------")
    return "OK", 201