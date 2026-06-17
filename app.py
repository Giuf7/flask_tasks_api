from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

TASKS = [
    {
        "id": 1,
        "titre": "Acheter le pain",
        "description": "Prendre une baguette bien cuite",
        "done": False,
        "created_at": datetime.now()
    },
    {
        "id": 2,
        "titre": "Faire le ménage",
        "description": "Nettoyer la maison et faire le ménage",
        "done": False,
        "created_at": datetime.now()
    },
    {
        "id": 3,
        "titre": "Faire du sport",
        "description": "Aller à la salle de sport ou faire une promenade",
        "done": False,
        "created_at": datetime.now()
    }
]

@app.route('/')
def home():
    return "Bienvenue sur l'API Tasks !"

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"count": len(TASKS), "data": TASKS})

@app.route('/api/tasks', methods=['POST'])
def create_task():

    # Récupérer les données JSON de la requête
    data = request.get_json()
    
    # Vérifier si le titre est présent
    if not data or 'titre' not in data or not data.get('titre'):
        return jsonify({"error": "Le champ 'titre' est obligatoire."}), 400
    
    # Générer l'ID unique
    task_id = max([t['id'] for t in TASKS]) + 1 if TASKS else 1
    
    # Créer le dictionnaire de la tâche
    task = {
        "id": task_id,
        "titre": data.get("titre"),
        "description": data.get("description", ""), # Chaîne vide par défaut si absent
        "done": False,
        "created_at": datetime.now()
    }
    
    TASKS.append(task)
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in TASKS:
        print(task)
        if task['id'] == task_id:
            return jsonify(task)
    return jsonify({"error": "Tâche non trouvée."}), 404

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    for task in TASKS:
        if task['id'] == task_id:
            data = request.get_json()
            task['titre'] = data.get('titre', task['titre'])
            task['description'] = data.get('description', task['description'])
            task['done'] = data.get('done', task['done'])
            return jsonify(task)
    return jsonify({"error": "Tâche non trouvée."}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global TASKS
    initial_length = len(TASKS)
    TASKS = [task for task in TASKS if task['id'] != task_id]
    
    # Si la taille n'a pas changé, la tâche n'existait pas
    if len(TASKS) == initial_length:
        return jsonify({"error": "Tâche non trouvée."}), 404
        
    return jsonify({"message": "Tâche supprimée avec succès."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)