# app/models.py
from . import db
import datetime


# Model reprezentujący projekt
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unikalny identyfikator projektu
    name = db.Column(db.String(100), nullable=False)  # Nazwa projektu (wymagana)
    description = db.Column(db.String(255))  # Opcjonalny opis projektu
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # Data utworzenia

    # Relacja z zadaniami – każdy projekt może mieć wiele zadań
    tasks = db.relationship('Task', backref='project', lazy=True)


# Model reprezentujący zadanie
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unikalny identyfikator zadania
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)  # Klucz obcy wskazujący projekt
    title = db.Column(db.String(100), nullable=False)  # Tytuł zadania (wymagany)
    description = db.Column(db.String(255))  # Opis zadania
    #assigned_to = db.Column(db.String(100))  # Osoba przypisana do zadania
    status = db.Column(db.String(20), default='pending')  # Status zadania (np. pending, in progress, done)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # Data utworzenia zadania


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unikalny identyfikator pracownika
    name = db.Column(db.String(100), nullable=False)  # Nazwa / imię pracownika
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unikalny adres email
    role = db.Column(db.String(50))  # Rola pracownika (np. Manager, Developer)

    # Relacja many-to-many: pracownik może być przypisany do wielu projektów i zadań
    projects = db.relationship('Project', secondary='employee_project', backref=db.backref('employees', lazy='dynamic'))
    tasks = db.relationship('Task', secondary='employee_task', backref=db.backref('employees', lazy='dynamic'))


# Tabela łącząca pracowników z projektami (many-to-many)
class EmployeeProject(db.Model):
    __tablename__ = 'employee_project'
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)


# Tabela łącząca pracowników z zadaniami (many-to-many)
class EmployeeTask(db.Model):
    __tablename__ = 'employee_task'
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)
