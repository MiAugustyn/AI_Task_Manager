# app/views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash 
from .models import Project, Task, Employee
from . import db

# Tworzymy blueprint dla widoków (interfejs użytkownika)
views_bp = Blueprint('views_bp', __name__)


# Strona główna
@views_bp.route('/')
def index():
    return render_template('index.html')


# Widok listy projektów
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


# Widok formularza tworzenia nowego zadania
@views_bp.route('/tasks/new', methods=['GET', 'POST'])
def create_task():
    projects = Project.query.all()  # Potrzebujemy listy projektów do wyboru
    if request.method == 'POST':
        # Pobieramy dane z formularza
        project_id = request.form.get('project_id')
        title = request.form.get('title')
        description = request.form.get('description')
        assigned_to = request.form.get('assigned_to')
        if not project_id or not title:
            flash("Projekt i tytuł zadania są wymagane")
            return redirect(url_for('views_bp.create_task'))
        # Sprawdzamy, czy projekt istnieje
        project = Project.query.get(project_id)
        if not project:
            flash("Projekt nie został znaleziony")
            return redirect(url_for('views_bp.create_task'))
        # Tworzymy nowe zadanie
        task = Task(project_id=project_id, title=title, description=description, assigned_to=assigned_to)
        db.session.add(task)
        db.session.commit()
        flash("Zadanie zostało utworzone!")
        return redirect(url_for('views_bp.list_tasks'))
    return render_template('create_task.html', projects=projects)


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
