import click
import requests

BASE_URL = "http://localhost:5000/lista/v1"

@click.group()
def todo():
    """
    Aplicación de gestión de tareas cliente.
    Utiliza comandos para interactuar con el servidor.
    """
    pass

@todo.command()
@click.argument("description")
@click.argument("status", type=bool)
def add(description, status):
    """
    Añade una nueva tarea con la descripción y estado proporcionados.
    """
    response = requests.post(f"{BASE_URL}/tareas", json={"descripcion": description, "completada": status})
    if response.status_code == 201:
        print("Nueva tarea añadida:")
        tarea = response.json()["tarea"]
        print(f"URI: {tarea['uri']} - {tarea['descripcion']} - {'Completada' if tarea['completada'] else 'Pendiente'}")
    else:
        print("Error al añadir la nueva tarea.")

@todo.command()
def list():
    """
    Obtiene la lista completa de tareas desde el servidor.
    """
    response = requests.get(f"{BASE_URL}/tareas")
    if response.status_code == 200:
        tareas = response.json()["tareas"]
        for tarea in tareas:
            print(f"URI: {tarea['uri']} - {tarea['descripcion']} - {'Completada' if tarea['completada'] else 'Pendiente'}")
    else:
        print("Error al obtener la lista de tareas.")

@todo.command()
@click.argument("task_id", type=int)
def check(task_id):
    """
    Marca la tarea con el ID proporcionado como completada.
    """
    response = requests.put(f"{BASE_URL}/tarea/{task_id}", json={"completada": True})
    if response.status_code == 200:
        print(f"Tarea {task_id} marcada como completada.")
    else:
        print(f"Error al marcar la tarea {task_id} como completada.")

@todo.command()
@click.argument("task_id", type=int)
def uncheck(task_id):
    """
    Marca la tarea con el ID proporcionado como no completada.
    """
    response = requests.put(f"{BASE_URL}/tarea/{task_id}", json={"completada": False})
    if response.status_code == 200:
        print(f"Tarea {task_id} marcada como no completada.")
    else:
        print(f"Error al marcar la tarea {task_id} como no completada.")

@todo.command()
@click.argument("task_id", type=int)
def delete(task_id):
    """
    Elimina la tarea con el ID proporcionado.
    """
    response = requests.delete(f"{BASE_URL}/tarea/{task_id}")
    if response.status_code == 200:
        print(f"Tarea {task_id} eliminada.")
    else:
        print(f"Error al eliminar la tarea {task_id}.")

@todo.command()
@click.argument("task_id", type=int)
@click.argument("new_description")
def edit(task_id, new_description):
    """
    Modifica la descripción de la tarea con el ID proporcionado.
    """
    response = requests.put(f"{BASE_URL}/tarea/{task_id}", json={"descripcion": new_description})
    if response.status_code == 200:
        print(f"Descripción de la tarea {task_id} modificada.")
    else:
        print(f"Error al modificar la descripción de la tarea {task_id}.")

if __name__ == "__main__":
    todo()