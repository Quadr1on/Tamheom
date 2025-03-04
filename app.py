import os
from datetime import datetime
from flask import Flask, Blueprint, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Configuration
class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Use environment variable for database URL - in production this will be different
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'local_experiences.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'AdornIsnfdhdasdajsd'

# Database Models
db = SQLAlchemy()

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    experiences = db.relationship('Experience', backref='city', lazy=True, cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Experience(db.Model):
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'hidden_gem', 'local_event', 'walking_tour'
    description = db.Column(db.Text)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id', ondelete='CASCADE'), nullable=False)
    details = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

# Routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    cities = City.query.all()
    return render_template('index.html', cities=cities)

@main.route('/api/experiences/<int:city_id>')
def get_experiences(city_id):
    experiences = Experience.query.filter_by(city_id=city_id, active=True).all()
    
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

@main.route('/api/search')
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

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

# App Factory
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    app.register_blueprint(main)
    
    return app

# Database Initialization - pre-populate with sample data
def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # Only add sample data if no cities exist yet
        if City.query.count() == 0:
            # Add sample cities
            chennai = City(name='Chennai', state='Tamil Nadu', country='India')
            banglore = City(name='Banglore', state='Karnataka', country='India')
            mumbai = City(name='Mumbai', state='Maharashtra', country='India')
            lucknow = City(name='Lucknow', state='Uttar Pradesh', country='India')
            delhi = City(name='Delhi', state='Delhi', country='India')

            db.session.add_all([chennai, delhi, mumbai, banglore, lucknow])
            db.session.commit()
            
            # Add sample experiences
            experiences = [
                Experience(
                    name='Samay Raina Unfiltered.',
                    type='local_event',
                    description='Stand-up comedy',
                    city_id=chennai.id,
                    details={'time': 'Sun 17 Nov 2024 7:00pm', 'location': 'The Music Academy'}
                ),
                Experience(
                    name='Marina Beach Sunrise Walk',
                    type='walking_tour',
                    description='Early morning walk on the second longest beach in the world',
                    city_id=chennai.id,
                    details={'distance': '3 km', 'duration': '1.5 hours'}
                ),
                Experience(
                    name='Kalyan Bhavan Restaurant',
                    type='hidden_gem',
                    description='Authentic South Indian vegetarian food',
                    city_id=chennai.id,
                    details={'type': 'Restaurant', 'cuisine': 'South Indian'}
                ),
                Experience(
                    name='Red Fort Light Show',
                    type='local_event',
                    description='Historical light and sound show',
                    city_id=delhi.id,
                    details={'time': 'Every evening 7:30pm', 'location': 'Red Fort'}
                ),
                Experience(
                    name='Old Delhi Food Walk',
                    type='walking_tour',
                    description='Culinary journey through the streets of Old Delhi',
                    city_id=delhi.id,
                    details={'distance': '2.5 km', 'duration': '3 hours'}
                )
            ]
            
            db.session.add_all(experiences)
            db.session.commit()

# Create app instance for Vercel
app = create_app()

# Initialize database on first run
# Note: This is not ideal for production, but works for demo purposes
try:
    with app.app_context():
        db.create_all()
        if City.query.count() == 0:
            init_db()
except Exception as e:
    print(f"Database initialization error: {e}")

# This is used when running locally only. When deployed to Vercel,
# Vercel automatically uses the Flask application without invoking this.
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
