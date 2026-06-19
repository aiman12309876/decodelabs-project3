from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    course = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'course': self.course,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return jsonify({
        'message': 'Student Management API',
        'routes': {
            'GET /students': 'Get all students',
            'GET /students/<id>': 'Get student by ID',
            'POST /students': 'Create a new student',
            'PUT /students/<id>': 'Update a student',
            'DELETE /students/<id>': 'Delete a student'
        }
    })


@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify({
        'status': 'success',
        'data': [s.to_dict() for s in students],
        'count': len(students)
    })


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'status': 'error', 'message': 'Student not found'}), 404
    return jsonify({'status': 'success', 'data': student.to_dict()})


@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()

    if not data or not data.get('name') or not data.get('email'):
        return jsonify({
            'status': 'error',
            'message': 'Name and email are required'
        }), 400

    existing = Student.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({
            'status': 'error',
            'message': 'Email already exists'
        }), 409

    student = Student(
        name=data['name'],
        email=data['email'],
        age=data.get('age'),
        course=data.get('course')
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Student created successfully',
        'data': student.to_dict()
    }), 201


@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'status': 'error', 'message': 'Student not found'}), 404

    data = request.get_json()

    if 'name' in data:
        student.name = data['name']
    if 'age' in data:
        student.age = data['age']
    if 'course' in data:
        student.course = data['course']
    if 'email' in data:
        existing = Student.query.filter_by(email=data['email']).first()
        if existing and existing.id != student_id:
            return jsonify({
                'status': 'error',
                'message': 'Email already exists'
            }), 409
        student.email = data['email']

    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Student updated successfully',
        'data': student.to_dict()
    })


@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'status': 'error', 'message': 'Student not found'}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Student deleted successfully'
    })


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("   STUDENT MANAGEMENT API")
    print("=" * 60)
    print("\n Server running at: http://127.0.0.1:5001")
    print(" Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5001)