# fragment pliku app_service/app/views.py - modyfikacja do współpracy z task_assign_service

import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash 
from .models import Project, Task, Employee
from . import db

# Tworzymy blueprint dla widoków (interfejs użytkownika)
views_bp = Blueprint('views_bp', __name__)

# ... (apostasy kod bez zmian)
# Strona główna
@views_bp.route('/')
def index():
    return render_template('index.html')


# Widok listy projector
@views_bp.route('/list_projects')
def list_projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)


# Widok formularza tworzenia nowego projektu
@views_bp.route('/projects/new', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        # Pobieramy dane z formularza
        name = request.form.get('name')
        description = request.form.get('description')
        if not name:
            flash("Nazwa projektu jest wymagana")
            return redirect(url_for('views_bp.create_project'))

        # Tworzymy nowy projekt
        project = Project(name=name, description=description)
        db.session.add(project)
        db.session.commit()
        flash("Projekt został utworzony!")

        return redirect(url_for('views_bp.list_projects'))

    return render_template('create_project.html')


# Widok listy zadań
@views_bp.route('/list_tasks')
def list_tasks():
    tasks = Task.query.all()

    return render_template('tasks.html', tasks=tasks)


@views_bp.route('/list_tasks/<int:task_id>', methods=['GET', 'POST'])
def remove_task(task_id):
    if request.method == 'POST':
        task = Task.query.where(Task.id == task_id).first()
        db.session.delete(task)
        db.session.commit()
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)


@views_bp.route('/task_status_update/<int:task_id>', methods=['GET', 'POST'])
def update_task_status(task_id):
    if request.method == 'POST':
        task = Task.query.where(Task.id == task_id).first()
        status = request.form.get('status')
        task.status = status
        db.session.commit()
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)


# Widok formularza tworzenia nowego zadania
@views_bp.route('/tasks/new', methods=['GET', 'POST'])
def create_task():
    projects = Project.query.all()  # Potrzebujemy listy projektów do wyboru
    if request.method == 'POST':
        # Pobieramy dane z formularza
        project_id = request.form.get('project_id')
        title = request.form.get('title')
        description = request.form.get('description')
        if not project_id or not title:
            flash("Projekt i tytuł zadania są wymagane")
            return redirect(url_for('views_bp.create_task'))
        # Sprawdzamy, czy projekt istnieje
        project = Project.query.get(project_id)
        if not project:
            flash("Projekt nie został znaleziony")
            return redirect(url_for('views_bp.create_task'))
        # Tworzymy nowe zadanie
        task = Task(project_id=project_id, title=title, description=description)
        db.session.add(task)
        db.session.commit()
        flash("Zadanie zostało utworzone!")
        return redirect(url_for('views_bp.list_tasks'))
    return render_template('create_task.html', projects=projects)


@views_bp.route('/assign_employees/<int:project_id>')
def assign_employees(project_id):
    project = Project.query.where(Project.id == project_id).first()
    employees = Employee.query.filter(Employee.projects.any(Project.id == project.id)).all()
    all_employees = Employee.query.all()

    return render_template('manage_projects.html', employees=employees, all_employees=all_employees, project=project)


@views_bp.route('/employee/assign/<int:project_id>', methods=['GET', 'POST'])
def assign_employee(project_id):
    if request.method == 'POST':
        id = request.form.get('employee')
        if id:
            employee = Employee.query.where(Employee.id == id).first()
            project = Project.query.where(Project.id == project_id).first()
            employee.projects += [project]
            db.session.commit()
            return redirect(url_for('views_bp.assign_employees', project_id=project_id))
    return redirect(url_for('views_bp.list_projects'))


@views_bp.route('/employee/deassign/<int:project_id>', methods=['GET', 'POST'])
def deassign_employee(project_id):
    if request.method == 'POST':
        id = request.form.get('employee')
        if id:
            employee = Employee.query.where(Employee.id == id).first()
            project = Project.query.where(Project.id == project_id).first()
            employee.projects.remove(project)
            db.session.commit()
            return redirect(url_for('views_bp.assign_employees', project_id=project_id))
    return redirect(url_for('views_bp.list_projects'))


@views_bp.route('/list_employees')
def list_employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)


@views_bp.route('/employee/new', methods=['GET', 'POST'])
def create_employee():
    employees = Employee.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        email = request.form.get('email')
        if name and role and email:
            # Dodanie nowego pracownika do listy
            employee = Employee(name=name, email=email, role=role)
            db.session.add(employee)
            db.session.commit()
            return redirect(url_for('views_bp.list_employees', employees=employees))
    return render_template('create_employee.html', employees=employees)


# Nowy widok do przydzielania zadań przez AI
@views_bp.route('/ai_assign_task', methods=['GET', 'POST'])
def ai_assign_task():
    projects = Project.query.all()  # Potrzebujemy listy projektów do wyboru
    
    if request.method == 'POST':
        # Pobieramy dane z formularza
        project_id = request.form.get('project_id')
        title = request.form.get('title')
        description = request.form.get('description', '')
        
        if not project_id or not title:
            flash("Projekt i tytuł zadania są wymagane")
            return redirect(url_for('views_bp.ai_assign_task'))
        
        # Sprawdzamy, czy projekt istnieje
        project = Project.query.get(project_id)
        if not project:
            flash("Projekt nie został znaleziony")
            return redirect(url_for('views_bp.ai_assign_task'))
        
        # Wysyłamy request do mikroserwisu task_assign
        try:
            response = requests.post(
                'http://task_assign:5000/assign',
                json={
                    'project_id': project_id,
                    'title': title,
                    'description': description
                }
            )
            
            # Sprawdzamy odpowiedź
            if response.status_code == 201:
                flash("Zadanie zostało utworzone i przypisane!")
            else:
                error_data = response.json()
                flash(f"Błąd: {error_data.get('error', 'Nieznany błąd')}")
                
        except requests.RequestException as e:
            flash(f"Błąd połączenia z serwisem przydzielania zadań: {str(e)}")
            
        return redirect(url_for('views_bp.list_tasks'))
        
    return render_template('ai_assign_task.html', projects=projects)