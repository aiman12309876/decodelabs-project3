from flask import Flask, request, jsonify
import jwt
import bcrypt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

users_db = []

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'status': 'error', 'message': 'Token is missing'}), 401

        try:
            if token.startswith('Bearer '):
                token = token[7:]

            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = None
            for user in users_db:
                if user['email'] == data['email']:
                    current_user = user
                    break

            if not current_user:
                return jsonify({'status': 'error', 'message': 'User not found'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'status': 'error', 'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/')
def home():
    return jsonify({
        'message': 'Secure Authentication System',
        'routes': {
            'POST /register': 'Register a new user',
            'POST /login': 'Login and get JWT token',
            'GET /profile': 'Protected route (requires token)'
        }
    })

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'status': 'error', 'message': 'Email and password are required'}), 400

    for user in users_db:
        if user['email'] == data['email']:
            return jsonify({'status': 'error', 'message': 'User already exists'}), 409

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    new_user = {
        'email': data['email'],
        'password': hashed_password,
        'full_name': data.get('full_name', ''),
        'created_at': datetime.datetime.now().isoformat()
    }

    users_db.append(new_user)

    return jsonify({
        'status': 'success',
        'message': 'User registered successfully',
        'user': {'email': new_user['email'], 'full_name': new_user['full_name']}
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'status': 'error', 'message': 'Email and password are required'}), 400

    user = None
    for u in users_db:
        if u['email'] == data['email']:
            user = u
            break

    if not user:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

    if not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'email': user['email'],
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'status': 'success',
        'message': 'Login successful',
        'token': token,
        'user': {'email': user['email'], 'full_name': user.get('full_name', '')}
    })

@app.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        'status': 'success',
        'user': {
            'email': current_user['email'],
            'full_name': current_user.get('full_name', ''),
            'created_at': current_user.get('created_at')
        }
    })

@app.route('/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({
        'status': 'success',
        'message': 'You have accessed a protected route',
        'user': current_user['email']
    })

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("   SECURE AUTHENTICATION SYSTEM")
    print("=" * 60)
    print("\n Server running at: http://127.0.0.1:5001")
    print(" Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5001)