# coding: utf-8
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()
auth.realm = "Es necesario autenticarse"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tarea_user:tarea_pass@localhost/tarea_db'
db = SQLAlchemy(app)



class Tarea(db.Model): 
    """
    Definición de la tabla 'tareas' de la base de datos
    """

    __tablename__ = "tareas" 

    id = db.Column(db.Integer, primary_key=True) 
    descripcion = db.Column(db.String(100), nullable=False)
    completada = db.Column(db.Boolean(create_constraint=True), default=False)

    # Podemos escribir la función siguiente para implementar cómo debe
    # mostrarse un objeto de esta clase si lo imprimes desde python
    def __repr__(self): 
        return "<Tarea[{}]: {} - {}>".format(self.id, self.descripcion, self.completada)




def exportar_tarea(tarea):
    return {
        'descripcion': tarea.descripcion,
        'completada': tarea.completada,
        'uri': url_for('get_tarea', id=tarea.id, _external=True)
    }



@app.route("/lista/v1/tareas", methods=["GET"])
@auth.login_required
def get_tareas():
    tareas = Tarea.query.all() 
    exportadas = [exportar_tarea(t) for t in tareas]
    return jsonify({"tareas": exportadas})

@app.route("/lista/v1/tarea/<int:id>", methods=["GET"])
@auth.login_required
def get_tarea(id):
    tarea = Tarea.query.get(id) 
    if tarea:
        return jsonify({ "tarea": exportar_tarea(tarea) })
    else:
        abort(404)


@app.route("/lista/v1/tareas", methods=["POST"])
@auth.login_required
def create_tarea():

    try:
        dic = request.json
    except:
        abort(400)

    if "descripcion" not in dic:
        abort(400)

    if "completada" not in dic:
        dic['completada'] = False

    elif type(dic['completada']) != bool:
        abort(400)

    nueva_tarea = Tarea(descripcion=dic["descripcion"], completada=dic["completada"])
    db.session.add(nueva_tarea)
    db.session.commit()
    return jsonify({"tarea": exportar_tarea(nueva_tarea)}), 200



@app.route("/lista/v1/tarea/<id>", methods=["PUT"])
@auth.login_required
def update_tarea(id):

    try:
        data = request.json
        if "descripcion" in data:
            if not isinstance(data["descripcion"], str):
                abort(400)

        if "completada" in data:
            if not isinstance(data["completada"], bool):
                abort(400)

        tarea = Tarea.query.get(id)
        tarea.completada = data["completada"]
        tarea.descripcion = data["descripcion"]
        db.session.commit()
        return jsonify({"tarea": exportar_tarea(tarea)}), 200
    except:
        abort(400)




@app.route("/lista/v1/tarea/<id>", methods=["DELETE"])
@auth.login_required
def delete_tarea(id):
    delt = Tarea.query.get(int(id))

    """
    if not tarea:
        abort(404)
    """
    db.session.delete(delt)
    db.session.commit()
    return jsonify({"borrado": True}), 200


@app.errorhandler(404)
def no_encontrado(error):
    return make_response(jsonify({'error': 'Tarea inexistente'}), 404)

@app.errorhandler(400)
def soli_incorrecta(error):
    return make_response(jsonify({'error': 'Solicitud incorrecta'}), 400)


# Crea las tablas en la base de datos (si aún no existen)
with app.app_context(): 
    db.create_all()

# Único usuario permitido: "alumno" con clave "alumno_pass"
@auth.verify_password
def verificar(usuario, contraseña):
    # Esta función debe retornar True si la el usuario/contraseña es válido
    # y False en caso contrario
    if usuario == "alumno" and contraseña == "alumno_pass":
        return True
    else:
        return False

@auth.error_handler
def no_autorizado():
    # Esta función debe retornar la respuesta en caso de error de
    # autenticación, que se produce si el cliente no envía la cabecera
    # Authenticate, o si el usuario enviado no está autorizado, o si
    # la clave proporcionada no encaja con la esperada.
    # Elegimos retornar un código 403 (Forbidden) para este caso
    return make_response(jsonify({'error': 'Acceso no autorizado'}), 403)



if __name__ == "__main__":
    app.run(debug=True)

