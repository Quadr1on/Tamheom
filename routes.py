from flask import Blueprint, render_template, jsonify, request
from models import db, City, Experience

app = Blueprint('app', __name__)

@app.route('/')
def index():
    cities = City.query.all()
    return render_template('index.html', cities=cities)

@app.route('/api/experiences/<city_id>')
def get_experiences(city_id):
    experiences = Experience.query.filter_by(city_id=city_id, active=True).all()
    
    # Organize experiences by type
    organized_experiences = {
        'events': [],
        'gems': [],
        'tours': []
    }
    
    for exp in experiences:
        if exp.type == 'local_event':
            organized_experiences['events'].append({
                'name': exp.name,
                'time': exp.details.get('time', 'TBD')
            })
        elif exp.type == 'hidden_gem':
            organized_experiences['gems'].append({
                'name': exp.name,
                'type': exp.details.get('type', 'Unknown')
            })
        elif exp.type == 'walking_tour':
            organized_experiences['tours'].append({
                'name': exp.name,
                'duration': exp.details.get('distance', 'undefined')
            })
    
    return jsonify(organized_experiences)

@app.route('/api/search')
def search_experiences():
    query = request.args.get('q', '').lower()
    city_id = request.args.get('city_id')
    
    experiences = Experience.query.filter(
        Experience.city_id == city_id,
        Experience.active == True,
        Experience.name.ilike(f'%{query}%')
    ).all()
    
    results = [{
        'name': exp.name,
        'type': exp.type,
        'details': exp.details
    } for exp in experiences]
    
    return jsonify(results)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
