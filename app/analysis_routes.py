# app/analysis_routes.py
from flask import Blueprint, jsonify
from .models import Task

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
