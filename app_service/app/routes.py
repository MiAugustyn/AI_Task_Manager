# app_service/app/routes.py
from flask import Blueprint, request, jsonify
from .models import Project, Task, Employee
from . import db

# Utworzenie blueprintu dla endpointów API
routes_bp = Blueprint('routes_bp', __name__)

# Endpoint do tworzenia projektu
@routes_bp.route('/projects', methods=['POST'])
def create_project_api():
    data = request.get_json()  # Pobieramy dane JSON z żądania
    name = data.get('name')
    description = data.get('description', '')
    if not name:
        # Zwracamy błąd, jeśli nie podano nazwy projektu
        return jsonify({'error': 'Nazwa jest wymagana'}), 400
    # Tworzymy nowy obiekt projektu
    project = Project(name=name, description=description)
    db.session.add(project)
    db.session.commit()  # Zapisujemy zmiany w bazie
    return jsonify({'id': project.id, 'name': project.name, 'description': project.description}), 201

# Endpoint do pobierania listy projektów
@routes_bp.route('/projects', methods=['GET'])
def get_projects_api():
    projects = Project.query.all()
    result = [{'id': p.id, 'name': p.name, 'description': p.description} for p in projects]
    return jsonify(result)

# Endpoint do tworzenia zadania
@routes_bp.route('/tasks', methods=['POST'])
def create_task_api():
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
    # Tworzymy nowe zadanie
    task = Task(project_id=project_id, title=title, description=description)
    db.session.add(task)
    db.session.commit()
    return jsonify({
        'id': task.id,
        'title': task.title,
        'status': task.status
    }), 201

# Endpoint do pobierania listy zadań
@routes_bp.route('/tasks', methods=['GET'])
def get_tasks_api():
    tasks = Task.query.all()
    result = [{
        'id': t.id,
        'project_id': t.project_id,
        'title': t.title,
        'description': t.description,
        'status': t.status
    } for t in tasks]
    return jsonify(result)

# Endpoint do aktualizacji zadania (np. zmiana statusu lub przypisania)
@routes_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_api(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Zadanie nie zostało znalezione'}), 404
    # Aktualizacja pól zadania, jeśli zostały przesłane w żądaniu
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({
        'id': task.id,
        'title': task.title,
        'status': task.status
    })

# Endpoint do pobierania listy pracowników
@routes_bp.route('/employees', methods=['GET'])
def get_employees_api():
    employees = Employee.query.all()
    result = [{'id': e.id, 'name': e.name, 'email': e.email, 'role': e.role} for e in employees]
    return jsonify(result)

# Endpoint do tworzenia pracownika
@routes_bp.route('/employees', methods=['POST'])
def create_employee_api():
    data = request.get_json()  # Pobieramy dane JSON z żądania
    name = data.get('name')
    role = data.get('role')
    email = data.get('email')
    if not name or not role or not email:
        return jsonify({'error': 'Imię, rola i email są wymagane'}), 400

    # Tworzymy nowego pracownika
    employee = Employee(name=name, role=role, email=email)
    db.session.add(employee)
    db.session.commit()
    return jsonify({
        'name': employee.name,
        'email': employee.email,
        'role': employee.role
    }), 201