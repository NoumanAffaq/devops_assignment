from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure the JWT secret key
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key in production
jwt = JWTManager(app)

# Connect to MongoDB
client = MongoClient("mongodb+srv://noumana:Turing!!@cluster0.xydhc.mongodb.net/")  # Replace with your MongoDB URI
db = client['auth_service']
users_collection = db['users']

# Register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if users_collection.find_one({'username': username}):
        return jsonify({'error': 'User already exists'}), 400

    # Hash the password before saving to the database
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({'username': username, 'password': hashed_password})
    return jsonify({'message': 'User registered successfully'}), 201

# Login a user and issue a JWT
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = users_collection.find_one({'username': username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Create a JWT token
    access_token = create_access_token(
        identity=username,
        expires_delta=datetime.timedelta(hours=1)  # Token expires in 1 hour
    )
    return jsonify({'access_token': access_token}), 200

# Protected route (requires valid JWT)
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user}! This is a protected route.'}), 200

# Test endpoint
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'User Authentication Service is running'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
