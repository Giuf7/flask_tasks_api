from datetime import datetime
from flask import jsonify, request

TASKS = [
    {
        "id": 1,
        "titre": "Acheter le pain",
        "description": "Prendre une baguette bien cuite",
        "done": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 2,
        "titre": "Faire le ménage",
        "description": "Nettoyer la maison et faire le ménage",
        "done": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 3,
        "titre": "Faire du sport",
        "description": "Aller à la salle de sport ou faire une promenade",
        "done": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

def home():
    return "Bienvenue sur l'API Tasks !"

def get_tasks():
    done_param = request.args.get('done')

    if done_param is None:
        return jsonify({"count": len(TASKS), "data": TASKS})
    
    filtered_tasks = []

    for task in TASKS:
        if done_param == 'true' and task['done'] is True:
            filtered_tasks.append(task)
        elif done_param == 'false' and task['done'] is False:
            filtered_tasks.append(task)

    return jsonify({"count": len(filtered_tasks), "data": filtered_tasks})

def create_task():

    data = request.get_json()
    
    if not data or 'titre' not in data or not data.get('titre'):
        return jsonify({"error": "Le champ 'titre' est obligatoire."}), 400
    
    # Générer l'ID unique
    task_id = max([t['id'] for t in TASKS]) + 1 if TASKS else 1
    
    task = {
        "id": task_id,
        "titre": data.get("titre"),
        "description": data.get("description", ""), # Chaîne vide par défaut si absent
        "done": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    TASKS.append(task)
    return jsonify(task), 201

def get_task(task_id):
    for task in TASKS:
        print(task)
        if task['id'] == task_id:
            return jsonify(task)
    return jsonify({"error": "Tâche non trouvée."}), 404

def update_task(task_id):
    for task in TASKS:
        if task['id'] == task_id:
            data = request.get_json()
            task['titre'] = data.get('titre', task['titre'])
            task['description'] = data.get('description', task['description'])
            task['done'] = data.get('done', task['done'])
            task['updated_at'] = datetime.now()
            return jsonify(task)
    return jsonify({"error": "Tâche non trouvée."}), 404

def delete_task(task_id):
    global TASKS
    initial_length = len(TASKS)
    TASKS = [task for task in TASKS if task['id'] != task_id]
    
    # Si la taille n'a pas changé, la tâche n'existait pas
    if len(TASKS) == initial_length:
        return jsonify({"error": "Tâche non trouvée."}), 404
        
    return jsonify({"message": "Tâche supprimée avec succès."})