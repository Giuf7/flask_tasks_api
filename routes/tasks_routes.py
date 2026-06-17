from flask import Blueprint
from controllers.task_controller import home, get_tasks, create_task, update_task, delete_task

tasks_bp = Blueprint('tasks_bp', __name__)

@tasks_bp.route('/')
def home_bp():
    return home()

@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks_bp():
    return get_tasks()

@tasks_bp.route('/api/tasks', methods=['POST'])
def create_task_bp():
    return create_task()

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task_bp(task_id):
    return get_tasks()

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task_bp(task_id):
    return update_task()

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_bp(task_id):
    return delete_task()