# app_service/app/analysis_routes.py
from flask import Blueprint, jsonify, render_template
from .models import Task, Project, Employee

# Tworzymy blueprint dla endpointów analitycznych
analysis_bp = Blueprint('analysis_bp', __name__)

# Endpoint obliczający produktywność na podstawie wykonanych zadań
@analysis_bp.route('/productivity', methods=['GET'])
def productivity_analysis():
    total_tasks = Task.query.count()  # Całkowita liczba zadań
    done_tasks = Task.query.filter_by(status='done').count()  # Liczba zadań oznaczonych jako 'done'
    # Obliczamy procent wykonanych zadań
    score = (done_tasks / total_tasks * 100) if total_tasks else 0
    return jsonify({
        'total_tasks': total_tasks,
        'done_tasks': done_tasks,
        'productivity_score': score
    })

# Endpoint do wyświetlania interfejsu użytkownika z analizą produktywności
@analysis_bp.route('/dashboard', methods=['GET'])
def productivity_dashboard():
    # Obliczenia statystyk
    total_tasks = Task.query.count()
    done_tasks = Task.query.filter_by(status='done').count()
    pending_tasks = Task.query.filter_by(status='pending').count()
    in_progress_tasks = Task.query.filter_by(status='in progress').count()
    productivity = (done_tasks / total_tasks * 100) if total_tasks else 0
    
    # Statystyki dla projektów
    projects = Project.query.all()
    project_stats = []
    
    for project in projects:
        project_total = Task.query.filter_by(project_id=project.id).count()
        project_done = Task.query.filter_by(project_id=project.id, status='done').count()
        project_productivity = (project_done / project_total * 100) if project_total else 0
        
        project_stats.append({
            'id': project.id,
            'name': project.name,
            'total': project_total,
            'done': project_done,
            'productivity': round(project_productivity, 1)
        })
    
    # Statystyki dla pracowników
    employees = Employee.query.all()
    employee_stats = []
    
    for employee in employees:
        # Zliczamy zadania przypisane do pracownika
        employee_tasks = Task.query.filter(Task.employees.any(Employee.id == employee.id)).all()
        employee_total = len(employee_tasks)
        employee_done = sum(1 for task in employee_tasks if task.status == 'done')
        employee_productivity = (employee_done / employee_total * 100) if employee_total else 0
        
        employee_stats.append({
            'id': employee.id,
            'name': employee.name,
            'total': employee_total,
            'done': employee_done,
            'productivity': round(employee_productivity, 1)
        })
    
    return render_template(
        'dashboard.html', 
        productivity=round(productivity, 1),
        total_tasks=total_tasks,
        done_tasks=done_tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        project_stats=project_stats,
        employee_stats=employee_stats
    )