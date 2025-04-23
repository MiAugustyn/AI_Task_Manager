# task_assign_service/app/ai_routes.py
from flask import Blueprint, request, jsonify
from .models import Project, Task, Employee
from . import db

# Tworzymy blueprint dla endpointów z logiką "AI"
ai_bp = Blueprint('ai_bp', __name__)

# Endpoint symulujący automatyczne przydzielanie zadania
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

    try:
        project_id = int(project_id)
    except ValueError:
        return jsonify({'error': 'Nieprawidłowy format project_id'}), 400

    employee = None
    lowest = None
    employees = Employee.query.filter(Employee.projects.any(Project.id == project_id)).all()

    if not employees:
        return jsonify({'error': 'Brak dostępnych pracowników w projekcie'}), 400

    for x in employees:
        tasks = Task.query.filter(Task.employees.any(Employee.id == x.id)).count()
        if lowest is None or lowest > tasks:
            lowest = tasks
            employee = x

    if employee is None:
        return jsonify({'error': 'Nie udało się przypisać pracownika do zadania'}), 400
    
    # Tworzymy zadanie z przypisanym członkiem zespołu
    task = Task(project_id=project_id, title=title, description=description)
    task.employees.append(employee)
    db.session.add(task)
    db.session.commit()

    return jsonify({
        'id': task.id,
        'title': task.title,
        'status': task.status,
        'assigned_to': employee.name
    }), 201