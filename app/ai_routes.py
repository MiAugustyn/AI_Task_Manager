# app/ai_routes.py
from flask import Blueprint, request, jsonify
from .models import Project, Task
from . import db
import random

# Tworzymy blueprint dla endpointów z logiką "AI"
ai_bp = Blueprint('ai_bp', __name__)

# Przykładowy endpoint symulujący automatyczne przydzielanie zadania
@ai_bp.route('/assign', methods=['POST'])
def assign_task():
    data = request.get_json()  # Pobieramy dane JSON z żądania
    project_id = data.get('project_id')
    title = data.get('title')
    description = data.get('description', '')
    if not project_id or not title:
        return jsonify({'error': 'project_id oraz tytuł są wymagane'}), 400
    # Sprawdzamy, czy projekt o podanym ID istnieje
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Projekt nie został znaleziony'}), 404

    # Przykładowa logika "AI" – losowo wybieramy członka zespołu
    team_members = ["Alice", "Bob", "Charlie"]
    assigned_to = random.choice(team_members)
    # Tworzymy zadanie z przypisanym członkiem zespołu
    task = Task(project_id=project_id, title=title, description=description, assigned_to=assigned_to)
    db.session.add(task)
    db.session.commit()
    return jsonify({
        'id': task.id,
        'title': task.title,
        'assigned_to': task.assigned_to,
        'status': task.status
    }), 201
